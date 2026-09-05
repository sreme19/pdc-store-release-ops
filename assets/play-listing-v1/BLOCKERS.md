# Blockers — Play listing v1 (Android, India)

Written 2026-09-05. Three items stop this set from shipping. None is a build problem.

## 1. ~~Slots 05/06/07 cannot be captured~~ — RESOLVED 2026-09-05, no login needed

The concern was real: `mobile/lib/config.dart` says **"Always points at production"** —
no dev or staging target exists, so a logged-in screenshot would show real members'
photos, names and messages, and a Play screenshot is published worldwide and
permanently.

The demo account (`review@riteangle.com` / `123456`, hardcoded in `auth_screen.dart`
and published on the app's own support page) does **not** solve that on its own:
`supabase/functions/demo-login/index.ts` only mints a session for a real user row in
the production database. It seeds nothing.

**It turned out not to be needed.** The app's PRE-AUTH lane renders three product
screens before any sign-in, and none of them contains a single member's data:

| Capture | Screen | Why it earns a slot |
|---|---|---|
| `ui-captures/05-gate.png` | "Two questions. Then we move." | "we ID-verify everyone, no exceptions" — verification as a gate, not a claim |
| `ui-captures/06-lane.png` | "Pick your lane." | live "matched within 09:52 minutes" + "We verify ID, photos, lifestyle & intent" |
| `ui-captures/07-fit.png` | Forever-Focused lane sheet | the matching logic itself: BEST MATCH / GOOD FIT / YOU WON'T SEE |

Capture method, reusable: `pdc` AVD, `adb shell wm size 1080x1920` +
`wm density 420` (restart the app afterwards or Flutter renders a zero-width
surface), launch `com.riteangle.app/.MainActivity`, then drive with `adb shell input tap`.

**Still worth knowing for later:** anything past the auth wall — the ranked
shortlist, AI Bestie, a real conversation — remains blocked on the same production-data
question. `is_seed` exists (`true` = "fabricated demo profiles shown when real pool is
empty", per `member-state.ts`) and `scripts/seed-profiles.ts` bootstraps ~10 seed
matches across 21 male + 22 female seed personas. Whether the demo account's own
shortlist resolves to those seed rows or to real members is **unverified** — it needs a
login and a look before any post-auth screen is published.

## 2. Two approved claims are not confirmed in the product

Both were approved for the listing this session. Neither could be found in the
shipped app, and Play's misleading-claims policy bites on both.

- **The replacement guarantee** ("if a match goes quiet, we replace it"). Source is
  the objection-handling table in `pdc-ad-management-agent/rules/creative-style.md`.
  A grep of `mobile/lib/*.dart` found no replacement, guarantee or goes-quiet logic.
  This is the single highest-leverage line available — it answers the one complaint
  the audit found across Tinder, Aisle, Shaadi.com, BharatMatrimony *and* OkCupid —
  and it must be a promise the product actually keeps before it goes on the store.
- **"Verified, then deleted."** A grep of `proof_upload_screen.dart`,
  `category_proof_screen.dart` and `verification_screen.dart` found no
  deletion language. Confirm the proof is genuinely deleted before claiming it.

## 3. The §8 independent QA pass has not been run

`compliance.md` §8 requires a second, independent pass (different model or fresh
session) on any finished asset. These plates have had one pass only — this one.

One item specifically for that pass: **§7's Don't list includes "ranking people,"**
and the hero strap reads "ordered by fit — not by who gamed the photo." The
phrasing is lifted from the approved objection-handling table and "ordered" was
chosen over "ranked" deliberately, but the call belongs to an independent reviewer,
not to the session that wrote the line.
