from __future__ import annotations

from pathlib import Path

import typer

from awepep.agent.pipeline import AddInputs, run_add
from awepep.agent.settings import load_settings


app = typer.Typer(no_args_is_help=True, add_completion=False)


@app.callback()
def main() -> None:
    """
    Private maintenance agent for awesome-peptide.
    """


@app.command("add")
def add(
    doi: str | None = typer.Option(None, "--doi", help="DOI, e.g. 10.1038/..."),
    url: str | None = typer.Option(None, "--url", help="DOI URL or arXiv URL"),
    doi_or_url: str | None = typer.Option(None, "--doi-or-url", help="Convenience alias for --doi/--url (CI)"),
    pdf: Path | None = typer.Option(None, "--pdf", exists=True, dir_okay=False, help="Local PDF path"),
    csv_path: Path = typer.Option(Path("data/paper.csv"), "--csv", help="CSV path to update"),
    config_path: str | None = typer.Option(None, "--config", help="Path to awepep-agent.toml"),
    write_csv: bool = typer.Option(True, "--write-csv/--no-write-csv", help="Append to data/paper.csv"),
    write_readme: bool = typer.Option(True, "--write-readme/--no-write-readme", help="Regenerate README.md"),
    emit_notes: bool = typer.Option(True, "--emit-notes/--no-emit-notes", help="Write out/<doi_slug>/notes.md"),
    emit_json: bool = typer.Option(True, "--emit-json/--no-emit-json", help="Write out/<doi_slug>/paper.json"),
    emit_pr_body: bool = typer.Option(True, "--emit-pr-body/--no-emit-pr-body", help="Write out/<doi_slug>/pr_body.md"),
    non_interactive: bool = typer.Option(False, "--non-interactive", help="Disable prompts (CI)"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Do not modify repo; only generate artifacts"),
    ocr: bool = typer.Option(False, "--ocr", help="(Reserved) OCR for scanned PDFs"),
    max_pdf_pages: int = typer.Option(2, "--max-pdf-pages", min=1, max=10, help="Pages to extract from PDF for signals"),
):
    """
    Add a paper to the awesome list from PDF/DOI/URL and generate a draft PR-ready change.
    """
    if doi_or_url and not doi and not url:
        if "doi.org" in doi_or_url or doi_or_url.lower().startswith("http"):
            url = doi_or_url
        else:
            doi = doi_or_url

    settings = load_settings(config_path)
    inputs = AddInputs(pdf=pdf, doi=doi, url=url, ocr=ocr, max_pdf_pages=max_pdf_pages)

    draft, outputs = run_add(
        settings=settings,
        inputs=inputs,
        csv_path=csv_path,
        write_csv=write_csv,
        write_readme=write_readme,
        emit_notes=emit_notes,
        emit_json=emit_json,
        emit_pr_body=emit_pr_body,
        non_interactive=non_interactive,
        dry_run=dry_run,
    )

    typer.echo("\nDone.")
    typer.echo(f"- DOI: {draft.canonical_doi}")
    typer.echo(f"- Slug: {outputs.doi_slug}")
    typer.echo(f"- Out dir: {outputs.out_dir}")
    if write_csv:
        typer.echo(f"- Updated: {csv_path}")
    if write_readme:
        typer.echo("- Updated: README.md")


if __name__ == "__main__":
    app()
