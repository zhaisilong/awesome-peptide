---
name: maintain-awepep-tooling
description: Maintain awesome-peptide discovery, metadata snapshots, offline README generation, validation, packaging and CI. Use for awepep Python code, Liquid templates, taxonomy migrations, console scripts and workflow documentation.
---

# Maintain Awepep Tooling

Use this skill for code and workflow maintenance in the `awesome-peptide` repository. Keep tooling changes separate from paper curation unless the user asks for both.

## Quick Start

1. Inspect the worktree and relevant code:
```bash
git status --short
rg "awe-pep|awe-check|awepep|awecheck|python-liquid|Template|README" .
```

2. Read the relevant references:
- `references/tooling-maintenance.md` for package, dependency, and validation behavior.
- `references/generated-readme.md` for generator/template rules.

3. Install dependencies if validation imports fail:
```bash
python -m pip install -e ".[dev]"
```

4. Run focused checks after changes:
```bash
awe-check
python .codex/skills/curate-peptide-papers/scripts/audit_tags.py --strict
python -m unittest discover -s tests -v
python - <<'PY'
from awepep.paper import PaperList
md = PaperList("data/paper.csv", offline=True).get_md(write=False)
print(len(md), md.splitlines()[0])
PY
awe-pep --offline --as-of 2026-10-03
git diff -- README.md
```

## Maintenance Workflow

For package, generator, or validation changes:

1. Identify whether the task affects generation, validation, packaging, documentation, or all of them.
2. Read the affected implementation before editing. Generation lives in `paper.py` and `template.py`; API discovery in `discovery.py` and `crossref.py`; snapshots in `metadata.py`; schema/tag checks in `check.py`, `config.py` and `tags.py`.
3. Preserve the CSV schema and generated Markdown shape unless the user asks for a migration.
4. If changing templates or generation order, regenerate `README.md` and inspect the diff for unintended content loss.
5. If changing validation logic, test both passing data and at least one failing condition when practical.
6. Keep unrelated paper metadata changes out of tooling fixes.

## Known Audit Points

- Runtime package metadata lives in `pyproject.toml`; keep console scripts, CI, and docs aligned when changing command names.
- `README.md` contains a top note about update frequency and MolAstra links; keep it in `awepep/template.py` so regeneration preserves it.
- License metadata should stay aligned with the GPLv3 `LICENSE` file.
- `awepep.check.main` should raise validation errors so CI fails on invalid data.
- Verify installed CLI entrypoints actually parse new flags, not just module invocations.
- Keep discovery non-mutating. Report API errors and truncation; use bounded retries and no scheduled paper-adding workflow.
- Test offline generation with the network disabled by mocks, snapshot misses, refresh fallback, partial/future dates, false flags, subsection order and heading anchors.

## Guardrails

- Use `apply_patch` for manual source edits.
- Do not run formatters that rewrite unrelated files.
- Do not change taxonomy spelling or CSV content while fixing command/dependency issues unless that is required for the task.
- Treat `README.md` as generated output except for deliberate template or generator migrations.
- Mention any validation that could not run because dependencies are missing.

## References

- Read `references/tooling-maintenance.md` before source changes.
- Read `references/generated-readme.md` before changing templates, generation flow, or `README.md`.
