from fire import Fire

from awepep.paper import PaperList


def main(
    data_path: str = "data/paper.csv", paper_read_path: str = "data/paper-read.csv"
):
    paper_list = PaperList(data_path, paper_read_path)
    print(paper_list.get_md())


if __name__ == "__main__":
    Fire(main)
