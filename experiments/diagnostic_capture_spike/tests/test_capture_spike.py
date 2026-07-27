"""Standard-library tests for the bounded non-canonical capture spike."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import tempfile
import unittest
from unittest import mock
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = REPOSITORY_ROOT / "experiments/diagnostic_capture_spike/run_capture_spike.py"
SPEC = importlib.util.spec_from_file_location("capture_spike", MODULE_PATH)
assert SPEC and SPEC.loader
capture_spike = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = capture_spike
SPEC.loader.exec_module(capture_spike)
MANIFEST_PATH = REPOSITORY_ROOT / "experiments/diagnostic_capture_spike/fixtures/manifest.json"
FROZEN_COMMIT = "75a580d8057b483fa76cedcc2e773e2144016a96"


class CaptureSpikeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        self.source_root = self.root / "source"
        for fixture in self.manifest["fixtures"]:
            destination = self.source_root / fixture["relative_path"]
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(bytes.fromhex(fixture["byte_construction"]["hex"]))
        self.manifest_path = self.source_root / "experiments/diagnostic_capture_spike/fixtures/manifest.json"
        self.manifest_path.write_text(json.dumps(self.manifest), encoding="utf-8")
        self.output = self.root / "output"

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def _run(self) -> dict:
        return capture_spike.run_experiment(
            self.source_root, self.manifest_path, FROZEN_COMMIT, self.output, "a" * 40
        )

    def _write_manifest(self) -> None:
        self.manifest_path.write_text(json.dumps(self.manifest), encoding="utf-8")

    def _cli_arguments(self, output: Path | None = None) -> list[str]:
        return [
            "--source-root", str(self.source_root),
            "--manifest", str(self.manifest_path),
            "--frozen-input-commit", FROZEN_COMMIT,
            "--implementation-commit", "a" * 40,
            "--output-directory", str(output or self.output),
        ]

    def test_all_frozen_fixtures_process_with_expected_decode_split(self) -> None:
        summary = self._run()
        self.assertEqual(11, summary["source_verified_count"])
        self.assertEqual(9, summary["utf8_decode_success_count"])
        self.assertEqual(2, summary["utf8_decode_failure_count"])

    def test_source_byte_distinctions_and_binary_cases_are_preserved(self) -> None:
        fixtures = {entry["fixture_id"]: entry for entry in self.manifest["fixtures"]}
        lf = (self.source_root / fixtures["DC-FX-UTF8-LF-001"]["relative_path"]).read_bytes()
        crlf = (self.source_root / fixtures["DC-FX-UTF8-CRLF-001"]["relative_path"]).read_bytes()
        bom = (self.source_root / fixtures["DC-FX-UTF8-BOM-001"]["relative_path"]).read_bytes()
        trailing = (self.source_root / fixtures["DC-FX-TRAILING-WHITESPACE-001"]["relative_path"]).read_bytes()
        nul = (self.source_root / fixtures["DC-FX-NUL-BYTE-001"]["relative_path"]).read_bytes()
        self.assertNotEqual(lf, crlf)
        self.assertTrue(bom.startswith(b"\xef\xbb\xbf"))
        self.assertTrue(trailing.endswith(b" \t"))
        self.assertIn(b"\x00", nul)

    def test_lf_and_crlf_sources_have_distinct_exact_bytes(self) -> None:
        fixtures = {entry["fixture_id"]: entry for entry in self.manifest["fixtures"]}
        lf = (self.source_root / fixtures["DC-FX-UTF8-LF-001"]["relative_path"]).read_bytes()
        crlf = (self.source_root / fixtures["DC-FX-UTF8-CRLF-001"]["relative_path"]).read_bytes()
        self.assertNotEqual(lf, crlf)
        self.assertNotEqual(hashlib.sha256(lf).hexdigest(), hashlib.sha256(crlf).hexdigest())

    def test_bom_remains_in_source_bytes(self) -> None:
        fixture = next(item for item in self.manifest["fixtures"] if item["fixture_id"] == "DC-FX-UTF8-BOM-001")
        self.assertTrue((self.source_root / fixture["relative_path"]).read_bytes().startswith(b"\xef\xbb\xbf"))

    def test_trailing_whitespace_remains_in_source_bytes(self) -> None:
        fixture = next(item for item in self.manifest["fixtures"] if item["fixture_id"] == "DC-FX-TRAILING-WHITESPACE-001")
        self.assertTrue((self.source_root / fixture["relative_path"]).read_bytes().endswith(b" \t"))

    def test_embedded_nul_remains_in_source_bytes(self) -> None:
        fixture = next(item for item in self.manifest["fixtures"] if item["fixture_id"] == "DC-FX-NUL-BYTE-001")
        self.assertIn(b"\x00", (self.source_root / fixture["relative_path"]).read_bytes())

    def test_invalid_and_truncated_utf8_are_hashed_before_decode_failure(self) -> None:
        self._run()
        receipts = [json.loads(line) for line in (self.output / "diagnostic_receipts.jsonl").read_text().splitlines()]
        failures = [receipt for receipt in receipts if receipt["transformation_status"] == "FAILED"]
        self.assertEqual(["DC-FX-INVALID-UTF8-001", "DC-FX-TRUNCATED-UTF8-001"], [item["fixture_id"] for item in failures])
        self.assertTrue(all(item["capture_status"] == "SOURCE_BYTES_VERIFIED" for item in failures))
        self.assertTrue(all(item["transformation_error_type"] == "UnicodeDecodeError" for item in failures))

    def test_empty_file_and_no_derivatives(self) -> None:
        summary = self._run()
        self.assertEqual(0, summary["derivative_artifact_count"])
        empty = next(item for item in self.manifest["fixtures"] if item["fixture_id"] == "DC-FX-EMPTY-001")
        self.assertEqual(b"", (self.source_root / empty["relative_path"]).read_bytes())
        self.assertEqual({"diagnostic_receipts.jsonl", "run_summary.json"}, {path.name for path in self.output.iterdir()})

    def test_empty_file_succeeds_as_zero_byte_source(self) -> None:
        summary = self._run()
        self.assertEqual(11, summary["fixture_count_processed"])
        fixture = next(item for item in self.manifest["fixtures"] if item["fixture_id"] == "DC-FX-EMPTY-001")
        self.assertEqual(0, len((self.source_root / fixture["relative_path"]).read_bytes()))

    def test_length_mismatch_invalidates_before_transformation(self) -> None:
        target = self.source_root / self.manifest["fixtures"][0]["relative_path"]
        target.write_bytes(b"wrong")
        with self.assertRaises(capture_spike.ExperimentInvalidated):
            self._run()
        self.assertFalse(self.output.exists())

    def test_hash_mismatch_with_same_length_invalidates(self) -> None:
        target = self.source_root / self.manifest["fixtures"][0]["relative_path"]
        original = target.read_bytes()
        target.write_bytes(b"z" + original[1:])
        with self.assertRaises(capture_spike.ExperimentInvalidated):
            self._run()
        self.assertFalse(self.output.exists())

    def test_missing_fixture_invalidates(self) -> None:
        target = self.source_root / self.manifest["fixtures"][0]["relative_path"]
        target.unlink()
        with self.assertRaises(capture_spike.ExperimentInvalidated):
            self._run()

    def test_unexpected_fixture_invalidates(self) -> None:
        target = self.source_root / self.manifest["fixtures"][0]["relative_path"]
        (target.parent / "unexpected.bin").write_bytes(b"x")
        with self.assertRaises(capture_spike.ExperimentInvalidated):
            self._run()

    def test_nested_unexpected_manifest_name_invalidates(self) -> None:
        fixture_directory = self.source_root / "experiments/diagnostic_capture_spike/fixtures"
        nested = fixture_directory / "unexpected/manifest.json"
        nested.parent.mkdir(parents=True)
        nested.write_bytes(b"unexpected")
        with self.assertRaises(capture_spike.ExperimentInvalidated):
            self._run()

    def test_second_nested_unexpected_manifest_name_invalidates(self) -> None:
        fixture_directory = self.source_root / "experiments/diagnostic_capture_spike/fixtures"
        nested = fixture_directory / "nested/manifest.json"
        nested.parent.mkdir(parents=True)
        nested.write_bytes(b"unexpected")
        with self.assertRaises(capture_spike.ExperimentInvalidated):
            self._run()

    def test_length_hash_missing_and_unexpected_source_invalidate_before_transformation(self) -> None:
        target = self.source_root / self.manifest["fixtures"][0]["relative_path"]
        target.write_bytes(b"wrong")
        with self.assertRaises(capture_spike.ExperimentInvalidated):
            self._run()
        self.assertFalse(self.output.exists())
        target.write_bytes(bytes.fromhex(self.manifest["fixtures"][0]["byte_construction"]["hex"]))
        target.unlink()
        with self.assertRaises(capture_spike.ExperimentInvalidated):
            self._run()
        target.write_bytes(bytes.fromhex(self.manifest["fixtures"][0]["byte_construction"]["hex"]))
        (target.parent / "unexpected.bin").write_bytes(b"x")
        with self.assertRaises(capture_spike.ExperimentInvalidated):
            self._run()

    def test_duplicate_fixture_id_fails_closed(self) -> None:
        self.manifest["fixtures"][1]["fixture_id"] = self.manifest["fixtures"][0]["fixture_id"]
        self._write_manifest()
        with self.assertRaises(capture_spike.ExperimentInvalidated):
            self._run()

    def test_duplicate_fixture_path_fails_closed(self) -> None:
        self.manifest["fixtures"][1]["relative_path"] = self.manifest["fixtures"][0]["relative_path"]
        self._write_manifest()
        with self.assertRaises(capture_spike.ExperimentInvalidated):
            self._run()

    def test_path_escape_fails_closed(self) -> None:
        self.manifest["fixtures"][1]["relative_path"] = "../escape.bin"
        self._write_manifest()
        with self.assertRaises(capture_spike.ExperimentInvalidated):
            self._run()

    def test_malformed_manifest_fails_closed(self) -> None:
        self.manifest_path.write_text("{", encoding="utf-8")
        with self.assertRaises(capture_spike.ExperimentInvalidated):
            self._run()

    def test_invalidation_does_not_create_a_successful_output_directory(self) -> None:
        target = self.source_root / self.manifest["fixtures"][0]["relative_path"]
        target.write_bytes(b"wrong")
        with self.assertRaises(capture_spike.ExperimentInvalidated):
            self._run()
        self.assertFalse((self.output / "diagnostic_receipts.jsonl").exists())
        self.assertFalse((self.output / "run_summary.json").exists())

    def test_receipts_are_deterministic_and_statuses_are_separate(self) -> None:
        self._run()
        first = (self.output / "diagnostic_receipts.jsonl").read_bytes()
        alternate = self.root / "alternate"
        capture_spike.run_experiment(self.source_root, self.manifest_path, FROZEN_COMMIT, alternate, "a" * 40)
        self.assertEqual(first, (alternate / "diagnostic_receipts.jsonl").read_bytes())
        receipts = [json.loads(line) for line in first.decode("utf-8").splitlines()]
        self.assertEqual(sorted(item["fixture_id"] for item in receipts), [item["fixture_id"] for item in receipts])
        self.assertTrue(all(item["capture_status"] == "SOURCE_BYTES_VERIFIED" for item in receipts))

    def test_receipts_have_exact_fields_and_no_replacement_decode(self) -> None:
        self._run()
        receipts = [json.loads(line) for line in (self.output / "diagnostic_receipts.jsonl").read_text().splitlines()]
        self.assertTrue(all(tuple(receipt) == capture_spike.RECEIPT_FIELDS for receipt in receipts))
        failures = [receipt for receipt in receipts if receipt["transformation_status"] == "FAILED"]
        self.assertTrue(all(receipt["transformation_error_type"] == "UnicodeDecodeError" for receipt in failures))

    def test_capture_and_transformation_statuses_are_distinct(self) -> None:
        self._run()
        receipts = [json.loads(line) for line in (self.output / "diagnostic_receipts.jsonl").read_text().splitlines()]
        failed = next(receipt for receipt in receipts if receipt["fixture_id"] == "DC-FX-INVALID-UTF8-001")
        self.assertEqual("SOURCE_BYTES_VERIFIED", failed["capture_status"])
        self.assertEqual("FAILED", failed["transformation_status"])
        self.assertTrue(failed["transformation_attempted"])

    def test_sources_are_unchanged_after_execution(self) -> None:
        before = {
            entry["relative_path"]: (self.source_root / entry["relative_path"]).read_bytes()
            for entry in self.manifest["fixtures"]
        }
        self._run()
        after = {
            entry["relative_path"]: (self.source_root / entry["relative_path"]).read_bytes()
            for entry in self.manifest["fixtures"]
        }
        self.assertEqual(before, after)

    def test_no_derivative_file_is_created(self) -> None:
        self._run()
        self.assertTrue(all(not receipt["derivative_artifact_created"] for receipt in [
            json.loads(line) for line in (self.output / "diagnostic_receipts.jsonl").read_text().splitlines()
        ]))

    def test_cli_missing_required_argument_returns_usage_code(self) -> None:
        self.assertEqual(capture_spike.EXIT_USAGE, capture_spike.main([]))

    def test_cli_configuration_error_returns_usage_code(self) -> None:
        self.output.mkdir()
        (self.output / "already-present").write_text("x", encoding="utf-8")
        self.assertEqual(capture_spike.EXIT_USAGE, capture_spike.main(self._cli_arguments()))

    def test_cli_source_identity_mismatch_returns_invalidation_code(self) -> None:
        target = self.source_root / self.manifest["fixtures"][0]["relative_path"]
        target.write_bytes(b"wrong")
        self.assertEqual(capture_spike.EXIT_INVALIDATED, capture_spike.main(self._cli_arguments()))

    def test_cli_unexpected_execution_error_returns_failure_code(self) -> None:
        with mock.patch.object(capture_spike, "run_experiment", side_effect=RuntimeError("unexpected")):
            self.assertEqual(capture_spike.EXIT_FAILURE, capture_spike.main(self._cli_arguments()))

    def test_cli_successful_invocation_returns_success_code(self) -> None:
        self.assertEqual(capture_spike.EXIT_SUCCESS, capture_spike.main(self._cli_arguments()))


if __name__ == "__main__":
    unittest.main()
