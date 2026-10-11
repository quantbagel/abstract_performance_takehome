# Synthetic Compute Quant input contract

**Every observation, provider, quote, performance figure, cost, and economic assumption
in this folder is a fabricated demo.** Nothing is a Hot Aisle offer or market-price claim.
No remote data request or paid purchase is needed to read it.

`demo-case.json` points to CSVs relative to its own directory. Dates are UTC; delivery
ends are exclusive. The synthetic as-of date is **2026-10-01T00:00:00Z**. The reference
product and deal are explicit in the case. Reproduce all inputs by hash in your output.
Before production release the organizer must freeze real archived evidence, licenses,
source URLs/quote documents, timestamps, schema, and unit tests for the same contract.

## Quotes (`demo-quotes.csv`)

- `id`, `synthetic`, `source_ref`, `provider`: evidence identity; `fixture://` is not a
  real source URL. Every demo row has `synthetic=true`.
- `observed_at`, `valid_until`: information/expiry timestamps. The CSV intentionally
  retains expired and post-as-of observations so a model must handle them, not silently
  use all rows as current executable evidence.
- `kind`, `side`: `current_on_demand`, `usage_commitment`, `firm_forward`, or `spot_current`;
  quote side is `ask` or `bid`. “Firm” describes a **fictional case assumption**, not an
  actually tradable provider offer. No executable trade is authorized.
- `gpu`, `memory_gib`, `gpu_count`, `region`, `isolation`, `preemptible`, `sla_pct`:
  product fields. Node quantities and differing service quality matter beyond arithmetic.
- `currency`, `price`, `unit`: quote amount/unit. `gpu_hour` is already per accelerator;
  `node_hour` is per the whole specified GPU count; `node_month` is for the entire stated
  billing/delivery month. Do not hard-code 720 hours or normalize quantity twice.
- `delivery_start`, `delivery_end`: specified service windows, exclusive end. Empty
  windows in a usage commitment do **not** imply a future guaranteed capacity strip.
- `commitment_months`, `capacity_guaranteed`, `payment`, `cancellation`: economic rights.
  A long spending commitment can be postpaid and lack guaranteed capacity. Current
  monthly rent, future reserved capacity, and flexible hourly usage are different products.

Supplementary CPU/RAM/network/fees are given by `quote_common_terms` in the case only
where specified. Missing product/cost evidence is unknown, not zero or perfect quality.
For real quotes, archive exceptions individually rather than assuming those common terms.

## Performance (`demo-performance.csv`)

Purely synthetic same-model dense-decode workload measurements. `output_tokens_per_s`
refers to one accelerator; do not use it as a universal performance exchange rate or
as an Etalon fluidity statistic. Input/output shape, precision, software, and uncertainty
are supplied; no inference was actually run. Some hardware has no matching measurement.

## Economics and reservation (`demo-case.json`)

- Capex includes the stated per-accelerator share of supporting hardware. Power is kW,
  energy price is USD/kWh, PUE is unitless, utilization is a fraction, and financing is
  an annual assumption. Their purposes are explicit, not a market-implied rate curve.
- Fixed reserved capacity is one GPU continuously from 2027-01-01 to 2027-04-01,
  **not** only the hours the buyer ends up using. Compute calendar hours from dates.
- Fixed contract price is USD/GPU-hour, monthly payment in arrears, no cancellation,
  no make-good beyond the stated credits. Estimated used fraction does not reduce fees.
- Define the meaning/viewpoint of fair value and any discount/default/SLA treatment.
  There is no supplied “correct forward curve” to copy from these assumptions.

The CSV intentionally leaves tenors sparse and includes non-comparable products. That
is a valuation-identification problem, not permission to invent quotes or present the
demo's numeric output as real market evidence.
