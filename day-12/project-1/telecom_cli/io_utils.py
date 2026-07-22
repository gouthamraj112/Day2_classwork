"""File loading and report writing helpers."""

import csv
import json
import logging
from pathlib import Path
from typing import Dict, List, Tuple

from telecom_cli.models import CDR, Subscriber
from telecom_cli.parsing import parse_cdr_line
from telecom_cli.rating import compute_cost


logger = logging.getLogger(__name__)


def load_subscribers(json_path: str) -> Dict[str, Subscriber]:
    with open(json_path, "r", encoding="utf-8") as handle:
        payload = json.load(handle)

    subscribers = {}
    for item in payload:
        subscriber = Subscriber(msisdn=item["msisdn"], plan_type=item["plan_type"])
        subscribers[subscriber.msisdn] = subscriber
    return subscribers


def load_cdrs(csv_path: str) -> Tuple[List[CDR], int]:
    cdrs: List[CDR] = []
    malformed_count = 0

    with open(csv_path, "r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            try:
                parsed_row = parse_cdr_line(row)
                duration_sec = parsed_row["duration_sec"]
                cost = compute_cost(parsed_row["call_type"], duration_sec)
                cdr = CDR(
                    msisdn=parsed_row["msisdn"],
                    call_type=parsed_row["call_type"],
                    duration_sec=duration_sec,
                    cost=cost,
                )
                cdrs.append(cdr)
            except (KeyError, TypeError, ValueError) as exc:
                malformed_count += 1
                logger.warning("Skipping malformed CDR row: %s", exc)

    return cdrs, malformed_count


def write_report(report: dict, output_path: str) -> None:
    output = Path(output_path)
    output.write_text(json.dumps(report, indent=2), encoding="utf-8")
