import subprocess
import sys
from pathlib import Path
import yaml

REPO_ROOT = Path(__file__).parent.parent


def test_build_cli_writes_index_html(tmp_path):
    out_dir = tmp_path / "out"
    out_dir.mkdir()
    result = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "build.py"),
         "--site", str(REPO_ROOT / "data" / "site.yaml"),
         "--showcase", str(REPO_ROOT / "data" / "showcase.yaml"),
         "--out-html", str(out_dir / "index.html"),
         "--out-readme", str(out_dir / "profile-README.md")],
        capture_output=True, text=True, check=False,
    )
    assert result.returncode == 0, result.stderr
    assert (out_dir / "index.html").exists()
    assert (out_dir / "profile-README.md").exists()


def test_build_cli_index_contains_all_15_card_titles(tmp_path):
    showcase = yaml.safe_load((REPO_ROOT / "data" / "showcase.yaml").read_text(encoding="utf-8"))
    out_dir = tmp_path / "out"
    out_dir.mkdir()
    subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "build.py"),
         "--site", str(REPO_ROOT / "data" / "site.yaml"),
         "--showcase", str(REPO_ROOT / "data" / "showcase.yaml"),
         "--out-html", str(out_dir / "index.html"),
         "--out-readme", str(out_dir / "profile-README.md")],
        check=True,
    )
    html = (out_dir / "index.html").read_text(encoding="utf-8")
    for card in showcase["cards"]:
        assert card["title"] in html, f"missing card: {card['title']}"


def test_build_cli_validates_yaml_against_schema(tmp_path):
    bad_site = tmp_path / "bad_site.yaml"
    bad_site.write_text("name: X\n", encoding="utf-8")
    out_dir = tmp_path / "out"
    out_dir.mkdir()
    result = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "build.py"),
         "--site", str(bad_site),
         "--showcase", str(REPO_ROOT / "data" / "showcase.yaml"),
         "--out-html", str(out_dir / "index.html"),
         "--out-readme", str(out_dir / "profile-README.md")],
        capture_output=True, text=True, check=False,
    )
    assert result.returncode != 0
    assert "schema" in (result.stderr + result.stdout).lower()
