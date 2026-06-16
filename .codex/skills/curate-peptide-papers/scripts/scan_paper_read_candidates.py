#!/usr/bin/env python3
"""Scan vendor/paper-read notes for peptide-related paper candidates."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path
from typing import Dict, Iterable, List, Sequence

ROOT = Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from awepep import crossref

KEYWORDS = [
    "peptide",
    "peptid",
    "cyclic peptide",
    "macrocycle",
    "macrocyclic",
    "protein-peptide",
    "protein peptide",
    "antimicrobial peptide",
    "AMP",
    "AMPs",
    "肽",
    "多肽",
    "抗菌肽",
    "环肽",
    "肽段",
]

DOI_RE = re.compile(r"10\.\d{3,9}/[-._;()/:A-Z0-9]+", re.IGNORECASE)
URL_RE = re.compile(r"https?://[^\s<>)\"']+")
H1_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)
PERMALINK_RE = re.compile(r'"permalink"\s*:\s*"([^"]+)"')


def repo_root() -> Path:
    return Path(__file__).resolve().parents[4]


def normalize_doi(doi: str) -> str:
    return doi.rstrip(".,;:)]}").lower()


def current_dois(csv_paths: Sequence[Path]) -> set:
    dois = set()
    for csv_path in csv_paths:
        if not csv_path.exists():
            continue
        with csv_path.open(newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                for doi in DOI_RE.findall(row.get("publications", "")):
                    dois.add(normalize_doi(doi))
                for doi in DOI_RE.findall(row.get("doi", "")):
                    dois.add(normalize_doi(doi))
    return dois


def ordered_dois(text: str) -> List[str]:
    dois = []
    seen = set()
    for doi in DOI_RE.findall(text):
        normalized = normalize_doi(doi)
        if normalized not in seen:
            dois.append(normalized)
            seen.add(normalized)
    return dois


def strip_frontmatter(text: str) -> str:
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            return parts[2]
    return text


def infer_note_month(relative_path: Path) -> str:
    for part in relative_path.parts:
        if re.fullmatch(r"20\d{4}", part):
            return f"{part[:4]}-{part[4:]}"
    for part in relative_path.parts:
        if re.fullmatch(r"20\d{2}", part):
            return part
    return ""


def title_from_note(text: str, path: Path) -> str:
    body = strip_frontmatter(text)
    match = H1_RE.search(body)
    if match:
        return match.group(1).strip()
    return path.stem


def keyword_hits(text: str, keywords: Sequence[str]) -> Dict[str, int]:
    hits = {}
    for keyword in keywords:
        flags = (
            0 if any("\u4e00" <= ch <= "\u9fff" for ch in keyword) else re.IGNORECASE
        )
        pattern = re.escape(keyword)
        count = len(re.findall(pattern, text, flags))
        if count:
            hits[keyword] = count
    return hits


def snippets(text: str, keywords: Sequence[str], max_snippets: int = 3) -> List[str]:
    lines = [
        line.strip() for line in strip_frontmatter(text).splitlines() if line.strip()
    ]
    found = []
    for line in lines:
        lower = line.lower()
        if any(
            keyword.lower() in lower for keyword in keywords if keyword.isascii()
        ) or any(keyword in line for keyword in keywords if not keyword.isascii()):
            found.append(line[:240])
        if len(found) >= max_snippets:
            break
    return found


def split_links(urls: Iterable[str]) -> Dict[str, List[str]]:
    code = []
    dataset = []
    doi = []
    other = []
    for raw_url in urls:
        url = raw_url.rstrip(".,;:)]}")
        lower = url.lower()
        if "doi.org/" in lower:
            doi.append(url)
        elif (
            "github.com" in lower or "huggingface.co" in lower or "gitlab.com" in lower
        ):
            code.append(url)
        elif any(
            token in lower
            for token in ["zenodo", "figshare", "dryad", "dataset", "data"]
        ):
            dataset.append(url)
        else:
            other.append(url)
    return {
        "doi_links": sorted(set(doi)),
        "code_links": sorted(set(code)),
        "dataset_links": sorted(set(dataset)),
        "other_links": sorted(set(other)),
    }


def scan(
    notes_root: Path,
    csv_paths: Sequence[Path],
    keywords: Sequence[str],
    enrich_crossref: bool = False,
    crossref_timeout: int = 20,
) -> List[dict]:
    existing_dois = current_dois(csv_paths)
    candidates = []
    for path in sorted(notes_root.rglob("*.md")):
        text = path.read_text(encoding="utf-8", errors="ignore")
        hits = keyword_hits(text, keywords)
        if not hits:
            continue

        relative_path = path.relative_to(notes_root)
        dois = ordered_dois(text)
        link_groups = split_links(URL_RE.findall(text))
        duplicate_dois = sorted(set(dois) & existing_dois)
        score = sum(hits.values())
        group = relative_path.parts[0] if relative_path.parts else ""
        crossref_metadata = {}
        crossref_error = ""
        if enrich_crossref and dois:
            try:
                crossref_metadata = crossref.metadata_for_doi(
                    dois[0], timeout=crossref_timeout
                )
            except Exception as exc:
                crossref_error = str(exc)

        candidates.append(
            {
                "score": score,
                "note_path": str(relative_path),
                "group": group,
                "title": title_from_note(text, path),
                "note_month": infer_note_month(relative_path),
                "permalink": (
                    PERMALINK_RE.search(text).group(1)
                    if PERMALINK_RE.search(text)
                    else ""
                ),
                "keyword_hits": hits,
                "primary_doi": dois[0] if dois else "",
                "dois": dois,
                "duplicate_dois": duplicate_dois,
                "already_in_awesome": bool(duplicate_dois),
                "crossref_metadata": crossref_metadata,
                "crossref_error": crossref_error,
                "snippets": snippets(text, keywords),
                **link_groups,
            }
        )

    return sorted(
        candidates,
        key=lambda item: (
            item["already_in_awesome"],
            -item["score"],
            item["note_path"],
        ),
    )


def write_markdown(candidates: Sequence[dict], output_path: Path, limit: int) -> None:
    rows = candidates[:limit] if limit else candidates
    lines = ["# Paper-Read Peptide Candidates", ""]
    lines.append(f"Total candidates: {len(candidates)}")
    if limit:
        lines.append(f"Showing top: {len(rows)}")
    lines.append("")

    for idx, item in enumerate(rows, 1):
        duplicate = "yes" if item["already_in_awesome"] else "no"
        lines.extend(
            [
                f"## {idx}. {item['title']}",
                "",
                f"- Score: {item['score']}",
                f"- Path: `{item['note_path']}`",
                f"- Group: `{item['group']}`",
                f"- Note month: `{item['note_month']}`",
                f"- Already in awesome: `{duplicate}`",
                f"- Primary DOI: {item['primary_doi'] or '(none)'}",
                f"- DOI: {', '.join(item['dois']) if item['dois'] else '(none)'}",
                f"- Code links: {', '.join(item['code_links']) if item['code_links'] else '(none)'}",
                f"- Dataset links: {', '.join(item['dataset_links']) if item['dataset_links'] else '(none)'}",
                f"- Permalink: {item['permalink'] or '(none)'}",
                "",
            ]
        )
        if item["crossref_metadata"]:
            metadata = item["crossref_metadata"]
            lines.extend(
                [
                    "Crossref:",
                    f"- Title: {metadata['title']}",
                    f"- Authors: {metadata['authors']}",
                    f"- Publication: {metadata['publications']}",
                    f"- Publish date: {metadata['publish_date']}",
                    "",
                ]
            )
        if item["crossref_error"]:
            lines.extend(["Crossref:", f"- Error: {item['crossref_error']}", ""])
        if item["snippets"]:
            lines.append("Snippets:")
            for snippet in item["snippets"]:
                lines.append(f"> {snippet}")
            lines.append("")

    output_path.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    root = repo_root()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--notes-root", type=Path, default=root / "vendor/paper-read/src/site/notes"
    )
    parser.add_argument("--csv", type=Path, default=root / "data/paper.csv")
    parser.add_argument(
        "--paper-read-csv", type=Path, default=root / "data/paper-read.csv"
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        default=Path("/tmp/paper-read-peptide-candidates.json"),
    )
    parser.add_argument(
        "--output-md", type=Path, default=Path("/tmp/paper-read-peptide-candidates.md")
    )
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--min-score", type=int, default=1)
    parser.add_argument("--include-duplicates", action="store_true")
    parser.add_argument("--enrich-crossref", action="store_true")
    parser.add_argument("--crossref-timeout", type=int, default=20)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.notes_root.exists():
        raise FileNotFoundError(
            f"notes root not found: {args.notes_root}. Run `git submodule update --init --recursive`."
        )

    candidates = scan(
        args.notes_root,
        [args.csv, args.paper_read_csv],
        KEYWORDS,
        enrich_crossref=args.enrich_crossref,
        crossref_timeout=args.crossref_timeout,
    )
    candidates = [item for item in candidates if item["score"] >= args.min_score]
    if not args.include_duplicates:
        candidates = [item for item in candidates if not item["already_in_awesome"]]

    args.output_json.write_text(
        json.dumps(candidates, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    write_markdown(candidates, args.output_md, args.limit)
    print(f"candidates={len(candidates)}")
    print(f"json={args.output_json}")
    print(f"markdown={args.output_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
