from liquid import Template

header = Template(
    """# Deep Learning for peptides

🔬 __Comprehensive List of Research Papers on Peptides and Deep Learning__

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)  [![stars](https://shields.io/github/stars/zhaisilong/awesome-peptide?style=social)](https://github.com/zhaisilong/awesome-peptide)

🔗 Link directly to <a href="#contents">Contents</a>, <a href="#citations">Citations</a>

✅ __What sets us apart from similar resources:__

1. Versatile Tags: Organize and filter papers easily.
2. Easy Navigation: Internal links for quick jumps between sections and papers.
3. Expert Insights: Links to expert reviews and analysis.
4. Tag System: Quickly catch the paper features
5. [CSV Downloads](data/paper.csv): Quick access to paper data in `CSV` format.
6. Automation: Use [Liquid](https://liquid.readthedocs.io/en/latest/) templates to generate Markdown from `CSV`, making it easy to build your own paper repository. >>> [[Details](CONTRIBUTING.md)]
"""
)

paper = Template(
    """**{{paper.title}}**  
{{paper.authors}}  
[{{paper.publish_date_}}] >> {{paper.publications}}{% if paper.quality or paper.dataset or paper.code or paper.blogs or paper.tags %}{% if paper.quality %} • {{paper.quality}}{% else %}{% endif %}{% if paper.dataset %} • {{paper.dataset}}{% else %}{% endif %}{% if paper.code %} • {{paper.code}}{% else %}{% endif %}{% if paper.blogs %} • {{paper.blogs}}{% else %}{% endif %}{% if paper.tags %} • {{paper.tags}}{% else %}{% endif %}{% else %}{% endif %}
{% if paper.abstract %}  
<details>
<summary>🔎 Abstract</summary>
<p>{{paper.abstract}}</p>
</details>  
{% endif %}
"""
)

toc_header = Template(
    """
<p id="contents" align='center'>
  <strong><a href='#0-benchmarks-and-datasets'>0) Benchmarks and Datasets</a></strong>
  <br>
  <a href="#01-benchmarks">Benchmarks</a> •
  <a href="#02-datasets">Datasets</a> •
  <a href="#03-similar-list">Similar List</a> •
  <a href="#04-tools">Tools</a>
  <br>"""
)

toc_sec = Template(
    """
  <strong><a href='#{{ idx | replace: ".",  "" }}-{{ sec | replace: " ", "-" | downcase }}'>{{idx}}) {{sec}}</a></strong>
  <br>"""
)

toc_subsec = Template(
    """<a href='#{{ idx | replace: ".",  "" }}-{{ sec | replace: " ", "-" | downcase }}'>{{sec}}</a>{% if dot %} • {% endif %}
  {% unless dot %}<br>{% endunless %}"""
)


toc_tail = Template(
    """
</p>

---
"""
)

sec = Template(
    """
## {{ idx }}. {{ sec }}
"""
)

subsec = Template(
    """
### {{ idx }} {{ sec }}

"""
)

paper_last_week_header = Template(
    """
📅 _Papers last six month, updated on {{ date }}:_

"""
)

paper_pined_header = Template(
    """📌 _Papers pined:_

"""
)

fig = Template(
    """---

<p align="center">
  <a href="https://doi.org/10.1038/s41586-023-05909-9">
  <img src="cover.png" alt="deep learning for peptides">
  </a>
</p>
"""
)

bibtext = """

```bibtex
@article{zhaiArtificialIntelligencePeptidebased2025,
  title = {Artificial Intelligence in Peptide-Based Drug Design},
  author = {Zhai, Silong and Liu, Tiantao and Lin, Shaolong and Li, Dan and Liu, Huanxiang and Yao, Xiaojun and Hou, Tingjun},
  date = {2025-02-01},
  journaltitle = {Drug Discovery Today},
  shortjournal = {Drug Discovery Today},
  volume = {30},
  number = {2},
  pages = {104300},
  issn = {1359-6446},
  doi = {10.1016/j.drudis.2025.104300}
}

```"""

contributing_and_see_also = Template(
    f"""
## Cntribution

[Contributions](https://github.com/zhaisilong/awesome-peptide/blob/main/CONTRIBUTING.md) and [suggestions](https://github.com/zhaisilong/awesome-peptide/issues) are warmly welcome! Community Values, Guiding Principles, and Commitments for the Responsible Development of AI for Peptide Design

## See Also

- [List of papers about Protein Design using Deep Learning](https://github.com/Peldom/papers_for_protein_design_using_DL)
- [Machine learning for proteins](https://github.com/yangkky/Machine-learning-for-proteins)

## Citations

{bibtext}

<picture>
  <source
    media="(prefers-color-scheme: dark)"
    srcset="
      https://api.star-history.com/svg?repos=zhaisilong/awesome-peptide&type=Date&theme=dark
    "
  />
  <source
    media="(prefers-color-scheme: light)"
    srcset="
      https://api.star-history.com/svg?repos=zhaisilong/awesome-peptide&type=Date
    "
  />
  <img
    alt="Star History Chart"
    src="https://api.star-history.com/svg?repos=zhaisilong/awesome-peptide&type=Date" 
  />
</picture>
"""
)

