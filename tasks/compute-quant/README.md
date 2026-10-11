# Task 3 — Compute Quant

**What should future GPU capacity cost, and is the supplied reservation a good deal?**

Estimate prices for a defined compute product delivered **1, 3, 6, and 12 months ahead**.
Use that curve to value the supplied capacity reservation. Here **FV means fair value**.
No GPU, paid dataset, or trade is required.

> **Draft:** the included data is entirely synthetic, not market evidence or a provider
> offer. A real dated evidence pack must be frozen before a market-valuation release.
> See [release status](../../docs/RELEASE_STATUS.md).

## We provide at release

- An as-of date and reference product: hardware, region, resources, SLA, and contract terms.
- Dated price observations with sources, units, and delivery/payment terms.
- Supply-cost assumptions and a reservation case to value.

The [demo input pack](data/README.md) illustrates the interface using fake numbers.

## Your job

1. **Make prices comparable.** Account for GPU versus node pricing, actual calendar hours,
   hardware, region, service quality, fees, and payment/cancellation terms. Keep products
   separate when a credible comparison is not possible.
2. **Build the curve.** Report USD/GPU-hour for each delivery month, with evidence and
   uncertainty. Separate observed/implied prices from modeled estimates or unidentified
   points. A discount for today's usage commitment is not automatically a forward quote.
3. **Cross-check the valuation.** Compare a market/comparable view with a transparent
   supply-cost view. Explain disagreements; cost is not a guaranteed price floor.
4. **Value the reservation.** Show its reserved hours, payment cash flows, fair price,
   and buyer's mark-to-model versus the fixed deal. Expected usage does not reduce the
   bill for reserved capacity. Include discounting, service risk, and cancellation terms.
5. **Stress-test it.** Show base, cheap-compute, and scarcity scenarios. Explain which
   assumptions matter most and what extra evidence would reduce uncertainty.

Each curve node prices capacity reserved throughout a future UTC calendar month—not
an arbitrary hour or a long-term discount on current usage. Use only information available
as of the cutoff. Label forecasts and judgmental ranges honestly; a supported range or
“not identifiable” is better than invented precision.

## Submit

Work in `tasks/compute-quant/`; keep supplied inputs unchanged.

| Artifact | Contents |
| --- | --- |
| Runnable model and tests | Pinned dependencies, input hashes, and a documented rerun command |
| `curve.csv` | Delivery dates, prices/ranges, units, evidence IDs/status, and scenarios |
| `valuation.json` | Reservation quantities, cash flows, fair price, buyer mark, and assumptions |
| `REPORT.md` | Normalization, methods, market/cost comparison, scenarios, and limitations |
| `submission.json` | Completed [manifest](submission.example.json) identifying source and inputs |

We grade evidence, normalization, consistency, uncertainty, and reproducibility—not
agreement with a single target price. See the [rubric](RUBRIC.md).

## Time and resources

Proposed: **8–12 hours over one week**, **$50 API credit**, and **zero GPU-hours**.
Use the supplied sources; paid data, provider signups, and compute purchases are not
required or authorized. Resources are not yet issued.

Before implementation, read the [input contract](data/README.md) and
[budget policy](../../docs/BUDGETS.md).
