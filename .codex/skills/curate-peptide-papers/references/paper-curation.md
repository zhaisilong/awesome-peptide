# Paper Curation Rules

## Evidence And Scope

Include experimental and computational peptide research; skip incidental mentions in generic protein/drug-discovery papers. Use notes as discovery leads, then verify against DOI/publisher pages, Crossref, PubMed, arXiv or official project sources. The shared `awepep.discovery` module searches multiple providers, paces requests, retries transient failures twice and reports failures/truncation.

A precise publication window requires a verified day. Preserve partial dates in the source table when that is all the evidence supports; registration, acceptance and note dates are not publication dates. Preprints use the initial submission date and an explicit arXiv venue. Do not imply peer review.

## CSV Rules

Schemas and field order live in `awepep.paper.PAPER_COLUMNS` and `PAPER_READ_COLUMNS`, also documented in CONTRIBUTING. Main entries require title, section, subsection, authors, Markdown DOI publication link and date. Optional unknown fields stay blank. Paper-read entries require DOI and the agent-selected section/subsection; source/title/resource links are optional.

Use `[Journal](https://doi.org/10.xxxx/example)` and short Markdown labels for code/dataset/blog links. A resource must be explicitly provided by an author or primary source, not inferred from a similarly named repository. The row draft helper prints a schema-correct main CSV row without writing:
`python .codex/skills/curate-peptide-papers/scripts/draft_paper_row.py --help`.

## Classification

Read the live taxonomy in `awepep/config.py`; do not copy a stale label catalog into a new row.

- Reviews: literature synthesis, including chemistry, mechanisms and delivery.
- Data, Representation & Analysis: datasets, benchmarks, representations and experimental characterization.
- Property & Activity: prediction or systematic measurement of bioactivity, permeability/developability or binding.
- Structure & Interaction: conformations, complexes, docking and simulation.
- Peptide Design & Generation: sequence/structure generation and optimization.
- Synthesis & Chemical Modification: assembly chemistry, ligation/cyclization, noncanonical/conjugated peptides and biosynthetic engineering.
- Biology & Mechanisms: signaling, membrane/immune mechanisms and natural peptide biology.
- Delivery & Biomaterials: formulations, assemblies/hydrogels, materials and sensors.
- Applications & Tools: software, screening and validated translational use cases.

Assign by the main contribution. A hydrogel designed with an agent remains a biomaterials paper; an AI-engineered synthetase can belong to biosynthesis. A prediction web tool belongs in software when the usable platform is its main contribution. Related protein-binder benchmarks already retained by the project should not justify indiscriminate addition of generic protein research.

## Tags And Editorial Flags

Use a small number of canonical, slash-separated tags from `config.tag_groups`. Prefer method/domain tags; add resource/person tags only when useful and verified. Add meaningful vocabulary first, not one-off aliases. The tag audit's suggestions are review prompts, not automatic annotations.

`quality` is blank or `high`; new high designations need strong methodological, experimental or community evidence. `pined` is blank, `true` or `false`; count actual true values against `config.max_pined`. Journal prestige alone is not sufficient.

Use concise factual abstract summaries. Distinguish predicted efficacy from experimentally measured outcomes and animal models from clinical evidence.

## Acceptance Checklist

Check DOI and normalized-title duplicates across both tables, including preprint/journal relationships. Review provider failures and truncated searches. Run `awe-check`, strict tag audit and tests, refresh missing snapshots, regenerate offline, and inspect output. Keep accepted, duplicate, outside-window, ambiguous and missing-evidence counts distinct in the final report.
