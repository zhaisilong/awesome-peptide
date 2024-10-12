import pandas as pd
from tqdm.auto import tqdm
from liquid import Template
from fire import Fire

from awepep.paper import PaperList

#

# print(template.render(you="World"))  # "Hello, World!"
# print(template.render(you="Liquid"))  # "Hello, Liquid!"

# Generate and print the TOC
# toc_output = generate_toc()
# toc_output

# paper_list = PaperList(DATA_PATH)
# paper_list.generate_context()


def main(data_path: str = "data/paper.csv"):
    paper_list = PaperList(data_path)
    print(paper_list.get_md())


if __name__ == "__main__":
    Fire(main)
