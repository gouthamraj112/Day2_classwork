import json
import tempfile
from pathlib import Path

from telecom_cli.fraud import is_suspicious
from telecom_cli.io_utils import load_cdrs, load_subscribers
from telecom_cli.models import CDR, Subscriber
from telecom_cli.parsing import parse_cdr_line, parse_legacy_line
from telecom_cli.rating import compute_cost
from telecom_cli.reporting import build_report


def test_compute_cost_uses_rate_table():
    assert compute_cost("domestic", 180) == 4.5
    assert compute_cost("international", 600) == 120.0


def test_is_suspicious_flags_zero_cost_and_high_international_duration():
    cdr = CDR(msisdn="999", call_type="domestic", duration_sec=60, cost=0.0)
    assert is_suspicious(cdr, 3600) is True

    intl_cdr = CDR(msisdn="999", call_type="international", duration_sec=3601, cost=720.2)
    assert is_suspicious(intl_cdr, 3600) is True


def test_load_subscribers_builds_subscriber_objects(tmp_path):
    data_path = tmp_path / "subscribers.json"
    data_path.write_text(json.dumps([
        {"msisdn": "111", "plan_type": "basic"},
        {"msisdn": "222", "plan_type": "premium"},
    ]), encoding="utf-8")

    subscribers = load_subscribers(str(data_path))

    assert "111" in subscribers
    assert isinstance(subscribers["111"], Subscriber)
    assert subscribers["111"].plan_type == "basic"


def test_load_cdrs_skips_malformed_rows_and_returns_metrics(tmp_path):
    data_path = tmp_path / "cdrs.csv"
    data_path.write_text(
        "msisdn,call_type,duration_sec\n"
        "111,domestic,120\n"
        "222,roaming,abc\n"
        "333,international,180\n"
        "444,unknown,60\n",
        encoding="utf-8",
    )

    cdrs, malformed_count = load_cdrs(str(data_path))

    assert len(cdrs) == 2
    assert malformed_count == 2


def test_parse_cdr_line_and_legacy_line():
    assert parse_cdr_line({"msisdn": "111", "call_type": "domestic", "duration_sec": "120"}) == {
        "msisdn": "111",
        "call_type": "domestic",
        "duration_sec": 120,
    }
    assert parse_legacy_line("9876543210|international|600") == {
        "msisdn": "9876543210",
        "call_type": "international",
        "duration_sec": "600",
    }


def test_build_report_groups_totals_and_unknown_subscribers():
    subscribers = {
        "111": Subscriber("111", "basic"),
        "222": Subscriber("222", "premium"),
    }
    cdrs = [
        CDR("111", "domestic", 180, 4.5),
        CDR("333", "international", 600, 120.0),
    ]

    report = build_report(subscribers, cdrs, malformed_rows=0, suspicious_calls=1, unknown_subscribers={"333"})

    assert report["summary"]["total_calls"] == 2
    assert report["summary"]["total_cost"] == 124.5
    assert report["subscribers"]["111"]["call_count"] == 1
    assert report["subscribers"]["111"]["total_cost"] == 4.5
    assert report["unknown_subscribers"] == ["333"]
