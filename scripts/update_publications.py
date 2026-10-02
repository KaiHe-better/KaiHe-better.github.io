#!/usr/bin/env python3
"""Update bounded News and Publications from live Scholar and public ORCID records.

Never treat incomplete metadata, a failed source, or a cached response as a deletion.
Crossref DOI metadata verifies author identity and publication type before publishing.
"""
from __future__ import annotations

import argparse
import copy
import html
import json
import os
import re
import sys
import time
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError

ORCID = "0000-0003-2639-1532"
SCHOLAR = "4nWk-HYAAAAJ"
START = "<!-- AUTO_PUBLICATIONS_START -->"
END = "<!-- AUTO_PUBLICATIONS_END -->"
HEADERS = {"User-Agent": "KaiHeHomepage/1.0 (https://github.com/KaiHe-better/KaiHe-better.github.io)", "Accept": "application/json"}


def clean(value):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]*>", "", str(value or "")))).strip()


def key(value):
    return re.sub(r"[^a-z0-9]", "", unicodedata.normalize("NFKD", clean(value)).encode("ascii", "ignore").decode().lower())


def get(url, accept="application/json"):
    req = Request(url, headers={**HEADERS, "Accept": accept})
    # No proxy rotation or CAPTCHA handling. A blocked source is reported and skipped.
    with urlopen(req, timeout=20) as response:
        payload = response.read(8_000_001)
    if len(payload) > 8_000_000:
        raise ValueError("Source response is unexpectedly large")
    return payload if accept == "text/html" else payload.decode("utf-8")


_JSON_CACHE = {}


def get_json(url):
    if url not in _JSON_CACHE:
        for attempt in range(3):
            try:
                _JSON_CACHE[url] = json.loads(get(url))
                break
            except HTTPError as exc:
                if exc.code not in (429, 502, 503, 504) or attempt == 2:
                    raise
                time.sleep(min(30, max(5, int(exc.headers.get("Retry-After", "10")))))
    return _JSON_CACHE[url]


def scholar_records():
    from bs4 import BeautifulSoup
    records = []
    for offset in range(0, 1000, 100):
        params = urlencode({"user": SCHOLAR, "hl": "en", "sortby": "pubdate", "cstart": offset, "pagesize": 100})
        soup = BeautifulSoup(get("https://scholar.google.com/citations?" + params, "text/html"), "html.parser")
        if not soup.select_one("#gsc_a_b"):
            raise ValueError("Scholar did not return its publication table (possibly blocked)")
        rows = soup.select("tr.gsc_a_tr")
        for row in rows:
            title = row.select_one("a.gsc_a_at")
            if title:
                gray = row.select(".gs_gray")
                records.append({"title": title.get_text(" ", strip=True), "source": "Google Scholar", "citation": gray[1].get_text(" ", strip=True) if len(gray) > 1 else "", "detail": "https://scholar.google.com" + title.get("href", "")})
        more = soup.select_one("#gsc_bpf_more")
        if len(rows) < 100 or (more and more.has_attr("disabled")):
            return records
        time.sleep(1)
    raise ValueError("Scholar pagination limit reached; refusing a silently truncated source")


def orcid_records():
    data = get_json(f"https://pub.orcid.org/v3.0/{ORCID}/works")
    if "group" not in data:
        raise ValueError("ORCID did not return a works list")
    records = []
    for group in data["group"]:
        for work in group.get("work-summary", []):
            title = work.get("title", {}).get("title", {}).get("value", "")
            ids = work.get("external-ids", {}).get("external-id", [])
            dois = [x.get("external-id-value", "") for x in ids if x.get("external-id-type") == "doi" and x.get("external-id-relationship") == "self"]
            for doi in dois or [""]:
                records.append({"title": title, "doi": doi, "source": "ORCID"})
    return records


def is_kai(author):
    orcid = author.get("ORCID", "").rstrip("/").rsplit("/", 1)[-1]
    if orcid:
        return orcid == ORCID
    return key(author.get("family")) == "he" and key(author.get("given")) in {"kai", "k"}


