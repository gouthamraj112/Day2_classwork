"""Reporting helpers for summary generation."""

import json
from typing import Dict, List, Set

from telecom_cli.models import CDR, Subscriber


def build_report(
    subscribers: Dict[str, Subscriber],
    cdrs: List[CDR],
    malformed_rows: int,
    suspicious_calls: int,
    unknown_subscribers: Set[str],
) -> dict:
    report = {
        "summary": {
            "total_calls": len(cdrs),
            "total_cost": round(sum(cdr.cost for cdr in cdrs), 2),
            "malformed_rows": malformed_rows,
            "suspicious_calls": suspicious_calls,
        },
        "subscribers": {},
        "unknown_subscribers": sorted(unknown_subscribers),
    }

    for msisdn, subscriber in subscribers.items():
        subscriber.calls = [cdr for cdr in cdrs if cdr.msisdn == msisdn]
        report["subscribers"][msisdn] = {
            "plan_type": subscriber.plan_type,
            "call_count": len(subscriber.calls),
            "total_cost": round(subscriber.total_cost(), 2),
        }

    return report
