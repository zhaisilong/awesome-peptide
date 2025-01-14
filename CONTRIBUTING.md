# Contribution guidelines

## Setup

We use [Liquid](https://liquid.readthedocs.io/en/latest/) as the template language and pandas for handling paper metadata to generate the · documentation.

```bash
git clone git@github.com:zhaisilong/awesome-peptide.git
cd awesome-peptide

mamba create -n awepep python=3.9
mamba activate awepep

pip install -e .

awepep  # This command builds the markdown from the CSV files
awecheck  # Check validation of data/paper.csv
```

### Package Archietecchre

```yaml
- awepep
    - main.py: the main functionality
    - templates.py: Liquid templates for markdown generation
    - paper.py: builds documentation from CSV data
    - config.py: handles section ordering configuration
- data
    - paper.csv: curated dataset containing paper metadata
- resource: curated paper files by doi
- cover.png: cover image derived from [Nature Springer](https://doi.org/10.1038/s41586-023-05909-9)
- DATABASE.md: Chapter 0 for content that requires special formatting and handling
- setup.py: installation script
- LICENSE.md: GNU license
```

## Quality Assessment

Papers are categorized into three quality levels:

1. High: High impact factor (IF), well-written, and high-quality research.
2. Medium: Moderate quality and impact.
3. Low: Less influential but still valuable.
