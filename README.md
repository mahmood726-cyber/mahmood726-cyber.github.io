# mahmood726-cyber.github.io

Source for **[mahmood726-cyber.github.io](https://mahmood726-cyber.github.io/)** — Mahmood Ahmad's curated portfolio of evidence-synthesis tools, courses, and methods atlases.

## How it works

- `data/site.yaml` — hero copy, byline, stats, about, footer.
- `data/showcase.yaml` — 15 hand-curated showcase cards in 3 sections.
- `templates/index.html.j2` — landing-page template.
- `templates/README.md.j2` — profile-README template (output pushed to `mahmood726-cyber/mahmood726-cyber`).
- `scripts/build.py` — renders both outputs from the YAML.
- `.github/workflows/build.yml` — GitHub Actions runs the build on every push to `master`, commits `index.html`, and pushes the profile README.
- `all/` — the legacy flat-table dashboard, preserved.
- The hero **"Claim a paper"** CTA points at `https://mahmood726-cyber.github.io/e156/students.html`, which is served by the **separate** repo `github.com/mahmood726-cyber/e156` (project Pages share the username domain via path). `students.html`, `claims.json`, and the generator scripts all live there — nothing in this repo needs to know how that page is built.

## Local build

```bash
pip install -r requirements.txt
python scripts/build.py \
  --site data/site.yaml \
  --showcase data/showcase.yaml \
  --out-html index.html \
  --out-readme dist/profile-README.md
pytest
```

## Editing showcase cards

Edit `data/showcase.yaml`. Schema is enforced by `tests/test_schemas.py` and by `scripts/build.py` at build time (exit code 2 on schema violation).

## License

MIT.
