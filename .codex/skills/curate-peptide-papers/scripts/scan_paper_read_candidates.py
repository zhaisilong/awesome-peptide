#!/usr/bin/env python3
"""Report peptide notes without changing curated CSV sources."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))

from awepep.discovery import KEYWORDS, enrich_note, keyword_hits, note_candidates


def scan(
    notes_root, csv_paths, keywords=KEYWORDS, enrich_crossref=False, crossref_timeout=20
):
    candidates = note_candidates(notes_root, csv_paths, keywords)
    if enrich_crossref:
        candidates = [enrich_note(item, crossref_timeout) for item in candidates]
    return candidates


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--notes-root", type=Path, default=ROOT / "vendor/paper-read/src/site/notes"
    )
    parser.add_argument("--csv", type=Path, default=ROOT / "data/paper.csv")
    parser.add_argument(
        "--paper-read-csv", type=Path, default=ROOT / "data/paper-read.csv"
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        default=Path("/tmp/paper-read-peptide-candidates.json"),
    )
    parser.add_argument(
        "--output-md", type=Path, default=Path("/tmp/paper-read-peptide-candidates.md")
    )
    parser.add_argument("--limit", type=int, default=50, help="Zero means no limit")
    parser.add_argument("--min-score", type=int, default=1)
    parser.add_argument("--include-duplicates", action="store_true")
    parser.add_argument("--enrich-crossref", action="store_true")
    parser.add_argument("--crossref-timeout", type=int, default=20)
    args = parser.parse_args()
    if not args.notes_root.is_dir():
        parser.error(
            "Initialize vendor/paper-read with git submodule update --init --recursive"
        )
    if args.limit < 0:
        parser.error("limit cannot be negative")
    candidates = scan(args.notes_root, [args.csv, args.paper_read_csv])
    candidates = [
        item
        for item in candidates
        if item["score"] >= args.min_score
        and (args.include_duplicates or not item["already_in_awesome"])
    ]
    total = len(candidates)
    if args.limit:
        candidates = candidates[: args.limit]
    if args.enrich_crossref:
        candidates = [enrich_note(item, args.crossref_timeout) for item in candidates]
    args.output_json.write_text(
        json.dumps(candidates, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    lines = [
        "# Paper-Read Peptide Candidates",
        "",
        f"Matched: {total}; showing: {len(candidates)}",
        "",
    ]
    for item in candidates:
        lines.extend(
            [
                f"## {item['title']}",
                "",
                f"- Note: {item['note_path']}",
                f"- Primary DOI: {item['primary_doi'] or '(missing)'}",
                f"- Publication date: {item.get('publish_date') or '(unknown)'}",
                f"- Already in awesome: {item['already_in_awesome']}",
                f"- Referenced known DOIs: {', '.join(item['duplicate_dois']) or '(none)'}",
                f"- Source: {item['source_urls'][0]}",
                f"- Metadata error: {item['crossref_error'] or '(none)'}",
                "",
            ]
        )
    args.output_md.write_text("\n".join(lines), encoding="utf-8")
    print(
        f"matched={total}, candidates={len(candidates)}\njson={args.output_json}\nmarkdown={args.output_md}"
    )


if __name__ == "__main__":
    main()
