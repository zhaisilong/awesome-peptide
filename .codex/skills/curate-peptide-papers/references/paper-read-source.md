# Paper-Read Source

The source submodule is `https://github.com/zhaisilong/paper-read.git` at `vendor/paper-read`; Markdown notes live in `src/site/notes`. Many notes contain JSON frontmatter, a permalink, Chinese/English prose and multiple DOI links.

## Update And Scan

```bash
git submodule update --init --recursive
git submodule update --remote vendor/paper-read
python .codex/skills/curate-peptide-papers/scripts/scan_paper_read_candidates.py --limit 200 --enrich-crossref
```

The compatibility scanner delegates to `awepep.discovery`. It prioritizes recent note paths, excludes README files, respects AMP word boundaries, distinguishes primary identifiers from known reference DOIs, and applies the display limit before API enrichment. Reports include ranked notes, identifier/link hints, snippets and enrichment errors. These hints are not verified resource associations.

Use `awe-discover --since DATE --until DATE --sources paper-read` when a publication-window report is required. Note month controls triage order only, never publication eligibility. Initialize the submodule if notes are missing; never edit vendor content.

## Accept Into The Minimal Table

Use the raw normalized DOI and exact config taxonomy in `data/paper-read.csv`. Use `source` for the note permalink or repo path, which renders as a paper-read blog link. Keep code/dataset links only when the note or primary source explicitly associates them with this paper. Bibliographic authors/venue/date/abstract live in the snapshot, not this CSV.

Skip incidental peptide mentions, uncertain primary identifiers, duplicates and ambiguous relevance. If a note lists several papers, verify which one its title describes instead of accepting the first DOI blindly. Outside-window older papers are migrations/updates only when separately requested, not new-window additions.

Run explicit metadata refresh after adding rows, commit the resulting snapshot alongside the CSV, and verify offline generation. A failed refresh with a cached record warns visibly; a missing offline record fails.
