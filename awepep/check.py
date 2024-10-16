import pandas as pd
from pathlib import Path
from awepep import config
from tqdm.auto import tqdm
import re
from collections import Counter
from fire import Fire
import pprint
import traceback

tqdm.pandas()

# 检查章节是否有效
def check_section(row):
    sec, subsec = row["sec"], row["subsec"]
    if sec not in config.sections:
        raise ValueError(f"No such section: {sec}")
    if subsec not in config.sections[sec]:
        raise ValueError(f"No such subsection: {subsec} in section {sec}")

# 提取 DOI 并验证格式
def extract_dois(publication):
    pattern = r'(10\.\d{3,9}/[-._;()/:A-Z0-9]+)\)'
    dois = re.findall(pattern, publication, re.IGNORECASE)
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
    missing_fields = [field for field in required_fields if pd.isna(row[field]) or row[field] == ""]
    if missing_fields:
        raise ValueError(f"Missing required fields: {missing_fields} in row: {row}")

# 更新统计信息
def update_statistics(row, quality_counter, tags_counter):
    quality_counter[row['quality']] += 1
    if row['tags']:
        tags = row.get('tags', '').split('/')
        tags_counter.update(filter(None, tags))
    return row['pined'] != False

# 打印统计信息
def pretty_print_statistics(quality_counter, pined_count, tags_counter):
    print("\n===== Statistics Summary =====")
    print("\nQuality counts:")
    pprint.pprint(dict(quality_counter), width=1)
    print(f"\nPined count (non-False): {pined_count}")
    print("\nTags counts:")
    pprint.pprint(dict(tags_counter), width=1)

# 主流程
def main(csv: str="data/paper.csv"):
    try:
        csv_path = Path(csv)
        df = pd.read_csv(csv_path).infer_objects(copy=False).fillna(False)

        required_fields = ["title", "sec", "subsec", "authors", "publications", "publish_date"]
        df.progress_apply(lambda row: check_required_fields(row, required_fields), axis=1)
        print("Required fields check passed")

        df.progress_apply(check_section, axis=1)
        print("Section check passed")

        # 提取 DOI 并检查重复
        doi_pool = set()
        df['dois'] = df['publications'].apply(extract_dois)
        df['dois'].progress_apply(lambda dois: check_duplicate(dois, doi_pool))
        print("Duplicate check passed")

        # 更新统计信息
        quality_counter = Counter()
        tags_counter = Counter()
        pined_count = sum(df.progress_apply(lambda row: update_statistics(row, quality_counter, tags_counter), axis=1))

        if pined_count > config.max_pined:
            raise ValueError(f"Too many pined papers. Maximum allowed: {config.max_pined}")

        pretty_print_statistics(quality_counter, pined_count, tags_counter)

    except:
        traceback.print_exc()

if __name__ == "__main__":
    Fire(main)