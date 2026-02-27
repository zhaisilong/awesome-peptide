from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import typer

from awepep.agent import links
from awepep.agent.doi import (
    arxiv_doi_from_id,
    arxiv_id_from_url,
    canonicalize_doi,
    doi_slug,
    extract_doi_from_text,
)
from awepep.agent.draft_schema import PaperDraft
from awepep.agent.llm_client import OpenAICompatibleClient
from awepep.agent.metadata import fetch_arxiv_metadata, fetch_crossref_metadata
from awepep.agent.pdf_extract import extract_pdf_text
from awepep.agent.repo_ops import append_csv_row, generate_readme, load_existing_dois, validate_csv
from awepep.agent.settings import AgentSettings
from awepep import config


@dataclass(frozen=True)
class AddInputs:
    pdf: Path | None
    doi: str | None
    url: str | None
    ocr: bool
    max_pdf_pages: int


@dataclass(frozen=True)
class AddOutputs:
    doi_slug: str
    canonical_doi: str
    out_dir: Path
    notes_path: Path | None
    json_path: Path | None
    pr_body_path: Path | None


def _auto_quality(publications: str, *, auto_high_venues: tuple[str, ...]) -> str:
    p = publications.lower()
    for v in auto_high_venues:
        if v.lower() in p:
            return "high"
    return ""


def _build_llm_prompt(*, canonical_doi: str, signals: dict[str, Any]) -> tuple[str, str]:
    allowed = {sec: subsecs for sec, subsecs in config.sections.items()}
    system = (
        "You are a careful research assistant helping maintain an awesome list of papers.\n"
        "Return a single JSON object only (no markdown, no backticks).\n"
        "Do not hallucinate links: only use links provided in signals, or the DOI link.\n"
    )
    user = {
        "task": "Given the paper signals, propose a CSV-ready entry and collaboration notes.",
        "constraints": {
            "canonical_doi": canonical_doi,
            "sec_subsec_allowed": allowed,
            "publications_must_include": f"https://doi.org/{canonical_doi}",
            "publish_date_format": "YYYY-MM-DD",
            "tags_format": "tag1/tag2/tag3 (empty allowed)",
        },
        "output_schema": {
            "canonical_doi": canonical_doi,
            "title": "string",
            "authors": "string",
            "publish_date": "YYYY-MM-DD",
            "sec": "string",
            "subsec": "string",
            "publications": "string",
            "code": "string (markdown link or empty)",
            "dataset": "string (markdown link or empty)",
            "quality_suggestion": "high|medium|low|''",
            "quality_rationale": "string",
            "abstract": "string (optional, plain text, no HTML)",
            "blogs": "string (markdown link or empty)",
            "pined": "boolean",
            "tags": "string",
            "notes_md": "markdown string in English with sections: TL;DR, What it is, Data, Method, Results, Limitations, Links found, Why section/tag",
            "evidence": {"field": "short evidence snippet from signals"},
        },
        "signals": signals,
    }
    return system, json.dumps(user, ensure_ascii=False)


def _edit_json(initial_json: str) -> str:
    edited = typer.edit(initial_json)
    if edited is None:
        return initial_json
    return edited


