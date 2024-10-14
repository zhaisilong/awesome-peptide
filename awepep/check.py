import pandas as pd
from awepep import config
from tqdm.auto import tqdm
import re
from collections import Counter
import numpy as np
import pprint

tqdm.pandas()

## Check sections
def check_section(row):
    if row["sec"] not in config.sections.keys():
        raise ValueError(f"No such section: {row}")

    if row["subsec"] not in config.sections[row["sec"]]:
        raise ValueError(f"No such subsection: {row['subsec']} in section {row['sec']}")

doi_pool = set()

def extract_dois(publication):
    doi_matches = re.findall(r'(10\.\d{3,9}/[-._;()/:A-Z0-9]+)\)', publication, re.IGNORECASE)
    return [doi for doi in doi_matches]

def check_duplicate(dois):
    for doi in dois:
        if doi in doi_pool:
            raise ValueError(f"Duplicate DOI found: {doi}")
        else:
            doi_pool.add(doi)

# 检查必须字段是否为空
def check_required_fields(row):
    required_fields = ["title", "sec", "subsec", "authors", "publications", "publish_date"]
    
    for field in required_fields:
        if pd.isna(row[field]) or row[field] == "":
            raise ValueError(f"Missing required field: {field} in row: {row}")

# 初始化统计
quality_counter = Counter()
pined_count = 0
tags_counter = Counter()

def update_statistics(row):
    global pined_count
    
    # 统计 quality 类别数量
    quality_counter[row['quality']] += 1
    
    # 统计 pined 为非 False 的数量
    if row['pined'] != False:
        pined_count += 1
    
    # 统计 tags 类别数量，假设 tags 以 '/' 分割
    if row['tags']:
        tags = row['tags'].split('/')
        tags_counter.update(tags)

########### main ##############

df = pd.read_csv("data/paper.csv").infer_objects(copy=False).replace({np.nan: False})

df.progress_apply(check_required_fields, axis=1)
print("Required fields check passed")

df.progress_apply(check_section, axis=1)
print("Section check passed")

# 提取 DOI 并检查重复
df['dois'] = df['publications'].apply(extract_dois)
df['dois'].progress_apply(check_duplicate)
print("Duplicate check passed")

df.progress_apply(update_statistics, axis=1)

if pined_count > config.max_pined:
    raise ValueError(f"Too many pined papers. Maximum allowed: {config.max_pined}")

# 打印统计结果
def pretty_print_statistics():
    print("\n===== Statistics Summary =====")
    
    # 打印 Quality 统计信息
    print("\nQuality counts:")
    pprint.pprint(dict(quality_counter), width=1)

    # 打印 Pined 统计信息
    print(f"\nPined count (non-False): {pined_count}")

    # 打印 Tags 统计信息
    print("\nTags counts:")
    pprint.pprint(dict(tags_counter), width=1)
    
pretty_print_statistics()

except ValueError as e:
    print(f"Error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")

