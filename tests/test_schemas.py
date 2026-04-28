import json
from pathlib import Path
import pytest
import yaml
from jsonschema import validate, ValidationError

REPO_ROOT = Path(__file__).parent.parent

def load_schema(name: str) -> dict:
    with (REPO_ROOT / "schemas" / f"{name}.schema.json").open() as f:
        return json.load(f)

def load_yaml(path: Path) -> dict:
    with path.open() as f:
        return yaml.safe_load(f)

def test_minimal_site_passes_schema():
    schema = load_schema("site")
    data = load_yaml(REPO_ROOT / "tests" / "fixtures" / "minimal_site.yaml")
    validate(instance=data, schema=schema)  # raises if invalid

def test_site_schema_rejects_missing_hero():
    schema = load_schema("site")
    bad = {"name": "X", "byline_lines": ["Y"], "about": "Z", "stats": []}
    with pytest.raises(ValidationError):
        validate(instance=bad, schema=schema)