def citation(record, expected_title):
    title = clean((record.get("title") or [""])[0])
    if key(title) != key(expected_title):
        raise ValueError("DOI title differs from the author-profile title")
    authors = record.get("author", [])
    if not authors or not any(is_kai(a) for a in authors):
        raise ValueError("Author list does not identify Kai He")
    kind = {"journal-article": "J", "proceedings-article": "C", "posted-content": "Preprint"}.get(record.get("type"))
    if not kind or (kind == "Preprint" and record.get("subtype") not in {None, "preprint"}):
        raise ValueError("Unsupported or ambiguous publication type")
    parts = (record.get("published-online") or record.get("published") or {}).get("date-parts", [[]])[0]
    if not parts or not 1900 <= parts[0] <= datetime.now(timezone.utc).year + 1:
        raise ValueError("Missing or invalid publication year")
    venue = clean((record.get("container-title") or [""])[0])
    if not venue and kind == "Preprint":
        venue = clean(record.get("institution", [{}])[0].get("name", ""))
    if not venue:
        raise ValueError("Missing venue or preprint repository")
    doi = record.get("DOI", "").lower().strip()
    if not re.fullmatch(r"10\.\d{4,9}/\S+", doi):
        raise ValueError("Missing or invalid DOI")
    names = []
    for author in authors:
        name = clean(" ".join(filter(None, [author.get("given"), author.get("family")])))
        if not name:
            raise ValueError("Incomplete author list")
        given = clean(author.get("given"))
        initials = " ".join(part[0] + "." for part in given.split() if part)
        short = (initials + " " + clean(author.get("family"))).strip()
        names.append("***Kai He***" if is_kai(author) else html.escape(short).replace("{", "&#123;").replace("}", "&#125;"))
    # Encode external text as HTML entities so it cannot inject markup or Liquid.
    safe = lambda s: html.escape(s).replace("{", "&#123;").replace("}", "&#125;").replace("[", "&#91;").replace("]", "&#93;")
    suffix = f"{safe(venue)}, {parts[0]}"
    if record.get("volume"):
        suffix += ", " + safe(clean(record["volume"]))
    if record.get("issue"):
        suffix += "(" + safe(clean(record["issue"])) + ")"
    pages = record.get("page") or record.get("article-number")
    if pages:
        suffix += ": " + safe(clean(pages))
    line = f"- {', '.join(names)}. {safe(title)} [{kind}]. {suffix}."
    return {"title": title, "venue": venue, "doi": doi, "year": parts[0], "section": "preprint" if kind == "Preprint" else "publication", "markdown": line, "sort_date": "-".join(str(p).zfill(2) for p in parts)}


def resolve(item):
    doi = item.get("doi", "").strip().removeprefix("https://doi.org/")
    if doi:
        return citation(get_json("https://api.crossref.org/works/" + quote(doi, safe=""))["message"], item["title"])
    params = urlencode({"query.title": item["title"], "query.author": "Kai He", "rows": 3})
    matches = get_json("https://api.crossref.org/works?" + params)["message"]["items"]
    for match in matches:
        try:
            result = citation(match, item["title"])
            _JSON_CACHE["https://api.crossref.org/works/" + quote(result["doi"], safe="")] = {"message": match}
            return result
        except ValueError:
            pass
    arxiv = re.search(r"arXiv[: ]+(\d{4}\.\d{4,5})", item.get("citation", ""), re.I)
    if arxiv:
        return arxiv_citation(arxiv.group(1), item["title"])
    raise ValueError("No exact-title verified record; left for later verification")


def arxiv_citation(identifier, expected_title):
    from bs4 import BeautifulSoup
    # The official abstract page exposes complete citation metadata, no PDF needed.
    soup = BeautifulSoup(get("https://arxiv.org/abs/" + identifier, "text/html"), "html.parser")
    values = lambda name: [tag.get("content", "") for tag in soup.select(f'meta[name="{name}"]')]
    titles, dates, names = values("citation_title"), values("citation_date"), values("citation_author")
    if not titles or key(titles[0]) != key(expected_title) or not dates or not names:
        raise ValueError("Incomplete or mismatched arXiv metadata")
    authors = []
    for name in names:
        if "," in name:
            family, given = name.split(",", 1)
        else:
            given, family = name.rsplit(" ", 1)
        authors.append({"given": given.strip(), "family": family.strip()})
    record = {"title": titles, "DOI": "10.48550/arXiv." + identifier,
              "author": authors, "type": "posted-content", "subtype": "preprint",
              "container-title": ["arXiv:" + identifier],
              "published": {"date-parts": [[int(p) for p in re.split(r"[-/]", dates[0])]]}}
    return citation(record, expected_title)


