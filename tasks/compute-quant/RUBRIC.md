# Task 3 rubric — Compute Quant

**Proposed independent 100-point rubric.** The organizer freezes the as-of input pack,
reference product, reservation case, criteria, and supporting quotas before release.
There is no single objectively known fair-value number and no prize for fabricated precision.

## Integrity and validity

Identify sources and as-of dates; preserve supplied evidence; label synthetic/demo data.
Fabricated quotes, look-ahead leakage presented as an as-of result, unsupported “executable
forward” claims, hidden data purchases, and unreported extra resources fail integrity review.
An honest sparse-data/unidentified result is acceptable; a smooth curve with no support is not.

## Scoring

| Area | Points | What matters |
| --- | ---: | --- |
| Data quality and market interpretation | 25 | Provenance/as-of filtering; firm versus indicative/list quotes; commitment versus delivery; bid/ask, liquidity, missing coverage |
| Product and unit normalization | 20 | GPU/node/calendar hours, hardware/workload, region, SLA/preemption, quantity, fees, payment timing, and optionality |
| Curve and reservation valuation | 25 | Supported observed/implied versus modeled nodes; defensible market/cost reconciliation; transparent quantities, cash flows, and buyer mark |
| Risk and uncertainty | 15 | Plausible scenarios/sensitivities; limitations; ranges correctly labeled; no unjustified cash-and-carry or forced curve shape |
| Reproducibility and explanation | 15 | Runnable pipeline, hashes/config, tests, plots/tables, exclusions, and useful decision memo |

## Checks we run/review

- Node-hour/month prices are normalized with actual accelerator counts and billed hours.
- Current usage commitments do not masquerade as guaranteed future delivery.
- Expired/post-cutoff quotes and incompatible product variants are handled explicitly.
- Changing region/preemption/payment terms does not silently leave an identical product.
- Sparse evidence is surfaced rather than labeled an observed 12-month price.
- Higher/lower utilization and economic assumptions have effects consistent with the
  candidate's declared model; simplistic universal monotonic rules are not ground truth.
- Delivery windows and GPU counts reconcile to reserved hours; payment cash flows and
  discounting reconcile to the contract mark. Usage forecasts do not erase reserved fees.
- Uncertainty increases or identification weakens when evidence is removed, unless a
  justified structural constraint explains otherwise.
- Clean reruns use supplied evidence and declared assumptions, not current network data.

Published synthetic fixtures test plumbing and financial consistency, not forecast accuracy.
The organizer may supply held-out perturbations of the same input schema; no hidden rubric
or requirement to guess a future realized spot price. If a dated historical panel is later
added, freeze the backtest/split and give it to everyone before the task begins.

## Independence and cost

No inference engine, GPU benchmark, optimized image, agent harness, or live trade is
required. CPU grading is sufficient. Any future pricing-quality comparison needs a
real provenance-bearing input pack; the included fake numbers cannot establish market FV.
