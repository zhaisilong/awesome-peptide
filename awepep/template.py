from liquid import Template

header = Template(
    """# Deep Learning for peptides

Comprehensive List of Research Papers on Peptides and Deep Learning

__What sets us apart from similar resources:__

1. Versatile Tags: Organize and filter papers easily.
2. Expert Insights: Links to expert reviews and analysis.
3. [CSV Downloads](data/paper.csv): Quick access to paper data in `CSV` format.
4. Automation: Use [Liquid](https://liquid.readthedocs.io/en/latest/) templates to generate Markdown from `CSV`, making it easy to build your own paper repository.
"""
)

paper = Template(
    """**{{paper.title}}**  
{{paper.authors}}  
[{{paper.publish_date_}}] >> {{paper.publications}}{% if paper.quality or paper.dataset or paper.code or paper.blogs or paper.tags %}{% if paper.quality %} • {{paper.quality}}{% else %}{% endif %}{% if paper.dataset %} • {{paper.dataset}}{% else %}{% endif %}{% if paper.code %} • {{paper.code}}{% else %}{% endif %}{% if paper.blogs %} • {{paper.blogs}}{% else %}{% endif %}{% if paper.tags %} • {{paper.tags}}{% else %}{% endif %}{% else %}{% endif %}
{% if paper.abstract %}  
<details>
<summary>Abstract</summary>
{{paper.abstract}}
</details>
{% endif %}
""")

toc_header = Template(
    """
<p align='center'>
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
_Papers last month, updated on {{ date }}:_

"""
)

paper_pined_header = Template(
    """_Papers pined:_

"""
)

fig = Template(
    """---

<p align="center">
  <img src="cover.png" alt="deep learning for peptides">
</p>
"""
)

contributing_and_see_also = Template(
    """
## Cntribution

[Contributions](https://github.com/zhaisilong/awesome-peptide/blob/main/CONTRIBUTING.md) and [suggestions](https://github.com/zhaisilong/awesome-peptide/issues) are warmly welcome! Community Values, Guiding Principles, and Commitments for the Responsible Development of AI for Peptide Design

## See Also

- [List of papers about Protein Design using Deep Learning](https://github.com/Peldom/papers_for_protein_design_using_DL)
- [Machine learning for proteins](https://github.com/yangkky/Machine-learning-for-proteins)
"""
)
