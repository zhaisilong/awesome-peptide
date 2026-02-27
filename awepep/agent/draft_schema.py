from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator, model_validator

from awepep import config


class PaperDraft(BaseModel):
    canonical_doi: str = Field(..., description="Canonical DOI, e.g. 10.1038/...")

    title: str
    authors: str
    publish_date: str = Field(..., description="YYYY-MM-DD")

    sec: str
    subsec: str

    publications: str = Field(..., description="Markdown with at least one https://doi.org/<doi> link")
    code: str = ""
    dataset: str = ""
    quality: Literal["", "high", "medium", "low"] = ""
    abstract: str = ""
    blogs: str = ""
    pined: bool = False
    tags: str = ""

    quality_suggestion: Literal["", "high", "medium", "low"] = ""
    quality_rationale: str = ""

    notes_md: str = Field("", description="English markdown notes for PR/comment")
    evidence: dict[str, str] = Field(default_factory=dict, description="field->evidence snippet")

    @field_validator("title", "authors", "publications")
    @classmethod
    def _non_empty(cls, v: str) -> str:
        v = (v or "").strip()
        if not v:
            raise ValueError("Field must be non-empty")
        return v

    @field_validator("sec")
    @classmethod
    def _validate_sec(cls, v: str) -> str:
        if v not in config.sections:
            raise ValueError(f"Invalid sec: {v!r}")
        return v

    @model_validator(mode="after")
    def _validate_subsec(self) -> "PaperDraft":
        allowed = config.sections.get(self.sec, [])
        if self.subsec not in allowed:
            raise ValueError(f"Invalid subsec: {self.subsec!r} for sec={self.sec!r}")
        return self

    @field_validator("publish_date")
    @classmethod
    def _validate_publish_date(cls, v: str) -> str:
        from datetime import datetime

        datetime.strptime(v, "%Y-%m-%d")
        return v

    @field_validator("tags")
    @classmethod
    def _normalize_tags(cls, v: str) -> str:
        v = (v or "").strip()
        if not v:
            return ""
        parts = [p.strip() for p in v.split("/") if p.strip()]
        return "/".join(parts)

    def to_csv_row(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "sec": self.sec,
            "subsec": self.subsec,
            "authors": self.authors,
            "publications": self.publications,
            "code": self.code,
            "dataset": self.dataset,
            "quality": self.quality,
            "publish_date": self.publish_date,
            "abstract": self.abstract,
            "blogs": self.blogs,
            "pined": "true" if self.pined else "",
            "tags": self.tags,
        }
