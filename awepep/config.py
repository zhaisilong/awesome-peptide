from liquid import Template

sections = {
    "Reviews": ["Interaction", "Property", "Sequence", "Structure", "Design"],
    "Representation": ["Grpah-based", "Sequence-based"],
    "Proprty Prediction": ["Traditional", "Sequence-based"],
    "Structure Modeling": ["Monomer", "Complex"],
    "Interaction Modeling": ["Grpah-based", "Sequence-based", "Site Prediction"],
    "Design": [
        "Traditional",
        "Sequence-based",
        "Structure-based",
        "Diffusion-based",
        "Graph-based",
    ],
    "Others": ["Therapeutic", "Principle", "PROTAC", "Protein Binders", "RaPID"],
}

max_pined = 12
last_days = 180

authors = {
    "Tingjun Hou": "https://scholar.google.com/citations?hl=en&user=vHW2kqUAAAAJ",
    "Luhua Lai": "https://scholar.google.com/citations?hl=en&user=8NJFCTYAAAAJ",
    "Hiroaki Suga": "https://www.chem.s.u-tokyo.ac.jp/users/bioorg/English/member/Suga.html",
    "Akiyama Yutaka": "https://scholar.google.com/citations?hl=en&user=eHAafMgAAAAJ",
    "Yuedong Yang": "https://scholar.google.com/citations?user=AfjwTKoAAAAJ",
    "David Baker": "https://scholar.google.com/citations?hl=en&user=UKqIqRsAAAAJ",
    "Hongliang Duan": "https://www.mpu.edu.mo/esca/en/duanhongliang.php",
    "Patrick Bryant": "https://scholar.google.com/citations?user=KPlaFQQAAAAJ",
}

tools = {
    "ProteinMPNN": "https://www.science.org/doi/10.1126/science.add2187",
    "AF": "https://deepmind.google/technologies/alphafold/",
    "ColabDesign": "https://github.com/sokrypton/ColabDesign",
    "RosettaCommons": "https://www.rosettacommons.org",
    "Molecular AI": "https://github.com/molecularai",
}

tags = authors | tools
