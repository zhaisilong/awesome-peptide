# Deep Learning for peptides

🔬 __Comprehensive List of Research Papers on Peptides and Deep Learning__

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)  [![stars](https://shields.io/github/stars/zhaisilong/awesome-peptide?style=social)](https://github.com/zhaisilong/awesome-peptide)

✅ __What sets us apart from similar resources:__

1. Versatile Tags: Organize and filter papers easily.
2. Easy Navigation: Internal links for quick jumps between sections and papers.
3. Expert Insights: Links to expert reviews and analysis.
4. [CSV Downloads](data/paper.csv): Quick access to paper data in `CSV` format.
5. Automation: Use [Liquid](https://liquid.readthedocs.io/en/latest/) templates to generate Markdown from `CSV`, making it easy to build your own paper repository. >>> [[Details](CONTRIBUTING.md)]

📅 _Papers last six month, updated on 2024-10-16:_

**Design of linear and cyclic peptide binders of different lengths from protein sequence information**  
Qiuzhen Li, Efstathios Nikolaos Vlachos, Patrick Bryant  
[**2024**-10-12] >> [Arxive](https://doi.org/10.1101/2024.06.20.599739) • [zenodo](https://zenodo.org/uploads/11543503) • [EvoBind](https://github.com/patrickbryant1/EvoBind) • Cyclic

**BindCraft: one-shot design of functional protein binders**  
Martin Pacesa, Lennart Nickel, ..., Sergey Ovchinnikov, Bruno E. Correia  
[**2024**-10-1] >> [Arxive](https://doi.org/10.1101/2024.09.30.615802) • high • [GitHub](https://github.com/martinpacesa/BindCraft)
  
<details>
<summary>🔎 Abstract</summary>
<p>BindCraft is an open-source, automated pipeline for <em>de novo</em> protein binder design, achieving experimental success rates of 10-100%. Using deep learning models like AlphaFold2, BindCraft generates high-affinity binders without the need for high-throughput screening or prior knowledge of binding sites. It has been successfully applied to challenging targets, including cell-surface receptors, allergens, and CRISPR-Cas9. In one example, the binders reduced IgE binding to birch allergens in patient samples, showcasing its potential in therapeutics, diagnostics, and biotechnology.</p>
</details>  

**PepINVENT: Generative peptide design beyond the natural amino acids**  
Gökçe Geylan, Jon Paul Janet, Alessandro Tibo, Jiazhen He, Atanas Patronov, Mikhail Kabeshov, Florian David, Werngard Czechtizky, Ola Engkvist, Leonardo De Maria  
[**2024**-9-21] >> [Axive](https://doi.org/10.48550/arXiv.2409.14040) • RL/Molecular AI/AstraZeneca

**Beware of extreme calculated lipophilicity when designing cyclic peptides**  
Vasanthanathan Poongavanam, Duc Duy Vo & Jan Kihlberg  
[**2024**-9-19] >> [Nat. Chem. Biol.](https://doi.org/10.1038/s41589-024-01715-0) • [SI](https://www.nature.com/articles/s41589-024-01715-0#MOESM1) • [Weixin](https://mp.weixin.qq.com/s/B65rJB1i_xrP8fTfbQ3Taw) • Cyclic/clogP

**Target-Specific De Novo Peptide Binder Design with DiffPepBuilder**  
Fanhao Wang, Yuzhe Wang, Laiyi Feng, Changsheng Zhang, and Luhua Lai  
[**2024**-9-4] >> [JCIM](https://doi.org/10.1021/acs.jcim.4c00975) • high • [GitHub](https://github.com/YuzheWangPKU/DiffPepBuilder) • Diffusion/Luhua Lai/AfDeisgn/ProteinMPNN/MD
  
<details>
<summary>🔎 Abstract</summary>
<p>Despite the exciting progress in target-specific de novo protein binder design, peptide binder design remains challenging due to the flexibility of peptide structures and the scarcity of protein-peptide complex structure data. In this study, we curated a large synthetic data set, referred to as PepPC-F, from the abundant protein−protein interface data and developed DiffPepBuilder, a de novo target-specific peptide binder generation method that utilizes an SE(3)-equivariant diffusion model trained on PepPC-F to codesign peptide sequences and structures. DiffPepBuilder also introduces disulfide bonds to stabilize the generated peptide structures. We tested DiffPepBuilder on 30 experimentally verified strong peptide binders with available protein−peptide complex structures. DiffPepBuilder was able to effectively recall the native structures and sequences of the peptide ligands and to generate novel peptide binders with improved binding free energy. We subsequently conducted de novo generation case studies on three targets. In both the regeneration test and case studies, DiffPepBuilder outperformed AfDesign and RFdiffusion coupled with ProteinMPNN, in terms of sequence and structure recall, interface quality, and structural diversity. Molecular dynamics simulations confirmed that the introduction of disulfide bonds enhanced the structural rigidity and binding performance of the generated peptides. As a general peptide binder de novo design tool, DiffPepBuilder can be used to design peptide binders for given protein targets with three-dimensional and binding site information.</p>
</details>  

**Design of Peptide Binders to Conformationally Diverse Targets with Contrastive Language Modeling**  
Suhaas Bhat, Kalyan Palepu, ..., Pranam Chatterjee  
[**2024**-7-22] >> [Arxive](https://doi.org/10.1101/2023.06.26.546591) • [zenodo](https://zenodo.org/doi/10.5281/zenodo.10971077) • [huggingface](https://huggingface.co/ubiquitx/pepprclip) • Pipline
  
<details>
<summary>🔎 Abstract</summary>
<p>针对难以成药的蛋白质设计结合剂是药物开发中的难题，尤其是无序或构象不稳定的蛋白。我们提出了一种通用算法框架，利用目标蛋白的氨基酸序列设计短链线性多肽。通过对ESM-2蛋白语言模型的潜在空间进行高斯扰动生成多肽候选序列，并通过基于CLIP的对比学习架构筛选靶向选择性。最终创建了Peptide Prioritization via CLIP（PepPrCLIP）管道，并在实验中验证了这些多肽的有效性，既可作为抑制剂，也可通过与E3泛素连接酶融合降解多种蛋白靶标。该策略无需稳定的三级结构，能够靶向无序和难以成药的蛋白质，如转录因子和融合致癌蛋白。</p>
</details>  

**HELM-GPT: de novo macrocyclic peptide design using generative pre-trained transformer**  
Xiaopeng Xu,   Chencheng Xu, Wenjia He, Lesong Wei, Haoyang Li, Juexiao Zhou, Ruochi Zhang, Yu Wang, Yuanpeng Xiong, Xin Gao  
[**2024**-6-12] >> [Bioinformatics](https://doi.org/10.1093/bioinformatics/btae364) • [Github](https://github.com/charlesxu90/helm-gpt) • GPT/HELM/Cyclic/RL

📌 _Papers pined:_

**PepINVENT: Generative peptide design beyond the natural amino acids**  
Gökçe Geylan, Jon Paul Janet, Alessandro Tibo, Jiazhen He, Atanas Patronov, Mikhail Kabeshov, Florian David, Werngard Czechtizky, Ola Engkvist, Leonardo De Maria  
[**2024**-9-21] >> [Axive](https://doi.org/10.48550/arXiv.2409.14040) • RL/Molecular AI/AstraZeneca

**Target-Specific De Novo Peptide Binder Design with DiffPepBuilder**  
Fanhao Wang, Yuzhe Wang, Laiyi Feng, Changsheng Zhang, and Luhua Lai  
[**2024**-9-4] >> [JCIM](https://doi.org/10.1021/acs.jcim.4c00975) • high • [GitHub](https://github.com/YuzheWangPKU/DiffPepBuilder) • Diffusion/Luhua Lai/AfDeisgn/ProteinMPNN/MD
  
<details>
<summary>🔎 Abstract</summary>
<p>Despite the exciting progress in target-specific de novo protein binder design, peptide binder design remains challenging due to the flexibility of peptide structures and the scarcity of protein-peptide complex structure data. In this study, we curated a large synthetic data set, referred to as PepPC-F, from the abundant protein−protein interface data and developed DiffPepBuilder, a de novo target-specific peptide binder generation method that utilizes an SE(3)-equivariant diffusion model trained on PepPC-F to codesign peptide sequences and structures. DiffPepBuilder also introduces disulfide bonds to stabilize the generated peptide structures. We tested DiffPepBuilder on 30 experimentally verified strong peptide binders with available protein−peptide complex structures. DiffPepBuilder was able to effectively recall the native structures and sequences of the peptide ligands and to generate novel peptide binders with improved binding free energy. We subsequently conducted de novo generation case studies on three targets. In both the regeneration test and case studies, DiffPepBuilder outperformed AfDesign and RFdiffusion coupled with ProteinMPNN, in terms of sequence and structure recall, interface quality, and structural diversity. Molecular dynamics simulations confirmed that the introduction of disulfide bonds enhanced the structural rigidity and binding performance of the generated peptides. As a general peptide binder de novo design tool, DiffPepBuilder can be used to design peptide binders for given protein targets with three-dimensional and binding site information.</p>
</details>  

**Full-Atom Peptide Design with Geometric Latent Diffusion**  
Xiangzhe Kong, Yinjun Jia, Wenbing Huang, Yang Liu  
[**2024**-2-21] >> NeurIPS/[Arxive](https://doi.org/10.48550/arXiv.2402.13555) • [code](https://github.com/THUNLP-MT/PepGLAD) • Full-Atom/Diffusion

**Denovo design of modular peptide-binding proteins by superhelical matching**  
Kejia Wu, Hua Bai, ..., Emmanuel Derivery, Daniel Adriano Silva, David Baker  
[**2023**-3-5] >> [Nature](https://doi.org/10.1038/s41586-023-05909-9) • high • [data](https://files.ipd.uw.edu/pub/2023_modular_peptide_binding_proteins/all_data_modular_peptide_binding_proteins.tar.gz) • [GitHub](https://github.com/tjs23/prot_pep_scan) • David Baker
  
<details>
<summary>🔎 Abstract</summary>
<p>General approaches for designing sequence-specific peptide-binding proteins would have wide utility in proteomics and synthetic biology. However, designing peptide-binding proteins is challenging, as most peptides do not have defined structures in isolation, and hydrogen bonds must be made to the buried polar groups in the peptide backbone1–3. Here, inspired by natural and re-engineered proteinpeptide systems4–11, we set out to design proteins made out of repeating units that bind peptides with repeating sequences, with a one-to-one correspondence between the repeat units of the protein and those of the peptide. We use geometric hashing to identify protein backbones and peptide-docking arrangements that are compatible with bidentate hydrogen bonds between the side chains of the protein and the peptide backbone12. The remainder of the protein sequence is then optimized for folding and peptide binding. We design repeat proteins to bind to six different tripeptide-repeat sequences in polyproline II conformations. The proteins are hyperstable and bind to four to six tandem repeats of their tripeptide targets with nanomolar to picomolar affinities in vitro and in living cells. Crystal structures reveal repeating interactions between protein and peptide interactions as designed, including ladders of hydrogen bonds from protein side chains to peptide backbones. By redesigning the binding interfaces of individual repeat units, specificity can be achieved for non-repeating peptide sequences and for disordered regions of native proteins.</p>
</details>  

**Target structure based computational design of cyclic peptides**  
WANG Fanhao, LAI Luhua, ZHANG Changsheng  
[**2023**-1-1] >> [SynbioJ](https://doi.org/10.12211/2096-8280.2023-006) • high • [pdf](./resource/10.12211/2096-8280.2023-006.pdf) • Cyclic/MD/Luhua Lai

**Design of Protein Segments and Peptides for Binding to Protein Targets**  
Suchetana Gupta, Noora Azadvari, and Parisa Hosseinzadeh  
[**2022**-1-1] >> [BioDesign Research](https://doi.org/10.34133/2022/9783197) • high

**Anchor extension: a structure-guided approach to  design cyclic peptides targeting enzyme active sites**  
Parisa Hosseinzadeh, ..., David Baker  
[**2021**-7-7] >> NC • [Peptide_HDACBinders](https://github.com/ParisaH-Lab/publications.git) • [](https://cloud.tencent.com/developer/article/1880256) • Cyclic/David Baker/MD/Crystal

---

<p align="center">
  <a href="https://doi.org/10.1038/s41586-023-05909-9">
  <img src="cover.png" alt="deep learning for peptides">
  </a>
</p>

<p align='center'>
  <strong><a href='#0-benchmarks-and-datasets'>0) Benchmarks and Datasets</a></strong>
  <br>
  <a href="#01-benchmarks">Benchmarks</a> •
  <a href="#02-datasets">Datasets</a> •
  <a href="#03-similar-list">Similar List</a> •
  <a href="#04-tools">Tools</a>
  <br>
  <strong><a href='#1-reviews'>1) Reviews</a></strong>
  <br><a href='#11-design'>Design</a> • 
  <a href='#12-interaction'>Interaction</a> • 
  <a href='#13-property'>Property</a> • 
  <a href='#14-structure'>Structure</a>
  <br>
  <strong><a href='#2-representation'>2) Representation</a></strong>
  <br>
  <strong><a href='#3-proprty-prediction'>3) Proprty Prediction</a></strong>
  <br>
  <strong><a href='#4-structure-modeling'>4) Structure Modeling</a></strong>
  <br>
  <strong><a href='#5-design'>5) Design</a></strong>
  <br><a href='#51-sequence-based'>Sequence-based</a> • 
  <a href='#52-structure-based'>Structure-based</a> • 
  <a href='#53-traditional'>Traditional</a>
  <br>
  <strong><a href='#6-others'>6) Others</a></strong>
  <br><a href='#61-protac'>PROTAC</a> • 
  <a href='#62-principle'>Principle</a> • 
  <a href='#63-protein-binders'>Protein Binders</a> • 
  <a href='#64-rapid'>RaPID</a> • 
  <a href='#65-therapeutic'>Therapeutic</a>
  <br>
</p>

---

## 0. Benchmarks and Datasets

### 0.1 Benchmarks

#### 0.1.1 Sequence Benchmarks

#### 0.1.2 Structure Benchmarks

**Predicting Protein−Peptide Interactions: Benchmarking Deep Learning Techniques and a Comparison with Focused Docking**  
Sudhanshu Shanker and Michel F. Sanner  
[**2024**-5-11] >> [JCIM](https://doi.org/10.1021/acs.jcim.3c00602) • [GitHub](https://github.com/sannerlab/benchmarking_2023) • Fold

**Benchmarking AlphaFold2 on peptide structure prediction**  
Eli Fritz McDonald, Taylor Jones, Lars Plate, Jens Meiler, Alican Gulsevin  
[**2024**-1-5] >> [Structure](https://doi.org/10.1016/j.str.2022.11.012) • [SI](https://doi.org/10.1016/j.str.2022.11.012) • [Weixin](https://mp.weixin.qq.com/s/9mpyZXITVC6RBbNQmjJLcg) • AF

#### 0.1.3 Evaluations

### 0.2 Datasets

### 0.2.1 Public Datasets

> A list of suggested peptide datasets

| Datasets | Description                                                                                                                                                                                                                                                         | Link |
| -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---- |
| PDB      | The Protein Data Bank (PDB) is a database of 3D structural data of large biological molecules, such as proteins and nucleic acids. These data are gathered using experimental methods such as X-ray crystallography, NMR spectroscopy, or cryo-electron microscopy. |      |

|CycPeptMPDB| CycPeptMPDB, the first web-accessible database of cyclic peptide membrane permeability. |[CycPeptMPDB](http://cycpeptmpdb.com)|

#### 0.2.1 Sequence Datasets

**CycPeptMPDB: A Comprehensive Database of Membrane Permeability of Cyclic Peptides**  
Jianan Li, Keisuke Yanagisawa, Masatake Sugita, Takuya Fujie, Masahito Ohue & Yutaka Akiyama  
[**2023**-3-17] >> [JCIM](https://doi.org/10.1021/acs.jcim.2c01573) • [CycPeptMPDB](http://cycpeptmpdb.com)

#### 0.2.2 Structure Datasets

### 0.3 Similar List

> Some similar GitHub lists that include papers about peptide using deep learning

1. Similar List 1
2. Similar List 2

### 0.4 Guides

> Guides/Tutorials for beginners on GitHub

1. Tutorials 1
2. Tutorials 2

### 0.5 Tools

> Tools for peptide develpements

1. HELM
   1. [HELM Online](http://webeditor.openhelm.org/hwe/examples/App.htm)
   2. [HELM Doc](https://pistoiaalliance.atlassian.net/wiki/spaces/PUB/pages/35028994/HELM+Web-editor)
   3. [HELM GitHub HELMWebEditor](https://github.com/PistoiaHELM/HELMWebEditor)
2. PDB
   1. [pdb-tools](http://www.bonvinlab.org/pdb-tools/)

## 1. Reviews

### 1.1 Design

**Unlocking novel therapies: cyclic peptide design for amyloidogenic targets through synergies of experiments, simulations, and machine learning**  
Daria de Raffele and Ioana M. Ilie  
[**2023**-11-7] >> [Chem. Commun.](https://doi.org/10.1039/D3CC04630C) • Cyclic

**Target structure based computational design of cyclic peptides**  
WANG Fanhao, LAI Luhua, ZHANG Changsheng  
[**2023**-1-1] >> [SynbioJ](https://doi.org/10.12211/2096-8280.2023-006) • high • [pdf](./resource/10.12211/2096-8280.2023-006.pdf) • Cyclic/MD/Luhua Lai

**Design of Protein Segments and Peptides for Binding to Protein Targets**  
Suchetana Gupta, Noora Azadvari, and Parisa Hosseinzadeh  
[**2022**-1-1] >> [BioDesign Research](https://doi.org/10.34133/2022/9783197) • high


### 1.2 Interaction

**A comprehensive review of protein-centric predictors for biomolecular interactions: from proteins to nucleic acids and beyond**  
Pengzhen Jia, Fuhao Zhang, Chaojin Wu and Min Li  
[**2024**-3-31] >> [BIB](https://doi.org/10.1093/bib/bbae162)


### 1.3 Property

**Machine learning for antimicrobial peptide identification and design**  
Fangping Wan, Felix Wong, James J. Collins & Cesar de la Fuente-Nunez  
[**2024**-2-26] >> [Nat Rev Bioeng](https://doi.org/10.1038/s44222-024-00152-x) • AMPs


### 1.4 Structure

**Modelling peptide–protein complexes: docking, simulations and machine learning**  
Arup Mondal, Liwei Chang and Alberto Perez  
[**2022**-8-26] >> [QRB Discovery](https://doi.org/10.1017/qrd.2022.14)


## 2. Representation

## 3. Proprty Prediction

## 4. Structure Modeling

## 5. Design

### 5.1 Sequence-based

**Design of linear and cyclic peptide binders of different lengths from protein sequence information**  
Qiuzhen Li, Efstathios Nikolaos Vlachos, Patrick Bryant  
[**2024**-10-12] >> [Arxive](https://doi.org/10.1101/2024.06.20.599739) • [zenodo](https://zenodo.org/uploads/11543503) • [EvoBind](https://github.com/patrickbryant1/EvoBind) • Cyclic

**PepINVENT: Generative peptide design beyond the natural amino acids**  
Gökçe Geylan, Jon Paul Janet, Alessandro Tibo, Jiazhen He, Atanas Patronov, Mikhail Kabeshov, Florian David, Werngard Czechtizky, Ola Engkvist, Leonardo De Maria  
[**2024**-9-21] >> [Axive](https://doi.org/10.48550/arXiv.2409.14040) • RL/Molecular AI/AstraZeneca

**Design of Peptide Binders to Conformationally Diverse Targets with Contrastive Language Modeling**  
Suhaas Bhat, Kalyan Palepu, ..., Pranam Chatterjee  
[**2024**-7-22] >> [Arxive](https://doi.org/10.1101/2023.06.26.546591) • [zenodo](https://zenodo.org/doi/10.5281/zenodo.10971077) • [huggingface](https://huggingface.co/ubiquitx/pepprclip) • Pipline
  
<details>
<summary>🔎 Abstract</summary>
<p>针对难以成药的蛋白质设计结合剂是药物开发中的难题，尤其是无序或构象不稳定的蛋白。我们提出了一种通用算法框架，利用目标蛋白的氨基酸序列设计短链线性多肽。通过对ESM-2蛋白语言模型的潜在空间进行高斯扰动生成多肽候选序列，并通过基于CLIP的对比学习架构筛选靶向选择性。最终创建了Peptide Prioritization via CLIP（PepPrCLIP）管道，并在实验中验证了这些多肽的有效性，既可作为抑制剂，也可通过与E3泛素连接酶融合降解多种蛋白靶标。该策略无需稳定的三级结构，能够靶向无序和难以成药的蛋白质，如转录因子和融合致癌蛋白。</p>
</details>  

**HELM-GPT: de novo macrocyclic peptide design using generative pre-trained transformer**  
Xiaopeng Xu,   Chencheng Xu, Wenjia He, Lesong Wei, Haoyang Li, Juexiao Zhou, Ruochi Zhang, Yu Wang, Yuanpeng Xiong, Xin Gao  
[**2024**-6-12] >> [Bioinformatics](https://doi.org/10.1093/bioinformatics/btae364) • [Github](https://github.com/charlesxu90/helm-gpt) • GPT/HELM/Cyclic/RL


### 5.2 Structure-based

**Target-Specific De Novo Peptide Binder Design with DiffPepBuilder**  
Fanhao Wang, Yuzhe Wang, Laiyi Feng, Changsheng Zhang, and Luhua Lai  
[**2024**-9-4] >> [JCIM](https://doi.org/10.1021/acs.jcim.4c00975) • high • [GitHub](https://github.com/YuzheWangPKU/DiffPepBuilder) • Diffusion/Luhua Lai/AfDeisgn/ProteinMPNN/MD
  
<details>
<summary>🔎 Abstract</summary>
<p>Despite the exciting progress in target-specific de novo protein binder design, peptide binder design remains challenging due to the flexibility of peptide structures and the scarcity of protein-peptide complex structure data. In this study, we curated a large synthetic data set, referred to as PepPC-F, from the abundant protein−protein interface data and developed DiffPepBuilder, a de novo target-specific peptide binder generation method that utilizes an SE(3)-equivariant diffusion model trained on PepPC-F to codesign peptide sequences and structures. DiffPepBuilder also introduces disulfide bonds to stabilize the generated peptide structures. We tested DiffPepBuilder on 30 experimentally verified strong peptide binders with available protein−peptide complex structures. DiffPepBuilder was able to effectively recall the native structures and sequences of the peptide ligands and to generate novel peptide binders with improved binding free energy. We subsequently conducted de novo generation case studies on three targets. In both the regeneration test and case studies, DiffPepBuilder outperformed AfDesign and RFdiffusion coupled with ProteinMPNN, in terms of sequence and structure recall, interface quality, and structural diversity. Molecular dynamics simulations confirmed that the introduction of disulfide bonds enhanced the structural rigidity and binding performance of the generated peptides. As a general peptide binder de novo design tool, DiffPepBuilder can be used to design peptide binders for given protein targets with three-dimensional and binding site information.</p>
</details>  

**Full-Atom Peptide Design with Geometric Latent Diffusion**  
Xiangzhe Kong, Yinjun Jia, Wenbing Huang, Yang Liu  
[**2024**-2-21] >> NeurIPS/[Arxive](https://doi.org/10.48550/arXiv.2402.13555) • [code](https://github.com/THUNLP-MT/PepGLAD) • Full-Atom/Diffusion

**Denovo design of modular peptide-binding proteins by superhelical matching**  
Kejia Wu, Hua Bai, ..., Emmanuel Derivery, Daniel Adriano Silva, David Baker  
[**2023**-3-5] >> [Nature](https://doi.org/10.1038/s41586-023-05909-9) • high • [data](https://files.ipd.uw.edu/pub/2023_modular_peptide_binding_proteins/all_data_modular_peptide_binding_proteins.tar.gz) • [GitHub](https://github.com/tjs23/prot_pep_scan) • David Baker
  
<details>
<summary>🔎 Abstract</summary>
<p>General approaches for designing sequence-specific peptide-binding proteins would have wide utility in proteomics and synthetic biology. However, designing peptide-binding proteins is challenging, as most peptides do not have defined structures in isolation, and hydrogen bonds must be made to the buried polar groups in the peptide backbone1–3. Here, inspired by natural and re-engineered proteinpeptide systems4–11, we set out to design proteins made out of repeating units that bind peptides with repeating sequences, with a one-to-one correspondence between the repeat units of the protein and those of the peptide. We use geometric hashing to identify protein backbones and peptide-docking arrangements that are compatible with bidentate hydrogen bonds between the side chains of the protein and the peptide backbone12. The remainder of the protein sequence is then optimized for folding and peptide binding. We design repeat proteins to bind to six different tripeptide-repeat sequences in polyproline II conformations. The proteins are hyperstable and bind to four to six tandem repeats of their tripeptide targets with nanomolar to picomolar affinities in vitro and in living cells. Crystal structures reveal repeating interactions between protein and peptide interactions as designed, including ladders of hydrogen bonds from protein side chains to peptide backbones. By redesigning the binding interfaces of individual repeat units, specificity can be achieved for non-repeating peptide sequences and for disordered regions of native proteins.</p>
</details>  


### 5.3 Traditional

**Anchor extension: a structure-guided approach to  design cyclic peptides targeting enzyme active sites**  
Parisa Hosseinzadeh, ..., David Baker  
[**2021**-7-7] >> NC • [Peptide_HDACBinders](https://github.com/ParisaH-Lab/publications.git) • [](https://cloud.tencent.com/developer/article/1880256) • Cyclic/David Baker/MD/Crystal


## 6. Others

### 6.1 PROTAC

**A Top-Down Design Approach for Generating a Peptide PROTAC Drug Targeting Androgen Receptor for Androgenetic Alopecia Therapy**  
Bohan MaDonghua LiuZhe WangDize ZhangYanlin Jian, et. al.  
[**2021**-6-5] >> [JMC](https://doi.org/10.1021/acs.jmedchem.4c00828) • [Weixin](https://mp.weixin.qq.com/s/xeJWFVcV5LkIlVJ1Zxf5Eg) • PROTAC


### 6.2 Principle

**Beware of extreme calculated lipophilicity when designing cyclic peptides**  
Vasanthanathan Poongavanam, Duc Duy Vo & Jan Kihlberg  
[**2024**-9-19] >> [Nat. Chem. Biol.](https://doi.org/10.1038/s41589-024-01715-0) • [SI](https://www.nature.com/articles/s41589-024-01715-0#MOESM1) • [Weixin](https://mp.weixin.qq.com/s/B65rJB1i_xrP8fTfbQ3Taw) • Cyclic/clogP


### 6.3 Protein Binders

**BindCraft: one-shot design of functional protein binders**  
Martin Pacesa, Lennart Nickel, ..., Sergey Ovchinnikov, Bruno E. Correia  
[**2024**-10-1] >> [Arxive](https://doi.org/10.1101/2024.09.30.615802) • high • [GitHub](https://github.com/martinpacesa/BindCraft)
  
<details>
<summary>🔎 Abstract</summary>
<p>BindCraft is an open-source, automated pipeline for <em>de novo</em> protein binder design, achieving experimental success rates of 10-100%. Using deep learning models like AlphaFold2, BindCraft generates high-affinity binders without the need for high-throughput screening or prior knowledge of binding sites. It has been successfully applied to challenging targets, including cell-surface receptors, allergens, and CRISPR-Cas9. In one example, the binders reduced IgE binding to birch allergens in patient samples, showcasing its potential in therapeutics, diagnostics, and biotechnology.</p>
</details>  


### 6.4 RaPID

**The RaPID Platform for the Discovery of Pseudo-Natural Macrocyclic Peptides**  
Yuki Goto & Hiroaki Suga  
[**2021**-9-10] >> [Acc. Chem. Res.](https://doi.org/10.1021/acs.accounts.1c00391) • RaPID/Cyclic/Hiroaki Suga/mRNA


### 6.5 Therapeutic

**Converting peptides into drugs  targeting intracellular  protein–protein interactions**  
Grégoire J.B. Philippe, David J. Craik and Sónia T. Henriques  
[**2021**-6-1] >> [Drug Discov Today](https://doi.org/10.1016/j.drudis.2021.01.022)

**Trends in peptide drug discovery**  
Markus Muttenthaler, GlennF.King, DavidJ.Adams and Paul F. Alewood  
[**2021**-4-1] >> [Nature Reviews Drug Discovery](https://doi.org/10.1038/s41573-020-00135-8) • high

**A Global Review on Short Peptides: Frontiers and Perspectives**  
Vasso Apostolopoulos, Joanna Bojarska, ...  
[**2021**-1-15] >> Molecules


## Cntribution

[Contributions](https://github.com/zhaisilong/awesome-peptide/blob/main/CONTRIBUTING.md) and [suggestions](https://github.com/zhaisilong/awesome-peptide/issues) are warmly welcome! Community Values, Guiding Principles, and Commitments for the Responsible Development of AI for Peptide Design

## See Also

- [List of papers about Protein Design using Deep Learning](https://github.com/Peldom/papers_for_protein_design_using_DL)
- [Machine learning for proteins](https://github.com/yangkky/Machine-learning-for-proteins)