def with_scholar_date(candidate, item):
    if not item.get("detail"):
        return candidate
    now = datetime.now(timezone.utc)
    date = candidate["sort_date"]
    source_is_preprint = any(term in item.get("citation", "").lower() for term in ("arxiv", "biorxiv", "medrxiv", "techrxiv", "ssrn", "preprint"))
    if candidate["section"] == "publication" and source_is_preprint:
        return candidate
    if len(date) >= 7 and date[:7] <= now.strftime("%Y-%m"):
        return candidate
    from bs4 import BeautifulSoup
    try:
        soup = BeautifulSoup(get(item["detail"], "text/html"), "html.parser")
        fields = {}
        for row in soup.select(".gs_scl"):
            label, value = row.select_one(".gsc_oci_field"), row.select_one(".gsc_oci_value")
            if label and value:
                fields[label.get_text(strip=True)] = value.get_text(" ", strip=True)
        raw = fields.get("Publication date", "")
        if not re.fullmatch(r"\d{4}/\d{1,2}(/\d{1,2})?", raw):
            return candidate
        parts = [int(p) for p in raw.split("/")]
        actual = datetime(parts[0], parts[1], parts[2] if len(parts) > 2 else 1, tzinfo=timezone.utc)
        if actual > now:
            return candidate
        old_year = candidate["year"]
        candidate["year"] = parts[0]
        candidate["sort_date"] = "-".join(str(p).zfill(2) for p in parts)
        # Prefer the primary profile's online publication date to a future issue date.
        candidate["markdown"] = candidate["markdown"].replace(", " + str(old_year), ", " + str(parts[0]), 1)
        candidate["date_source"] = "Google Scholar publication date"
    except Exception as exc:
        print(f"::warning::Scholar publication date unavailable: {exc}", flush=True)
    return candidate


def line_key(line):
    import sync_publications as legacy
    return key(legacy.parse_title_from_markdown(line))


def parsed(text):
    import sync_publications as legacy
    return legacy.parse_existing_publications(text)


def baseline(text, overrides):
    return {"citations": {k: e.markdown for k, e in parsed(text).items()},
            "overrides": copy.deepcopy(overrides)}


