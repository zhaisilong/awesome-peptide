from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Optional

from awepep import config


@dataclass(frozen=True)
class TagWarning:
    kind: str
    original: str
    canonical: Optional[str] = None

    def message(self) -> str:
        if self.kind == "alias":
            return (
                f"tag {self.original!r} should be canonicalized to {self.canonical!r}"
            )
        if self.kind == "unknown":
            return f"tag {self.original!r} is not in awepep.config.valid_tags"
        return f"tag {self.original!r} has warning kind {self.kind!r}"


def is_blank(value) -> bool:
    if value is None or value is False:
        return True
    try:
        if value != value:
            return True
    except TypeError:
        return True
    return str(value).strip() == ""


def split(value) -> list[str]:
    if is_blank(value):
        return []
    return [tag.strip() for tag in str(value).split("/") if tag.strip()]


def canonicalize(tag: str) -> str:
    return config.tag_aliases.get(tag.strip(), tag.strip())


def canonicalize_many(value) -> list[str]:
    canonical_tags = []
    seen = set()
    for tag in split(value):
        canonical = canonicalize(tag)
        if canonical and canonical not in seen:
            canonical_tags.append(canonical)
            seen.add(canonical)
    return canonical_tags


def join(tags: Iterable[str]) -> str:
    return "/".join(tags)


def normalize(value) -> str:
    return join(canonicalize_many(value))


def linkify(tag: str) -> str:
    url = config.tag_links.get(tag)
    if not url:
        return tag
    return f"[{tag}]({url})"


def format_for_readme(value):
    if is_blank(value):
        return value
    return join(linkify(tag) for tag in canonicalize_many(value))


def warnings(value) -> list[TagWarning]:
    seen = set()
    results = []
    for tag in split(value):
        canonical = canonicalize(tag)
        key = (tag, canonical)
        if key in seen:
            continue
        seen.add(key)
        if canonical != tag:
            results.append(TagWarning("alias", tag, canonical))
        if canonical not in config.valid_tags:
            results.append(TagWarning("unknown", canonical))
    return results
