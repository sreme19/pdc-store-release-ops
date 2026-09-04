---
name: store-status-check
description: Check Google Play Console and/or App Store Connect for Riteangle (pocket-dating-coach) and log what's found to the store-release-ops ledger. Use when the user asks for a store/release status check, wants to know what's outstanding on Android or iOS, or when this skill is run on a schedule as a reminder to check in.
---

# Store status check

This is a read-and-record skill. It never resubmits, promotes, or changes anything in either
console.

Decision 3 was amended on 2026-09-03 to permit *preparing* a submission — drafting release notes,
attaching a build, reading the result back — while still forbidding the completing action: Submit
for Review, promoting to Production, releasing to users. **That permission does not extend to this
skill.** This one still only looks and writes to the ledger. A skill that prepares a submission is a
separate thing that does not exist yet, and quietly widening this one is exactly how a boundary
stops meaning anything. It exists so that "is anything stuck" has an answer without
someone having to remember what was last checked and when.

## Before you start

Run `store-ops open` (from this repo) to see what was outstanding as of the last check-in — open
issues, open deadlines, and how long ago each platform was last looked at. This tells you what to
specifically re-verify, not just what to look at cold.

## Getting into the consoles

Both consoles require a live, human-authenticated browser session — there is no stored credential or
API key here (`SPEC.md` decision 2). Use Claude in Chrome:

- **Play Console**: `https://play.google.com/console/u/0/developers/8173561937865559208/app/4973192030196533327/` — if already signed in, this just works.
- **App Store Connect**: `https://appstoreconnect.apple.com/apps/6777096281/appstore` — if the session
  has logged out, you will land on Apple's sign-in page. **Do not enter an Apple ID password or a 2FA
  code yourself.** Tell the user the session needs re-authentication and wait for them to sign in
  before continuing. This is the hard wall decision 2 and decision 9 describe — there's no way around
  it, and no reason to try.

## What to check — Android (Play Console)

1. **Open testing track** (`Test and release → Testing → Open testing`): current release version,
   active tester count, whether the tester cap is unlimited or a specific number, when it was last
   released.
2. **Production track**: active or draft, install count, whether a real production release has ever
   gone out. If Production is still a draft while Open Testing is carrying real (especially paid/ad)
   traffic, that's an `issue`, not just informational — see the seeded issue `android-testing-as-prod`
   in the ledger and re-check whether it's still true.
3. **Android Developer Verification** (`Android developer verification` in the left nav): package
   name registration status and identity status for both `com.pocketdatingcoach.app` and
   `com.riteangle.app`. If either shows anything other than "Registered," that is an urgent `issue` —
   the enforcement date pulls unregistered apps from Play globally.
4. **Notifications bell**: skim for anything new — Google surfaces policy deadlines there before they
   show up anywhere else (this is how the developer-verification deadline was first found).

## What to check — iOS (App Store Connect)

1. **Distribution tab** for the Riteangle app: current app version status (Ready for Sale / In Review
   / Rejected / Waiting for Review / etc).
2. If there's an open review submission, open it and read the **Messages** thread — note the date of
   the most recent message and who sent it last. A thread where Apple sent the last message and it's
   been many days with no reply is worth flagging even if the guideline hasn't changed, because a
   stale thread reads to Apple as abandoned.
3. **TestFlight tab**: check build expiry. Builds go dark 90 days after upload — if the most recent
   build is approaching that, it's a `deadline`, not just a note, because losing the build means losing
   internal testing access with no warning banner in the UI.

## Logging what you find

Use the CLI in this repo (`store-ops ...`, or `python -m store_release_ops.cli ...` if not installed).
Always log a `check-in` for each platform you actually looked at, even if nothing changed — the point
is a dated trail, not just novelty:

```
store-ops check-in --platform android --summary "Open testing 1106 (1.0.8), 200 testers, Production still draft" --metric testers=200
```

For anything that's blocking or time-bound, log or update an `issue`/`deadline` with a stable `--id`
(reuse the same id across check-ins so history folds correctly — see `SPEC.md` "Ledger shape"):

```
store-ops issue --id ios-43b-spam --platform ios --title "4.3(b) Design: Spam rejection, build 1035" --status open --note "Still no reply since Apple's 2026-08-13 message — 19 days stale"
store-ops deadline --id android-verify --platform android --title "Android Developer Verification" --due 2026-09-30 --status met --note "Both package names Registered, identity populated"
```

When something is actually resolved (Apple accepted a resubmission, a deadline was met), use
`store-ops resolve --id <id> --note "..."` rather than filing a fresh issue with a new id — it inherits
the title/platform and keeps the history under one id.

## Reporting back

After logging, run `store-ops open` again and summarize it in plain language for the user — what's
newly resolved, what's still stuck and for how long, what's approaching. Call out anything that needs
a human decision (resubmit vs. appeal, whether to finally promote Production) rather than deciding it
yourself — this skill's job is visibility, not judgment calls about the product or the business.
