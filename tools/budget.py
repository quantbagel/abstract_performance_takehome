"""Planning arithmetic only: not measured runtime, a spend ledger, or budget enforcement."""

import argparse
import json
import math
import tomllib
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TASKS = ("benchmark-design", "harness-design", "compute-quant", "puzzle-design")


def estimate(
    config: dict[str, Any], task: str, gpu_hourly_usd: float | None = None
) -> dict[str, Any]:
    if task not in TASKS:
        raise ValueError(f"unknown task: {task}; choose one of {', '.join(TASKS)}")
    definition = config["tasks"][task]
    candidate, organizer = definition["candidate"], definition["organizer"]
    rate = config["pricing"].get("gpu_hourly_usd") if gpu_hourly_usd is None else gpu_hourly_usd
    if rate is not None and (not math.isfinite(rate) or rate <= 0):
        raise ValueError("GPU hourly quote must be finite and positive")
    phases = {}
    for name, workload in definition.get("benchmark", {}).items():
        requests, repetitions = workload["requests_per_cell"], workload["repetitions"]
        qps = workload["qps"]
        if requests <= 0 or repetitions <= 0 or not qps:
            raise ValueError("benchmark requires positive request/repetition counts and load cells")
        if any(not math.isfinite(q) or q <= 0 for q in qps):
            raise ValueError("QPS must be finite and positive")
        wall = workload["wall_budget_minutes"]
        if not math.isfinite(wall) or wall <= 0:
            raise ValueError("wall envelope must be finite and positive")
        arrival_minutes = repetitions * sum(requests / q for q in qps) / 60
        gpu_envelope = wall / 60 * candidate["gpus_at_once"]
        phases[name] = {
            "offered_requests": requests * repetitions * len(qps),
            "expected_arrival_minutes_only": arrival_minutes,
            "proposed_total_wall_envelope_minutes": wall,
            "proposed_gpu_hour_envelope": gpu_envelope,
            "remaining_minutes_for_startup_correctness_ttft_drain": wall - arrival_minutes,
            "startup_launches": workload["startup_launches"],
            "fits_arrival_expectation": arrival_minutes <= wall,
            "quoted_envelope_cost_usd": None if rate is None else rate * gpu_envelope,
        }
    caveats = [
        "Allowances are task-specific proposals, not issued credits; no transfers between tasks.",
        "Envelopes are unmeasured; pilot before promising required evidence fits.",
        "Costs exclude taxes, CPU builds, storage, registry, and full-node minimums.",
        "This command does not provision resources or enforce spending caps.",
    ]
    if phases:
        caveats += [
            "QPS is a draft, not calibrated MI355X capacity.",
            "Poisson arrival span can differ from its expectation.",
        ]
    elif task == "benchmark-design":
        caveats.append(
            "Task 1 designs its own workload; no Task 2 arrival plan or runtime estimate is reused."
        )
    elif task == "harness-design":
        caveats += [
            "Task 2 grading is private/offline after submission; no official workload is exposed.",
            "Budget candidate-chosen development measurements within the GPU allowance.",
        ]
    else:
        caveats += ["This task is CPU-only; no GPU allocation or inference baseline is required."]
        if task == "compute-quant":
            caveats += ["Included valuation inputs are synthetic, not real market-price evidence."]
        else:
            caveats += [
                "Planning does not run Astra or start either 20-minute clock.",
                "Premature solver API-cap exhaustion cannot earn puzzle resistance credit.",
            ]

    def gpu_cost(hours: float) -> float | None:
        return 0.0 if hours == 0 else (None if rate is None else rate * hours)

    gpu_needed = candidate["gpu_hours"] > 0 or organizer["grading_gpu_hours"] > 0
    return {
        "task": task,
        "status": "planning-only-unmeasured",
        "benchmark_owner": definition.get("benchmark_owner"),
        "evaluation_owner": definition.get("evaluation_owner"),
        "evaluation_mode": definition.get("evaluation_mode"),
        "author_wall_minutes": definition.get("author_wall_minutes"),
        "solver_wall_minutes": definition.get("solver_wall_minutes"),
        "solver_runs": definition.get("solver_runs"),
        "proposed_suite_wall_budget_minutes": definition.get("suite_wall_budget_minutes"),
        "pricing_status": (
            "not-needed-no-gpu"
            if not gpu_needed
            else "quote-required"
            if rate is None
            else "user-supplied-or-configured-quote"
        ),
        "gpu_hourly_usd": rate,
        "candidate_api_cap_usd": candidate["api_usd"],
        "candidate_gpu_hour_cap": candidate["gpu_hours"],
        "organizer_grading_gpu_hours": organizer["grading_gpu_hours"],
        "candidate_compute_cost_usd": gpu_cost(candidate["gpu_hours"]),
        "organizer_compute_cost_usd": gpu_cost(organizer["grading_gpu_hours"]),
        "organizer_grading_api_cap_usd": organizer.get("api_usd"),
        "candidate_cpu_build_core_hours": candidate["cpu_build_core_hours"],
        "candidate_artifact_storage_gib": candidate["artifact_storage_gib"],
        "benchmark": phases,
        "caveats": caveats,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["estimate"])
    parser.add_argument(
        "--task",
        choices=TASKS,
        required=True,
        help="select a separate task allowance; there is no combined pool",
    )
    parser.add_argument("--config", type=Path, default=ROOT / "budgets.toml")
    parser.add_argument("--gpu-hourly-usd", type=float)
    args = parser.parse_args()
    try:
        config = tomllib.loads(args.config.read_text(encoding="utf-8"))
        result = estimate(config, args.task, args.gpu_hourly_usd)
        print(json.dumps(result, indent=2, allow_nan=False))
    except (ValueError, OSError, KeyError) as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
