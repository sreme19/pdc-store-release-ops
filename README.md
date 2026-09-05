# store-release-ops

Tracks Google Play Console and App Store Connect status for Riteangle (`pocket-dating-coach`) — open
review rejections, testing-track age, tester counts, and platform deadlines (Android Developer
Verification, TestFlight build expiry). Zero API key, zero stored credentials — see `SPEC.md`.

This repo doesn't build, sign, or release anything. It's the tracker, not the trigger. Release
engineering (keystores, CI, version bumps) lives in `pocket-dating-coach/mobile`, as it always has.

## Setup

```bash
uv venv && uv pip install -e ".[dev]"
pytest tests/ -v
```

**If `store-ops` fails with `bad interpreter: .../Code/store-release-ops/.venv/bin/python3.14`,
the venv predates this repo being renamed to `pdc-store-release-ops`** — the console script's
shebang holds an absolute path and does not survive a directory rename. Rebuild it:

```bash
rm -rf .venv && uv venv && uv pip install -e ".[dev]"
```

This matters more than a normal dev-setup nit: `SPEC.md` decision 9 contemplates scheduling
this loop, and a scheduled run would have hit the broken shebang and failed. Found and fixed
2026-09-05, after working around it with `PYTHONPATH=src python3 -m store_release_ops.cli`.

## Usage

The `store-status-check` skill (`.claude/skills/store-status-check/`) does the actual console-reading,
using Claude in Chrome against a live, human-authenticated session — there's no way to automate past
Apple's 2FA, so this always needs a human at the keyboard to sign in when a session has expired.

Everything that skill finds gets logged through the CLI:

```bash
store-ops check-in --platform android --summary "..." [--metric key=value ...]
store-ops deadline --id <slug> --platform android|ios|both --title "..." --due YYYY-MM-DD [--status open|met|missed]
store-ops issue     --id <slug> --platform android|ios|both --title "..." [--status open|resolved]
store-ops resolve   --id <slug> [--note "..."]

store-ops open    # everything currently outstanding, with age
store-ops stats   # record counts
```

`ledger/records.jsonl` is the durable record — append-only, one JSON object per line, tracked in git
(no secrets in it, unlike `ad-management-agent`'s `config.local.yaml`).

## Why a separate repo

See `SPEC.md` "Problem framing" — same shape as `ad-management-agent` and `job-hunt-agent`: recurring
ops work that isn't product code, kept out of `pocket-dating-coach` so the product repo stays about the
product.
