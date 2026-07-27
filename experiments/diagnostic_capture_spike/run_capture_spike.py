#!/usr/bin/env python3
"""Non-production implementation for the bounded diagnostic capture spike.

This program is an experimental helper only.  Its receipt and summary outputs
are non-canonical diagnostic material; it is not a runner, artifact store,
validator, or qualification mechanism.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import shutil
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any


EXIT_SUCCESS = 0
EXIT_USAGE = 1
EXIT_INVALIDATED = 2
EXIT_FAILURE = 3
RECEIPT_FIELDS = (
    "receipt_type",
    "fixture_id",
    "source_relative_path",
    "expected_source_class",
    "expected_byte_length",
    "observed_byte_length",
    "expected_sha256",
    "observed_sha256",
    "source_identity_match",
    "capture_status",
    "transformation_attempted",
    "transformation_kind",
    "transformation_status",
    "transformation_error_type",
    "derivative_artifact_created",
)


class ConfigurationError(ValueError):
    """The requested invocation or manifest is unsuitable for this spike."""


class ExperimentInvalidated(RuntimeError):
    """Frozen source identity or fixture-manifest integrity did not hold."""


class CaptureArgumentParser(argparse.ArgumentParser):
    """Keep malformed invocation distinct from frozen-input invalidation."""

    def error(self, message: str) -> None:
        raise ConfigurationError(message)


@dataclass(frozen=True)
class FrozenFixture:
    fixture_id: str
    relative_path: str
    expected_source_class: str
    expected_byte_length: int
    expected_sha256: str


@dataclass(frozen=True)
class ObservedFixture:
    fixture: FrozenFixture
    source_bytes: bytes
    observed_sha256: str


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _load_manifest(manifest_path: Path) -> list[FrozenFixture]:
    try:
        parsed = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ExperimentInvalidated(f"manifest is unreadable or malformed: {error}") from error

    if not isinstance(parsed, dict) or parsed.get("hash_algorithm") != "SHA-256":
        raise ExperimentInvalidated("manifest does not declare the required SHA-256 fixture corpus")
    fixtures = parsed.get("fixtures")
    if not isinstance(fixtures, list) or len(fixtures) != 11:
        raise ExperimentInvalidated("manifest must contain exactly 11 fixtures")

    required = {
        "fixture_id",
        "relative_path",
        "expected_source_class",
        "expected_byte_length",
        "expected_sha256",
    }
    identifiers: set[str] = set()
    paths: set[str] = set()
    loaded: list[FrozenFixture] = []
    for item in fixtures:
        if not isinstance(item, dict) or not required.issubset(item):
            raise ExperimentInvalidated("manifest fixture entry is incomplete")
        fixture_id = item["fixture_id"]
        relative_path = item["relative_path"]
        expected_class = item["expected_source_class"]
        expected_length = item["expected_byte_length"]
        expected_hash = item["expected_sha256"]
        if not isinstance(fixture_id, str) or not fixture_id or fixture_id in identifiers:
            raise ExperimentInvalidated("manifest has an invalid or duplicate fixture_id")
        if not isinstance(relative_path, str) or not relative_path or relative_path in paths:
            raise ExperimentInvalidated("manifest has an invalid or duplicate relative_path")
        path_object = Path(relative_path)
        if path_object.is_absolute() or ".." in path_object.parts or "\\" in relative_path:
            raise ExperimentInvalidated("manifest fixture path escapes the source root")
        if not isinstance(expected_class, str) or not expected_class:
            raise ExperimentInvalidated("manifest has an invalid expected_source_class")
        if type(expected_length) is not int or expected_length < 0:
            raise ExperimentInvalidated("manifest has an invalid expected_byte_length")
        if not isinstance(expected_hash, str) or len(expected_hash) != 64 or any(
            character not in "0123456789abcdef" for character in expected_hash
        ):
            raise ExperimentInvalidated("manifest has an invalid expected_sha256")
        identifiers.add(fixture_id)
        paths.add(relative_path)
        loaded.append(
            FrozenFixture(
                fixture_id,
                relative_path,
                expected_class,
                expected_length,
                expected_hash,
            )
        )
    return sorted(loaded, key=lambda fixture: fixture.fixture_id)


def _ensure_expected_fixture_set(source_root: Path, fixtures: list[FrozenFixture]) -> None:
    fixture_directory = source_root / "experiments/diagnostic_capture_spike/fixtures"
    if not fixture_directory.is_dir():
        raise ExperimentInvalidated("frozen fixture directory is missing")
    authorized_manifest = (fixture_directory / "manifest.json").resolve()
    actual = {
        path.relative_to(source_root).as_posix()
        for path in fixture_directory.rglob("*")
        if path.is_file() and path.resolve() != authorized_manifest
    }
    expected = {fixture.relative_path for fixture in fixtures}
    if actual != expected:
        raise ExperimentInvalidated("frozen fixture directory has missing or unexpected files")


def _read_and_verify_sources(source_root: Path, fixtures: list[FrozenFixture]) -> list[ObservedFixture]:
    source_root = source_root.resolve()
    _ensure_expected_fixture_set(source_root, fixtures)
    observed: list[ObservedFixture] = []
    for fixture in fixtures:
        source_path = (source_root / fixture.relative_path).resolve()
        try:
            source_path.relative_to(source_root)
        except ValueError as error:
            raise ExperimentInvalidated("fixture source path escapes the source root") from error
        try:
            source_bytes = source_path.read_bytes()
        except OSError as error:
            raise ExperimentInvalidated(f"fixture source is missing or unreadable: {fixture.relative_path}") from error
        observed_hash = _sha256(source_bytes)
        if len(source_bytes) != fixture.expected_byte_length or observed_hash != fixture.expected_sha256:
            raise ExperimentInvalidated(f"frozen source identity mismatch: {fixture.fixture_id}")
        observed.append(ObservedFixture(fixture, source_bytes, observed_hash))
    return observed


def _make_receipts(observed: list[ObservedFixture]) -> list[dict[str, Any]]:
    receipts: list[dict[str, Any]] = []
    for item in observed:
        try:
            item.source_bytes.decode("utf-8", errors="strict")
            transformation_status = "SUCCEEDED"
            error_type: str | None = None
        except UnicodeDecodeError:
            transformation_status = "FAILED"
            error_type = "UnicodeDecodeError"
        receipt = {
            "receipt_type": "NON_CANONICAL_DIAGNOSTIC_RECEIPT",
            "fixture_id": item.fixture.fixture_id,
            "source_relative_path": item.fixture.relative_path,
            "expected_source_class": item.fixture.expected_source_class,
            "expected_byte_length": item.fixture.expected_byte_length,
            "observed_byte_length": len(item.source_bytes),
            "expected_sha256": item.fixture.expected_sha256,
            "observed_sha256": item.observed_sha256,
            "source_identity_match": True,
            "capture_status": "SOURCE_BYTES_VERIFIED",
            "transformation_attempted": True,
            "transformation_kind": "STRICT_UTF8_DECODE",
            "transformation_status": transformation_status,
            "transformation_error_type": error_type,
            "derivative_artifact_created": False,
        }
        if tuple(receipt) != RECEIPT_FIELDS:
            raise RuntimeError("receipt field contract changed unexpectedly")
        receipts.append(receipt)
    return receipts


def _write_success_output(
    output_directory: Path,
    receipts: list[dict[str, Any]],
    frozen_input_commit: str,
    implementation_commit: str,
) -> dict[str, Any]:
    if output_directory.exists() and any(output_directory.iterdir()):
        raise ConfigurationError("output directory must not already contain files")
    output_directory.parent.mkdir(parents=True, exist_ok=True)
    temporary_directory = Path(tempfile.mkdtemp(prefix="casef-diagnostic-capture-", dir=output_directory.parent))
    try:
        receipt_path = temporary_directory / "diagnostic_receipts.jsonl"
        receipt_bytes = b"".join(
            json.dumps(receipt, ensure_ascii=True, separators=(",", ":")).encode("utf-8") + b"\n"
            for receipt in receipts
        )
        receipt_path.write_bytes(receipt_bytes)
        successful = sum(receipt["transformation_status"] == "SUCCEEDED" for receipt in receipts)
        failed = len(receipts) - successful
        summary = {
            "summary_type": "NON_CANONICAL_DIAGNOSTIC_RUN_SUMMARY",
            "frozen_input_commit": frozen_input_commit,
            "implementation_commit": implementation_commit,
            "execution_status": "COMPLETED",
            "experiment_invalidated": False,
            "fixture_count_expected": 11,
            "fixture_count_processed": len(receipts),
            "source_verified_count": len(receipts),
            "source_mismatch_count": 0,
            "capture_failure_count": 0,
            "utf8_decode_success_count": successful,
            "utf8_decode_failure_count": failed,
            "derivative_artifact_count": 0,
            "receipt_output_path": "diagnostic_receipts.jsonl",
            "receipt_sha256": _sha256(receipt_bytes),
            "python_version": platform.python_version(),
            "platform_system": platform.system(),
            "limitations": [
                "Non-canonical bounded diagnostic experiment only.",
                "No derivative byte artifacts are generated.",
                "No evidence eligibility, qualification, safety, or clinical conclusion is asserted.",
            ],
        }
        (temporary_directory / "run_summary.json").write_bytes(
            json.dumps(summary, ensure_ascii=True, indent=2).encode("utf-8") + b"\n"
        )
        output_directory.mkdir(exist_ok=True)
        os.replace(receipt_path, output_directory / receipt_path.name)
        os.replace(temporary_directory / "run_summary.json", output_directory / "run_summary.json")
        return summary
    finally:
        shutil.rmtree(temporary_directory, ignore_errors=True)


def run_experiment(
    source_root: Path,
    manifest_path: Path,
    frozen_input_commit: str,
    output_directory: Path,
    implementation_commit: str,
) -> dict[str, Any]:
    """Run the two-phase experimental process or raise an explicit failure."""
    fixtures = _load_manifest(manifest_path)
    observed = _read_and_verify_sources(source_root, fixtures)
    receipts = _make_receipts(observed)
    return _write_success_output(
        output_directory, receipts, frozen_input_commit, implementation_commit
    )


def _arguments(argv: list[str] | None = None) -> argparse.Namespace:
    parser = CaptureArgumentParser(description="Non-canonical diagnostic capture spike")
    parser.add_argument("--source-root", required=True, type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--frozen-input-commit", required=True)
    parser.add_argument("--implementation-commit", required=True)
    parser.add_argument("--output-directory", required=True, type=Path)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    try:
        arguments = _arguments(argv)
        summary = run_experiment(
            arguments.source_root,
            arguments.manifest,
            arguments.frozen_input_commit,
            arguments.output_directory,
            arguments.implementation_commit,
        )
    except ConfigurationError as error:
        print(f"CASEF-DIAGNOSTIC-CONFIG: {error}", file=sys.stderr)
        return EXIT_USAGE
    except ExperimentInvalidated as error:
        print(f"CASEF-DIAGNOSTIC-INVALIDATED: {error}", file=sys.stderr)
        return EXIT_INVALIDATED
    except Exception as error:  # bounded diagnostic reporting, not canonical output
        print(f"CASEF-DIAGNOSTIC-FAILURE: {type(error).__name__}: {error}", file=sys.stderr)
        return EXIT_FAILURE
    print(
        "CASEF-DIAGNOSTIC-COMPLETED: "
        f"fixtures={summary['fixture_count_processed']} "
        f"utf8_success={summary['utf8_decode_success_count']} "
        f"utf8_failure={summary['utf8_decode_failure_count']}"
    )
    return EXIT_SUCCESS


if __name__ == "__main__":
    raise SystemExit(main())