def apply_candidates(text, candidates, overrides, expected=None):
    import sync_publications as legacy
    for start, end in [(START, END), (legacy.NEWS_START, legacy.NEWS_END)]:
        if text.count(start) != 1 or text.count(end) != 1:
            raise ValueError("Missing or duplicated bounded region")
    data = copy.deepcopy(overrides)
    normalize = legacy.normalize_title
    aliases = {}
    for entry in data.get("entries", []):
        canonical = normalize(entry["title"])
        for alias in entry.get("aliases", []) + [legacy.parse_title_from_markdown(entry["markdown"])]:
            aliases[normalize(alias)] = canonical
    canonical = lambda title: aliases.get(normalize(title), normalize(title))
    suppressed = {canonical(t) for t in data.get("suppressed_titles", [])}
    existing = parsed(text)
    merged = {aliases.get(k, k): e for k, e in existing.items()}
    curated = {canonical(e["title"]): e for e in data.get("entries", [])}
    for k, entry in curated.items():
        if k in merged:
            if entry.get("year") == merged[k].year:
                merged[k].sort_date = entry.get("sort_date", "")
            merged[k].news = entry.get("news", "")
    expected_entries = {canonical(e["title"]): e for e in (expected or {}).get("overrides", {}).get("entries", [])}
    expected_citations = {aliases.get(k, k): v for k, v in (expected or {}).get("citations", {}).items()}
    changes, conflicts = [], []
    # The first primary-source record wins at equal publication status. A formal
    # publication always supersedes its preprint; never the reverse.
    choices = {}
    for candidate in candidates:
        k = canonical(candidate["title"])
        if k not in choices or (choices[k]["section"] == "preprint" and candidate["section"] == "publication"):
            choices[k] = candidate
    for k, candidate in choices.items():
        if k in suppressed:
            continue
        current = merged.get(k)
        saved = curated.get(k)
        identifier = candidate["doi"].lower()
        arxiv_id = identifier.split("10.48550/arxiv.", 1)[1] if identifier.startswith("10.48550/arxiv.") else ""
        same_ids = [old_key for old_key, old_entry in merged.items() if old_key != k and
                    ((curated.get(old_key, {}).get("doi", "").lower() == identifier) or
                     (arxiv_id and arxiv_id in old_entry.markdown))]
        if expected is not None and any(expected_citations.get(old_key) != merged[old_key].markdown or expected_entries.get(old_key) != curated.get(old_key) for old_key in same_ids):
            conflicts.append(candidate["title"])
            continue
        if expected is not None and (expected_citations.get(k) != (current.markdown if current else None) or expected_entries.get(k) != saved):
            conflicts.append(candidate["title"])
            continue
        promotion = bool(current and current.section == "preprint" and candidate["section"] == "publication")
        repair = bool(current and legacy.is_low_fidelity_entry(current))
        if current and not (promotion or repair):
            # Preserve hand-edited citations, but enrich their date for sorting.
            if current.year == candidate["year"] and current.section == candidate["section"]:
                # Persist sorting metadata without replacing the existing citation.
                item = copy.deepcopy(saved or {})
                item.update(title=(saved["title"] if saved else current.title), markdown=current.markdown, section=current.section,
                            year=current.year, sort_date=candidate["sort_date"])
                item.setdefault("doi", candidate["doi"])
                curated[k] = item
                current.sort_date = item["sort_date"]
            continue
        item = copy.deepcopy(saved or {})
        item.update({name: candidate[name] for name in ("title", "doi", "section", "year", "sort_date", "markdown")})
        item["metadata_source"] = candidate.get("metadata_source", "Crossref/arXiv")
        if saved and saved["title"] != item["title"]:
            item["aliases"] = list(dict.fromkeys(item.get("aliases", []) + [saved["title"]]))
        date = candidate["sort_date"][:7]
        if len(date) < 7 or date > datetime.now(timezone.utc).strftime("%Y-%m"):
            # Do not invent publication month; use the discovery month for News.
            date = datetime.now(timezone.utc).strftime("%Y-%m")
        title = html.escape(candidate["title"]).replace("{", "&#123;").replace("}", "&#125;")
        venue = html.escape(candidate["venue"])
        repository = venue.split(":")[0]
        article = "an" if repository[:1].lower() in "aeiou" else "a"
        action = f'is published in {venue}' if candidate["section"] == "publication" else f'is released as {article} {repository} preprint'
        item["news"] = f'- *{date.replace("-", ".")}*: &nbsp;🎉🎉 Our paper “{title}” {action}.'
        for old_key in same_ids:
            old_entry = merged.pop(old_key)
            removed = curated.pop(old_key, {})
            item["aliases"] = list(dict.fromkeys(item.get("aliases", []) + [old_entry.title] + removed.get("aliases", [])))
        curated[k] = item
        merged[k] = legacy.Entry(title=item["title"], markdown=item["markdown"], section=item["section"], year=item["year"], sort_date=item["sort_date"], news=item["news"])
        changes.append({"title": item["title"], "doi": item["doi"], "action": "promoted" if promotion else ("corrected" if repair else "added")})
    data["entries"] = list(curated.values())
    old_news = text.split(legacy.NEWS_START, 1)[1].split(legacy.NEWS_END, 1)[0]
    result = legacy.replace_region(text, START, END, legacy.render_publications(merged))
    result = legacy.replace_region(result, legacy.NEWS_START, legacy.NEWS_END, legacy.render_news(merged, existing=old_news))
    # Assert both edits stay inside the two authorized regions.
    scrub = lambda value: re.sub(re.escape(START) + r".*?" + re.escape(END), "PUBS", re.sub(re.escape(legacy.NEWS_START) + r".*?" + re.escape(legacy.NEWS_END), "NEWS", value, flags=re.S), flags=re.S)
    if scrub(text) != scrub(result):
        raise ValueError("Attempt to modify content outside News and Publications")
    return result, data, changes, conflicts


