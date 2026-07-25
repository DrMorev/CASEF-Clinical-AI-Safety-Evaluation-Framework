from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tools.validate_schemas import (
    EXPECTED_INVALID_ERROR,
    EXPECTED_VALID_ERROR,
    ID_ERROR,
    JSON_ERROR,
    REGISTRY_ERROR,
    HarnessFailure,
    validate_repository,
)


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DRAFT_2020_12 = "https://json-schema.org/draft/2020-12/schema"


class SchemaValidationHarnessTests(unittest.TestCase):
    def _temporary_repository(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name)
        (root / "schemas" / "v0.6.1").mkdir(parents=True)
        return temporary, root

    def _write_schema(self, root: Path, name: str, schema: dict) -> Path:
        path = root / "schemas" / "v0.6.1" / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(schema), encoding="utf-8")
        return path

    def _write_vectors(
        self,
        root: Path,
        schema_id: str,
        reference: str,
        valid: list,
        invalid: list,
    ) -> Path:
        path = root / "schemas" / "v0.6.1" / "fixture" / "tests" / "fixture_cases.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(
                {
                    "schema_id": schema_id,
                    "cases": [
                        {
                            "name": "fixture",
                            "ref": reference,
                            "valid": valid,
                            "invalid": invalid,
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        return path

    @staticmethod
    def _schema(schema_id: str, definition: dict | None = None) -> dict:
        schema = {
            "$schema": DRAFT_2020_12,
            "$id": schema_id,
            "title": "Temporary harness fixture",
            "type": "object",
            "properties": {},
            "additionalProperties": False,
        }
        if definition is not None:
            schema["$defs"] = {"value": definition}
        return schema

    def test_current_repository_schema_tree_passes(self) -> None:
        summary = validate_repository(REPOSITORY_ROOT)
        self.assertEqual(summary.schema_count, 5)
        self.assertEqual(summary.vector_file_count, 5)
        self.assertEqual(summary.valid_count, 67)
        self.assertEqual(summary.invalid_count, 199)

    def test_malformed_schema_json_is_classified(self) -> None:
        temporary, root = self._temporary_repository()
        self.addCleanup(temporary.cleanup)
        path = root / "schemas" / "v0.6.1" / "bad.schema.json"
        path.write_text("{", encoding="utf-8")
        with self.assertRaises(HarnessFailure) as caught:
            validate_repository(root)
        self.assertEqual(caught.exception.code, JSON_ERROR)
        self.assertEqual(caught.exception.exit_code, 2)

    def test_duplicate_schema_id_fails(self) -> None:
        temporary, root = self._temporary_repository()
        self.addCleanup(temporary.cleanup)
        schema_id = "urn:casef:harness:duplicate"
        self._write_schema(root, "a.schema.json", self._schema(schema_id))
        self._write_schema(root, "b.schema.json", self._schema(schema_id))
        with self.assertRaises(HarnessFailure) as caught:
            validate_repository(root)
        self.assertEqual(caught.exception.code, ID_ERROR)
        self.assertEqual(caught.exception.exit_code, 2)

    def test_missing_registry_mapping_fails_closed(self) -> None:
        temporary, root = self._temporary_repository()
        self.addCleanup(temporary.cleanup)
        schema = self._schema("urn:casef:harness:missing")
        schema["$defs"] = {"missing": {"$ref": "absent.schema.json#/$defs/value"}}
        self._write_schema(root, "missing.schema.json", schema)
        with self.assertRaises(HarnessFailure) as caught:
            validate_repository(root)
        self.assertEqual(caught.exception.code, REGISTRY_ERROR)
        self.assertEqual(caught.exception.exit_code, 2)

    def test_relative_uri_is_rejected_with_format_checking(self) -> None:
        temporary, root = self._temporary_repository()
        self.addCleanup(temporary.cleanup)
        schema_id = "urn:casef:harness:uri"
        self._write_schema(
            root,
            "uri.schema.json",
            self._schema(schema_id, {"type": "string", "format": "uri"}),
        )
        self._write_vectors(root, schema_id, "#/$defs/value", ["relative/path"], [])
        with self.assertRaises(HarnessFailure) as caught:
            validate_repository(root)
        self.assertEqual(caught.exception.code, EXPECTED_VALID_ERROR)
        self.assertEqual(caught.exception.exit_code, 3)

    def test_expected_valid_failure_is_detected(self) -> None:
        temporary, root = self._temporary_repository()
        self.addCleanup(temporary.cleanup)
        schema_id = "urn:casef:harness:expected-valid"
        self._write_schema(
            root,
            "valid.schema.json",
            self._schema(schema_id, {"type": "integer"}),
        )
        self._write_vectors(root, schema_id, "#/$defs/value", ["not-an-integer"], [])
        with self.assertRaises(HarnessFailure) as caught:
            validate_repository(root)
        self.assertEqual(caught.exception.code, EXPECTED_VALID_ERROR)

    def test_expected_invalid_success_is_detected(self) -> None:
        temporary, root = self._temporary_repository()
        self.addCleanup(temporary.cleanup)
        schema_id = "urn:casef:harness:expected-invalid"
        self._write_schema(
            root,
            "invalid.schema.json",
            self._schema(schema_id, {"type": "integer"}),
        )
        self._write_vectors(root, schema_id, "#/$defs/value", [], [1])
        with self.assertRaises(HarnessFailure) as caught:
            validate_repository(root)
        self.assertEqual(caught.exception.code, EXPECTED_INVALID_ERROR)

    def test_unknown_schema_id_fails(self) -> None:
        temporary, root = self._temporary_repository()
        self.addCleanup(temporary.cleanup)
        self._write_schema(
            root,
            "known.schema.json",
            self._schema("urn:casef:harness:known", {"type": "string"}),
        )
        self._write_vectors(root, "urn:casef:harness:unknown", "#/$defs/value", [], [])
        with self.assertRaises(HarnessFailure) as caught:
            validate_repository(root)
        self.assertEqual(caught.exception.code, REGISTRY_ERROR)
        self.assertEqual(caught.exception.exit_code, 3)

    def test_unresolved_fragment_fails(self) -> None:
        temporary, root = self._temporary_repository()
        self.addCleanup(temporary.cleanup)
        schema_id = "urn:casef:harness:fragment"
        self._write_schema(
            root,
            "fragment.schema.json",
            self._schema(schema_id, {"type": "string"}),
        )
        self._write_vectors(root, schema_id, "#/$defs/absent", [], [])
        with self.assertRaises(HarnessFailure) as caught:
            validate_repository(root)
        self.assertEqual(caught.exception.code, REGISTRY_ERROR)
        self.assertEqual(caught.exception.exit_code, 3)

    def test_no_network_retrieval_is_attempted(self) -> None:
        temporary, root = self._temporary_repository()
        self.addCleanup(temporary.cleanup)
        schema = self._schema("urn:casef:harness:no-network")
        schema["$defs"] = {
            "remote": {"$ref": "https://example.invalid/remote.schema.json"}
        }
        self._write_schema(root, "no-network.schema.json", schema)
        with (
            mock.patch("urllib.request.urlopen") as urlopen,
            mock.patch("socket.create_connection") as create_connection,
            self.assertRaises(HarnessFailure) as caught,
        ):
            validate_repository(root)
        self.assertEqual(caught.exception.code, REGISTRY_ERROR)
        urlopen.assert_not_called()
        create_connection.assert_not_called()


if __name__ == "__main__":
    unittest.main()
