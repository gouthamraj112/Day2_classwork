"""Billing and fraud rating helpers."""

from decimal import Decimal, ROUND_HALF_UP

from telecom_cli.config import RATES


def compute_cost(call_type: str, duration_sec: int) -> float:
    normalized_type = str(call_type).strip().lower()
    if normalized_type not in RATES:
        raise ValueError("call_type must be domestic, roaming, or international")

    rate = RATES[normalized_type]
    cost = Decimal(str(rate)) * Decimal(str(duration_sec)) / Decimal("60")
    return float(cost.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
