"""Fraud detection heuristics."""

from telecom_cli.models import CDR


def is_suspicious(cdr: CDR, threshold_sec: int) -> bool:
    if cdr.duration_sec > 0 and cdr.cost == 0:
        return True
    if cdr.call_type == "international" and cdr.duration_sec > threshold_sec:
        return True
    return False
