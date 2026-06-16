from datetime import datetime, timedelta
from pathlib import Path
import re

import pandas as pd

from awepep import config, crossref, tags as tag_utils, template, utils

PAPER_COLUMNS = [
    "title",
    "sec",
    "subsec",
    "authors",
    "publications",
    "code",
    "dataset",
    "quality",
    "publish_date",
    "abstract",
    "blogs",
    "pined",
    "tags",
]
PAPER_READ_COLUMNS = [
    "doi",
    "title",
    "source",
    "sec",
    "subsec",
    "code",
    "dataset",
    "quality",
    "pined",
    "tags",
]
PAPER_READ_BASE_URL = "https://paper.molastra.org"
DOI_IN_PUBLICATION_RE = re.compile(r"10\.\d{3,9}/[-._;()/:A-Z0-9]+", re.IGNORECASE)


class PaperList:
    def __init__(
        self,
        data_path: str = "data/paper.csv",
        paper_read_path: str = "data/paper-read.csv",
    ):
        self.data_path = Path(data_path)
        df_paper = pd.read_csv(self.data_path)
        df_paper = self.load_paper_read(df_paper, Path(paper_read_path))
        df_paper = df_paper.astype("object").where(pd.notna(df_paper), False)
        self.df_paper = self.process_tags(
            self.improver(df_paper)
        )  # Required to display tags

    @staticmethod
    def row_value(row, key):
        value = row.get(key, "")
        if pd.isna(value) or value is False:
            return ""
        return str(value).strip()

    @classmethod
    def optional_row_value(cls, row, key):
        return cls.row_value(row, key) or False

    @staticmethod
    def source_to_blog(source: str) -> str:
        if not source:
            return ""
        if source.startswith(("http://", "https://")):
            url = source
        elif source.startswith("vendor/paper-read/"):
            repo_path = source.replace("vendor/paper-read/", "", 1)
            url = f"https://github.com/zhaisilong/paper-read/blob/main/{repo_path}"
        elif source.startswith("src/site/notes/"):
            url = f"https://github.com/zhaisilong/paper-read/blob/main/{source}"
        else:
            url = f"{PAPER_READ_BASE_URL}/{source.lstrip('/')}"
        return f"[paper-read]({url})"

    @staticmethod
    def dois_from_publications(publications):
        dois = set()
        for publication in publications:
            if pd.isna(publication) or not publication:
                continue
            for doi in DOI_IN_PUBLICATION_RE.findall(str(publication)):
                dois.add(crossref.normalize_doi(doi))
        return dois

    def load_paper_read(self, df_paper, paper_read_path: Path):
        if not paper_read_path.exists():
            return df_paper

        df_paper_read = pd.read_csv(paper_read_path)
        missing_columns = set(PAPER_READ_COLUMNS) - set(df_paper_read.columns)
        if missing_columns:
            missing = ", ".join(sorted(missing_columns))
            raise ValueError(f"{paper_read_path} is missing columns: {missing}")

        existing_dois = self.dois_from_publications(df_paper["publications"])
        paper_read_rows = []
        for _, source_row in df_paper_read.iterrows():
            doi = crossref.normalize_doi(self.row_value(source_row, "doi"))
            if doi in existing_dois:
                continue

            try:
                metadata = crossref.metadata_for_doi(doi)
            except Exception as exc:
                title = self.row_value(source_row, "title") or doi
                raise RuntimeError(
                    f"Could not enrich paper-read row {title!r} with DOI {doi}"
                ) from exc

            paper_read_rows.append(
                {
                    "title": self.row_value(source_row, "title") or metadata["title"],
                    "sec": self.row_value(source_row, "sec"),
                    "subsec": self.row_value(source_row, "subsec"),
                    "authors": metadata["authors"],
                    "publications": metadata["publications"],
                    "code": self.optional_row_value(source_row, "code"),
                    "dataset": self.optional_row_value(source_row, "dataset"),
                    "quality": self.optional_row_value(source_row, "quality"),
                    "publish_date": metadata["publish_date"],
                    "abstract": metadata["abstract"] or False,
                    "blogs": self.source_to_blog(self.row_value(source_row, "source"))
                    or False,
                    "pined": self.optional_row_value(source_row, "pined"),
                    "tags": self.optional_row_value(source_row, "tags"),
                }
            )
            existing_dois.add(doi)

        if not paper_read_rows:
            return df_paper
        return pd.concat(
            [df_paper, pd.DataFrame(paper_read_rows, columns=PAPER_COLUMNS)],
            ignore_index=True,
        )

    @staticmethod
    def improver(df):
        df["publish_date_"] = df["publish_date"].apply(
            lambda x: re.sub(r"(\d{4})", r"**\1**", x)
        )
        return df

    @staticmethod
    def process_tags(df):
        df["tags"] = df["tags"].apply(tag_utils.format_for_readme)
        return df

    def load_data_part(self):
        with open("DATABASE.md", "r", encoding="utf-8") as file:
            return file.read()

    @staticmethod
    def render_paper_rows(rows):
        if not rows:
            return ""
        rows_df = pd.DataFrame(rows).sort_values(
            by="publish_date",
            key=lambda x: x.apply(utils.custom_sort),
            ascending=False,
        )
        return "".join(
            template.paper.render(paper=row.to_dict()) for _, row in rows_df.iterrows()
        )

    def get_md(self, write=True):
        current_time = datetime.now()

        md_str = template.header.render()
        toc_str = ""
        toc_str += template.toc_header.render()
        paper_str = ""
        paper_last_week_str = template.paper_last_week_header.render(
            date=current_time.strftime("%Y-%m-%d")
        )
        paper_last_week_list = []
        paper_pined_str = template.paper_pined_header.render()
        paper_pined_list = []

        seci = 1
        custom_sec_order = config.sections.keys()
        self.df_paper["sec_cat"] = pd.Categorical(
            self.df_paper["sec"], categories=custom_sec_order, ordered=True
        )

        # 先按照时间排序
        self.df_paper.sort_values(
            by="publish_date",
            key=lambda x: x.apply(utils.custom_sort),
            ascending=False,
            inplace=True,
        )
        for sec, group in self.df_paper.groupby(by="sec_cat", observed=False):
            assert sec in config.sections.keys(), "No such section: %s" % sec
            subseci = 1
            idx_str = str(seci)
            toc_str += template.toc_sec.render(idx=idx_str, sec=sec)
            paper_str += template.sec.render(idx=idx_str, sec=sec)

            num = len(group["subsec"].unique())

            custom_subsec_order = config.sections[sec]
            group["subsec_cat"] = pd.Categorical(
                group["subsec"], categories=custom_subsec_order, ordered=True
            )
            for subsec, subgroup in group.groupby(by="subsec"):
                assert subsec in config.sections[sec], "No such subsection: %s" % subsec
                dot = False if subseci == num else True
                idx_str = str(seci) + "." + str(subseci)
                toc_str += template.toc_subsec.render(idx=idx_str, sec=subsec, dot=dot)
                paper_str += template.subsec.render(idx=idx_str, sec=subsec)

                for i, row in subgroup.iterrows():
                    paper_str += template.paper.render(paper=row.to_dict())
                    if row["pined"]:
                        paper_pined_list.append(row)
                    target_time = datetime.strptime(row["publish_date"], "%Y-%m-%d")
                    time_difference = current_time - target_time
                    if time_difference < timedelta(days=config.last_days):
                        paper_last_week_list.append(row)
                subseci += 1
            seci += 1
        toc_str += template.toc_tail.render()

        md_str += paper_last_week_str
        md_str += self.render_paper_rows(paper_last_week_list)

        md_str += paper_pined_str
        md_str += self.render_paper_rows(paper_pined_list)

        md_str += template.fig.render()
        md_str += toc_str + "\n"
        md_str += self.load_data_part()
        md_str += paper_str
        md_str += template.contributing_and_see_also.render()

        if write:
            with open("README.md", "w") as readme_file:
                readme_file.write(md_str)
        return md_str
