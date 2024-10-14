from liquid import Template

sections = {
    "Reviews": ["Interaction", "Sequence", "Structure", "Design"],
    "Representation": ["Grpah-based", "Sequence-based"],
    "Proprty Prediction": ["Traditional", "Sequence-based"],
    "Structure Modeling": ["Homology", "Fragment", "MD", "DL"],
    "Design": [
        "Traditional",
        "Sequence-based",
        "Structure-based",
        "Diffusion-based",
        "Target-specific",
    ],
    "Others": ["Therapeutic", "Mechanism", "Principle", "PROTAC", "Protein Binders"],
}

max_pined = 10
