# store-release-ops — Spec

**Status: v1 scaffold.** Ledger CLI (`store-ops check-in` / `deadline` / `issue` / `resolve` /
`open` / `stats`) is built and seeded with the first real check-in (2026-09-01). One skill
(`store-status-check`) is built. Nothing here has run unattended yet.

## Problem framing

Riteangle (`pocket-dating-coach`) ships to Google Play and the Apple App Store. Both consoles need
periodic, non-obvious attention — pending review threads, testing-track age, tester counts, upcoming
platform deadlines (Android Developer Verification, TestFlight build expiry) — and until now nothing
tracked *when it was last checked* or *what was found*, so status went stale silently (the iOS 4.3(b)
rejection sat unanswered for 19 days before anyone re-looked). This repo is a loop-engineered,
harness-driven agent in the same spirit as `job-hunt-agent` and `ad-management-agent`: the checking and
judgment happen live in whatever Claude Code session runs the skill, and this repo only persists the
result through a deterministic CLI.

## Locked decisions

1. **No Anthropic API key, anywhere, ever, in this repo.** Same rule as `ad-management-agent`
   (`ad-management-agent/SPEC.md` decision 1) and `job-hunt-agent`. Every mode here is a skill; the CLI
   never imports or calls an Anthropic client.

2. **No console credentials stored, anywhere — stronger than "gitignored," genuinely absent.**
   `ad-management-agent` eventually took on live Snap/Meta API credentials in a gitignored
   `config.local.yaml`, with real safety rails, because those APIs support long-lived scoped tokens.
   Google Play Console and App Store Connect don't offer an equivalent this repo should hold: Play's
   API needs a service-account key with real publish/edit scope (too much blast radius for a status
   read), and App Store Connect logins go through Apple ID + 2FA, which cannot be scripted or stored at
   all. So this repo reads both consoles through a live, human-authenticated browser session (Claude in
   Chrome, driven from a Claude Code session) — never an API key, never a saved session token. **The
   loop always needs a human at the keyboard to (re)authenticate.** That is a real limitation, not an
   oversight: don't try to route around it later without the app owner explicitly signing off, the same
   way `ad-management-agent` decision 3's live-account boundary was only ever loosened by the app owner
   in as many words.

3. **Read and record; prepare but never complete.** **Amended by the app owner on 2026-09-03**, in
   the form this decision itself asked for: explicitly, with the cost stated, and on the
   `ad-management-agent` precedent this decision named. The original rule was *read and record, never
   act* — the tracker, not the trigger.

   **What is now allowed.** Navigating both consoles, drafting release notes, attaching a build,
   preparing a submission, and reading the result back to diff it against what was intended. The
   shape is Snap and Meta's: create the object, leave the activation to a person.

   **What is still never allowed.** Pressing *Submit for Review*. Promoting Open Testing → Production.
   Releasing to users. Changing a rollout percentage or a tester list. Those are human actions, every
   time, in the same way that starting ad spend in Ads Manager is.

   **Unchanged.** Never enter an Apple ID password or a 2FA code — decisions 2 and 9, and a hard wall
   rather than a preference. Cutting builds, signing and version bumps stay in
   `pocket-dating-coach/mobile` per decision 4; nothing about release engineering moved here.

   **Be clear about what this cost.** The old rule was true *by construction*: this repo had no
   credentials and no way to touch a console, so "never acts" needed no enforcement. It now has a hand
   on the controls, and what replaces construction is a named list of forbidden actions — which is
   weaker, because a list is only as good as the skill that reads it and a console UI can move a button
   under it. The trade was made because release work was being routed here anyway, and a boundary
   people work around is worse than one that is written down honestly.

   **Not yet built.** No skill implements co-driving. `store-status-check` remains read-and-record;
   this decision records permission, not a capability. When a submission skill is written it must cite
   this amendment, and the forbidden list above belongs in the skill file verbatim rather than by
   reference — a rule one link away from the person following it is a rule that gets skipped.

   **The other half of the amendment.** `pocket-dating-coach` now tells this repo when a release
   ships, through `store-ops check-in`. That is an append into this ledger through this repo's own
   CLI — see `portfolio-commons/CONVENTIONS.md`, write path 1 — and it is the only way another repo
   writes here.

