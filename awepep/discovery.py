"""Discover candidates from public APIs; editorial decisions stay with curators."""

from __future__ import annotations

import argparse
import csv
from datetime import date, datetime
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET
from urllib.parse import unquote, urlencode

from awepep import crossref, utils

TOPICS = {
    "design": "peptide design",
    "property": "peptide bioactivity",
    "structure": "peptide structure",
    "synthesis": "peptide synthesis",
    "biology": "peptide signaling",
    "delivery": "peptide delivery",
    "biomaterials": "peptide self assembly",
    "therapeutics": "peptide therapeutics",
    "screening": "peptide discovery",
    "data": "peptide database benchmark",
}
KEYWORDS = [
    "peptide",
    "peptid",
    "cyclic peptide",
    "macrocycle",
    "macrocyclic",
    "protein-peptide",
    "antimicrobial peptide",
    "AMP",
    "AMPs",
    "肽",
    "多肽",
    "抗菌肽",
    "环肽",
    "套索肽",
]
DOI_RE = re.compile(r"10\.\d{3,9}/[-._;()/:A-Z0-9]+", re.IGNORECASE)
URL_RE = re.compile(r"https?://[^\s<>)\"']+")
ARXIV_RE = re.compile(
    r"arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5})(?:v\d+)?", re.IGNORECASE
)


def identifiers(text):
    values = DOI_RE.findall(unquote(text))
    values += ["10.48550/arxiv." + value for value in ARXIV_RE.findall(text)]
    return list(dict.fromkeys(crossref.normalize_doi(value) for value in values))


