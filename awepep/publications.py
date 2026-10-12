"""Shared publication identities for validation, discovery and deduplication."""

import re
from urllib.parse import quote, unquote, urlsplit, urlunsplit

from awepep import crossref

LINK_RE = re.compile(r"\[[^\[\]]+\]\((https?://\S+?)\)(?=\s|$|/|\[)")
DOI_RE = re.compile(r"10\.\d{3,9}/[-._;()/:A-Z0-9]+", re.IGNORECASE)
PREPRINT_HOSTS = {
    "arxiv.org",
    "biorxiv.org",
    "medrxiv.org",
    "chemrxiv.org",
    "preprints.org",
    "researchsquare.com",
}


def is_preprint_doi(doi):
    return (
        str(doi)
        .lower()
        .startswith(
            (
                "10.48550/arxiv.",
                "10.1101/",
                "10.26434/chemrxiv",
                "10.20944/preprints",
                "10.21203/rs.",
            )
        )
    )


def normalize_url(value):
    try:
        parts = urlsplit(value)
        host, port = parts.hostname, parts.port
    except ValueError as exc:
        raise ValueError(f"Invalid publication URL: {value}") from exc
    if (
        parts.scheme.lower() != "https"
        or not host
        or "." not in host
        or parts.username is not None
        or parts.password is not None
        or re.search(r"[\s<>\\]", value)
    ):
        raise ValueError(f"Expected a stable HTTPS publication URL: {value}")
    netloc = host.lower() + (f":{port}" if port and port != 443 else "")
    # Query parameters can identify OpenReview papers; only fragments are disposable.
    return urlunsplit(("https", netloc, parts.path or "/", parts.query, ""))


def is_preprint_url(value):
    host = (urlsplit(value).hostname or "").lower()
    return any(
        host == domain or host.endswith("." + domain) for domain in PREPRINT_HOSTS
    ) or any(is_preprint_doi(doi) for doi in DOI_RE.findall(unquote(value)))


def note_url(source):
    if source.startswith(("https://", "http://")):
        url = source
    elif source.startswith("vendor/paper-read/"):
        url = (
            "https://github.com/zhaisilong/paper-read/blob/main/"
            + source.removeprefix("vendor/paper-read/")
        )
    elif source.startswith("src/site/notes/"):
        url = "https://github.com/zhaisilong/paper-read/blob/main/" + source
    else:
        url = "https://paper.molastra.org/" + source.lstrip("/")
    parts = urlsplit(url)
    return urlunsplit(
        (
            parts.scheme,
            parts.netloc,
            quote(parts.path, safe="/%:@"),
            parts.query,
            parts.fragment,
        )
    )


def publication_keys(value, *, allow_preprints=False):
    urls = LINK_RE.findall(str(value or ""))
    if not urls:
        raise ValueError(f"Expected a Markdown publication link: {value}")
    keys = []
    for url in urls:
        normalized = normalize_url(url)
        dois = [crossref.normalize_doi(doi) for doi in DOI_RE.findall(unquote(url))]
        if not allow_preprints and (
            is_preprint_url(url) or any(is_preprint_doi(doi) for doi in dois)
        ):
            raise ValueError(
                f"Preprint-only publication belongs in the archive: {value}"
            )
        keys.extend(dois or [normalized])
    return list(dict.fromkeys(keys))
