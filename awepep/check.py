from collections import Counter
from pathlib import Path
import pprint
import re

import pandas as pd
from fire import Fire
from tqdm.auto import tqdm

from awepep import config, crossref

tqdm.pandas()

PAPER_READ_COLUMNS = [
    "doi",
    "title",
    "source",
    "sec",
    "subsec",
    "code",
    "dataset",
    "quality",
    "pined",
    "tags",
]


# 检查章节是否有效
def check_section(row):
    sec, subsec = row["sec"], row["subsec"]
    if sec not in config.sections:
        raise ValueError(f"No such section: {sec}")
    if subsec not in config.sections[sec]:
        raise ValueError(f"No such subsection: {subsec} in section {sec}")


# 提取 DOI 并验证格式
def extract_dois(publication):
    pattern = r"(10\.\d{3,9}/[-._;()/:A-Z0-9]+)\)"
    dois = [
        crossref.normalize_doi(doi)
        for doi in re.findall(pattern, publication, re.IGNORECASE)
    ]
    if not dois:
        raise ValueError(f"Invalid DOI: {publication}")
    return dois


# 检查 DOI 是否重复
def check_duplicate(dois, doi_pool):
    for doi in dois:
        if doi in doi_pool:
            raise ValueError(f"Duplicate DOI found: {doi}")
        doi_pool.add(doi)


# 检查必填字段
def check_required_fields(row, required_fields):
    missing_fields = [
        field for field in required_fields if pd.isna(row[field]) or row[field] == ""
    ]
    if missing_fields:
        raise ValueError(f"Missing required fields: {missing_fields} in row: {row}")


# 更新统计信息
def update_statistics(row, quality_counter, tags_counter):
    quality_counter[row["quality"]] += 1
    if row["tags"]:
        tags = row.get("tags", "").split("/")
        tags_counter.update(filter(None, tags))
    return row["pined"] != False


# 打印统计信息
def pretty_print_statistics(quality_counter, pined_count, tags_counter):
    print("\n===== Statistics Summary =====")
    print("\nQuality counts:")
    pprint.pprint(dict(quality_counter), width=1)
    print(f"\nPinned count (non-False): {pined_count}")
    print("\nTags counts:")
    pprint.pprint(dict(tags_counter), width=1)


def load_csv(csv_path: Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    return df.astype("object").where(pd.notna(df), False)


def validate_main_csv(csv_path: Path, doi_pool: set) -> pd.DataFrame:
    df = load_csv(csv_path)

    required_fields = [
        "title",
        "sec",
        "subsec",
        "authors",
        "publications",
        "publish_date",
    ]
    df.progress_apply(lambda row: check_required_fields(row, required_fields), axis=1)
    print(f"{csv_path} required fields check passed")

    df.progress_apply(check_section, axis=1)
    print(f"{csv_path} section check passed")

    # 提取 DOI 并检查重复
    df["dois"] = df["publications"].apply(extract_dois)
    df["dois"].progress_apply(lambda dois: check_duplicate(dois, doi_pool))
    print(f"{csv_path} duplicate check passed")
    return df


def check_paper_read_schema(df: pd.DataFrame, csv_path: Path):
    missing = set(PAPER_READ_COLUMNS) - set(df.columns)
    extra = set(df.columns) - set(PAPER_READ_COLUMNS)
    if missing or extra:
        parts = []
        if missing:
            parts.append(f"missing columns: {', '.join(sorted(missing))}")
        if extra:
            parts.append(f"unexpected columns: {', '.join(sorted(extra))}")
        raise ValueError(f"{csv_path} schema mismatch: {'; '.join(parts)}")


def validate_paper_read_csv(csv_path: Path, doi_pool: set) -> pd.DataFrame:
    if not csv_path.exists():
        print(f"{csv_path} not found; paper-read check skipped")
        return pd.DataFrame(columns=PAPER_READ_COLUMNS)

    df = load_csv(csv_path)
    check_paper_read_schema(df, csv_path)
    required_fields = ["doi", "sec", "subsec"]
    df.progress_apply(lambda row: check_required_fields(row, required_fields), axis=1)
    print(f"{csv_path} required fields check passed")

    df.progress_apply(check_section, axis=1)
    print(f"{csv_path} section check passed")

    df["dois"] = df["doi"].apply(lambda doi: [crossref.normalize_doi(doi)])
    df["dois"].progress_apply(lambda dois: check_duplicate(dois, doi_pool))
    print(f"{csv_path} duplicate check passed")
    return df


# 主流程
def main(csv: str = "data/paper.csv", paper_read_csv: str = "data/paper-read.csv"):
    doi_pool = set()
    df = validate_main_csv(Path(csv), doi_pool)
    df_paper_read = validate_paper_read_csv(Path(paper_read_csv), doi_pool)

    # 更新统计信息
    stats_df = pd.concat([df, df_paper_read], ignore_index=True, sort=False)
    quality_counter = Counter()
    tags_counter = Counter()
    pined_count = sum(
        stats_df.progress_apply(
            lambda row: update_statistics(row, quality_counter, tags_counter), axis=1
        )
    )

    if pined_count > config.max_pined:
        print(stats_df[stats_df["pined"] == True])
        raise ValueError(f"Too many pinned papers. Maximum allowed: {config.max_pined}")

    pretty_print_statistics(quality_counter, pined_count, tags_counter)


if __name__ == "__main__":
    Fire(main)
