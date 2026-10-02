# Weekly publication updates

The existing `Sync Publications` workflow runs every Monday at 08:00 Asia/Singapore (00:00 UTC), using GitHub-hosted runners. GitHub may queue scheduled runs. No local computer, ChatGPT session, personal token, or paid API is required. Pushes changing the implementation also exercise the workflow.

Google Scholar `4nWk-HYAAAAJ` is the primary discovery source; public ORCID `0000-0003-2639-1532` supplements it. Crossref and official arXiv metadata verify title, authors, venue, date, and publication status. Blocked sources are reported and the other source is still attempted. Uncertain metadata is deferred, never fabricated. Both sources being unavailable fails without modifying the homepage.

New papers use the existing citation style, with Kai He in bold italics. Formal publications are grouped by year, preprints have their own section, and known publication dates sort newest first. A verified formal publication supersedes the matching preprint. New entries and promotions generate a news item in the existing style. News retains the latest five items, including announcements created by other tools. Publication is not described as acceptance unless acceptance is actually verified. No acceptance dates, corresponding-author marks, or congratulations are invented.

## Coordination with other tools

- `_pages/about.md` is edited only within `AUTO_NEWS_*` and `AUTO_PUBLICATIONS_*`. All other sections and site layout are preserved.
- `data/publication_overrides.json` stores the compatible authoritative records, aliases, exclusions, sort dates, and news. New verified state is written there in the same commit as the page. Existing `scripts/sync_publications.py` consumers therefore cannot restore a superseded preprint.
- Writers should use the same data file and preserve entries they do not own. For intentional removal, add a title to `suppressed_titles` rather than merely deleting a rendered line.
- The workflow keeps the existing `sync-publications` concurrency group. Other GitHub Actions that modify the same regions should use that group too; it does not lock external tools.
- Data collection and publication are separate. Before writing, the publisher reads the latest branch revision and reapplies verified additions. Intervening edits to the same paper are skipped. A concurrent remote commit rejects a normal push, prompting up to three recomputations. Force pushes and automatic conflict-resolution overrides are never used.
- No script can prevent an unrelated writer that intentionally force-pushes or later replaces the whole page from undoing changes. Such writers need the same ownership/version-check agreement. Time separation alone is insufficient.
- The two existing citation-statistics workflows write `google-scholar-stats`; this workflow leaves that branch alone. Their legacy dependency problem is separate from this publication pipeline.

`data/publication_sync_status.json` records source availability, changes and deferrals after each successful fetch. Its weekly commit records liveness even when there are no new papers, preventing routine repository inactivity. Run artifacts and the Actions summary provide diagnostics. GitHub's existing failure notification settings apply; this does not send separate mail or chat messages.

The publisher builds the site before committing, then explicitly requests a Pages build and checks that the committed revision is built. This matters because a `GITHUB_TOKEN` push alone does not necessarily trigger a Pages build.