4. **Release engineering stays in `pocket-dating-coach`.** Keystores, signing config, CI release
   workflows, version bumps — all product-repo concerns that need direct repo access. This repo never
   duplicates them. See `pocket-dating-coach`'s own memory: [[reference_pdc_android_play_release]],
   [[reference_pdc_ios_testflight]]. What lives here instead is *status* — is a release stuck, is a
   deadline approaching, is a track running longer than it should.

5. **The ledger is the durable record; every check-in closes or extends an open thread.** Modeled on
   `ad-management-agent`'s propose → log-setup → audit lifecycle (`ad-management-agent/SPEC.md`
   decision 4): a `deadline` or `issue` that's still open at the next check-in should say so explicitly
   (age since last seen), not silently vanish. `store-ops open` is the one command that should always
   answer "what needs attention right now" without anyone having to remember what was found last time.

6. **Two platforms, one ledger, explicit platform tagging.** Every record (`check-in`, `deadline`,
   `issue`) carries `--platform android|ios|both`. Cross-platform deadlines (e.g. an app-wide policy
   change) use `both`; console-specific findings use the specific platform. This is what lets `open`
   answer "what's outstanding on iOS" and "what's outstanding on Android" separately, since the two
   consoles fail in different ways (Play: track-age/tester-count/policy drift; ASC: review rejections/
   TestFlight build expiry).

7. **Tech stack: Python (`uv`/`hatchling`), matching `ad-management-agent` and `job-hunt-agent`.** Same
   conventions, one less thing to context-switch on.

8. **Repo is private.** Rejection reasoning, App Store review correspondence, and Play Console tester
   counts are business-sensitive, even though none of it is as sensitive as `ad-management-agent`'s
   budget/targeting data.

9. **Promotion to a scheduled task is a later, deliberate step — not attempted now.** `ad-audit` only
   became a candidate for a Claude Code scheduled task after `ad-setup-loop`/`ad-audit` had been run by
   hand enough times to trust the loop unattended (`ad-management-agent/SPEC.md` decision 2). Decision 2
   above makes the ceiling explicit here: this loop can be scheduled to *remind* a human to check in
   (a `schedule`d nudge), but the actual browser check cannot run unattended while Apple ID 2FA is a
   hard wall. Don't build a fully unattended cron for this without that constraint changing.

## Ledger shape

Three record kinds, all appended to `ledger/records.jsonl` (one JSON object per line — append-only,
diffable, mergeable across concurrent sessions without lock contention):

- **`check-in`** — a dated snapshot of what a console showed: platform, track/status, key numbers
  (tester count, install count, version), free-text note. Written every time a skill run actually looks
  at a console, whether or not anything changed.
- **`deadline`** — a dated external requirement (Android Developer Verification, a TestFlight build's
  90-day expiry, a Play policy change's enforcement date). Has a `due` date, a `status`
  (`open`/`met`/`missed`), and the evidence for that status.
- **`issue`** — an open blocker (an App Store rejection, a paused testing track, a policy warning). Has
  a `status` (`open`/`resolved`), and every reopen/re-check appends a new line rather than mutating the
  old one — the history of an issue is the sequence of lines that mention its `id`.

`store-ops open` folds this log into "what's outstanding right now," computing age from the most recent
line per id rather than trusting any single line to be current.

## First real check-in (2026-09-01, seeded into the ledger at scaffold time)

- **Android**: Open Testing live at 1106 (1.0.8), 200 active testers, unlimited cap, released Aug 12.
  Production still Draft/Inactive (2 of 5 setup steps done, never actually released). Android Developer
  Verification (deadline Sep 30, 2026) — both package names already `Registered`, identity populated →
  logged as a **met** deadline, not open.
- **iOS**: 1.0.5 (build 1035) still `Rejected`, Guideline 4.3(b) Design: Spam, submission
  `3a44802f-5ff0-4445-b8b1-b54111a45b41`. Last message from Apple 2026-08-13; no resubmission or further
  correspondence since — **19 days stale as of this check-in**. Logged as an open `issue`.
- **Flagged as its own open issue, not just a note**: Android Open Testing is carrying live ad traffic
  as its de facto production release (Production has never published). Google's own Play Console copy
  frames testing tracks as being for testing; running paid acquisition against one long-term is the
  kind of pattern that can get testing access throttled with no warning. Tracked so it surfaces every
  time `open` runs, not just once in a conversation.
