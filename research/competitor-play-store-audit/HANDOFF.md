# Handoff — Riteangle Play Store listing project

**Written**: 2026-09-02, end of session. Reason for handoff: this Claude Code session is running low on
credit; the user is switching to a different Claude login to continue. This file is the resume point —
read it first in the next session, no other context needed.

## Where this fits

Three-phase project (user's own framing, stated at kickoff):
1. **Baseline research** — audit competitor Android Play Store listings. **Done, this session.**
2. **Infer Riteangle's own ideal store listing** from the baseline patterns. **Not started.**
3. **Develop creatives and update the live listing.** **Not started.**

## What was decided this session

- **Competitor list source**: reused the 24-app matrix from
  `../../../pdc-ad-management-agent/creatives/_competitor-reference/index.md` (originally built for
  Instagram organic research, not Play Store — user confirmed via AskUserQuestion that reusing it was
  fine for this purpose too).
- **Which competitors made the final cut**: 14 of the 24, trimmed to apps with an active Android Play
  Store presence relevant to India: Tinder, Bumble, Hinge, happn, OkCupid, Badoo, Coffee Meets Bagel
  (global mainstream), Aisle, QuackQuack, FRND (India-focused dating), Shaadi.com, BharatMatrimony,
  Betterhalf, Knot (India matrimony/marriage-intent). Dropped: Tantan, match.com, Seeking, SDM Dating,
  Ashley Madison, Sugar Book, Schmooze (no discoverable/appropriate Play Store presence), VLNCY
  (Bangalore-only, too small), Woo (see below), Plenty of Fish (deprioritized, not India-focused).
- **Woo could not be completed** — the India-founded "Woo" app (formerly U2opia Mobile,
  `com.u2opia.woo`) is not currently listed on Google Play India; it appears delisted or repositioned to
  a US 30+ market under a different name. No substitute was used. **Open decision for the user**: drop
  Woo from the competitive set going forward, or replace it with an active alternative — "you&me" and
  IndianCupid surfaced repeatedly as candidates during the search.
- **Output location**: this repo (`pdc-store-release-ops`), not `pdc-ad-management-agent`, since it feeds
  the store-listing update project tracked here. This research is **not** part of this repo's ledger
  (`ledger/records.jsonl`) — the ledger's three record kinds (check-in/deadline/issue) are for Riteangle's
  own Play Console / App Store Connect status, not competitive research, so nothing here touches it.

## Deliverables (all under this folder)

- **`Riteangle-Competitive-Play-Store-Audit.pdf`** — the 38-page report sent to the user. Sections:
  executive summary, comparison table, "Anatomy of an Attractive Play Store Listing" (title/subtitle,
  icon/screenshot visual systems, description structure/tone, trust signaling, monetization transparency
  spectrum), "Recurring Weaknesses & Whitespace," then one profile per app (metadata, icon + 5
  screenshots, description analysis, ASO tactics), then the Woo note.
- **`report.html`** — the report source (edit this, not the PDF, to make changes).
- **`build_report.py`** — regenerates `report.html` from a Python `APPS` list (one dict per app: metadata,
  description summary, screenshot captions, ASO bullet list). Edit the data in this file, rerun it, then
  re-render to PDF with:
  ```
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu \
    --no-pdf-header-footer --print-to-pdf="Riteangle-Competitive-Play-Store-Audit.pdf" \
    "file://$(pwd)/report.html"
  ```
  (No PDF library was installed for this — weasyprint/reportlab/PIL are not present in the environment;
  headless Chrome print-to-pdf was used instead since Chrome was already installed. `sips` was used for
  image format/resize conversions.)
- **`screenshots/<slug>/`** — full-resolution PNGs (icon + up to 5 screenshots) per app, downloaded
  directly from the Play Store CDN. These are the ones to pull from for future creative reference. Per
  the same "NOT SHIPPABLE" rule the `ad-management-agent` competitor-reference folder uses: reference for
  a brief, never reuse/trace directly into Riteangle's own assets.
- **`report-images/<slug>/`** — smaller, JPEG-compressed copies of the same images, used only to keep the
  PDF file size down (~2.9MB instead of tens of MB). Don't use these for actual creative work — go to
  `screenshots/` for full resolution.
- **`raw-notes/<slug>.md`** — the detailed per-app research notes (verbatim-adjacent description
  breakdowns, full screenshot-by-screenshot descriptions, sampled review complaints) that `build_report.py`
  was distilled from. More granular than the PDF profiles — check here first if the PDF's summary isn't
  detailed enough for something.
- `woo.md` — the dead-end search trail for Woo (see above), kept so it isn't re-researched from scratch.

## How the research was actually done (for context, not required reading)

Used the in-session Browser tool (`mcp__Claude_Browser__*`) directly against public Play Store listing
pages (`play.google.com/store/apps/details?id=...&gl=IN&hl=en`) — read-only, no login. Parallelized
across 5 background `general-purpose` agents (each given its own browser tab via `tabs_create` to avoid
clobbering a shared tab), 2-3 apps per agent, each agent downloading images via `curl` and writing its own
`raw-notes/<slug>.md`. This pattern (many-tab parallel Play Store scraping) is reusable if a similar
audit is needed again (e.g. re-running this for iOS App Store listings, or refreshing this same set of
Android listings after a few months).

## Next step when resuming

Phase 2 — infer what Riteangle's own Play Store listing should say and show, using the "Anatomy of an
Attractive Listing" section and the "Recurring Weaknesses & Whitespace" section (especially the
cross-category "matches dry up after paying" complaint pattern) as the input. Do not start Phase 3
(creative production / actually updating the live listing) until Phase 2 has been reviewed with the user
— this was the user's own stated sequencing, not an assumption.
