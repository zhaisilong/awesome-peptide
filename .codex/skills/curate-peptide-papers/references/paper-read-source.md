# Paper-Read Source

Use this reference when pulling latest paper notes from `vendor/paper-read`.

## Source Layout

- Submodule URL: `https://github.com/zhaisilong/paper-read.git`
- Local path: `vendor/paper-read`
- Notes path: `vendor/paper-read/src/site/notes/**/*.md`
- Main note groups: `journal`, `reviews`, `conference`, `webserver`, `news`, `tutorial`, `survey`
- Most useful groups for awesome-peptide curation: `journal`, `reviews`, `conference`, `webserver`

The notes are Markdown files. Many start with JSON frontmatter between `---` delimiters, followed by an H1 title and Chinese/English summary text. DOI and resource links usually appear in free text rather than a structured table.

## Update Flow

```bash
git submodule update --init --recursive
git submodule update --remote vendor/paper-read
```

Do not edit files inside `vendor/paper-read`; update the submodule pointer only.

## Candidate Scan

Run:

```bash
python .codex/skills/curate-peptide-papers/scripts/scan_paper_read_candidates.py --limit 50 --enrich-crossref
```

The scanner reads Markdown notes and ranks candidates by peptide-related keyword hits. It extracts:

- note path
- H1 title
- inferred note month from paths like `journal/2026/202604/...`
- DOI values
- GitHub/code-like links
- dataset-like links
- permalink/frontmatter when available
- optional Crossref metadata for the primary DOI
- short keyword snippets
- whether the DOI already exists in `data/paper.csv` or `data/paper-read.csv`

Crossref metadata comes from `https://api.crossref.org/works/{doi}` and should be used for title, authors, venue, published date, DOI link, and abstract. It should not decide awesome-peptide `sec/subsec`.

## Paper-Read CSV

Curate accepted paper-read candidates into `data/paper-read.csv` with this fixed minimal schema:

```text
doi,title,source,sec,subsec,code,dataset,quality,pined,tags
```

Use `source` for the paper-read permalink or note path. The README generator renders it as a `paper-read` blog link. Use `code` and `dataset` only for official links explicitly present in the note, DOI landing page, paper text, or official project pages.

## Curation Policy

Use scanner output as a triage queue. Codex should automatically add high-confidence papers after verifying metadata from the note, Crossref, and primary sources. Skip:

- broad drug-discovery notes with only incidental peptide mentions
- notes without DOI or stable source URL unless the user explicitly accepts them
- candidates that duplicate an existing DOI
- candidates whose awesome-peptide section/subsection is unclear

Prefer recent 2025/2026 notes first.
