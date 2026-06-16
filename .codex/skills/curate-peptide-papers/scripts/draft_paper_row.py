#!/usr/bin/env python3
"""Print a correctly ordered data/paper.csv row draft.

This helper validates section names without importing the package, so it can run
before the editable install step. It does not mutate repository files.
"""

from __future__ import annotations

import argparse
import ast
import csv
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional

COLUMNS = [
    "title",
    "sec",
    "subsec",
    "authors",
    "publications",
    "code",
    "dataset",
    "quality",
    "publish_date",
    "abstract",
    "blogs",
    "pined",
    "tags",
]


def default_repo_root() -> Path:
    return Path(__file__).resolve().parents[4]


def load_sections(repo_root: Path) -> Dict[str, List[str]]:
    config_path = repo_root / "awepep" / "config.py"
    module = ast.parse(config_path.read_text(encoding="utf-8"))
    for node in module.body:
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == "sections":
                return ast.literal_eval(node.value)
    raise RuntimeError(f"Could not find sections in {config_path}")


def markdown_link(label: Optional[str], url: Optional[str], field_name: str) -> str:
    if not label and not url:
        return ""
    if not label or not url:
        raise ValueError(f"{field_name} label and URL must be provided together")
    return f"[{label}]({url})"


def normalize_doi(doi: str) -> str:
    doi = doi.strip()
    doi = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", doi, flags=re.IGNORECASE)
    if not re.match(r"^10\.\d{3,9}/\S+$", doi, flags=re.IGNORECASE):
        raise ValueError(f"Invalid DOI: {doi}")
    return doi


def validate_date(value: str) -> str:
    if not re.match(r"^\d{4}-\d{1,2}-\d{1,2}$", value):
        raise ValueError("publish date must use YYYY-M-D or YYYY-MM-DD")
    year, month, day = (int(part) for part in value.split("-"))
    if not (1 <= month <= 12 and 1 <= day <= 31):
        raise ValueError(f"Invalid publish date: {value}")
    return f"{year}-{month}-{day}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=default_repo_root())
    parser.add_argument(
        "--header", action="store_true", help="print CSV header before the row"
    )
    parser.add_argument("--title", required=True)
    parser.add_argument("--sec", required=True)
    parser.add_argument("--subsec", required=True)
    parser.add_argument("--authors", required=True)
    parser.add_argument(
        "--venue", required=True, help="publication label, for example JCIM or arXiv"
    )
    parser.add_argument("--doi", required=True)
    parser.add_argument("--publish-date", required=True)
    parser.add_argument("--code-label")
    parser.add_argument("--code-url")
    parser.add_argument("--dataset-label")
    parser.add_argument("--dataset-url")
    parser.add_argument("--quality", choices=["", "high"], default="")
    parser.add_argument("--abstract", default="")
    parser.add_argument("--blog-label")
    parser.add_argument("--blog-url")
    parser.add_argument(
        "--pined", action="store_true", help="emit true in the pined column"
    )
    parser.add_argument("--tags", default="", help="slash-separated tags")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = args.repo_root.resolve()
    sections = load_sections(repo_root)

    if args.sec not in sections:
        valid = ", ".join(sections)
        raise ValueError(f"Invalid section {args.sec!r}. Valid sections: {valid}")
    if args.subsec not in sections[args.sec]:
        valid = ", ".join(sections[args.sec])
        raise ValueError(
            f"Invalid subsection {args.subsec!r} for {args.sec!r}. Valid subsections: {valid}"
        )

    doi = normalize_doi(args.doi)
    publication = f"[{args.venue}](https://doi.org/{doi})"

    row = {
        "title": args.title,
        "sec": args.sec,
        "subsec": args.subsec,
        "authors": args.authors,
        "publications": publication,
        "code": markdown_link(args.code_label, args.code_url, "code"),
        "dataset": markdown_link(args.dataset_label, args.dataset_url, "dataset"),
        "quality": args.quality,
        "publish_date": validate_date(args.publish_date),
        "abstract": args.abstract,
        "blogs": markdown_link(args.blog_label, args.blog_url, "blog"),
        "pined": "true" if args.pined else "",
        "tags": args.tags,
    }

    writer = csv.DictWriter(sys.stdout, fieldnames=COLUMNS, lineterminator="\n")
    if args.header:
        writer.writeheader()
    writer.writerow(row)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
