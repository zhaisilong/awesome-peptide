from liquid import Template

header = Template("""# Awesome Peptide

⚠️ Note: My PhD research keeps me very busy, so this repository may not be updated frequently. For the latest domain-specific updates, please follow our WeChat Official Account (公众号) [MolAstra](https://mp.weixin.qq.com/s/PI_3E2NzZWBGy95hpFmhHQ) and Our [Paper Reading Project](https://paper.molastra.org).
Updates are curated on demand with help from Codex agents.

🔬 **Curated peptide research across design, computation, synthesis, biology, delivery, biomaterials, and therapeutic applications.**

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re) [![stars](https://badgen.net/github/stars/zhaisilong/awesome-peptide)](https://github.com/zhaisilong/awesome-peptide/stargazers)

🤖 With help from Codex agents, paper discovery, metadata verification, classification, and validation are partially automated. Papers are curated from paper-read, Crossref, PubMed, arXiv, and primary sources; committed metadata snapshots make README generation reproducible offline.

🔗 Link directly to <a href="#contents">Contents</a>, <a href="#citations">Citations</a>

✅ **What sets us apart from similar resources:**

1. Versatile Tags: Organize and filter papers easily.
2. Easy Navigation: Internal links for quick jumps between sections and papers.
3. Expert Insights: Links to expert reviews and analysis.
4. Tag System: Quickly catch the paper features
5. CSV Downloads: [curated papers](data/paper.csv) and [paper-read papers](data/paper-read.csv).
6. Automation: Use [Liquid](https://liquid.readthedocs.io/en/latest/) templates to generate Markdown from `CSV`, making it easy to build your own paper repository. >>> [[Details](CONTRIBUTING.md)]
""")

paper = Template(
    "**{{paper.title}}**<br>\n"
    "{{paper.authors}}<br>\n"
    "[{{paper.publish_date_}}] >> {{paper.publications}}"
    "{% if paper.quality or paper.dataset or paper.code or paper.blogs or paper.tags %}"
    "{% if paper.quality %} • {{paper.quality}}{% else %}{% endif %}"
    "{% if paper.dataset %} • {{paper.dataset}}{% else %}{% endif %}"
    "{% if paper.code %} • {{paper.code}}{% else %}{% endif %}"
    "{% if paper.blogs %} • {{paper.blogs}}{% else %}{% endif %}"
    "{% if paper.tags %} • {{paper.tags}}{% else %}{% endif %}"
    "{% else %}{% endif %}\n"
    "{% if paper.abstract %}\n"
    "<details>\n"
    "<summary>🔎 Abstract</summary>\n"
    "<p>{{paper.abstract | escape}}</p>\n"
    "</details>\n"
    "{% endif %}\n"
)

toc_header = Template("""
<p id="contents" align='center'>
  <strong><a href='#0-benchmarks-and-datasets'>0) Benchmarks and Datasets</a></strong>
  <br>
  <a href="#01-benchmarks">Benchmarks</a> •
  <a href="#02-datasets">Datasets</a> •
  <a href="#03-related-resources">Related Resources</a> •
  <a href="#04-guides">Guides</a> •
  <a href="#05-tools">Tools</a>
  <br>""")

toc_sec = Template("""
  <strong><a href='#{{ anchor }}'>{{idx}}) {{sec}}</a></strong>
  <br>""")

toc_subsec = Template("""<a href='#{{ anchor }}'>{{sec}}</a>{% if dot %} •{% endif %}
  {% unless dot %}<br>{% endunless %}""")


toc_tail = Template("""
</p>

---
""")

sec = Template("""
## {{ idx }}. {{ sec }}
""")

subsec = Template("""
### {{ idx }} {{ sec }}

""")

paper_last_week_header = Template("""
📅 _Papers from the last six months, updated on {{ date }}:_

""")

paper_pined_header = Template("""📌 _Papers pinned:_

""")

fig = Template("""---

<p align="center">
  <a href="https://doi.org/10.1038/s41586-023-05909-9">
  <img src="cover.png" alt="deep learning for peptides">
  </a>
</p>
""")

bibtext = """

```bibtex
@article{zhaiArtificialIntelligencePeptidebased2025,
  title = {Artificial Intelligence in Peptide-Based Drug Design},
  author = {Zhai, Silong and Liu, Tiantao and Lin, Shaolong and Li, Dan and Liu, Huanxiang and Yao, Xiaojun and Hou, Tingjun},
  date = {2025-02-01},
  journaltitle = {Drug Discovery Today},
  volume = {30},
  number = {2},
  pages = {104300},
  issn = {1359-6446},
  doi = {10.1016/j.drudis.2025.104300}
}

```"""

contributing_and_see_also = Template(f"""
## Contribution

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
""")
