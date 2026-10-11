"""Etalon-compatible playback-slot metrics, not SSE-chunk metrics.

Algorithm reference: project-etalon/etalon at aeb65b2509e73b5450fb16d7f5fe9fc664431b33,
metrics/metric_utils.py (Apache-2.0; attribution in third_party/etalon/).
This implementation adds input validation and treats absent timing as invalid.
Callers must supply independently verified MODEL TOKEN arrival times.
"""

import math
from collections.abc import Sequence
from dataclasses import dataclass


def _nonnegative_finite(value: float, name: str) -> None:
    if not math.isfinite(value) or value < 0:
        raise ValueError(f"{name} must be finite and nonnegative")


@dataclass(frozen=True)
class Fluidity:
    accepted_slots: int
    missed_slots: int

    @property
    def total_slots(self) -> int:
        return self.accepted_slots + self.missed_slots

    @property
    def index(self) -> float:
        return self.accepted_slots / self.total_slots


def fluidity(
    intervals_s: Sequence[float],
    prefill_deadline_s: float,
    decode_deadline_s: float,
    *,
    ignore_first_token: bool = False,
) -> Fluidity:
    """Count playback-slot acceptance, including multiple misses for a long stall.

    intervals_s[0] is TTFT; later values are model-token inter-arrival times.
    Empty traces, or ignoring the only token, are not evidence of perfect fluidity.
    """
    _nonnegative_finite(prefill_deadline_s, "prefill deadline")
    _nonnegative_finite(decode_deadline_s, "decode deadline")
    if decode_deadline_s == 0:
        raise ValueError("decode deadline must be positive")
    if not intervals_s or (ignore_first_token and len(intervals_s) < 2):
        raise ValueError("no eligible token timing observations")
    for interval in intervals_s:
        _nonnegative_finite(interval, "token interval")

    return _fluidity(intervals_s, prefill_deadline_s, decode_deadline_s, ignore_first_token)


def _fluidity(
    intervals_s: Sequence[float], prefill_deadline_s: float,
    decode_deadline_s: float, ignore_first_token: bool,
) -> Fluidity:
    """Count slots after validation; deadline search reuses the validated trace."""
    accepted = missed = 0
    slack = 0.0
    for i in range(1 if ignore_first_token else 0, len(intervals_s)):
        interval = intervals_s[i]
        target = prefill_deadline_s if i == 0 else decode_deadline_s
        if interval <= target + slack:
            accepted += 1
            slack += target - interval
        else:
            # Match the pinned Etalon source's float floor-division behavior.
            slots = (
                1 + (interval - slack - target) // decode_deadline_s
                if i == 0
                else (interval - slack) // decode_deadline_s
            )
            missed += int(slots)
            slack = 0.0
    return Fluidity(accepted, missed)


def token_intervals(arrival_times_s: Sequence[float]) -> list[float]:
    """Convert request-relative verified token receive times to intervals (first=TTFT)."""
    if not arrival_times_s:
        raise ValueError("empty token trace")
    previous = 0.0
    intervals = []
    for arrival in arrival_times_s:
        _nonnegative_finite(arrival, "token arrival")
        if arrival < previous:
            raise ValueError("token arrivals must be nondecreasing")
        intervals.append(arrival - previous)
        previous = arrival
    return intervals


def quantile(values: Sequence[float], q: float) -> float:
    """Linear sample quantile (same convention as NumPy's default)."""
    if not values or not math.isfinite(q) or not 0 <= q <= 1:
        raise ValueError("quantile requires nonempty values and q in [0, 1]")
    if any(not math.isfinite(value) for value in values):
        raise ValueError("quantile values must be finite")
    ordered = sorted(values)
    position = (len(ordered) - 1) * q
    lower, upper = math.floor(position), math.ceil(position)
    return ordered[lower] + (ordered[upper] - ordered[lower]) * (position - lower)


def minimum_decode_deadline(
    intervals_s: Sequence[float], *, max_miss_rate: float = 0.1, resolution_s: float = 0.0001
) -> float | None:
    """Pinned Etalon interval-search convention, ignoring prefill.

    This is a source-defined search statistic, not proof of a continuous global optimum.
    None means timing is unresolved: all-at-once decode cannot establish a finite
    maximum fluid generation rate from a text stream. Don't award infinite speed.
    """
    if not math.isfinite(max_miss_rate) or not 0 <= max_miss_rate < 1:
        raise ValueError("max_miss_rate must be in [0, 1)")
    if not math.isfinite(resolution_s) or resolution_s <= 0:
        raise ValueError("resolution must be finite and positive")
    fluidity(intervals_s, 0.0, resolution_s, ignore_first_token=True)
    if max(intervals_s[1:]) == 0:
        return None
    # Retain the audited upstream search bounds and +/- resolution updates exactly.
    # A tighter initial bound changes the quantized answer and can affect rankings.
    deadline = right = 1e10
    upper = _fluidity(intervals_s, 0.0, right, True)
    if upper.missed_slots / upper.total_slots > max_miss_rate:
        raise ValueError("trace exceeds the pinned Etalon search range")
    left = 0.0
    while right - left > resolution_s:
        mid = (left + right) / 2
        if not left < mid < right:
            raise ValueError("resolution is below floating-point search precision")
        result = _fluidity(intervals_s, 0.0, mid, True)
        if result.missed_slots / result.total_slots > max_miss_rate:
            left = mid + resolution_s
        else:
            deadline = mid
            right = mid - resolution_s
    return deadline


def fluid_token_generation_rate(
    traces: Sequence[Sequence[float]], *, max_miss_rate: float = 0.1, request_quantile: float = 0.99
) -> float | None:
    """1/p99(minimum decode deadline), not aggregate output tokens/s.

    Caller handles failed requests as FI=0 and enforces completeness/error gates before
    computing this successful-trace statistic. Never silently omit unresolved traces.
    """
    if not traces:
        raise ValueError("no request traces")
    deadlines = [minimum_decode_deadline(t, max_miss_rate=max_miss_rate) for t in traces]
    if any(deadline is None for deadline in deadlines):
        return None
    tail = quantile([d for d in deadlines if d is not None], request_quantile)
    return 1 / tail
