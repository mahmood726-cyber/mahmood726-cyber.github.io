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


def test_minimal_showcase_passes_schema():
    schema = load_schema("showcase")
    data = load_yaml(REPO_ROOT / "tests" / "fixtures" / "minimal_showcase.yaml")
    validate(instance=data, schema=schema)

def test_showcase_schema_rejects_unknown_section():
    schema = load_schema("showcase")
    bad = {"cards": [{
        "id": "x",
        "title": "X",
        "one_liner": "y",
        "status": "live",
        "section": "ufology",  # not in enum
        "demo_url": "https://example.org",
        "repo_url": "https://example.org"
    }]}
    with pytest.raises(ValidationError):
        validate(instance=bad, schema=schema)

def test_showcase_schema_caps_at_15_cards():
    schema = load_schema("showcase")
    too_many = {"cards": [
        {
            "id": f"c{i}",
            "title": "T",
            "one_liner": "L",
            "status": "live",
            "section": "teaching",
            "demo_url": "https://example.org",
            "repo_url": "https://example.org",
        }
        for i in range(16)
    ]}
    with pytest.raises(ValidationError):
        validate(instance=too_many, schema=schema)


def test_production_site_passes_schema():
    schema = load_schema("site")
    data = load_yaml(REPO_ROOT / "data" / "site.yaml")
    validate(instance=data, schema=schema)


def test_production_showcase_passes_schema():
    schema = load_schema("showcase")
    data = load_yaml(REPO_ROOT / "data" / "showcase.yaml")
    validate(instance=data, schema=schema)

def test_production_showcase_has_15_cards():
    data = load_yaml(REPO_ROOT / "data" / "showcase.yaml")
    assert len(data["cards"]) == 15

def test_production_showcase_has_5_per_section():
    data = load_yaml(REPO_ROOT / "data" / "showcase.yaml")
    counts = {"teaching": 0, "atlases": 0, "clinical": 0}
    for card in data["cards"]:
        counts[card["section"]] += 1
    assert counts == {"teaching": 5, "atlases": 5, "clinical": 5}

def test_production_showcase_africa_thread_at_least_3():
    data = load_yaml(REPO_ROOT / "data" / "showcase.yaml")
    africa = [c for c in data["cards"] if c.get("africa_thread")]
    assert len(africa) >= 3, f"Africa thread on only {len(africa)} cards"
