"""Parsing helpers for raw CDR input."""

from typing import Dict


def parse_cdr_line(row: dict) -> dict:
    if not isinstance(row, dict):
        raise ValueError("CDR row must be a dictionary")

    cleaned = {}
    for key in ("msisdn", "call_type", "duration_sec"):
        value = row.get(key)
        if value is None or str(value).strip() == "":
            raise ValueError(f"Missing required field: {key}")
        cleaned[key] = value

    cleaned["call_type"] = str(cleaned["call_type"]).strip().lower()
    if cleaned["call_type"] not in {"domestic", "roaming", "international"}:
        raise ValueError("call_type must be domestic, roaming, or international")

    try:
        cleaned["duration_sec"] = int(str(cleaned["duration_sec"]).strip())
    except ValueError as exc:
        raise ValueError("duration_sec must be an integer") from exc

    if cleaned["duration_sec"] < 0:
        raise ValueError("duration_sec must be non-negative")

    return cleaned


def parse_legacy_line(line: str) -> dict:
    parts = [part.strip() for part in line.split("|")]
    if len(parts) != 3:
        raise ValueError("Legacy line must contain msisdn, call_type, and duration_sec")

    msisdn, call_type, duration_sec = parts
    return {"msisdn": msisdn, "call_type": call_type, "duration_sec": duration_sec}
