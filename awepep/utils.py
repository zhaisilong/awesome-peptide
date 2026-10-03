import calendar
from datetime import date, timedelta
import re


def date_bounds(value):
    """Keep uncertain publication dates as intervals rather than invented days."""
    value = str(value)
    if not re.fullmatch(r"\d{4}(?:-\d{1,2}){0,2}", value):
        raise ValueError(f"Invalid publication date: {value}")
    parts = [int(part) for part in value.split("-")]
    year = parts[0]
    if len(parts) == 1:
        return date(year, 1, 1), date(year, 12, 31)
    month = parts[1]
    if len(parts) == 2:
        return date(year, month, 1), date(
            year, month, calendar.monthrange(year, month)[1]
        )
    exact = date(year, month, parts[2])
    return exact, exact


def custom_sort(date_str):
    return date_bounds(date_str)[0].timetuple()[:3]


def is_recent(value, as_of, days):
    lower, upper = date_bounds(value)
    return as_of - timedelta(days=days) <= lower <= upper <= as_of


def heading_slug(heading):
    return re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-")


def truthy(value):
    return str(value).strip().lower() in ("true", "1", "yes")
