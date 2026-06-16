def custom_sort(date_str):
    year, month, day = map(int, date_str.split("-"))
    return (year, month, day)
