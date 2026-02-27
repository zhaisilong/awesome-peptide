from __future__ import annotations

import re

URL_RE = re.compile(r"https?://[^\s\)\]]+")


def extract_urls(text: str) -> list[str]:
    if not text:
        return []
    urls: list[str] = []
    for u in URL_RE.findall(text):
        u = u.strip().strip(").,;]}>\"'")
        if u and u not in urls:
            urls.append(u)
    return urls


def pick_first_github(urls: list[str]) -> str | None:
    for u in urls:
        if "github.com/" in u.lower():
            return u
    return None


def contains_any(haystack: str, needles: list[str]) -> bool:
    h = haystack.lower()
    return any(n.lower() in h for n in needles)

