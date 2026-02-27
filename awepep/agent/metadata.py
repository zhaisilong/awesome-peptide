from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import requests


@dataclass(frozen=True)
class PaperMetadata:
    title: str | None = None
    authors: list[str] | None = None
    publish_date: str | None = None  # YYYY-MM-DD
    venue: str | None = None


def _date_parts_to_iso(parts: list[int] | None) -> str | None:
    if not parts:
        return None
    year = parts[0]
    month = parts[1] if len(parts) >= 2 else 1
    day = parts[2] if len(parts) >= 3 else 1
    return f"{year:04d}-{month:02d}-{day:02d}"


def fetch_crossref_metadata(doi: str, *, timeout_s: float = 10.0) -> PaperMetadata | None:
    url = f"https://api.crossref.org/works/{doi}"
    try:
        resp = requests.get(url, timeout=timeout_s)
        if resp.status_code != 200:
            return None
        data: dict[str, Any] = resp.json()
        msg = data.get("message", {}) if isinstance(data, dict) else {}

        title = None
        if isinstance(msg.get("title"), list) and msg["title"]:
            title = str(msg["title"][0]).strip()

        authors: list[str] = []
        for a in msg.get("author", []) or []:
            if not isinstance(a, dict):
                continue
            given = str(a.get("given") or "").strip()
            family = str(a.get("family") or "").strip()
            name = " ".join(x for x in [given, family] if x).strip()
            if name:
                authors.append(name)

        date = None
        for key in ["published-print", "published-online", "issued"]:
            obj = msg.get(key)
            if isinstance(obj, dict):
                parts = obj.get("date-parts")
                if isinstance(parts, list) and parts and isinstance(parts[0], list):
                    date = _date_parts_to_iso([int(x) for x in parts[0]])
                    break

        venue = None
        if isinstance(msg.get("container-title"), list) and msg["container-title"]:
            venue = str(msg["container-title"][0]).strip()

        return PaperMetadata(title=title, authors=authors or None, publish_date=date, venue=venue)
    except requests.RequestException:
        return None


def fetch_arxiv_metadata(arxiv_id: str, *, timeout_s: float = 10.0) -> PaperMetadata | None:
    url = "http://export.arxiv.org/api/query"
    try:
        resp = requests.get(url, params={"id_list": arxiv_id}, timeout=timeout_s)
        if resp.status_code != 200:
            return None
        import xml.etree.ElementTree as ET

        root = ET.fromstring(resp.text)
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        entry = root.find("atom:entry", ns)
        if entry is None:
            return None
        title_el = entry.find("atom:title", ns)
        published_el = entry.find("atom:published", ns)
        author_els = entry.findall("atom:author", ns)

        title = title_el.text.strip() if title_el is not None and title_el.text else None
        published = None
        if published_el is not None and published_el.text:
            published = published_el.text.strip().split("T")[0]

        authors: list[str] = []
        for a in author_els:
            name_el = a.find("atom:name", ns)
            if name_el is not None and name_el.text:
                authors.append(name_el.text.strip())

        return PaperMetadata(title=title, authors=authors or None, publish_date=published, venue="arXiv")
    except requests.RequestException:
        return None
    except ET.ParseError:
        return None

