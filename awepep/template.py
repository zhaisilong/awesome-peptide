from liquid import Template

paper = Template(
    """**{{paper.title}}**  
{{paper.authors}}  
{{paper.publish_date}} >> {{paper.publications}}{% if paper.quality or paper.dataset or paper.code or paper.blogs %}{% if paper.quality %} • {{paper.quality}}{% else %}{% endif %}{% if paper.dataset %} • {{paper.dataset}}{% else %}{% endif %}{% if paper.code %} • {{paper.code}}{% else %}{% endif %}{% if paper.blogs %} • {{paper.blogs}}{% else %}{% endif %}{% else %}{% endif %}{% if paper.abstract %}
<details>
<summary>Abstract</summary>
{{paper.abstract}}
</details>
---
{% endif %}

"""
)

header = Template(
    """# Deep Learning for peptides

List of papers about Peptide research using Deep Learning

__The advantages that set us apart from competing products are as follows:__

1. Quality Tags: High-impact, concise tags for key paper highlights.
2. Expert Analysis: Links to blogs or sites with expert reviews.
3. Citations: Direct links to full paper references.
4. Database output: Python-aided curated `csv` file download.
"""
)

toc_header = Template(
    """
<p align='center'>
  <strong><a href='#0-benchmarks-and-datasets'>0) Benchmarks and Datasets</a></strong>
  <br>
  <a href="#01-sequence-datasets">Sequence Datasets</a> •
  <a href="#02-structure-datasets">Structure Datasets</a> •
  <a href="#03-databases">Public Database</a> •
  <a href="#04-similar-list">Similar List</a> •
  <a href="#05-guides">Guides</a>
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
_Papers last week, updated on {{ date }}:_

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
