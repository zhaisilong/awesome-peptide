from typing import Any, List
from pathlib import Path
import pandas as pd
from tqdm.auto import tqdm
from datetime import datetime, timedelta
from awepep import config
from awepep import template
import re


class PaperList:
    def __init__(self, data_path: str = None):
        self.data_path = Path(data_path)
        self.df_paper = self.improver(pd.read_csv(self.data_path).fillna(False))  # Required to display tags

    @staticmethod
    def improver(df):
        df["publish_date_"] = df["publish_date"].apply(lambda x: re.sub(r"(\d{4})", r"**\1**", x))
        return df

    def load_data_part(self):
        with open("DATABASE.md", "r", encoding="utf-8") as file:
            return file.read()

    def get_md(self, write=True):
        current_time = datetime.now()

        md_str = template.header.render()
        toc_str = ""
        toc_str += template.toc_header.render()
        paper_str = ""
        paper_last_week_str = template.paper_last_week_header.render(
            date=current_time.strftime("%Y-%m-%d")
        )
        paper_pined_str = template.paper_pined_header.render()

        seci = 1
        custom_sec_order = config.sections.keys()
        self.df_paper["sec_cat"] = pd.Categorical(
            self.df_paper["sec"], categories=custom_sec_order, ordered=True
        )
        for sec, group in self.df_paper.groupby(by="sec_cat"):
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
                        paper_pined_str += template.paper.render(paper=row.to_dict())

                    target_time = datetime.strptime(row["publish_date"], "%Y-%m-%d")
                    time_difference = current_time - target_time
                    if time_difference < timedelta(days=30):
                        paper_last_week_str += template.paper.render(
                            paper=row.to_dict()
                        )

                subseci += 1
            seci += 1
        toc_str += template.toc_tail.render()

        md_str += paper_last_week_str
        md_str += paper_pined_str
        md_str += template.fig.render()
        md_str += toc_str + "\n"
        md_str += self.load_data_part()
        md_str += paper_str
        md_str += template.contributing_and_see_also.render()

        if write:
            with open("README.md", "w") as readme_file:
                readme_file.write(md_str)
        return md_str

    def get_papers(self):
        md_str = ""
        for paper in self.paper_list:
            paper_str = template.paper.render(paper.context)
            md_str += paper_str + "\n"
        return md_str

    def get_toc(self):
        toc_str = ""
        i = 1
        for sec, subsecs in config.sections.items():
            print(sec, subsecs)
            toc_str += template.toc_sec.render(idx=str(i), sec=sec)
            subi = 1
            for subsec in subsecs:
                subi_str = str(i) + "." + str(subi)
                toc_str += template.toc_subsec.render(idx=subi_str, sec=subsec)
                subi += 1
            i += 1
        return toc_str
