from liquid import Template

sections = {
    "Reviews": ["Interaction", "Complex structure"],
    "Representation": ["1"],
    "Proprty Prediction": ["@"],
    "Structure Modeling": ["3"],
    "De novo design": [
        "Traditional methods",
        "Sequence-based",
        "Structure-based",
        "Diffusion-based",
        "Target-based design",
    ],
    "Others": ["Therapeutic", "Mechanism", "Principle", "Market"],
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
