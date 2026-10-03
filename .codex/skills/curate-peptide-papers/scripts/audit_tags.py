#!/usr/bin/env python3
"""Audit awesome-peptide CSV tags without mutating files."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

import pandas as pd

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))

from awepep import tags as tag_utils  # noqa: E402

SUGGESTION_RULES = [
    ("Cyclic", ("cyclic", "macrocyclic", "macrocycle", "cyclopeptide")),
    ("AMPs", ("antimicrobial peptide", "antimicrobial peptides", "amp ")),
    (
        "Diffusion",
        (
            "diffusion model",
            "diffusion-based",
            "latent diffusion",
            "discrete diffusion",
        ),
    ),
    ("Docking", ("docking",)),
    ("Flow", ("flow matching",)),
    ("Graph", ("graph",)),
    ("MD", ("molecular dynamics", "md simulation")),
    ("PLM", ("protein language model", "language model-based")),
    ("RL", ("reinforcement learning",)),
    ("Noncanonical", ("noncanonical", "non-canonical")),
    ("PDCs", ("peptide-drug conjugate", "peptide–drug conjugate")),
    ("CPPs", ("cell penetrating peptide", "cell-penetrating peptide")),
    ("Self-Assembly", ("self-assembly", "self-assembling", "self-assembled")),
    ("Hydrogel", ("hydrogel",)),
]


def row_text(row) -> str:
    return str(row.get("title", "")).lower()


def suggestions(row, current_tags: set[str]) -> list[str]:
    text = row_text(row)
    results = []
    for tag, needles in SUGGESTION_RULES:
        if tag in current_tags:
            continue
        if any(needle in text for needle in needles):
            results.append(tag)
    return results


def audit_csv(path: Path) -> tuple[int, int, int]:
    if not path.exists():
        print(f"{path}: missing, skipped")
        return 0, 0, 0

    df = pd.read_csv(path).fillna("")
    warning_count = 0
    empty_count = 0
    suggestion_count = 0
    print(f"\n{path}: {len(df)} rows")
    for index, row in df.iterrows():
        line = index + 2
        title = str(row.get("title", "")).strip()
        raw_tags = row.get("tags", "")
        canonical_tags = tag_utils.canonicalize_many(raw_tags)
        row_warnings = tag_utils.warnings(raw_tags)
        if row_warnings:
            warning_count += len(row_warnings)
            for warning in row_warnings:
                print(f"WARNING {path}:{line} {title!r}: {warning.message()}")

        if not canonical_tags:
            empty_count += 1

        row_suggestions = suggestions(row, set(canonical_tags))
        if row_suggestions:
            suggestion_count += len(row_suggestions)
            joined = "/".join(row_suggestions)
            print(f"SUGGEST {path}:{line} {title!r}: {joined}")

    print(
        f"{path}: warnings={warning_count}, empty_tag_rows={empty_count}, "
        f"suggestions={suggestion_count}"
    )
    return warning_count, empty_count, suggestion_count


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--paper-csv", type=Path, default=ROOT / "data/paper.csv")
    parser.add_argument(
        "--paper-read-csv", type=Path, default=ROOT / "data/paper-read.csv"
    )
    parser.add_argument(
        "--strict", action="store_true", help="Fail on vocabulary warnings"
    )
    args = parser.parse_args()

    total_warnings = 0
    total_empty = 0
    total_suggestions = 0
    for path in [args.paper_csv, args.paper_read_csv]:
        warnings, empty, suggestions_ = audit_csv(path)
        total_warnings += warnings
        total_empty += empty
        total_suggestions += suggestions_

    print(
        f"\nsummary: warnings={total_warnings}, empty_tag_rows={total_empty}, "
        f"suggestions={total_suggestions}"
    )
    return 1 if args.strict and total_warnings else 0


if __name__ == "__main__":
    raise SystemExit(main())
