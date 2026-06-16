"""Small Crossref Work API helpers for paper metadata enrichment."""

from __future__ import annotations

import html
import json
import re
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

CROSSREF_WORKS_API = "https://api.crossref.org/works/"
DOI_RE = re.compile(r"^10\.\d{3,9}/\S+$", re.IGNORECASE)
USER_AGENT = "awesome-peptide/1.2.0 (mailto:zhaisilong@outlook.com)"


def normalize_doi(value: str) -> str:
    doi = str(value).strip()
    doi = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", doi, flags=re.IGNORECASE)
    doi = doi.rstrip(".,;:)]}")
    if not DOI_RE.match(doi):
        raise ValueError(f"Invalid DOI: {value}")
    return doi.lower()


def fetch_work(doi: str, timeout: int = 20) -> dict:
    normalized = normalize_doi(doi)
    request = Request(
        CROSSREF_WORKS_API + quote(normalized, safe=""),
        headers={
            "Accept": "application/json",
            "User-Agent": USER_AGENT,
        },
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        raise RuntimeError(
            f"Crossref returned HTTP {exc.code} for DOI {normalized}"
        ) from exc
    except URLError as exc:
        raise RuntimeError(
            f"Could not reach Crossref for DOI {normalized}: {exc}"
        ) from exc

    if payload.get("status") != "ok" or "message" not in payload:
        raise RuntimeError(f"Unexpected Crossref response for DOI {normalized}")
    return payload["message"]


def _first_string(values, default: str = "") -> str:
    if isinstance(values, list) and values:
        return str(values[0]).strip()
    if isinstance(values, str):
        return values.strip()
    return default


def _date_parts(message: dict) -> list:
    for key in (
        "published-online",
        "published-print",
        "published",
        "issued",
        "created",
    ):
        parts = message.get(key, {}).get("date-parts", [])
        if parts and parts[0]:
            return parts[0]
    return []


def format_crossref_date(message: dict) -> str:
    parts = _date_parts(message)
    if not parts:
        raise RuntimeError("Crossref work has no usable publication date")
    year = int(parts[0])
    month = int(parts[1]) if len(parts) > 1 else 1
    day = int(parts[2]) if len(parts) > 2 else 1
    return f"{year}-{month}-{day}"


def format_authors(message: dict) -> str:
    authors = []
    for author in message.get("author", []):
        literal = str(author.get("literal", "")).strip()
        given = str(author.get("given", "")).strip()
        family = str(author.get("family", "")).strip()
        name = literal or " ".join(part for part in [given, family] if part)
        if name:
            authors.append(name)

    if not authors:
        raise RuntimeError("Crossref work has no author metadata")
    if len(authors) == 1:
        return authors[0]
    return ", ".join(authors[:-1]) + f" and {authors[-1]}"


def venue_label(message: dict) -> str:
    for key in ("short-container-title", "container-title", "event"):
        value = _first_string(message.get(key))
        if value:
            return value
    return _first_string(message.get("type"), "DOI")


def clean_abstract(value: str) -> str:
    if not value:
        return ""
    text = re.sub(r"<[^>]+>", " ", value)
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def metadata_from_work(message: dict, doi: str) -> dict:
    normalized = normalize_doi(doi)
    title = _first_string(message.get("title"))
    if not title:
        raise RuntimeError(f"Crossref work has no title for DOI {normalized}")
    label = venue_label(message)
    return {
        "title": title,
        "authors": format_authors(message),
        "publications": f"[{label}](https://doi.org/{normalized})",
        "publish_date": format_crossref_date(message),
        "abstract": clean_abstract(message.get("abstract", "")),
    }


def metadata_for_doi(doi: str, timeout: int = 20) -> dict:
    normalized = normalize_doi(doi)
    return metadata_from_work(fetch_work(normalized, timeout=timeout), normalized)
