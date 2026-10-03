import csv
from contextlib import redirect_stdout
from datetime import date
from io import StringIO
import json
from pathlib import Path
import re
import runpy
import tempfile
import sys
import unittest
from unittest.mock import patch
from urllib.error import HTTPError
import xml.etree.ElementTree as ET

from awepep import check, config, crossref, discovery, utils
from awepep.metadata import MetadataStore
from awepep.main import cli
from awepep.paper import PAPER_COLUMNS, PAPER_READ_COLUMNS, PaperList


def metadata(title="A peptide study", published="2026-7-15"):
    return {
        "title": title,
        "authors": "A. Author",
        "publications": "[Journal](https://doi.org/10.1234/new)",
        "publish_date": published,
        "abstract": "Peptide biology < affinity > effects.",
    }


class DatesAndMetadataTests(unittest.TestCase):
    def test_verified_primary_date_survives_refresh(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "metadata.json"
            store = MetadataStore(path)
            store.works["10.1234/new"] = {
                "metadata": metadata(),
                "verified_publish_date": {
                    "date": "2026-7-15",
                    "source": "https://pubmed.ncbi.nlm.nih.gov/123/",
                },
            }
            store.changed = True
            store.save()
            with patch.object(
                crossref, "metadata_for_doi", return_value=metadata(published="2026")
            ):
                refreshed = MetadataStore(path, refresh=True)
                self.assertEqual(
                    refreshed.get("10.1234/new")["publish_date"], "2026-7-15"
                )
                refreshed.save()
            self.assertEqual(
                MetadataStore(path, offline=True).get("10.1234/new")["publish_date"],
                "2026-7-15",
            )

    def test_partial_dates_keep_precision_and_do_not_use_created(self):
        self.assertEqual(
            crossref.format_crossref_date(
                {
                    "published-online": {"date-parts": [[2026]]},
                    "created": {"date-parts": [[2026, 7, 1]]},
                }
            ),
            "2026",
        )
        self.assertEqual(
            crossref.format_crossref_date({"published": {"date-parts": [[2026, 7]]}}),
            "2026-7",
        )
        with self.assertRaises(RuntimeError):
            crossref.format_crossref_date({"created": {"date-parts": [[2026, 7, 1]]}})

    def test_invalid_dates_and_future_papers(self):
        for value in ("2026-2-29", "2026-13", "", "2026-7-0", "2026-07-01T00:00:00"):
            with self.assertRaises(ValueError):
                utils.date_bounds(value)
        self.assertFalse(utils.is_recent("2026-10-4", date(2026, 10, 3), 180))
        self.assertFalse(utils.is_recent("2026", date(2026, 10, 3), 180))
        self.assertTrue(utils.is_recent("2026-7", date(2026, 10, 3), 180))

    def test_title_markup_and_doi_identity(self):
        work = {
            "DOI": "10.1234/new",
            "title": [" Design <i>of</i> peptides &amp; proteins "],
            "author": [{"given": "A", "family": "Author"}],
            "published": {"date-parts": [[2026, 7, 15]]},
        }
        self.assertEqual(
            crossref.metadata_from_work(work, "10.1234/new")["title"],
            "Design of peptides & proteins",
        )
        with self.assertRaises(RuntimeError):
            crossref.metadata_from_work(work, "10.1234/other")
        self.assertEqual(
            crossref.normalize_doi("https://doi.org/10.48550/arXiv.2607.12345v2"),
            "10.48550/arxiv.2607.12345",
        )

    def test_http_retry_only_transient_errors(self):
        transient = HTTPError("https://example.org", 503, "unavailable", {}, None)
        with (
            patch.object(
                crossref, "urlopen", side_effect=[transient, transient, transient]
            ) as request,
            patch.object(crossref.time, "sleep"),
        ):
            with self.assertRaises(RuntimeError):
                crossref.request_bytes("https://example.org")
            self.assertEqual(request.call_count, 3)
        permanent = HTTPError("https://example.org", 404, "missing", {}, None)
        with (
            patch.object(crossref, "urlopen", side_effect=permanent) as request,
            patch.object(crossref.time, "sleep"),
        ):
            with self.assertRaises(RuntimeError):
                crossref.request_bytes("https://example.org")
            self.assertEqual(request.call_count, 1)

    def test_snapshot_offline_refresh_and_fallback(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "metadata.json"
            store = MetadataStore(path, refresh=True)
            with patch.object(crossref, "metadata_for_doi", return_value=metadata()):
                self.assertEqual(store.get("10.1234/new"), metadata())
            store.save()
            with patch.object(
                crossref,
                "metadata_for_doi",
                side_effect=AssertionError("network forbidden"),
            ):
                self.assertEqual(
                    MetadataStore(path, offline=True).get("10.1234/new"), metadata()
                )
            with self.assertRaisesRegex(RuntimeError, "Offline metadata missing"):
                MetadataStore(path, offline=True).get("10.1234/missing")
            with (
                patch.object(
                    crossref,
                    "metadata_for_doi",
                    side_effect=RuntimeError("network down"),
                ),
                self.assertWarnsRegex(UserWarning, "using existing snapshot"),
            ):
                self.assertEqual(
                    MetadataStore(path, refresh=True).get("10.1234/new"), metadata()
                )
            with self.assertRaises(ValueError):
                MetadataStore(path, offline=True, refresh=True)


class DiscoveryTests(unittest.TestCase):
    def test_tag_audit_does_not_equate_all_simulation_with_md(self):
        audit = runpy.run_path(
            str(
                Path(__file__).resolve().parents[1]
                / ".codex/skills/curate-peptide-papers/scripts/audit_tags.py"
            )
        )
        self.assertNotIn(
            "MD",
            audit["suggestions"]({"title": "Peptide flexibility simulation"}, set()),
        )
        self.assertIn(
            "MD",
            audit["suggestions"](
                {"title": "Peptide molecular dynamics simulations"}, set()
            ),
        )

    def test_amp_word_boundaries(self):
        self.assertFalse(
            discovery.keyword_hits(
                "sample sampling example amplification", ["AMP", "AMPs"]
            )
        )
        self.assertEqual(
            discovery.keyword_hits("AMP and AMPs", ["AMP", "AMPs"]),
            {"AMP": 1, "AMPs": 1},
        )

    def test_referenced_doi_does_not_hide_new_note(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "journal").mkdir()
            (root / "journal/new.md").write_text(
                '---\n{"permalink":"/new/"}\n---\n# New peptide design\nPaper: https://doi.org/10.1234/new\nPrevious study https://doi.org/10.1234/old\n',
                encoding="utf-8",
            )
            csv_path = root / "papers.csv"
            csv_path.write_text(
                "doi,title\n10.1234/old,Previous study\n", encoding="utf-8"
            )
            item = discovery.note_candidates(root, [csv_path])[0]
            self.assertFalse(item["already_in_awesome"])
            self.assertEqual(item["duplicate_dois"], ["10.1234/old"])
            self.assertEqual(item["primary_doi"], "10.1234/new")

    def test_arxiv_url_and_version_identification(self):
        self.assertEqual(
            discovery.identifiers(
                "https://arxiv.org/abs/2607.12345v2 https://doi.org/10.48550/arXiv.2607.12345"
            ),
            ["10.48550/arxiv.2607.12345"],
        )

    def test_window_and_possible_duplicate(self):
        since, until = date(2026, 6, 16), date(2026, 10, 3)
        item = {"doi": "10.1234/new", **metadata()}
        self.assertEqual(
            discovery.candidate_status(item, since, until, set(), set()), "candidate"
        )
        self.assertEqual(
            discovery.candidate_status(item, since, until, {item["doi"]}, set()),
            "duplicate",
        )
        self.assertEqual(
            discovery.candidate_status(
                item, since, until, set(), {discovery.title_key(item["title"])}
            ),
            "possible_duplicate",
        )
        self.assertEqual(
            discovery.candidate_status(
                {**item, "publish_date": "2026"}, since, until, set(), set()
            ),
            "needs_date_verification",
        )
        self.assertEqual(
            discovery.candidate_status(
                {**item, "publish_date": "2025-7-15"}, since, until, set(), set()
            ),
            "out_of_window",
        )

    def test_cross_source_merge_and_date_enrichment(self):
        a = {
            "doi": "10.1234/new",
            "source": "crossref",
            "source_urls": ["https://doi.org/10.1234/new"],
            **metadata(published="2026"),
        }
        b = {
            **a,
            "source": "pubmed",
            "source_urls": ["https://pubmed.ncbi.nlm.nih.gov/123/"],
            "publish_date": "2026-7-15",
        }
        merged = discovery.merge_candidates([a, b])
        self.assertEqual(len(merged), 1)
        self.assertEqual(merged[0]["publish_date"], "2026-7-15")
        self.assertEqual(len(merged[0]["source_urls"]), 2)

    def test_crossref_cursor_uses_compatible_sort_and_reports_limit(self):
        work = {
            "DOI": "10.1234/new",
            "title": ["A peptide study"],
            "author": [{"family": "Author"}],
            "published": {"date-parts": [[2026, 7, 15]]},
        }
        response = json.dumps(
            {"message": {"items": [work], "total-results": 2, "next-cursor": "next"}}
        ).encode()
        statuses = []
        with (
            patch.dict(discovery.TOPICS, {"design": "peptide design"}, clear=True),
            patch.object(crossref, "request_bytes", return_value=response) as request,
        ):
            items = list(
                discovery.crossref_candidates("2026-06-16", "2026-10-03", 1, statuses)
            )
        self.assertEqual(len(items), 1)
        self.assertIn("sort=score", request.call_args.args[0])
        self.assertTrue(statuses[0]["truncated"])

    def test_provider_failure_is_in_report(self):
        statuses = []
        with (
            patch.dict(discovery.TOPICS, {"design": "peptide design"}, clear=True),
            patch.object(
                crossref, "request_bytes", side_effect=RuntimeError("offline")
            ),
        ):
            self.assertEqual(
                list(
                    discovery.crossref_candidates(
                        "2026-06-16", "2026-10-03", 1, statuses
                    )
                ),
                [],
            )
        self.assertEqual(statuses[0]["error"], "offline")

    def test_pubmed_prefers_online_date_and_article_doi(self):
        article = ET.fromstring(
            '<PubmedArticle><MedlineCitation><PMID>123</PMID><Article><ArticleTitle>A peptide <i>study</i></ArticleTitle><Journal><Title>Journal</Title><JournalIssue><PubDate><Year>2027</Year></PubDate></JournalIssue></Journal><ArticleDate DateType="Electronic"><Year>2026</Year><Month>7</Month><Day>15</Day></ArticleDate><AuthorList><Author><ForeName>A</ForeName><LastName>Author</LastName></Author></AuthorList></Article></MedlineCitation><PubmedData><ArticleIdList><ArticleId IdType="doi">10.1234/new</ArticleId></ArticleIdList><ReferenceList><Reference><ArticleIdList><ArticleId IdType="doi">10.1234/old</ArticleId></ArticleIdList></Reference></ReferenceList></PubmedData></PubmedArticle>'
        )
        item = discovery.pubmed_article(article)
        self.assertEqual(item["publish_date"], "2026-7-15")
        self.assertEqual(item["doi"], "10.1234/new")
        self.assertEqual(item["title"], "A peptide study")


class GenerationTests(unittest.TestCase):
    def test_console_entrypoint_parses_generation_flags(self):
        with (
            patch("awepep.main.PaperList") as papers,
            patch.object(sys, "argv", ["awe-pep", "--offline", "--as-of=2026-10-03"]),
            redirect_stdout(StringIO()),
        ):
            cli()
        self.assertTrue(papers.call_args.kwargs["offline"])
        papers.return_value.get_md.assert_called_once_with(as_of="2026-10-03")

    def test_offline_generation_order_anchors_and_recent_dates(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            rows = []
            for title, sub, published, pinned in [
                ("Sequence paper", "Sequence-Based Design", "2026-7-15", ""),
                ("Diffusion paper", "Diffusion & Flow", "2026-7-16", "true"),
                ("Future paper", "Diffusion & Flow", "2027-1-1", "false"),
            ]:
                rows.append(
                    {
                        **dict.fromkeys(PAPER_COLUMNS, ""),
                        **metadata(title, published),
                        "sec": "Peptide Design & Generation",
                        "subsec": sub,
                        "pined": pinned,
                    }
                )
                rows[-1][
                    "publications"
                ] = f"[Journal](https://doi.org/10.1234/{len(rows)})"
            main_csv = root / "papers.csv"
            with main_csv.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=PAPER_COLUMNS)
                writer.writeheader()
                writer.writerows(rows)
            paper_read = root / "paper-read.csv"
            with paper_read.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=PAPER_READ_COLUMNS)
                writer.writeheader()
                writer.writerow(
                    {
                        "doi": "10.1234/new",
                        "sec": "Peptide Design & Generation",
                        "subsec": "Structure-Based Design",
                    }
                )
            snapshot = root / "snapshot.json"
            snapshot.write_text(
                json.dumps(
                    {
                        "version": 1,
                        "works": {
                            "10.1234/new": {"metadata": metadata("Cached paper")}
                        },
                    }
                ),
                encoding="utf-8",
            )
            with (
                patch.object(
                    crossref,
                    "metadata_for_doi",
                    side_effect=AssertionError("network forbidden"),
                ),
                patch.object(PaperList, "load_data_part", return_value=""),
            ):
                papers = PaperList(
                    str(main_csv), str(paper_read), offline=True, metadata_path=snapshot
                )
                before = main_csv.read_bytes()
                md = papers.get_md(write=False, as_of="2026-10-03")
                self.assertEqual(md, papers.get_md(write=False, as_of="2026-10-03"))
                self.assertEqual(main_csv.read_bytes(), before)
            body = md.split("## 5. Peptide Design & Generation", 1)[1]
            self.assertLess(
                body.index("Sequence-Based Design"),
                body.index("Structure-Based Design"),
            )
            self.assertLess(
                body.index("Structure-Based Design"), body.index("Diffusion & Flow")
            )
            recent = md.split("Papers pinned", 1)[0]
            self.assertNotIn("Future paper", recent)
            self.assertIn("Cached paper", md)
            self.assertIn("&lt; affinity &gt;", md)
            headings = {
                utils.heading_slug(line.lstrip("# "))
                for line in md.splitlines()
                if line.startswith("#")
            }
            for anchor in re.findall(r"href=['\"]#([^'\"]+)", md):
                if re.match(r"[1-9]", anchor):
                    self.assertIn(anchor, headings)

    def test_invalid_classification_and_flag_validation(self):
        with self.assertRaises(ValueError):
            check.check_section({"sec": "Unknown", "subsec": "Unknown"})
        with self.assertRaises(ValueError):
            check.check_editorial_fields({"quality": "excellent", "pined": False})
        with self.assertRaises(ValueError):
            check.check_editorial_fields({"quality": False, "pined": "banana"})
        pool = {"10.1234/new"}
        with self.assertRaises(ValueError):
            check.check_duplicate(
                check.extract_dois("[J](https://doi.org/10.1234/NEW)"), pool
            )


if __name__ == "__main__":
    unittest.main()