def collect(skip_scholar=False):
    sources, records, skipped, candidates = {}, [], [], []
    original = Path("_pages/about.md").read_text()
    overrides = json.loads(Path("data/publication_overrides.json").read_text())
    for name, fetch in [("Google Scholar", scholar_records), ("ORCID", orcid_records)]:
        try:
            if name == "Google Scholar" and skip_scholar:
                raise ValueError("Skipped in diagnostic mode")
            found = fetch()
            sources[name] = {"ok": True, "count": len(found)}
            records.extend(found)
        except Exception as exc:
            sources[name] = {"ok": False, "error": str(exc)}
            print(f"::warning::{name}: {exc}", flush=True)
    done = set()
    for item in records:
        identity = item.get("doi") or key(item["title"])
        if identity in done:
            continue
        done.add(identity)
        try:
            candidate = with_scholar_date(resolve(item), item)
            candidate["discovery_source"] = item["source"]
            candidates.append(candidate)
        except Exception as exc:
            skipped.append({"title": item["title"], "source": item["source"], "reason": str(exc)})
        time.sleep(0.2)
    if not any(s["ok"] and s["count"] for s in sources.values()):
        raise RuntimeError("No live publication source available; homepage left unchanged")
    return {"checked_at": datetime.now(timezone.utc).isoformat(), "sources": sources,
            "candidates": candidates, "skipped": skipped, "baseline": baseline(original, overrides)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--collect", type=Path, help="Save verified candidates without changing the repository")
    parser.add_argument("--apply", type=Path, help="Apply candidates to the latest checkout, preserving intervening edits")
    parser.add_argument("--report", default="/tmp/publication-sync-report.json")
    parser.add_argument("--skip-scholar", action="store_true", help="Diagnostic mode only")
    args = parser.parse_args()
    snapshot = json.loads(args.apply.read_text()) if args.apply else collect(args.skip_scholar)
    if args.collect:
        args.collect.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n")
        print(json.dumps({"sources": snapshot["sources"], "verified": len(snapshot["candidates"]), "deferred": len(snapshot["skipped"])}, ensure_ascii=False), flush=True)
        return 0
    age = datetime.now(timezone.utc) - datetime.fromisoformat(snapshot["checked_at"])
    if age.total_seconds() > 6 * 3600:
        raise ValueError("Candidate snapshot is stale; collect fresh sources")
    about, state = Path("_pages/about.md"), Path("data/publication_overrides.json")
    original = about.read_text()
    original_state = state.read_text()
    updated, data, changes, conflicts = apply_candidates(original, snapshot["candidates"], json.loads(original_state), snapshot["baseline"])
    report = {k: snapshot[k] for k in ("checked_at", "sources", "skipped")}
    report.update(changes=changes, concurrent_edits_skipped=conflicts)
    Path(args.report).write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, ensure_ascii=False, indent=2), flush=True)
    if args.write:
        # Check again before writing in case another local writer changed the files.
        if about.read_text() != original or state.read_text() != original_state:
            raise RuntimeError("Files changed during update; retry from the latest revision")
        state.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
        about.write_text(updated)
        Path("data/publication_sync_status.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a") as out:
            out.write("## Publication sync\n\n")
            for name, source in snapshot["sources"].items():
                out.write(f"- {name}: " + (f"{source['count']} records" if source["ok"] else f"unavailable — {source['error']}") + "\n")
            out.write(f"\n{len(changes)} changes; {len(snapshot['skipped'])} metadata deferrals; {len(conflicts)} intervening edits preserved.\n")
            for change in changes:
                out.write(f"- {change['action']}: {change['title']} — https://doi.org/{change['doi']}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
