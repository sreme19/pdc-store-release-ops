import pytest

from store_release_ops.ledger import Ledger, LedgerError


@pytest.fixture
def ledger(tmp_path):
    return Ledger(path=tmp_path / "records.jsonl")


def test_check_in_roundtrip(ledger):
    ledger.check_in("android", "200 active testers", metrics={"testers": "200"})
    records = ledger.read_all()
    assert len(records) == 1
    assert records[0]["kind"] == "check-in"
    assert records[0]["metrics"]["testers"] == "200"


def test_invalid_platform_rejected(ledger):
    with pytest.raises(LedgerError):
        ledger.check_in("windows", "n/a")


def test_issue_lifecycle(ledger):
    ledger.issue("ios-43b", "ios", "4.3(b) spam rejection", status="open")
    open_items = ledger.open_items()
    assert len(open_items["open_issues"]) == 1

    ledger.resolve("ios-43b", note="Apple accepted the resubmission")
    open_items = ledger.open_items()
    assert len(open_items["open_issues"]) == 0


def test_resolve_unknown_id_raises(ledger):
    with pytest.raises(LedgerError):
        ledger.resolve("does-not-exist")


def test_deadline_folds_to_latest_status(ledger):
    ledger.deadline("android-verify", "android", "Android Developer Verification", due="2026-09-30")
    ledger.resolve("android-verify", note="Both package names registered")
    open_items = ledger.open_items()
    assert len(open_items["open_deadlines"]) == 0
    latest = ledger.latest_by_id("android-verify")
    assert latest["status"] == "met"


def test_fold_keeps_all_check_ins(ledger):
    ledger.check_in("android", "first")
    ledger.check_in("android", "second")
    folded = ledger.fold()
    assert len(folded["check_ins"]) == 2
