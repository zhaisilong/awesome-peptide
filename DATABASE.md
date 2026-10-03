## 0. Benchmarks and Datasets

### 0.1 Benchmarks

Benchmark papers are curated in [Data, Representation & Analysis](#2-data-representation--analysis) alongside dataset papers.

| Resource | Scope | Link |
| --- | --- | --- |
| Protein-peptide docking benchmark | Deep-learning and focused-docking evaluation | [benchmarking_2023](https://github.com/sannerlab/benchmarking_2023) |
| CPSet | Protein-cyclic peptide complex benchmark | [CPSet](https://github.com/huifengzhao/CPSet) |
| LEADS-PEP / DockThor | Flexible protein-peptide docking | [DockThor](https://www.dockthor.lncc.br) |

### 0.2 Datasets

| Dataset | Description | Link |
| --- | --- | --- |
| CycPeptMPDB | Experimentally measured cyclic peptide membrane permeability. | [CycPeptMPDB](http://cycpeptmpdb.com) |
| State of Peptides 2026 | Open reference dataset of 156 peptide and peptide-adjacent compounds with regulatory status, category, route, half-life, molecular weight, CAS, and PubChem/DrugBank/Wikidata cross-references (CSV/JSON, CC BY 4.0). | [State of Peptides 2026](https://peptahub.com/state-of-peptides-2026) |

### 0.3 Related Resources

- [RCSB PDB](https://www.rcsb.org): experimentally determined structures, including peptide complexes.
- [HELM Web Editor](https://github.com/PistoiaHELM/HELMWebEditor): representations of chemically modified peptides and other complex polymers.

### 0.4 Guides

- [Biopython Bio.PDB tutorial](https://biopython.org/docs/latest/Tutorial/chapter_pdb.html): PDB/mmCIF parsing and structural analysis.
- [RDKit in Python](https://www.rdkit.org/docs/GettingStartedInPython.html): chemical representations and molecular analysis.

### 0.5 Tools

| Task | Resource |
| --- | --- |
| Peptide notation | [HELM Online](http://webeditor.openhelm.org/hwe/examples/App.htm), [HELM documentation](https://pistoiaalliance.atlassian.net/wiki/spaces/PUB/pages/35028994/HELM+Web-editor) |
| Structure processing | [pdb-tools](http://www.bonvinlab.org/pdb-tools/), [Biopython](https://biopython.org), [BioPandas](https://biopandas.github.io/biopandas/), [RDKit](https://www.rdkit.org) |
| Interaction analysis | [Protein-Ligand Interaction Profiler (PLIP)](https://plip-tool.biotec.tu-dresden.de/plip-web/plip/index) |
| Molecular weight | [Peptide Molecular Weight Calculator](https://peptidecalculatorpro.org/peptide-molecular-weight-calculator/): average mass, monoisotopic mass, formula and m/z for standard amino acid sequences, with acetylation, amidation and disulfide options. |
| Charge estimates | [Peptide Net Charge Calculator](https://peptidecalculatorpro.org/peptide-net-charge-calculator/): Henderson-Hasselbalch net charge over pH 0-14, estimated pI and GRAVY using EMBOSS pKa values, with terminal modification options. |
