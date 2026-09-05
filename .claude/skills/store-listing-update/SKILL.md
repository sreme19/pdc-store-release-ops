---
name: store-listing-update
description: Build or revise Riteangle's Google Play / App Store listing assets — title, short and full description, phone screenshots, feature graphic. Use when the user wants to improve, refresh, localize or re-cut a store listing, or produce store screenshots. Prepares assets only; never publishes to a console.
---

# Store listing update

Prepares listing assets. **Never publishes them.** `SPEC.md` decision 3, as amended
2026-09-03, permits preparing a submission and forbids the completing action — so this
skill writes files into `assets/play-listing-<version>/` and stops. Uploading to Play
Console, saving a store listing, or submitting for review stays a human action.

First run: 2026-09-05, `assets/play-listing-v1/`. Read
`SESSION-2026-09-05-store-listing.md` before starting a v2 — the decisions there were
made with the owner and should be changed deliberately, not re-derived.

## Before you start

1. `store-ops open` — what is outstanding, and which track is actually live.
2. `research/competitor-play-store-audit/report.html` — read the **"Anatomy of an
   Attractive Play Store Listing"** and **"Recurring Weaknesses & Whitespace"** sections.
   Read the HTML, not the PDF: same content, it is the source the PDF renders from, and
   it costs a fraction of the tokens.
3. `pdc-ad-management-agent/rules/` — `creative-style.md` (voice, taglines, palette,
   registered hooks, quotable stats), `compliance.md` (hard gates), `creative-generation.md`
   (POV rule §1, negative list §4, safe zones §7).

## Hard rules, learned the hard way

**Never generate new imagery.** Every plate re-cuts a frame the ad account already
generated and QA'd. `creatives/*/sourcing.md` maps each shipped asset to its exact source
file — **read it before cropping.** It records which frames must be letterboxed rather
than cropped (a 2x2 contact grid is destroyed by a cover-crop; a group shot loses half
its subjects) and which frames were rejected and why. A frame rejected once for a
wardrobe fault or a POV problem is still rejected.

**Strip the Flow watermark through the shared helper**, `ad_management_agent.watermark.
strip_flow_watermark`, never a local copy. It is shared so this build and the ad repo's
push gate cannot drift on the crop amount.

**Watch the POV rule (§1) at crop time, not just at source time.** A source frame that
passes can produce a crop that fails: cover-cropping the hero grid pulled two blurred
background men into sharp foreground focus. Look at every plate after building it.

**Never claim what the product does not do.** Two lines were approved for the v1 listing
and neither could be found in `pocket-dating-coach/mobile/lib/` — the replacement
guarantee, and the deletion half of "verified, then deleted". Grep the product before
writing a claim, and mark anything unconfirmed `[GATED]` in the copy rather than quietly
shipping or quietly dropping it.

**A `compliance.md` §8 independent pass is required** and cannot be done by the session
that wrote the asset. Hand it off.

## Capturing app screenshots

The app is Flutter, at `pocket-dating-coach/mobile`, package `com.riteangle.app`.

**The data boundary comes first.** `mobile/lib/config.dart` says *"Always points at
production"* — there is no dev or staging target. So **anything behind the auth wall
shows real members' photos, names and messages**, and a store screenshot is published
worldwide and permanently. Do not publish post-auth captures without resolving this.

The demo account (`review@riteangle.com` / `123456`, hardcoded in `auth_screen.dart` and
on the public support page) does **not** resolve it on its own:
`supabase/functions/demo-login/index.ts` only mints a session for a real production user
row and seeds nothing. A seed system does exist — `is_seed = true` marks "fabricated demo
profiles shown when real pool is empty", and `scripts/seed-profiles.ts` bootstraps ~10
seed matches across 21 male + 22 female personas — but whether the demo account's own
shortlist resolves to seed rows or real members is **unverified as of 2026-09-05**.

**Use the pre-auth lane instead.** It renders the gate screen, the lane picker (with the
live "matched within NN:NN minutes" strip and the verification line) and the per-lane fit
sheet showing BEST MATCH / GOOD FIT / YOU WON'T SEE — real product, zero member data.
That was enough for all three UI slots in v1.

Recipe, verified working:

```bash
export PATH=~/Library/Android/sdk/platform-tools:~/Library/Android/sdk/emulator:$PATH
emulator -avd pdc -no-snapshot-load -no-boot-anim &
adb -s emulator-5554 shell wm size 1080x1920     # Play's phone screenshot spec
adb -s emulator-5554 shell wm density 420
adb -s emulator-5554 shell am force-stop com.riteangle.app   # REQUIRED after a resize
adb -s emulator-5554 shell am start -n com.riteangle.app/.MainActivity
adb -s emulator-5554 exec-out screencap -p > shot.png
adb -s emulator-5554 shell input tap <x> <y>     # coordinates are full-res
```

