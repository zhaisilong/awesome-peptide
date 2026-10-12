# Paper-Read Source

The source submodule is `https://github.com/zhaisilong/paper-read.git` at `vendor/paper-read`; Markdown notes live in `src/site/notes`. Many notes contain JSON frontmatter, a permalink, Chinese/English prose and multiple DOI links.

## Update And Scan

```bash
git submodule update --init --recursive
git -C vendor/paper-read rev-parse HEAD
git submodule update --remote vendor/paper-read
git -C vendor/paper-read rev-parse HEAD
python .codex/skills/curate-peptide-papers/scripts/scan_paper_read_candidates.py --limit 200 --enrich-crossref
```

The compatibility scanner delegates to `awepep.discovery`. It prioritizes recent note paths, excludes README files, respects AMP word boundaries, distinguishes primary identifiers from known reference DOIs, and applies the display limit before API enrichment. Reports include ranked notes, identifier/link hints, snippets and enrichment errors. These hints are not verified resource associations.

Record the two SHAs and inspect `git -C vendor/paper-read diff --name-status OLD NEW -- src/site/notes`. Review new/modified notes first, then scan historical omissions. `awe-discover --limit 200` scans only paper-read by default. There is no publication-window cutoff for note-sourced papers; old publication dates belong in their normal chronological positions.

Accepted note URLs suppress duplicate additions even after replacing a preprint DOI with a formal URL. Archived preprints are skipped by default unless a new formal identifier appears. To review changed accepted/archived notes, use the compatibility scanner with `--include-duplicates` and inspect the changed paths explicitly. Neither a search cap nor a skipped archive record proves that the upstream library was exhaustively reviewed.

## Accept Into The Minimal Table

Use the verified formal publication DOI and exact config taxonomy in `data/paper-read.csv`. Use `source` for the note permalink or repo path, which renders as a paper-read blog link. Keep code/dataset links only when the note or primary source explicitly associates them with this paper. Bibliographic authors/venue/date/abstract live in the snapshot, not this CSV. When a formal conference paper or institutional technical report has no DOI, use `data/paper.csv` with its official HTTPS publication link and preserve `[paper-read](NOTE_URL)` in `blogs`; it still counts as a paper-read addition.

Include substantive peptide work irrespective of AI involvement. Skip incidental mentions, uncertain identity and duplicates. If a note lists several papers, verify which one its title describes instead of accepting the first DOI blindly. Formal publication is required even for owner-selected notes; unresolved preprints are not main-list additions.

## Historical Preprints

Check for a formal journal/conference version before archiving. Replace the citation and publication date only with primary-source evidence, preserving partial dates. Preserve the original preprint link in `blogs` when upgrading. Otherwise move the complete original record into `data/paper-archive.csv` with ISO `archived_at` and an evidence-based `archive_reason`. Expand a minimal row from its tracked snapshot and keep raw tags, source links and editorial fields; do not archive a README-formatted row. Retain existing snapshots as historical provenance. Archive records are excluded from generated paper lists, recent/pinned counts and active statistics, but remain validated. A later formal version can re-enter the active list without deleting the historical archive.

Run explicit metadata refresh after adding rows, commit the resulting snapshot alongside the CSV, and verify offline generation. A failed refresh with a cached record warns visibly; a missing offline record fails.
