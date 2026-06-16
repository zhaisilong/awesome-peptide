# Tooling Maintenance

Use this reference before changing package code, packaging metadata, validation logic, CI, or contributor docs.

## Important Files

- `pyproject.toml`: package metadata, dependencies, optional dev dependencies, and console scripts.
- `awepep/main.py`: CLI entrypoint that creates `PaperList` and prints/writes generated Markdown.
- `awepep/paper.py`: generator implementation.
- `awepep/template.py`: Liquid templates and README footer/citation text.
- `awepep/check.py`: validation and statistics.
- `awepep/config.py`: taxonomy, linked tags, pinned/recent settings.
- `CONTRIBUTING.md`: contributor setup commands.
- `README.md`: generated output, but may also reveal generator drift.
- `DATABASE.md`: manually maintained content inserted into README.

## Current Audit Points

- Keep `pyproject.toml`, `CONTRIBUTING.md`, `AGENTS.md`, and `.github/workflows/ci.yml` aligned when command names or dependencies change.
- Generated header drift is easy to reintroduce; keep the README top note in `awepep/template.py`.
- Keep package license metadata aligned with the GPLv3 `LICENSE` file.
- Keep validation errors uncaught in `awepep.check.main` so CI receives a nonzero exit code.
- The checker requires every `publications` field to contain a DOI-like Markdown link.

## Change Guidelines

- Keep generated README output stable unless the task explicitly changes presentation.
- If changing CSV schema, update generator, checker, references, and any helper scripts together.
- If changing taxonomy names, account for anchors in README and existing CSV rows.
- If changing command names, update `pyproject.toml`, `CONTRIBUTING.md`, `AGENTS.md`, CI, and skill references together.
- If changing validation behavior, preserve duplicate DOI checks, required field checks, section checks, and pinned count checks unless the user requests otherwise.

## Validation Commands

Install editable package:

```bash
pip install -e ".[dev]"
```

Run content validation:

```bash
awe-check
```

Run no-write generation smoke test:

```bash
python - <<'PY'
from awepep.paper import PaperList
md = PaperList("data/paper.csv").get_md(write=False)
print(len(md), md.splitlines()[0])
PY
```

Regenerate README when generator or template behavior changes:

```bash
awe-pep
git diff -- README.md
```

If console scripts are unavailable, use:

```bash
python -m awepep.check
python -m awepep.main
```
