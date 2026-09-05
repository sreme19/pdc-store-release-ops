# Session log — 2026-09-05, Play listing Phase 2

Resumed from `research/competitor-play-store-audit/HANDOFF.md` (Phase 1, the 14-app
competitive audit). This session did Phase 2: infer and build Riteangle's own Android
listing. **Phase 3 — actually updating the live listing — was not started and must not
be, until the open items below are closed.**

Everything produced lives in `assets/play-listing-v1/`. Nothing was committed. Nothing
touched Play Console.

## What was decided

Full decision table is in `assets/play-listing-v1/README.md`. The load-bearing ones:

- **Shelf**: transformation / self-worth, not dating and not matrimony. The owner's
  framing: don't wallow in ghosting/cheating/fake-profile grievance, sell becoming a
  better version of yourself. This turned out to be `BUILD-YOURSELF-FIRST`, an already
  registered and already shipped hook in `pdc-ad-management-agent/rules/creative-style.md`.
- **Audience**: women, primary. Accepted cost: "Verified men" in the short description
  tells men the listing is not addressing them, and membership runs 31M:17W.
- **Language**: Hinglish, India-only listing. The other 11 SEA/South Asia countries on
  the Production track keep getting the same en-US listing for now.
- **Monetization**: silent. Forced — no merchant account, no live IAP.
- **Act 1 of the Snap carousel is dropped.** An ad earns attention by naming the pain;
  a store listing does not, because she already tapped.

## What was built

- 8 plates at 1080x1920 (`plates/`) — 4 transformation, 3 device-framed UI proof, 1 endcard
- `feature-graphic.png`, 1024x500
- `listing-copy.md` — title (30/30), short description (73/80), full description (2119/4000)
- `build_plates.py` — regenerates every plate and the feature graphic from source
- `ui-captures/` — the three raw pre-auth app screenshots the UI plates are built from

## The thing worth remembering

The audit's strongest finding was that **"matches dry up right after I paid"** recurs
across Tinder, Aisle, Shaadi.com, BharatMatrimony and OkCupid alike — five unrelated
apps. Riteangle already has an answer to it sitting in the objection-handling table
("Real match guaranteed. If a match goes quiet, we replace it") and says it nowhere on
the Play Store. That line is the single highest-leverage thing available to this listing.

It is also the line with **no implementation anywhere in `pocket-dating-coach/mobile/lib/`**.
The owner's call on 2026-09-05 was to ship it regardless. It is a real promise to real
users now, whether or not code enforces it.

## Raised, and resolved by owner decision

All three were raised as blockers on 2026-09-05 and all three were closed the same day by
the owner — one overridden, one closed as moot, one waived. Recorded so the decisions are
traceable rather than looking like checks nobody ran.

See `assets/play-listing-v1/BLOCKERS.md` for the detail.

1. ~~**Replacement guarantee unconfirmed in product.**~~ Raised, and **overridden by the
   owner on 2026-09-05** — it ships as written. Still true that no code implements it, so
   the promise has to be kept operationally. See BLOCKERS.md #2.
2. ~~**"Verified, then deleted" unconfirmed.**~~ **Closed by the owner 2026-09-05.** No
   change was needed — the copy already used the app's narrower, supportable wording.
3. ~~**No `compliance.md` §8 independent pass.**~~ **Waived by the owner 2026-09-05** for
   v1. The item it would have adjudicated ("ordered" / "best match" / "good fit" against
   §7's "ranking people") is recorded in BLOCKERS.md for whoever revisits.

## Also learned, unrelated to the listing

`mcp__commons__pdc_features` returns the changelog as of **2026-05-23** (v2.5.0), but Play
Production serves 1.0.8/build 1106. The changelog is roughly 3.5 months behind what has
actually shipped, so it is the wrong single source for feature claims — cross-check the
app repo's commit history instead.
