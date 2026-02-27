from __future__ import annotations

import re

DOI_RE = re.compile(r"10\.\d{3,9}/[-._;()/:A-Z0-9]+", re.IGNORECASE)
ARXIV_ABS_RE = re.compile(r"(?:arxiv\.org/(?:abs|pdf)/)(?P<id>[^?#/]+)", re.IGNORECASE)


def canonicalize_doi(raw: str) -> str:
    if not raw:
        raise ValueError("Empty DOI")
    s = raw.strip()
    s = re.sub(r"^doi:\s*", "", s, flags=re.IGNORECASE)
    s = re.sub(r"^https?://doi\.org/", "", s, flags=re.IGNORECASE)
    s = s.strip().strip(").,;]}>\"'")
    m = DOI_RE.search(s)
    if not m:
        raise ValueError(f"Invalid DOI: {raw!r}")
    return m.group(0)


def extract_doi_from_text(text: str) -> str | None:
    if not text:
        return None
    m = DOI_RE.search(text)
    if not m:
        return None
    return canonicalize_doi(m.group(0))


def arxiv_id_from_url(url: str) -> str | None:
    if not url:
        return None
    m = ARXIV_ABS_RE.search(url)
    if not m:
        return None
    arxiv_id = m.group("id")
    arxiv_id = arxiv_id.removesuffix(".pdf")
    return arxiv_id


def arxiv_doi_from_id(arxiv_id: str) -> str:
    if not arxiv_id:
        raise ValueError("Empty arXiv id")
    return f"10.48550/arXiv.{arxiv_id}"


def doi_slug(doi: str) -> str:
    s = canonicalize_doi(doi)
    s = s.lower()
    s = s.replace("/", "_")
    s = re.sub(r"[^a-z0-9._-]+", "-", s)
    return s.strip("-")
