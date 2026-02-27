from __future__ import annotations

import csv
import re
from pathlib import Path

from awepep.agent.doi import canonicalize_doi


CSV_COLUMNS = [
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


_DOI_IN_MD_LINK_RE = re.compile(r"(10\.\d{3,9}/[-._;()/:A-Z0-9]+)\)", re.IGNORECASE)


def load_existing_dois(csv_path: Path) -> set[str]:
    dois: set[str] = set()
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            pubs = (row.get("publications") or "").strip()
            for m in _DOI_IN_MD_LINK_RE.findall(pubs):
                try:
                    dois.add(canonicalize_doi(m).lower())
                except ValueError:
                    continue
    return dois


def append_csv_row(csv_path: Path, row: dict[str, str]) -> None:
    missing = [c for c in CSV_COLUMNS if c not in row]
    if missing:
        raise ValueError(f"Missing CSV columns: {missing}")
    extra = [k for k in row.keys() if k not in CSV_COLUMNS]
    if extra:
        raise ValueError(f"Unexpected CSV columns: {extra}")

    file_exists = csv_path.exists()
    with csv_path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS, quoting=csv.QUOTE_MINIMAL)
        if not file_exists:
            writer.writeheader()
        writer.writerow({k: row.get(k, "") for k in CSV_COLUMNS})


def validate_csv(csv_path: Path) -> None:
    from awepep.check import validate_csv_file

    validate_csv_file(csv_path)


def generate_readme(csv_path: Path) -> None:
    try:
        from awepep.paper import PaperList
    except ModuleNotFoundError as e:
        raise RuntimeError(
            "README generation requires `python-liquid`. "
            "Install project deps: `pip install -e .`."
        ) from e

    PaperList(str(csv_path)).get_md(write=True)

