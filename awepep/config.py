from liquid import Template

sections = {
    "Reviews": ["Interaction", "Property", "Sequence", "Structure", "Design"],
    "Representation": ["Grpah-based", "Sequence-based"],
    "Proprty Prediction": ["Traditional", "Sequence-based", "Structure-based"],
    "Structure Modeling": ["Monomer", "Complex"],
    "Interaction Modeling": ["Grpah-based", "Sequence-based", "Site Prediction"],
    "Design": [
        "Traditional",
        "Sequence-based",
        "Structure-based",
        "Diffusion-based",
        "Graph-based",
    ],
    "Others": ["Screen", "Therapeutic", "Principle", "PROTAC", "Protein Binders", "RaPID"],
}

max_pined = 30
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

tags = authors | tools