Restarting the app after `wm size` is not optional — Flutter renders a zero-width surface
otherwise and logcat says `FlutterRenderer: Width is zero`. `adb` is not on `PATH` by
default on this machine; the SDK is at `~/Library/Android/sdk`.

## Design defaults that came out of the audit

- **Hybrid screenshot order** — emotional plates first, real device-framed UI proof after.
  Seven of fourteen audited apps do this and it is the safest default. A listing with no
  product visible at all is Betterhalf's self-imposed transparency gap; do not repeat it.
- **One consistent colour field** across icon, feature graphic and every screenshot is the
  single most reliable "looks professional" signal. Riteangle's field is the **light** one
  — cream `#FFF3F0`, pink `#FF3B6B`, ink `#1B1020`, real Gabarito, lowercase wordmark. Every
  major rival ships dark; do not default to a dark background out of habit.
- **Bake a stat into plate 1.** It is the search-result thumbnail.
- **Stats are rates and medians, never totals**, and for a women-first listing they must be
  measured on women — the 12-minute signup-to-match median is measured on men.

## Copy mechanics

Play caps: **title 30, short description 80, full description 4000.** Play indexes the
short *and* full description for keywords, unlike Apple — so a keyword that will not fit
the title can live in the description and still rank. Front-load the first ~170 characters
of the full description; that is all that shows before "Read more".

Check every string's length with a script before proposing it. "Riteangle: Matchmaking,
Not Swiping" reads like it fits and is 35.

**Avoid anything Play can read as a ranking or performance keyword.** Play Console
validates the short description on save and warns "your app may not be promoted on Google
Play" for "keywords that indicate store performance or ranking". On 2026-09-05 the word
**"ordered"** (as in "an ordered shortlist") tripped it. The penalty is exclusion from
promotional surfaces, not a publishing block, and the warning only appears *after* you
save — so budget a save-check-fix pass rather than assuming the first save is final.

Note this is the same word `compliance.md` §7's "ranking people" line catches. When two
independent rule sets flag one word, replace the word rather than argue either.

## Output layout

```
assets/play-listing-<version>/
  README.md          decision table, arc, sourcing notes
  BLOCKERS.md        what stops this shipping, and what resolved
  listing-copy.md    title / short / full, with [GATED] blocks marked
  build_plates.py    regenerates every plate + the feature graphic
  plates/            1080x1920 phone screenshots
  ui-captures/       raw pre-auth app captures the UI plates are built from
  feature-graphic.png
```

Keep `ui-captures/` — re-capturing means re-booting an emulator and re-walking the flow.

## Verifying a listing actually shipped

**The console is the authority, not the public page.** Publishing overview is the answer:
"Last published on <date>" with the "Changes in review" section gone means it is live.

The public Play page is only a valid check **with locale params attached**, because Play
serves a localization based on the *viewer's* Google account country and language — not
on what you published. A localized listing looks like it never shipped when you view it
from the wrong account. The console's own "View on Play" link is a bare
`play.google.com/store/apps/details?id=<pkg>` with no `gl`/`hl`, so it lands on whatever
the viewer's locale resolves to, which for this account is the en-US default.

```
https://play.google.com/store/apps/details?id=com.riteangle.app&gl=IN&hl=en_IN
```

Play country follows the account's Play/payment country, so a VPN does not change it.
This cost real confusion on 2026-09-05: the en-IN listing was already live and looked
unshipped.

**Review can be much faster than advertised.** The dialog warns up to 7 days; the en-IN
listing was approved and auto-rolled-out the same session it was submitted, and the
1106/1.0.8 production release cleared in about 14 hours. With managed publishing off
there is no second gate, so submitting is the last decision point.

## Measuring whether a listing change worked

Where the numbers live, as of 2026-09-05: **Grow users → overview** carries the funnel
(device impressions / acquisitions / first opens / MAD / retention) and a **Store
listings** card showing the conversion rate. The old **Store performance → Store
analysis** page is now an empty redirect stub that points back at those two.

Mind two traps. The conversion rate on that card defaults to **last 90 days** while the
funnel tiles default to **last 28 days** — they are different windows and must not be
divided against each other. And the card reads "Default listing", so once a localization
exists that figure stops describing the localized market.

**Do not present a before/after as a result at this app's volume.** ~139 acquisitions per
28 days means week-to-week noise is larger than any plausible listing effect, and the
window is already confounded (Production went live 2026-09-02, three days before the
listing change). The right instrument is a **Play store listing experiment** — a real
holdback — and none has ever been run here. Capture baselines and label them directional;
say plainly that the effect is not measurable yet rather than dressing a number up.

## What does not go in the ledger

`ledger/records.jsonl` holds console *status* — check-ins, deadlines, issues. Listing
creative is not console status and does not belong there, the same way the competitive
audit did not. If a listing change is eventually submitted, *that* is a check-in.