def run_add(
    *,
    settings: AgentSettings,
    inputs: AddInputs,
    csv_path: Path,
    write_csv: bool,
    write_readme: bool,
    emit_notes: bool,
    emit_json: bool,
    emit_pr_body: bool,
    non_interactive: bool,
    dry_run: bool,
) -> tuple[PaperDraft, AddOutputs]:
    extracted_text = ""
    pdf_backend = None
    pdf_low_text = False

    if inputs.pdf is not None:
        if inputs.ocr:
            raise RuntimeError("OCR mode is not implemented yet. Provide `--doi/--url`, or use a text-based PDF.")
        pdf_res = extract_pdf_text(inputs.pdf, max_pages=inputs.max_pdf_pages)
        extracted_text = pdf_res.text
        pdf_backend = pdf_res.backend
        pdf_low_text = pdf_res.low_text

    canonical = None
    if inputs.doi:
        canonical = canonicalize_doi(inputs.doi)
    elif inputs.url:
        try:
            canonical = canonicalize_doi(inputs.url)
        except ValueError:
            arxiv_id = arxiv_id_from_url(inputs.url)
            if arxiv_id:
                canonical = arxiv_doi_from_id(arxiv_id)
    if canonical is None:
        canonical = extract_doi_from_text(extracted_text)
    if canonical is None:
        raise RuntimeError("Could not determine DOI. Provide `--doi`, `--url`, or a PDF containing a DOI.")

    canonical = canonicalize_doi(canonical)
    slug = doi_slug(canonical)

    existing = load_existing_dois(csv_path)
    if canonical.lower() in existing:
        if dry_run:
            typer.echo(f"Warning: DOI already exists in {csv_path}: {canonical} (continuing because --dry-run is set)")
        else:
            raise RuntimeError(f"Duplicate DOI found in {csv_path}: {canonical}")

    arxiv_id = arxiv_id_from_url(inputs.url) if inputs.url else None
    crossref = fetch_crossref_metadata(canonical, timeout_s=settings.request_timeout_s)
    arxiv = fetch_arxiv_metadata(arxiv_id, timeout_s=settings.request_timeout_s) if arxiv_id else None

    signals: dict[str, Any] = {
        "doi": canonical,
        "doi_url": f"https://doi.org/{canonical}",
        "input_url": inputs.url or "",
        "pdf": str(inputs.pdf) if inputs.pdf else "",
        "pdf_backend": pdf_backend or "",
        "pdf_low_text": pdf_low_text,
        "pdf_text_excerpt": (extracted_text[:8000] if extracted_text else ""),
        "extracted_urls": links.extract_urls(extracted_text),
        "crossref": crossref.__dict__ if crossref else None,
        "arxiv": arxiv.__dict__ if arxiv else None,
        "known_tags": sorted(config.tags.keys()),
    }

    system, user = _build_llm_prompt(canonical_doi=canonical, signals=signals)
    client = OpenAICompatibleClient(
        base_url=settings.llm_base_url,
        api_key=settings.llm_api_key,
        model=settings.llm_model,
        timeout_s=settings.request_timeout_s,
    )
    llm_resp = client.chat_json(system=system, user=user)

    draft_json = llm_resp.content
    if not non_interactive:
        typer.echo("\nProposed JSON draft from LLM:\n")
        typer.echo(draft_json)
        if typer.confirm("\nEdit this JSON before applying?", default=False):
            draft_json = _edit_json(draft_json)

    try:
        draft_obj = json.loads(draft_json)
    except json.JSONDecodeError as e:
        raise RuntimeError("LLM output was not valid JSON.") from e

    draft = PaperDraft.model_validate(draft_obj)
    if canonicalize_doi(draft.canonical_doi) != canonical:
        raise RuntimeError(f"LLM returned mismatched DOI: {draft.canonical_doi} (expected {canonical})")

    if f"https://doi.org/{canonical}" not in draft.publications:
        raise RuntimeError("`publications` must include the canonical DOI link.")

    allowed_urls = set(links.extract_urls(extracted_text))
    allowed_urls.add(f"https://doi.org/{canonical}")
    if inputs.url:
        allowed_urls.add(inputs.url.strip().rstrip("/"))
    allowed_urls = {u.strip().rstrip("/") for u in allowed_urls if u.strip()}

    for field_name in ["publications", "code", "dataset", "blogs"]:
        value = getattr(draft, field_name, "") or ""
        for u in links.extract_urls(value):
            nu = u.strip().rstrip("/")
            if nu not in allowed_urls:
                msg = f"LLM provided a URL not present in signals: {u} (field={field_name})"
                if non_interactive:
                    raise RuntimeError(msg)
                typer.echo(f"\nWarning: {msg}\n")

    auto_quality = _auto_quality(draft.publications, auto_high_venues=settings.auto_high_venues)
    draft = draft.model_copy(update={"quality": auto_quality})

    if not non_interactive:
        typer.echo("\nCSV row preview:\n")
        typer.echo(json.dumps(draft.to_csv_row(), ensure_ascii=False, indent=2))
        if not dry_run:
            if not typer.confirm("\nApply this change to the repo?", default=True):
                raise typer.Abort()

    out_dir = settings.output_dir / slug
    notes_path = out_dir / "notes.md" if emit_notes else None
    json_path = out_dir / "paper.json" if emit_json else None
    pr_body_path = out_dir / "pr_body.md" if emit_pr_body else None

    outputs = AddOutputs(
        doi_slug=slug,
        canonical_doi=canonical,
        out_dir=out_dir,
        notes_path=notes_path,
        json_path=json_path,
        pr_body_path=pr_body_path,
    )

    out_dir.mkdir(parents=True, exist_ok=True)

    if emit_notes and notes_path is not None:
        notes_path.write_text(draft.notes_md.strip() + "\n", encoding="utf-8")

    if emit_json and json_path is not None:
        json_path.write_text(json.dumps(draft_obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if emit_pr_body and pr_body_path is not None:
        body = _build_pr_body(draft=draft, notes_path=notes_path, json_path=json_path)
        pr_body_path.write_text(body, encoding="utf-8")

    if not dry_run and write_csv:
        append_csv_row(csv_path, {k: str(v) for k, v in draft.to_csv_row().items()})
        validate_csv(csv_path)

    if not dry_run and write_readme:
        generate_readme(csv_path)

    run_meta = {
        "doi_slug": slug,
        "canonical_doi": canonical,
        "title": draft.title,
        "sec": draft.sec,
        "subsec": draft.subsec,
        "tags": draft.tags,
        "dry_run": dry_run,
        "csv_path": str(csv_path),
        "notes_path": str(notes_path) if notes_path else "",
        "json_path": str(json_path) if json_path else "",
        "pr_body_path": str(pr_body_path) if pr_body_path else "",
        "changed_files": [
            str(csv_path) if (write_csv and not dry_run) else "",
            "README.md" if (write_readme and not dry_run) else "",
        ],
    }
    (out_dir / "run.json").write_text(json.dumps(run_meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    return draft, outputs


def _build_pr_body(*, draft: PaperDraft, notes_path: Path | None, json_path: Path | None) -> str:
    lines: list[str] = []
    lines.append(f"Add paper: **{draft.title}**")
    lines.append("")
    lines.append(f"- DOI: `{draft.canonical_doi}`")
    lines.append(f"- Section: `{draft.sec} / {draft.subsec}`")
    lines.append(f"- Tags: `{draft.tags}`")
    lines.append("")

    if draft.quality_suggestion:
        lines.append(f"- Quality suggestion: `{draft.quality_suggestion}`")
        if draft.quality_rationale:
            lines.append(f"  - Rationale: {draft.quality_rationale}")
        lines.append("")

    if notes_path is not None:
        lines.append("<details>")
        lines.append("<summary>Notes</summary>")
        lines.append("")
        lines.append(draft.notes_md.strip())
        lines.append("")
        lines.append("</details>")
        lines.append("")

    if json_path is not None:
        lines.append("<details>")
        lines.append("<summary>Structured JSON</summary>")
        lines.append("")
        lines.append("```json")
        lines.append(json.dumps(draft.model_dump(), ensure_ascii=False, indent=2))
        lines.append("```")
        lines.append("")
        lines.append("</details>")
        lines.append("")

    return "\n".join(lines).strip() + "\n"