def existing_entries(paths):
    dois, titles = set(), set()
    for path in paths:
        if not Path(path).exists():
            continue
        with Path(path).open(encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                dois.update(
                    identifiers(row.get("doi", "") + " " + row.get("publications", ""))
                )
                if row.get("title"):
                    titles.add(title_key(row["title"]))
    return dois, titles


def title_key(value):
    return " ".join(re.findall(r"\w+", crossref.clean_text(value).casefold()))


def keyword_hits(text, keywords=KEYWORDS):
    result = {}
    for word in keywords:
        if word.isascii():
            pattern = r"(?<!\w)" + re.escape(word)
            pattern += (
                r"\w*" if word in ("peptide", "peptid", "macrocycle") else r"(?!\w)"
            )
            count = len(re.findall(pattern, text, re.IGNORECASE))
        else:
            count = text.count(word)
        if count:
            result[word] = count
    return result


def note_candidates(notes_root, csv_paths, keywords=KEYWORDS):
    existing, _ = existing_entries(csv_paths)
    candidates = []
    for path in sorted(Path(notes_root).rglob("*.md")):
        if path.name.lower() == "readme.md":
            continue
        text = path.read_text(encoding="utf-8")
        frontmatter = {}
        body = text
        if text.startswith("---"):
            parts = text.split("---", 2)
            if len(parts) == 3:
                body = parts[2]
                try:
                    frontmatter = json.loads(parts[1])
                except json.JSONDecodeError:
                    pass
        hits = keyword_hits(body, keywords)
        if not hits:
            continue
        relative = path.relative_to(notes_root)
        title_match = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else path.stem
        # References may contain known papers without making the note itself a duplicate.
        introduction = re.split(
            r"^##?\s+(?:References|参考文献|参考资料)\b",
            body,
            flags=re.MULTILINE | re.IGNORECASE,
        )[0]
        dois = identifiers(introduction)
        primary = dois[0] if dois else ""
        urls = list(dict.fromkeys(url.rstrip(".,;:") for url in URL_RE.findall(body)))
        month = next(
            (
                part[:4] + "-" + part[4:]
                for part in relative.parts
                if re.fullmatch(r"20\d{4}", part)
            ),
            "",
        )
        permalink = frontmatter.get("permalink", "")
        source_url = (
            "https://paper.molastra.org/" + permalink.lstrip("/")
            if permalink
            else "https://github.com/zhaisilong/paper-read/blob/main/src/site/notes/"
            + relative.as_posix()
        )
        candidates.append(
            {
                "doi": primary,
                "primary_doi": primary,
                "dois": dois,
                "title": title,
                "note_title": title,
                "publish_date": "",
                "note_path": relative.as_posix(),
                "group": relative.parts[0],
                "note_month": month,
                "permalink": permalink,
                "source": "paper-read",
                "source_urls": [source_url],
                "keyword_hits": hits,
                "score": sum(hits.values())
                + 5 * sum(keyword_hits(title, keywords).values()),
                "duplicate_dois": sorted(set(dois) & existing),
                "already_in_awesome": primary in existing,
                "code_links": [
                    url
                    for url in urls
                    if any(
                        host in url
                        for host in ("github.com/", "gitlab.com/", "huggingface.co/")
                    )
                ],
                "dataset_links": [
                    url
                    for url in urls
                    if any(
                        host in url
                        for host in ("zenodo.org/", "figshare.com/", "datadryad.org/")
                    )
                ],
                "doi_links": [url for url in urls if "doi.org/" in url],
                "other_links": [url for url in urls if "doi.org/" not in url],
                "snippets": [
                    line.strip()[:240]
                    for line in body.splitlines()
                    if keyword_hits(line, keywords)
                ][:3],
                "crossref_metadata": {},
                "crossref_error": "",
            }
        )
    return sorted(
        candidates,
        key=lambda item: (
            item["already_in_awesome"],
            -int(item["note_month"].replace("-", "") or 0),
            -item["score"],
            item["note_path"],
        ),
    )


def enrich_note(item, timeout=20):
    if not item["doi"]:
        return item
    try:
        metadata = crossref.metadata_for_doi(item["doi"], timeout)
        item["crossref_metadata"] = metadata
        item.update(metadata)
    except (RuntimeError, ValueError) as exc:
        item["crossref_error"] = str(exc)
    return item


def crossref_candidates(since, until, limit, statuses):
    for topic, query in TOPICS.items():
        count, total, cursor = 0, 0, "*"
        try:
            while count < limit:
                # Crossref cursor pagination does not support publication-date sorting.
                params = {
                    "query.bibliographic": query,
                    "filter": f"from-pub-date:{since},until-pub-date:{until},type:journal-article",
                    "sort": "score",
                    "order": "desc",
                    "rows": min(100, limit - count),
                    "cursor": cursor,
                    "mailto": "zhaisilong@outlook.com",
                }
                payload = json.loads(
                    crossref.request_bytes(
                        "https://api.crossref.org/works?" + urlencode(params)
                    )
                )["message"]
                total = payload["total-results"]
                batch = payload["items"]
                if not batch:
                    break
                for work in batch:
                    item = {
                        "doi": crossref.normalize_doi(work["DOI"]),
                        "title": crossref.clean_text(work.get("title", [""])[0]),
                        "source": "crossref",
                        "source_urls": [
                            work.get("URL", "https://doi.org/" + work["DOI"])
                        ],
                        "topics": [topic],
                    }
                    try:
                        item.update(crossref.metadata_from_work(work, item["doi"]))
                    except (ValueError, RuntimeError) as exc:
                        item["metadata_error"] = str(exc)
                    yield item
                count += len(batch)
                next_cursor = payload.get("next-cursor")
                if not next_cursor or next_cursor == cursor:
                    break
                cursor = next_cursor
            statuses.append(
                {
                    "source": "crossref",
                    "topic": topic,
                    "query": query,
                    "matched": total,
                    "retrieved": count,
                    "truncated": total > count,
                }
            )
        except (RuntimeError, ValueError, KeyError) as exc:
            statuses.append(
                {
                    "source": "crossref",
                    "topic": topic,
                    "query": query,
                    "retrieved": count,
                    "error": str(exc),
                }
            )


def _xml_date(element):
    if element is None:
        return ""
    year = element.findtext("Year", "")
    month = element.findtext("Month", "")
    day = element.findtext("Day", "")
    if not year:
        return ""
    if month and not month.isdigit():
        try:
            month = str(datetime.strptime(month[:3], "%b").month)
        except ValueError:
            return year
    parts = (
        [year]
        + ([str(int(month))] if month else [])
        + ([str(int(day))] if day and month else [])
    )
    value = "-".join(parts)
    utils.date_bounds(value)
    return value


def pubmed_article(article):
    content = article.find("./MedlineCitation/Article")
    doi = article.findtext(
        "./PubmedData/ArticleIdList/ArticleId[@IdType='doi']", ""
    ) or content.findtext("ELocationID[@EIdType='doi']", "")
    title_node = content.find("ArticleTitle")
    title = (
        crossref.clean_text("".join(title_node.itertext()))
        if title_node is not None
        else ""
    )
    authors = []
    for author in content.findall("./AuthorList/Author"):
        name = author.findtext("CollectiveName") or " ".join(
            filter(None, [author.findtext("ForeName"), author.findtext("LastName")])
        )
        if name:
            authors.append(name)
    published = _xml_date(content.find("ArticleDate[@DateType='Electronic']"))
    if not published:
        published = _xml_date(
            article.find("./PubmedData/History/PubMedPubDate[@PubStatus='epublish']")
        )
    if not published:
        published = _xml_date(content.find("./Journal/JournalIssue/PubDate"))
    pmid = article.findtext("./MedlineCitation/PMID")
    normalized = crossref.normalize_doi(doi) if doi else ""
    venue = content.findtext("./Journal/ISOAbbreviation") or content.findtext(
        "./Journal/Title", "PubMed"
    )
    return {
        "doi": normalized,
        "title": title,
        "authors": ", ".join(authors),
        "publications": (
            f"[{venue}](https://doi.org/{normalized})" if normalized else ""
        ),
        "publish_date": published,
        "abstract": " ".join(
            crossref.clean_text("".join(node.itertext()))
            for node in content.findall("./Abstract/AbstractText")
        ),
        "source": "pubmed",
        "source_urls": [f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"],
    }


def pubmed_candidates(since, until, limit, statuses):
    base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    for topic, query in TOPICS.items():
        term = (
            " AND ".join(word + "[Title/Abstract]" for word in query.split())
            + f" AND ({since.replace('-', '/')}:{until.replace('-', '/')}[Date - Publication])"
        )
        count, total = 0, 0
        common = {
            "db": "pubmed",
            "tool": "awesome-peptide",
            "email": "zhaisilong@outlook.com",
        }
        try:
            while count < limit:
                params = {
                    **common,
                    "term": term,
                    "sort": "pub date",
                    "retmode": "json",
                    "retstart": count,
                    "retmax": min(100, limit - count),
                }
                result = json.loads(
                    crossref.request_bytes(base + "esearch.fcgi?" + urlencode(params))
                )["esearchresult"]
                total = int(result["count"])
                ids = result["idlist"]
                if not ids:
                    break
                payload = crossref.request_bytes(
                    base
                    + "efetch.fcgi?"
                    + urlencode({**common, "id": ",".join(ids), "retmode": "xml"}),
                    accept="application/xml",
                )
                for article in ET.fromstring(payload).findall("PubmedArticle"):
                    try:
                        item = pubmed_article(article)
                    except (ValueError, AttributeError) as exc:
                        statuses.append(
                            {
                                "source": "pubmed",
                                "topic": topic,
                                "error": f"Invalid article metadata: {exc}",
                            }
                        )
                        continue
                    item["topics"] = [topic]
                    yield item
                count += len(ids)
            statuses.append(
                {
                    "source": "pubmed",
                    "topic": topic,
                    "query": term,
                    "matched": total,
                    "retrieved": count,
                    "truncated": total > count,
                }
            )
        except (RuntimeError, ValueError, KeyError, ET.ParseError) as exc:
            statuses.append(
                {
                    "source": "pubmed",
                    "topic": topic,
                    "query": term,
                    "retrieved": count,
                    "error": str(exc),
                }
            )


def arxiv_candidates(since, until, limit, statuses):
    query = f'(all:peptide OR all:peptides) AND submittedDate:[{since.replace("-", "")}0000 TO {until.replace("-", "")}2359]'
    ns = {
        "atom": "http://www.w3.org/2005/Atom",
        "arxiv": "http://arxiv.org/schemas/atom",
        "os": "http://a9.com/-/spec/opensearch/1.1/",
    }
    count, total = 0, 0
    try:
        while count < limit:
            params = {
                "search_query": query,
                "start": count,
                "max_results": min(100, limit - count),
                "sortBy": "submittedDate",
                "sortOrder": "descending",
            }
            root = ET.fromstring(
                crossref.request_bytes(
                    crossref.ARXIV_API + "?" + urlencode(params),
                    accept="application/atom+xml",
                )
            )
            total = int(root.findtext("os:totalResults", "0", ns))
            entries = root.findall("atom:entry", ns)
            if not entries:
                break
            for entry in entries:
                url = entry.findtext("atom:id", "", ns)
                arxiv_id = re.sub(r"v\d+$", "", url.rsplit("/", 1)[-1])
                if not re.fullmatch(r"\d{4}\.\d{4,5}", arxiv_id):
                    raise ValueError(f"Unexpected arXiv ID: {url}")
                doi = "10.48550/arxiv." + arxiv_id
                journal_doi = entry.findtext("arxiv:doi", "", ns)
                yield {
                    "doi": doi,
                    "title": crossref.clean_text(entry.findtext("atom:title", "", ns)),
                    "authors": ", ".join(
                        node.findtext("atom:name", "", ns)
                        for node in entry.findall("atom:author", ns)
                    ),
                    "publish_date": entry.findtext("atom:published", "", ns).split("T")[
                        0
                    ],
                    "abstract": crossref.clean_abstract(
                        entry.findtext("atom:summary", "", ns)
                    ),
                    "publications": f"[arXiv](https://doi.org/{doi})",
                    "source": "arxiv",
                    "source_urls": [f"https://arxiv.org/abs/{arxiv_id}"],
                    "related_dois": (
                        [crossref.normalize_doi(journal_doi)] if journal_doi else []
                    ),
                }
            count += len(entries)
        statuses.append(
            {
                "source": "arxiv",
                "query": query,
                "matched": total,
                "retrieved": count,
                "truncated": total > count,
            }
        )
    except (RuntimeError, ValueError, ET.ParseError) as exc:
        statuses.append(
            {"source": "arxiv", "query": query, "retrieved": count, "error": str(exc)}
        )


def candidate_status(item, since, until, known_dois, known_titles):
    doi = item.get("doi", "")
    if not doi:
        return "missing_doi"
    if doi in known_dois or set(item.get("related_dois", [])) & known_dois:
        return "duplicate"
    if item.get("metadata_error") or item.get("crossref_error"):
        return "metadata_error"
    if not item.get("publish_date"):
        return "needs_date_verification"
    lower, upper = utils.date_bounds(item["publish_date"])
    if upper < since or lower > until:
        return "out_of_window"
    if lower != upper:
        return "needs_date_verification"
    if title_key(item["title"]) in known_titles:
        return "possible_duplicate"
    return "candidate"


def merge_candidates(items):
    merged = {}
    for item in items:
        key = item.get("doi") or title_key(item["title"])
        if key not in merged:
            merged[key] = item.copy()
            merged[key]["sources"] = [item["source"]]
            continue
        prior = merged[key]
        prior["sources"] = sorted(set(prior["sources"] + [item["source"]]))
        prior["source_urls"] = sorted(set(prior["source_urls"] + item["source_urls"]))
        prior["topics"] = sorted(set(prior.get("topics", []) + item.get("topics", [])))
        for field in ("related_dois", "code_links", "dataset_links"):
            if field in item:
                prior[field] = sorted(set(prior.get(field, []) + item[field]))
        for field in ("title", "authors", "abstract", "publications", "publish_date"):
            if not prior.get(field) or (
                field == "publish_date"
                and len(item.get(field, "").split("-")) > len(prior[field].split("-"))
            ):
                prior[field] = item.get(field, "")
        if all(
            prior.get(field)
            for field in ("title", "authors", "publications", "publish_date")
        ):
            prior.pop("metadata_error", None)
            prior.pop("crossref_error", None)
    return list(merged.values())


def discover(since, until, sources, limit, notes_root, csv_paths):
    known_dois, known_titles = existing_entries(csv_paths)
    items, statuses = [], []
    if "paper-read" in sources:
        notes = note_candidates(notes_root, csv_paths)
        selected = [item for item in notes if not item["already_in_awesome"]][:limit]
        items.extend(enrich_note(item) for item in selected)
        statuses.append(
            {
                "source": "paper-read",
                "matched": len(notes),
                "retrieved": len(selected),
                "truncated": sum(not item["already_in_awesome"] for item in notes)
                > len(selected),
            }
        )
    for name, provider in (
        ("crossref", crossref_candidates),
        ("pubmed", pubmed_candidates),
        ("arxiv", arxiv_candidates),
    ):
        if name in sources:
            items.extend(provider(since, until, limit, statuses))
    candidates = merge_candidates(items)
    for item in candidates:
        item["status"] = candidate_status(
            item,
            date.fromisoformat(since),
            date.fromisoformat(until),
            known_dois,
            known_titles,
        )
    candidates.sort(
        key=lambda item: (
            item["status"] != "candidate",
            (
                utils.custom_sort(item["publish_date"])
                if item.get("publish_date")
                else (0, 0, 0)
            ),
            item["title"],
        )
    )
    return {
        "since": since,
        "until": until,
        "limit_per_query": limit,
        "source_status": statuses,
        "candidates": candidates,
    }


def write_report(report, output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "candidates.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    lines = [
        "# Peptide Paper Candidates",
        "",
        f"Window: {report['since']} to {report['until']}",
        "",
        "## Source Coverage",
        "",
    ]
    for status in report["source_status"]:
        lines.append(
            f"- {status['source']} {status.get('topic', '')}: {json.dumps(status, ensure_ascii=False)}"
        )
    lines.extend(["", "## Candidates", ""])
    for item in report["candidates"]:
        lines.extend(
            [
                f"### {item['title']}",
                "",
                f"- DOI: {item.get('doi') or '(missing)'}",
                f"- Date: {item.get('publish_date') or '(unknown)'}",
                f"- Status: {item['status']}",
                f"- Sources: {', '.join(item['source_urls'])}",
                f"- Topics: {', '.join(item.get('topics', []))}",
                "",
            ]
        )
    (output_dir / "candidates.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--since", required=True, help="Inclusive ISO publication date")
    parser.add_argument("--until", default=date.today().isoformat())
    parser.add_argument("--sources", default="paper-read,crossref,pubmed,arxiv")
    parser.add_argument(
        "--limit", type=int, default=200, help="Maximum records per source query"
    )
    parser.add_argument(
        "--output-dir", type=Path, default=Path("/tmp/awesome-peptide-discovery")
    )
    parser.add_argument(
        "--notes-root", type=Path, default=Path("vendor/paper-read/src/site/notes")
    )
    args = parser.parse_args()
    sources = args.sources.split(",")
    if args.limit <= 0 or date.fromisoformat(args.since) > date.fromisoformat(
        args.until
    ):
        parser.error("limit must be positive and since must not be after until")
    if set(sources) - {"paper-read", "crossref", "pubmed", "arxiv"}:
        parser.error("Unknown source")
    if "paper-read" in sources and not args.notes_root.is_dir():
        parser.error("paper-read notes missing; initialize the submodule first")
    report = discover(
        args.since,
        args.until,
        sources,
        args.limit,
        args.notes_root,
        ["data/paper.csv", "data/paper-read.csv"],
    )
    write_report(report, args.output_dir)
    print(f"candidates={len(report['candidates'])}; reports={args.output_dir}")
    errors = [status for status in report["source_status"] if status.get("error")]
    if errors:
        parser.exit(
            1,
            f"{len(errors)} source request(s) failed; inspect source_status in the report\n",
        )


if __name__ == "__main__":
    main()
