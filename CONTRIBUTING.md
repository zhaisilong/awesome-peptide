# Contribution guidelines

## Setup

“We use [Liquid](https://liquid.readthedocs.io/en/latest/) as the template language and pandas to store paper metadata for generating the README documentation.”

```bash
git clone git@github.com:zhaisilong/awesome-peptide.git
cd awesome-peptide

mamba create -n awepep python=3.9
mamba activate awepep

pip install .

python get_md.py  # to build markdown from csv
```

## Assessment

High-Medium-Low Quality

1. High IF
2. High written
3. Good Papers
