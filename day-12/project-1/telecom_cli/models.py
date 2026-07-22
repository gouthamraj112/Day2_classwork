"""Domain models for subscribers and CDR records."""

from dataclasses import dataclass, field
from typing import List


@dataclass
class Subscriber:
    msisdn: str
    plan_type: str
    calls: List["CDR"] = field(default_factory=list)

    def total_cost(self) -> float:
        return round(sum(call.cost for call in self.calls), 2)


@dataclass
class CDR:
    msisdn: str
    call_type: str
    duration_sec: int
    cost: float
    is_suspicious_flag: bool = False

    def is_suspicious(self, threshold_sec: int) -> bool:
        if self.duration_sec > 0 and self.cost == 0:
            return True
        if self.call_type == "international" and self.duration_sec > threshold_sec:
            return True
        return False
