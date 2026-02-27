from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PdfExtractResult:
    text: str
    num_pages: int
    backend: str
    low_text: bool


def extract_pdf_text(
    pdf_path: Path,
    *,
    max_pages: int = 2,
    low_text_threshold: int = 200,
) -> PdfExtractResult:
    if not pdf_path.exists():
        raise FileNotFoundError(str(pdf_path))

    try:
        import pdfplumber  # type: ignore

        texts: list[str] = []
        with pdfplumber.open(str(pdf_path)) as pdf:
            num_pages = len(pdf.pages)
            for page in pdf.pages[: max_pages]:
                texts.append(page.extract_text() or "")
        text = "\n".join(t for t in texts if t)
        low_text = len(text.strip()) < low_text_threshold
        return PdfExtractResult(text=text, num_pages=num_pages, backend="pdfplumber", low_text=low_text)
    except ModuleNotFoundError:
        pass

    try:
        from pypdf import PdfReader  # type: ignore

        reader = PdfReader(str(pdf_path))
        num_pages = len(reader.pages)
        texts = []
        for i in range(min(max_pages, num_pages)):
            texts.append(reader.pages[i].extract_text() or "")
        text = "\n".join(t for t in texts if t)
        low_text = len(text.strip()) < low_text_threshold
        return PdfExtractResult(text=text, num_pages=num_pages, backend="pypdf", low_text=low_text)
    except ModuleNotFoundError as e:
        raise RuntimeError(
            "PDF extraction requires `pdfplumber` or `pypdf`. "
            "Install agent extras: `pip install -e .[agent]`."
        ) from e

