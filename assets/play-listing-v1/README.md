# Play listing v1 — Android, India

**Status: all 8 plates built.** Nothing committed, nothing submitted to Play Console.

Phase 2 of the store-listing project. Phase 1 is the competitive audit in
`research/competitor-play-store-audit/`; its "Anatomy of an Attractive Play Store
Listing" and "Recurring Weaknesses & Whitespace" sections are the input here.

Build: `/Users/performek5/Desktop/Code/pdc-ad-management-agent/.venv/bin/python build_plates.py`

## Decisions, as settled with the owner on 2026-09-05

| # | Decision | Value |
|---|---|---|
| A1 | Shelf | Transformation / self-worth — **not** dating, **not** matrimony. `BUILD-YOURSELF-FIRST`. |
| A2 | Audience | **Women**, primary |
| A3 | Contrast | Named contrast allowed — "No swipes. Ever." |
| B4 | Title (30 cap) | **Revised 2026-09-05:** `riteangle: Pehle Tum, Phir Koi` (30/30). Was `riteangle: Matched, Not Swiped`. Trades the last title keyword for the Hinglish/empowerment framing. **Not yet applied in the console** — see listing-copy.md |
| B5 | Short description (80 cap) | `Matchmaking, not swiping. Verified men, an ordered shortlist — you first.` (73) |
| B6 | Emoji | Light, deliberate — Aisle/Bumble middle, not Tinder density |
| B7 | Language | **Hinglish**, India-only listing |
| B8 | Stats | First-party, women-centric only |
| C12 | Device chrome | Hybrid — borderless full-bleed for transformation plates, real device frames for the UI plates |
| C13 | Stat on plate 1 | Yes — it is the search-result thumbnail |
| C14 | Icon / feature graphic | Keep the icon (recognition, live ad traffic); rework the feature graphic to the cream field |
| D16 | Monetization | **Silent** — forced: no merchant account, no live IAP. Revisit when one exists. |
| D17 | Replacement guarantee | **In** — subject to BLOCKERS.md #2 |
| E18 | Localization | India only for now |
| E19 | Submission | Text + graphics together |

## Feature graphic

`feature-graphic.png`, 1024x500 — the Play spec. Cream panel left, the group shot
right, lowercase wordmark, "Pehle tum. Phir koi aur." The icon is **kept as-is**
(recognition matters more than consistency while live ad traffic is running); the
feature graphic is what moves onto the cream field, which is the cheap half of the
audit's "one consistent colour field" finding.

Nothing load-bearing sits in the centre: Play overlays a centred play button on the
feature graphic whenever a promo video exists. There is no promo video today, and
the layout does not assume there never will be.

## The arc

Act 1 of the shipped Snap carousel — ghosted / catfished / "kab tak" / "bas ab
nahin" — is **dropped**. An ad earns attention by naming the pain; a store listing
does not, because she already tapped. Owner's direction: sell the transformation,
not the grievance.

| Slot | Plate | Copy |
|---|---|---|
| 01 | `01-hero` | "Khud ko **bana** sakti ho." + stat strap |
| 02 | `02-strength` | "Pehle apni **taakat**." |
| 03 | `03-career` | "Pehle apna **career**." |
| 04 | `04-calm` | "Pehle apna **sukoon**." |
| 05 | `05-verified` | "Har koi **ID-verified**." |
| 06 | `06-minutes` | "**Minutes** mein. Months nahi." |
| 07 | `07-fit` | "**Fit** se match. Swipe se nahi." |
| 08 | `08-endcard` | "Pehle **tum**. Phir koi aur." + wordmark + "No swipes. Ever." |

## Why cream, not the carousel's dark footer

The audit's single most reliable "looks professional" signal is one consistent
colour field across the icon and every screenshot. riteangle's field is the light
one, and `creative-style.md` is explicit that this is deliberate: *"every major
rival ships a dark UI; in a feed of dark dating creative, cream reads as the
differentiator before a single word."* The same logic holds on a store shelf.

## Sourcing

No new generation. Every plate re-cuts a Flow frame from
`pdc-ad-management-agent/creatives/buildyourself-lead-w1830/_source/frames/`,
already QA'd once for the shipped video and carousel. Flow's "made with AI" sparkle
is stripped through the ad repo's shared `strip_flow_watermark`, so this build and
that repo's push gate cannot drift. Type is real Gabarito.

Two frames are handled specially, both recorded in the ad repo's `sourcing.md`:
the 2x2 hero grid is **recomposed panel-by-panel** (cover-cropping destroys the
grid; letterboxing leaves it too small to read as a thumbnail), and the endcard
group shot is **letterboxed** (cover-cropping drops two of the four women).

The meeting-room frame was **not** used for `03-career`, deliberately — the
carousel already rejected it for a vest-top-in-a-boardroom wardrobe fault, and it
puts men in sharp focus against `creative-generation.md` §1's POV rule.
