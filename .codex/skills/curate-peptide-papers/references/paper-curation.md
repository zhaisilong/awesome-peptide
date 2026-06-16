# Paper Curation Rules

Use this reference before editing `data/paper.csv`.

## Source Verification

- Browse for recent papers and any metadata that could have changed.
- When using `vendor/paper-read`, treat the note as a discovery source, not final bibliographic truth.
- For `data/paper-read.csv`, Crossref or arXiv supplies generated bibliographic fields during README generation.
- Prefer primary or structured sources: DOI landing page, journal page, arXiv/bioRxiv, PubMed, Crossref, official GitHub, official dataset repository, and author/project pages.
- Verify title, author list, publication date, DOI, venue, code URL, dataset URL, and abstract against the best available source.
- Do not infer code or dataset links from third-party summaries when an official source is unavailable.

## CSV Columns

The CSV column order is fixed:

```text
title,sec,subsec,authors,publications,code,dataset,quality,publish_date,abstract,blogs,pined,tags
```

`data/paper-read.csv` uses a separate minimal schema:

```text
doi,title,source,sec,subsec,code,dataset,quality,pined,tags
```

Required fields enforced by `awepep.check`:

- `title`
- `sec`
- `subsec`
- `authors`
- `publications`
- `publish_date`

Optional fields should be blank when unknown:

- `code`
- `dataset`
- `quality`
- `abstract`
- `blogs`
- `pined`
- `tags`

## Publication And Link Format

- Use Markdown links.
- `publications` must include a DOI URL ending with `)` because the current checker extracts DOI values with a regex over Markdown links.
- Preferred simple format:

```text
[JCIM](https://doi.org/10.1021/example)
```

- Conference plus preprint examples already in the repo use forms like:

```text
ICML/[arXiv](https://doi.org/10.48550/arXiv.2411.18463)
NeurIPS/[Arxive](https://doi.org/10.48550/arXiv.2402.13555)
```

- Keep existing spelling in old rows unless explicitly cleaning historical metadata.
- For code, dataset, and blog fields, use concise labels:

```text
[GitHub](https://github.com/org/repo)
[data](https://example.org/dataset)
[gongzhonghao](https://mp.weixin.qq.com/...)
```

For `data/paper-read.csv`, store the raw DOI in `doi`; do not store `publications`, `authors`, `publish_date`, `abstract`, or `blogs`. README generation fetches those fields from Crossref or arXiv and converts `source` into a `[paper-read](...)` blog link.

## Date Format

- Existing rows use non-padded dates such as `2025-4-14` and `2024-10-1`.
- The generator sorts by splitting `publish_date` on `-` and converting year, month, day to integers.
- Use `YYYY-M-D` or `YYYY-MM-DD`; do not use month names or partial dates.

## Sections And Subsections

Use exact values from `awepep/config.py`:

```text
Reviews: Design & Generation, Structure & Interaction, Property & Activity, Therapeutics & Applications
Representation & Data: Sequence & Language, Structure & Graph, Datasets & Benchmarks
Property & Activity Prediction: Bioactivity & Function, Permeability & Developability, Interaction & Binding
Structure & Interaction Modeling: Peptide Conformation, Peptide-Protein Complexes, Docking & Simulation
Peptide Design & Generation: Sequence-Based Design, Structure-Based Design, Diffusion & Flow, Reinforcement Learning, Classical & Fragment-Based
Applications & Tools: Software & Webservers, Screening & Discovery, Therapeutics & Translation, Protein Binders, Chemical Biology & Modalities
```

## Quality, Pinned, Abstract, Tags

- `quality`: currently blank or `high`. Mark `high` only for landmark, high-impact, or especially relevant papers.
- `pined`: leave blank by default. Use `true` only for selected important papers; `awepep/config.py` sets `max_pined = 30`.
- `abstract`: optional. If included, keep it concise and safe for inline HTML inside the README details block.
- `tags`: slash-separated canonical tags, for example `Diffusion/Cyclic/MD`.
- Choose tags from `awepep.config.tag_groups`, grouped as `method`, `domain`, `resource`, and `person`.
- Add a new tag to `tag_groups` before using it; add common misspellings or legacy values to `tag_aliases`.
- Tags matching `awepep.config.tag_links` render as links in generated README output.
- `awe-check` warns on unknown or alias tags without failing; resolve these warnings before release.
- Prefer existing tag vocabulary unless a new method or domain tag is clearly useful.

## Validation Checklist

After edits:

```bash
pip install -e .
awe-check
python .codex/skills/curate-peptide-papers/scripts/audit_tags.py
awe-pep
git diff -- data/paper.csv README.md
```

If `awe-check` prints a traceback, fix the CSV or checker issue before regenerating release-ready output.

## Automatic Paper-Read Curation

When the user asks Codex to scan `paper-read`, use the scanner report to automatically add high-confidence entries to `data/paper-read.csv`. Add a candidate only when:

- The DOI is not already in `data/paper.csv` or `data/paper-read.csv`.
- The note is clearly peptide/deep-learning relevant.
- The DOI or stable source URL is verified.
- The section/subsection assignment is clear.

Skip ambiguous papers and report the reason instead of forcing them into the CSV.
