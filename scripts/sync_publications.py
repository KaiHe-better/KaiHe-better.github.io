#!/usr/bin/env python3
"""Synchronize homepage publications from Google Scholar data.

The script is intentionally conservative:
- It keeps existing curated entries unless a same-title preprint is replaced by
  a formal publication.
- It only rewrites bounded AUTO_* regions in _pages/about.md.
- Optional overrides provide exact citation/news text for entries where Google
  Scholar metadata is incomplete or too coarse for a public CV.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


DEFAULT_ABOUT = Path("_pages/about.md")
DEFAULT_SCHOLAR_JSON = Path("google_scholar_crawler/results/gs_data.json")
DEFAULT_OVERRIDES = Path("data/publication_overrides.json")

NEWS_START = "<!-- AUTO_NEWS_START -->"
NEWS_END = "<!-- AUTO_NEWS_END -->"
PUBS_START = "<!-- AUTO_PUBLICATIONS_START -->"
PUBS_END = "<!-- AUTO_PUBLICATIONS_END -->"

PREPRINT_PATTERNS = (
    "arxiv",
    "techrxiv",
    "authorea",
    "medrxiv",
    "biorxiv",
    "chemrxiv",
    "ssrn",
    "research square",
    "preprint",
)

CONFERENCE_PATTERNS = (
    "proceedings",
    "conference",
    "annual meeting",
    "aaai",
    "acl",
    "emnlp",
    "neurips",
    "nips",
    "miccai",
    "bibm",
    "cikm",
    "coling",
)


@dataclass
class Entry:
    title: str
    markdown: str
    section: str  # "publication" or "preprint"
    year: int
    sort_date: str = ""
    news: str = ""
    order: int = 0

    @property
    def key(self) -> str:
        return normalize_title(self.title)


def normalize_title(title: str) -> str:
    title = title.lower()
    title = title.replace("‑", "-").replace("–", "-").replace("—", "-")
    title = re.sub(r"<[^>]+>", "", title)
    title = re.sub(r"[^a-z0-9]+", " ", title)
    return re.sub(r"\s+", " ", title).strip()


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def load_overrides(path: Path) -> tuple[dict[str, Entry], dict[str, str]]:
    data = load_json(path)
    entries: dict[str, Entry] = {}
    aliases: dict[str, str] = {}

    for item in data.get("entries", []):
        title = item["title"].strip()
        entry = Entry(
            title=title,
            markdown=item["markdown"].strip(),
            section=item.get("section", "publication"),
            year=int(item["year"]),
            sort_date=item.get("sort_date", ""),
            news=item.get("news", "").strip(),
        )
        entries[entry.key] = entry
        for alias in item.get("aliases", []):
            aliases[normalize_title(alias)] = entry.key

    return entries, aliases


def canonical_key(title: str, aliases: dict[str, str]) -> str:
    key = normalize_title(title)
    return aliases.get(key, key)


def parse_title_from_markdown(markdown: str) -> str:
    text = markdown.strip()
    if text.startswith("- "):
        text = text[2:]
    # Existing entries follow: Authors. Title [J/C/Preprint]. Venue...
    parts = text.split(". ", 1)
    rest = parts[1] if len(parts) == 2 else text
    title = re.split(r"\s+\[(?:J|C|Preprint)\]\.?", rest, maxsplit=1)[0]
    return title.strip()


def parse_existing_publications(about_text: str) -> dict[str, Entry]:
    body = publication_body(about_text)
    entries: dict[str, Entry] = {}
    current_section: str | None = None

    order = 0
    for raw_line in body.splitlines():
        line = raw_line.rstrip()
        heading = re.match(r"^##\s+(.+?)\s*$", line)
        if heading:
            current_section = heading.group(1)
            continue
        if not line.startswith("- ") or not current_section:
            continue
        order += 1

        title = parse_title_from_markdown(line)
        if current_section.lower() == "preprints":
            section = "preprint"
            year = extract_year(line) or 0
        elif re.fullmatch(r"20\d{2}", current_section):
            section = "publication"
            year = int(current_section)
        elif current_section == "2022 and Before":
            section = "publication"
            year = extract_year(line) or 2022
        else:
            continue

        entry = Entry(title=title, markdown=line, section=section, year=year, order=order)
        entries[entry.key] = entry

    return entries


def extract_year(text: str) -> int | None:
    years = [int(y) for y in re.findall(r"\b(20\d{2})\b", text)]
    return years[-1] if years else None


def publication_body(about_text: str) -> str:
    if PUBS_START in about_text and PUBS_END in about_text:
        return about_text.split(PUBS_START, 1)[1].split(PUBS_END, 1)[0]

    start = re.search(r"^##\s+20\d{2}\s*$", about_text, flags=re.M)
    end = about_text.find("<span class='anchor' id='-Honors-and-Awards'></span>")
    if not start or end == -1:
        raise ValueError("Could not locate publications section in about.md")
    return about_text[start.start() : end]


def scholar_publications(path: Path) -> list[dict[str, Any]]:
    data = load_json(path)
    pubs = data.get("publications", [])
    if isinstance(pubs, dict):
        pubs = list(pubs.values())
    return pubs


def entry_from_scholar(pub: dict[str, Any]) -> Entry | None:
    bib = pub.get("bib", {})
    title = str(bib.get("title") or pub.get("title") or "").strip()
    if not title:
        return None

    year = extract_year(str(bib.get("pub_year") or bib.get("year") or ""))
    citation = str(
        bib.get("citation")
        or bib.get("journal")
        or bib.get("conference")
        or bib.get("venue")
        or ""
    ).strip()
    if year is None:
        year = extract_year(citation) or 0

    authors = str(bib.get("author") or bib.get("authors") or "").strip()
    authors = authors.replace(" and ", ", ")
    authors = emphasize_kai_he(authors) if authors else ""

    lower_citation = citation.lower()
    is_preprint = any(pattern in lower_citation for pattern in PREPRINT_PATTERNS)
    kind = "Preprint" if is_preprint else ("C" if any(p in lower_citation for p in CONFERENCE_PATTERNS) else "J")
    section = "preprint" if is_preprint else "publication"

    if not citation:
        citation = "Google Scholar"

    prefix = f"{authors}. " if authors else ""
    markdown = f"- {prefix}{title} [{kind}]. {citation}"
    if year and str(year) not in citation:
        markdown += f", {year}"
    markdown += "."

    return Entry(title=title, markdown=markdown, section=section, year=year)


def emphasize_kai_he(authors: str) -> str:
    # Scholar often returns abbreviated author lists. Keep this deliberately
    # narrow so we do not accidentally bold other people.
    authors = re.sub(r"\bK He\b", "***Kai He***", authors)
    authors = re.sub(r"\bKai He\b", "***Kai He***", authors)
    return authors


def merge_entries(
    existing: dict[str, Entry],
    scholar_pubs: list[dict[str, Any]],
    overrides: dict[str, Entry],
    aliases: dict[str, str],
) -> dict[str, Entry]:
    merged: dict[str, Entry] = {}

    for key, entry in existing.items():
        merged[aliases.get(key, key)] = entry

    # Overrides are authoritative and can also seed entries before Scholar has
    # enough detail.
    for key, entry in overrides.items():
        merged[aliases.get(key, key)] = entry

    for pub in scholar_pubs:
        generated = entry_from_scholar(pub)
        if not generated:
            continue
        key = canonical_key(generated.title, aliases)
        entry = overrides.get(key, generated)
        current = merged.get(key)
        if not current:
            merged[key] = entry
            continue
        if current.section == "preprint" and entry.section == "publication":
            merged[key] = entry

    publication_keys = {key for key, entry in merged.items() if entry.section == "publication"}
    return {
        key: entry
        for key, entry in merged.items()
        if not (entry.section == "preprint" and key in publication_keys)
    }


def sort_entries(entries: list[Entry]) -> list[Entry]:
    return sorted(
        entries,
        key=lambda e: (1, e.sort_date, e.title.lower()) if e.sort_date else (0, -e.order, e.title.lower()),
        reverse=True,
    )


def render_publications(entries: dict[str, Entry]) -> str:
    publications: dict[int, list[Entry]] = {}
    old_publications: list[Entry] = []
    preprints: list[Entry] = []

    for entry in entries.values():
        if entry.section == "preprint":
            preprints.append(entry)
        elif entry.year:
            if entry.year <= 2022:
                old_publications.append(entry)
            else:
                publications.setdefault(entry.year, []).append(entry)

    blocks: list[str] = []
    for year in sorted(publications, reverse=True):
        blocks.append(f"## {year}")
        blocks.extend(entry.markdown for entry in sort_entries(publications[year]))
        blocks.append("")

    if old_publications:
        blocks.append("## 2022 and Before")
        blocks.extend(entry.markdown for entry in sort_entries(old_publications))
        blocks.append("")

    if preprints:
        blocks.append("## Preprints")
        blocks.extend(entry.markdown for entry in sort_entries(preprints))
        blocks.append("")

    return "\n\n".join(blocks).rstrip() + "\n"


def render_news(entries: dict[str, Entry], year: int) -> str:
    news_entries = [e for e in entries.values() if e.news and e.news.startswith(f"- *{year}.")]
    news_entries = sorted(news_entries, key=lambda e: (e.sort_date, e.title.lower()), reverse=True)
    return "\n".join(e.news for e in news_entries).rstrip() + "\n"


def replace_region(text: str, start: str, end: str, replacement: str) -> str:
    if start not in text or end not in text:
        raise ValueError(f"Missing region markers: {start} / {end}")
    before, rest = text.split(start, 1)
    _, after = rest.split(end, 1)
    return f"{before}{start}\n{replacement}{end}{after}"


def ensure_markers(text: str) -> str:
    if NEWS_START not in text:
        text = re.sub(
            r"(# 🔥 News\n\n)(.*?)(\n\n\n\n# 📝 Publications)",
            rf"\1{NEWS_START}\n\2\n{NEWS_END}\3",
            text,
            flags=re.S,
        )
    if PUBS_START not in text:
        start_match = re.search(r"^##\s+20\d{2}\s*$", text, flags=re.M)
        end_marker = "<span class='anchor' id='-Honors-and-Awards'></span>"
        if not start_match or end_marker not in text:
            raise ValueError("Could not insert publication markers")
        text = text[: start_match.start()] + PUBS_START + "\n" + text[start_match.start() :]
        end_idx = text.index(end_marker)
        text = text[:end_idx].rstrip() + "\n" + PUBS_END + "\n\n \n" + text[end_idx:]
    return text


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--about", type=Path, default=DEFAULT_ABOUT)
    parser.add_argument("--scholar-json", type=Path, default=DEFAULT_SCHOLAR_JSON)
    parser.add_argument("--overrides", type=Path, default=DEFAULT_OVERRIDES)
    parser.add_argument("--news-year", type=int, default=2026)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    about_text = args.about.read_text(encoding="utf-8")
    about_text = ensure_markers(about_text)
    existing = parse_existing_publications(about_text)
    overrides, aliases = load_overrides(args.overrides)
    scholar_pubs = scholar_publications(args.scholar_json)

    merged = merge_entries(existing, scholar_pubs, overrides, aliases)
    about_text = replace_region(about_text, NEWS_START, NEWS_END, render_news(merged, args.news_year))
    about_text = replace_region(about_text, PUBS_START, PUBS_END, render_publications(merged))

    if args.write:
        args.about.write_text(about_text, encoding="utf-8")
    else:
        print(about_text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
