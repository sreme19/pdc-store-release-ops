"""Append-only JSONL ledger for store-release-ops.

Three record kinds — check-in, deadline, issue — all appended to the same file. Folding
(latest-line-per-id) happens at read time in `fold()`, never by mutating a written line.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from pathlib import Path

DEFAULT_LEDGER_PATH = Path(__file__).resolve().parent.parent.parent / "ledger" / "records.jsonl"

VALID_PLATFORMS = {"android", "ios", "both"}
VALID_ISSUE_STATUSES = {"open", "resolved"}
VALID_DEADLINE_STATUSES = {"open", "met", "missed"}


class LedgerError(ValueError):
    pass


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _check_platform(platform: str) -> str:
    if platform not in VALID_PLATFORMS:
        raise LedgerError(f"platform must be one of {sorted(VALID_PLATFORMS)}, got {platform!r}")
    return platform


@dataclass
class Ledger:
    path: Path = field(default_factory=lambda: DEFAULT_LEDGER_PATH)

    def _append(self, record: dict) -> dict:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, sort_keys=True) + "\n")
        return record

    def read_all(self) -> list[dict]:
        if not self.path.exists():
            return []
        records = []
        with self.path.open(encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    records.append(json.loads(line))
        return records

    # -- writers -----------------------------------------------------------------

    def check_in(
        self,
        platform: str,
        summary: str,
        note: str = "",
        metrics: dict | None = None,
    ) -> dict:
        _check_platform(platform)
        record = {
            "kind": "check-in",
            "platform": platform,
            "ts": _now_iso(),
            "summary": summary,
            "note": note,
            "metrics": metrics or {},
        }
        return self._append(record)

    def deadline(
        self,
        id: str,
        platform: str,
        title: str,
        due: str,
        status: str = "open",
        note: str = "",
    ) -> dict:
        _check_platform(platform)
        if status not in VALID_DEADLINE_STATUSES:
            raise LedgerError(f"status must be one of {sorted(VALID_DEADLINE_STATUSES)}")
        try:
            date.fromisoformat(due)
        except ValueError as e:
            raise LedgerError(f"due must be YYYY-MM-DD, got {due!r}") from e
        record = {
            "kind": "deadline",
            "id": id,
            "platform": platform,
            "ts": _now_iso(),
            "title": title,
            "due": due,
            "status": status,
            "note": note,
        }
        return self._append(record)

    def issue(
        self,
        id: str,
        platform: str,
        title: str,
        status: str = "open",
        note: str = "",
    ) -> dict:
        _check_platform(platform)
        if status not in VALID_ISSUE_STATUSES:
            raise LedgerError(f"status must be one of {sorted(VALID_ISSUE_STATUSES)}")
        record = {
            "kind": "issue",
            "id": id,
            "platform": platform,
            "ts": _now_iso(),
            "title": title,
            "status": status,
            "note": note,
        }
        return self._append(record)

    def resolve(self, id: str, note: str = "") -> dict:
        """Append a resolved/met line for an existing issue or deadline id, inheriting title/platform."""
        latest = self.latest_by_id(id)
        if latest is None:
            raise LedgerError(f"no existing record with id {id!r} — use `issue`/`deadline` to create it")
        if latest["kind"] == "issue":
            return self.issue(id, latest["platform"], latest["title"], status="resolved", note=note)
        if latest["kind"] == "deadline":
            return self.deadline(
                id, latest["platform"], latest["title"], latest["due"], status="met", note=note
            )
        raise LedgerError(f"record {id!r} is a {latest['kind']}, not an issue or deadline")

    # -- readers -------------------------------------------------------------------

    def latest_by_id(self, id: str) -> dict | None:
        matches = [r for r in self.read_all() if r.get("id") == id]
        if not matches:
            return None
        return matches[-1]  # file order is append order — last match is the latest

    def fold(self) -> dict:
        """Latest line per id for issue/deadline records; all check-ins kept, newest last."""
        by_id: dict[str, dict] = {}
        check_ins: list[dict] = []
        for record in self.read_all():
            if record["kind"] == "check-in":
                check_ins.append(record)
            else:
                # File order is append order, i.e. already chronological — the last write for
                # a given id always wins, even if two writes land in the same wall-clock second.
                by_id[record["id"]] = record
        check_ins.sort(key=lambda r: r["ts"])
        return {"latest_by_id": by_id, "check_ins": check_ins}

    def open_items(self) -> dict:
        folded = self.fold()
        open_issues = [r for r in folded["latest_by_id"].values() if r["kind"] == "issue" and r["status"] == "open"]
        open_deadlines = [
            r for r in folded["latest_by_id"].values() if r["kind"] == "deadline" and r["status"] == "open"
        ]
        open_issues.sort(key=lambda r: r["ts"])
        open_deadlines.sort(key=lambda r: r["due"])
        last_check_in_by_platform: dict[str, dict] = {}
        for c in folded["check_ins"]:
            last_check_in_by_platform[c["platform"]] = c
        return {
            "open_issues": open_issues,
            "open_deadlines": open_deadlines,
            "last_check_in_by_platform": last_check_in_by_platform,
        }
