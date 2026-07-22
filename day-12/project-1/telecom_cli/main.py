"""CLI entry point for telecom billing processing."""

import argparse
import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set

from telecom_cli.config import DEFAULT_FRAUD_THRESHOLD_SEC
from telecom_cli.fraud import is_suspicious
from telecom_cli.io_utils import load_cdrs, load_subscribers, write_report
from telecom_cli.models import CDR, Subscriber
from telecom_cli.reporting import build_report


def _configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def _build_unknown_subscribers(cdrs: List[CDR], subscribers: Dict[str, Subscriber]) -> Set[str]:
    known = set(subscribers)
    return {cdr.msisdn for cdr in cdrs if cdr.msisdn not in known}


def main() -> int:
    parser = argparse.ArgumentParser(description="Process telecom CDR batch")
    parser.add_argument("--subscribers", required=True)
    parser.add_argument("--cdrs", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--fraud-threshold-sec", type=int, default=DEFAULT_FRAUD_THRESHOLD_SEC)
    args = parser.parse_args()

    _configure_logging()
    if __name__ == "__main__":
        print(f"Orbit Mobile CLI started on {datetime.now().date()}")
    logging.info("Starting telecom billing CLI")

    subscribers = load_subscribers(args.subscribers)
    cdrs, malformed_count = load_cdrs(args.cdrs)

    if malformed_count / max(len(cdrs) + malformed_count, 1) > 0.10:
        logging.critical("Too many malformed rows; aborting report generation")
        return 1

    suspicious_calls = 0
    for cdr in cdrs:
        if is_suspicious(cdr, args.fraud_threshold_sec):
            suspicious_calls += 1
            cdr.is_suspicious_flag = True

    unknown_subscribers = _build_unknown_subscribers(cdrs, subscribers)
    report = build_report(subscribers, cdrs, malformed_count, suspicious_calls, unknown_subscribers)
    write_report(report, args.output)

    logging.info("Report written to %s", args.output)
    print("\nDaily summary")
    print(json.dumps(report["summary"], indent=2))
    print("\nPer-subscriber totals:")
    for msisdn, subscriber_data in report["subscribers"].items():
        print(f"- {msisdn}: {subscriber_data['call_count']} calls, cost {subscriber_data['total_cost']:.2f}")
    if report["unknown_subscribers"]:
        print("\nUnknown subscribers:")
        for msisdn in report["unknown_subscribers"]:
            print(f"- {msisdn}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
