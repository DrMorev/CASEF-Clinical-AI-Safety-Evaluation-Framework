"""Development-only CASEF JSON Schema and vector validation harness.

The CASEF-HARNESS-* codes below are bounded developer diagnostics. They are
not the future canonical validation-error record or vocabulary, and this
harness does not produce validation_record evidence.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterator
from urllib.parse import urljoin

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import SchemaError
from referencing import Registry, Resource


DRAFT_2020_12 = "https://json-schema.org/draft/2020-12/schema"

JSON_ERROR = "CASEF-HARNESS-JSON"
META_ERROR = "CASEF-HARNESS-META"
ID_ERROR = "CASEF-HARNESS-ID"
REGISTRY_ERROR = "CASEF-HARNESS-REGISTRY"
VECTOR_ERROR = "CASEF-HARNESS-VECTOR"
EXPECTED_VALID_ERROR = "CASEF-HARNESS-EXPECTED-VALID"
EXPECTED_INVALID_ERROR = "CASEF-HARNESS-EXPECTED-INVALID"

SETUP_EXIT = 2
VECTOR_EXIT = 3


class HarnessFailure(Exception):
    """A bounded harness failure with deterministic classification."""

    def __init__(self, exit_code: int, code: str, message: str) -> None:
        super().__init__(message)
        self.exit_code = exit_code
        self.code = code
        self.message = message


@dataclass(frozen=True)
class HarnessSummary:
    schema_count: int
    vector_file_count: int
    valid_count: int
    invalid_count: int


def _relative(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def _load_json(path: Path, root: Path, exit_code: int) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        del exc
        raise HarnessFailure(
            exit_code,
            JSON_ERROR,
            f"{_relative(path, root)} is not readable canonical JSON",
        ) from None


def _iter_refs(value: Any) -> Iterator[str]:
    if isinstance(value, dict):
        for key, child in value.items():
            if key == "$ref" and isinstance(child, str):
                yield child
            else:
                yield from _iter_refs(child)
    elif isinstance(value, list):
        for child in value:
            yield from _iter_refs(child)


def _load_schemas(
    repository_root: Path,
) -> tuple[dict[str, dict[str, Any]], Registry]:
    schema_root = repository_root / "schemas" / "v0.6.1"
    schema_paths = sorted(schema_root.rglob("*.schema.json"))
    if not schema_paths:
        raise HarnessFailure(
            SETUP_EXIT,
            ID_ERROR,
            "schemas/v0.6.1 contains no discoverable schema files",
        )

    schemas: dict[str, dict[str, Any]] = {}
    sources: dict[str, Path] = {}
    for path in schema_paths:
        schema = _load_json(path, repository_root, SETUP_EXIT)
        if not isinstance(schema, dict):
            raise HarnessFailure(
                SETUP_EXIT,
                META_ERROR,
                f"{_relative(path, repository_root)} root is not an object",
            )
        schema_id = schema.get("$id")
        if not isinstance(schema_id, str) or not schema_id:
            raise HarnessFailure(
                SETUP_EXIT,
                ID_ERROR,
                f"{_relative(path, repository_root)} has no non-empty $id",
            )
        if schema_id in schemas:
            raise HarnessFailure(
                SETUP_EXIT,
                ID_ERROR,
                f"duplicate $id in {_relative(sources[schema_id], repository_root)} and {_relative(path, repository_root)}",
            )
        try:
            Draft202012Validator.check_schema(schema)
        except SchemaError:
            raise HarnessFailure(
                SETUP_EXIT,
                META_ERROR,
                f"{_relative(path, repository_root)} failed Draft 2020-12 meta-schema validation",
            ) from None
        schemas[schema_id] = schema
        sources[schema_id] = path

    try:
        resources = (
            (schema_id, Resource.from_contents(schema))
            for schema_id, schema in sorted(schemas.items())
        )
        # Registry() has no retrieval callback. Missing resources therefore
        # fail closed instead of falling back to network retrieval.
        registry = Registry().with_resources(resources)
    except Exception:
        raise HarnessFailure(
            SETUP_EXIT,
            REGISTRY_ERROR,
            "local immutable-$id registry construction failed",
        ) from None

    for schema_id, schema in sorted(schemas.items()):
        resolver = registry.resolver(base_uri=schema_id)
        for reference in sorted(set(_iter_refs(schema))):
            try:
                resolver.lookup(reference)
            except Exception:
                raise HarnessFailure(
                    SETUP_EXIT,
                    REGISTRY_ERROR,
                    f"{_relative(sources[schema_id], repository_root)} has an unresolved schema reference",
                ) from None

    return schemas, registry


def _require_vector_envelope(
    vector: Any,
    path: Path,
    repository_root: Path,
) -> tuple[str, list[dict[str, Any]]]:
    label = _relative(path, repository_root)
    if not isinstance(vector, dict):
        raise HarnessFailure(VECTOR_EXIT, VECTOR_ERROR, f"{label} root is not an object")
    schema_id = vector.get("schema_id")
    cases = vector.get("cases")
    if not isinstance(schema_id, str) or not schema_id or not isinstance(cases, list):
        raise HarnessFailure(
            VECTOR_EXIT,
            VECTOR_ERROR,
            f"{label} has an invalid vector envelope",
        )
    normalized: list[dict[str, Any]] = []
    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            raise HarnessFailure(
                VECTOR_EXIT,
                VECTOR_ERROR,
                f"{label} case {index} is not an object",
            )
        name = case.get("name")
        reference = case.get("ref")
        valid = case.get("valid")
        invalid = case.get("invalid")
        if (
            not isinstance(name, str)
            or not name
            or not isinstance(reference, str)
            or not reference
            or not isinstance(valid, list)
            or not isinstance(invalid, list)
        ):
            raise HarnessFailure(
                VECTOR_EXIT,
                VECTOR_ERROR,
                f"{label} case {index} has an invalid contract",
            )
        normalized.append(case)
    return schema_id, normalized


def validate_repository(repository_root: Path) -> HarnessSummary:
    """Validate discovered schemas and vectors without network retrieval."""

    repository_root = repository_root.resolve()
    schema_root = repository_root / "schemas" / "v0.6.1"
    schemas, registry = _load_schemas(repository_root)
    format_checker = FormatChecker()
    if "uri" not in format_checker.checkers:
        raise HarnessFailure(
            SETUP_EXIT,
            META_ERROR,
            "Draft 2020-12 URI format checker is unavailable",
        )

    vector_paths = sorted(
        path
        for path in schema_root.rglob("*_cases.json")
        if "tests" in path.relative_to(schema_root).parts
    )
    valid_count = 0
    invalid_count = 0

    for path in vector_paths:
        vector = _load_json(path, repository_root, VECTOR_EXIT)
        schema_id, cases = _require_vector_envelope(vector, path, repository_root)
        if schema_id not in schemas:
            raise HarnessFailure(
                VECTOR_EXIT,
                REGISTRY_ERROR,
                f"{_relative(path, repository_root)} names an unknown schema_id",
            )
        resolver = registry.resolver(base_uri=schema_id)
        for case_index, case in enumerate(cases):
            full_reference = (
                schema_id + case["ref"]
                if case["ref"].startswith("#")
                else urljoin(schema_id, case["ref"])
            )
            try:
                resolver.lookup(case["ref"])
            except Exception:
                raise HarnessFailure(
                    VECTOR_EXIT,
                    REGISTRY_ERROR,
                    f"{_relative(path, repository_root)} case {case_index} has an unresolved ref",
                ) from None
            validator = Draft202012Validator(
                {"$schema": DRAFT_2020_12, "$ref": full_reference},
                registry=registry,
                format_checker=format_checker,
            )
            for value_index, value in enumerate(case["valid"]):
                try:
                    errors = list(validator.iter_errors(value))
                except Exception:
                    raise HarnessFailure(
                        VECTOR_EXIT,
                        REGISTRY_ERROR,
                        f"{_relative(path, repository_root)} case {case_index} could not resolve a valid vector",
                    ) from None
                if errors:
                    raise HarnessFailure(
                        VECTOR_EXIT,
                        EXPECTED_VALID_ERROR,
                        f"{_relative(path, repository_root)} case {case_index} valid item {value_index} failed",
                    )
                valid_count += 1
            for value_index, value in enumerate(case["invalid"]):
                try:
                    errors = list(validator.iter_errors(value))
                except Exception:
                    raise HarnessFailure(
                        VECTOR_EXIT,
                        REGISTRY_ERROR,
                        f"{_relative(path, repository_root)} case {case_index} could not resolve an invalid vector",
                    ) from None
                if not errors:
                    raise HarnessFailure(
                        VECTOR_EXIT,
                        EXPECTED_INVALID_ERROR,
                        f"{_relative(path, repository_root)} case {case_index} invalid item {value_index} passed",
                    )
                invalid_count += 1

    return HarnessSummary(
        schema_count=len(schemas),
        vector_file_count=len(vector_paths),
        valid_count=valid_count,
        invalid_count=invalid_count,
    )


def main() -> int:
    repository_root = Path(__file__).resolve().parents[1]
    try:
        summary = validate_repository(repository_root)
    except HarnessFailure as failure:
        print(f"{failure.code}: {failure.message}", file=sys.stderr)
        return failure.exit_code
    print(
        "CASEF-HARNESS-OK "
        f"schemas={summary.schema_count} "
        f"vector_files={summary.vector_file_count} "
        f"valid={summary.valid_count} "
        f"invalid={summary.invalid_count}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
