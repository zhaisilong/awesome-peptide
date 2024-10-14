from datetime import datetime
from pathlib import Path

def custom_sort(date_str):
    # 将日期字符串拆分为 年、月、日
    year, month, day = map(int, date_str.split('-'))
    return (year, month, day)