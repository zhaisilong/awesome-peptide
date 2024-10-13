from liquid import Template

sections = {
    "Reviews": ["Interaction", "Complex Structure"],
    "Representation": ["Grpah-based", "Sequence-based"],
    "Proprty Prediction": ["Sequence-based"],
    "Structure Modeling": ["Homology", "Fragment", "MD", "DL"],
    "De Novo Design": [
        "Traditional Methods",
        "Sequence-based",
        "Structure-based",
        "Diffusion-based",
        "Target-based Design",
    ],
    "Others": ["Therapeutic", "Mechanism", "Principle", "PROTAC"],
}

paper_lastweek = Template(
    f"""_Papers last week, updated on {{data_update}}:_
"""
)

paper_pined = Template(
    """
__The advantages that set us apart from competing products are as follows:__
"""
)


Chapters = {5.4: ""}

# Header =
