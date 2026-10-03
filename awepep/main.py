from fire import Fire

from awepep.paper import PaperList


def main(
    data_path: str = "data/paper.csv",
    paper_read_path: str = "data/paper-read.csv",
    offline: bool = False,
    refresh_metadata: bool = False,
    as_of: str = None,
    metadata_path: str = None,
):
    paper_list = PaperList(
        data_path,
        paper_read_path,
        metadata_path=metadata_path,
        offline=offline,
        refresh_metadata=refresh_metadata,
    )
    print(paper_list.get_md(as_of=as_of))


def cli():
    Fire(main)


if __name__ == "__main__":
    cli()
