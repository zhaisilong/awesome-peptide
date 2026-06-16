sections = {
    "Reviews": [
        "Design & Generation",
        "Structure & Interaction",
        "Property & Activity",
        "Therapeutics & Applications",
    ],
    "Representation & Data": [
        "Sequence & Language",
        "Structure & Graph",
        "Datasets & Benchmarks",
    ],
    "Property & Activity Prediction": [
        "Bioactivity & Function",
        "Permeability & Developability",
        "Interaction & Binding",
    ],
    "Structure & Interaction Modeling": [
        "Peptide Conformation",
        "Peptide-Protein Complexes",
        "Docking & Simulation",
    ],
    "Peptide Design & Generation": [
        "Sequence-Based Design",
        "Structure-Based Design",
        "Diffusion & Flow",
        "Reinforcement Learning",
        "Classical & Fragment-Based",
    ],
    "Applications & Tools": [
        "Software & Webservers",
        "Screening & Discovery",
        "Therapeutics & Translation",
        "Protein Binders",
        "Chemical Biology & Modalities",
    ],
}

max_pined = 30
last_days = 180

tag_groups = {
    "method": [
        "AF",
        "AI",
        "Diffusion",
        "Docking",
        "Flow",
        "Graph",
        "GPT",
        "MD",
        "MLM",
        "Pipeline",
        "PLM",
        "RL",
    ],
    "domain": [
        "AMPs",
        "cLogP",
        "Crystal",
        "Cyclic",
        "Full-Atom",
        "HELM",
        "Lasso",
        "mRNA",
        "PROTAC",
        "RaPID",
    ],
    "resource": [
        "AstraZeneca",
        "ColabDesign",
        "ESM",
        "Molecular AI",
        "Nvidia",
        "ProteinMPNN",
        "RFdiffusion",
        "RosettaCommons",
    ],
    "person": [
        "Akiyama Yutaka",
        "Chang-Yu Hsieh",
        "Changsheng Zhang",
        "David Baker",
        "Gaurav Bhardwaj",
        "Hiroaki Suga",
        "Hongliang Duan",
        "Jianzhu Ma",
        "Luhua Lai",
        "Patrick Bryant",
        "Pranam Chatterjee",
        "Stan Z. Li",
        "Tingjun Hou",
        "Yang Liu",
        "Yuedong Yang",
    ],
}

tag_aliases = {
    "AF2": "AF",
    "AlphaFold": "AF",
    "AlphaFold2": "AF",
    "AMP": "AMPs",
    "clogP": "cLogP",
    "Pipline": "Pipeline",
}

authors = {
    "Tingjun Hou": "https://scholar.google.com/citations?hl=en&user=vHW2kqUAAAAJ",
    "Luhua Lai": "https://scholar.google.com/citations?hl=en&user=8NJFCTYAAAAJ",
    "Hiroaki Suga": "https://www.chem.s.u-tokyo.ac.jp/users/bioorg/English/member/Suga.html",
    "Akiyama Yutaka": "https://scholar.google.com/citations?hl=en&user=eHAafMgAAAAJ",
    "Yuedong Yang": "https://scholar.google.com/citations?user=AfjwTKoAAAAJ",
    "David Baker": "https://scholar.google.com/citations?hl=en&user=UKqIqRsAAAAJ",
    "Hongliang Duan": "https://www.mpu.edu.mo/esca/en/duanhongliang.php",
    "Patrick Bryant": "https://scholar.google.com/citations?user=KPlaFQQAAAAJ",
    "Jianzhu Ma": "https://scholar.google.com/citations?user=AATzYuAAAAAJ",
    "Gaurav Bhardwaj": "https://scholar.google.com/citations?user=AJSn9j0AAAAJ",
    "Pranam Chatterjee": "https://scholar.google.co.uk/citations?user=XExgv9YAAAAJ",
    "Chang-Yu Hsieh": "https://scholar.google.com/citations?user=K-AjhSgAAAAJ",
    "Changsheng Zhang": "https://scholar.google.com/citations?user=Y9Zb8akAAAAJ",
}

tools = {
    "ProteinMPNN": "https://www.science.org/doi/10.1126/science.add2187",
    "AF": "https://deepmind.google/technologies/alphafold/",
    "ColabDesign": "https://github.com/sokrypton/ColabDesign",
    "RosettaCommons": "https://www.rosettacommons.org",
    "Molecular AI": "https://github.com/molecularai",
    "RFdiffusion": "https://github.com/RosettaCommons/RFdiffusion",
}

valid_tags = {tag for grouped_tags in tag_groups.values() for tag in grouped_tags}
tag_links = authors | tools
tags = tag_links
