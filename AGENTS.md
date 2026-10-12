# Agent Guide

Use the repo-local skills in `.codex/skills` for recurring work:

- `$curate-peptide-papers`: add, verify, classify, and validate paper metadata.
- `$maintain-awepep-tooling`: update the Python package, templates, checks, CI, and docs.

## Source Of Truth

- Edit `data/paper.csv` for full paper entries, including DOI-less formal paper-read papers with their note link in `blogs`.
- Edit `data/paper-read.csv` for formal DOI-backed paper-read entries. Keep it minimal; bibliographic metadata is recorded in `data/paper-read-metadata.json` from Crossref. Historical arXiv snapshots are provenance, not new intake.
- Edit `data/paper-archive.csv` for historical preprints without a verified formal version; preserve fields/source and record `archived_at`/`archive_reason`. Archives never enter active generation or statistics. Check for formal upgrades before archiving.
- Keep metadata snapshots tracked with their source and retrieval time. Refresh explicitly; use offline generation for review and CI.
- Use canonical tags from `awepep.config.tag_groups`. Add new tags to the vocabulary before using them, and treat tag audit warnings as curation debt.
- Edit `DATABASE.md` for Chapter 0 resource tables and guides. Store benchmark/dataset papers in CSV, not a second manual paper list.
- Treat `README.md` as generated output from CSV, `DATABASE.md`, and `awepep/template.py`.
- Do not hand-edit generated paper sections in `README.md` unless the user explicitly asks for a one-off patch.
- Treat `vendor/paper-read` as an external source submodule. Do not edit files inside it; update it with `git submodule update --remote vendor/paper-read`.

## Paper-Read Curation

Use `$curate-peptide-papers` when pulling latest paper notes from `vendor/paper-read`. This owner-maintained library is the primary source; substantive peptide work is eligible regardless of AI involvement, subject to formal-publication verification.

```bash
git submodule update --init --recursive
git -C vendor/paper-read rev-parse HEAD
git submodule update --remote vendor/paper-read
git -C vendor/paper-read rev-parse HEAD
awe-discover --limit 200
```

Compare the old/new commits and prioritize new/modified notes, including formal-version updates to accepted/archived work. Scan historical omissions too; insert older papers by actual publication date, not note date or a recent-window cutoff. Choose `sec/subsec` by primary contribution from config. APIs supply bibliographic fields, not editorial decisions. Use code/data links only when explicitly associated with the paper.

## On-Demand Discovery

Independent discovery is a small supplement after paper-read: target 2-3 accepted papers, maximum 3 per run across all providers, no quota filling. Prefer AIDD; exceptional purely experimental work needs a significance rationale. Paper-read additions, historical upgrades and metadata verification are outside that quota.

```bash
awe-discover --sources crossref,pubmed --since YYYY-MM-DD --until YYYY-MM-DD --limit 10
```

External discovery requires explicit sources and dates; `--limit` caps candidates per query, not accepted additions. Default discovery uses only paper-read. Review reports, errors and truncation. The command does not modify CSVs. Require formal journals/conferences or credible institutional technical reports; ordinary arXiv/bioRxiv preprints are not new additions. Prefer formal DOI citations, otherwise official stable HTTPS URLs with publication evidence. Preserve partial dates; registration, acceptance and note dates are not publication dates. No scheduled paper-adding Actions are needed.

## Required Checks

```bash
python -m pip install -e ".[dev]"
git submodule update --init --recursive
awe-check
python .codex/skills/curate-peptide-papers/scripts/audit_tags.py --strict
python -m unittest discover -s tests -v
python - <<'PY'
from awepep.paper import PaperList
md = PaperList("data/paper.csv", offline=True).get_md(write=False)
print(len(md), md.splitlines()[0])
PY
```

Regenerate only after source/template changes. Use `awe-pep --refresh-metadata` to update snapshots online, then `awe-pep --offline --as-of YYYY-MM-DD` for reproducible output. Missing offline records fail; cached refresh fallback warns. Review generated anchors and content before committing.
