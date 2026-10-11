# Abstract take-homes

**Hard problems. Clear rules. Show us something surprising.**

We want difficulty to come from reasoning and experimentation, not guessing requirements
or fighting setup. Honest negative results and well-explained failures count as evidence.

Choose **one** of four standalone assignments. Each has its own submission, budget,
and score; none requires completing another. Only Tasks 1 and 2 need a GPU.

| Task | Question | Main deliverable |
| --- | --- | --- |
| [1. Benchmark design](tasks/benchmark-design/README.md) | How would you tell whether an inference server is fast, smooth, and correct? | Benchmark suite and validation report |
| [2. Harness design](tasks/harness-design/README.md) | Can you build a loop that makes inference faster and keeps only valid improvements? | Optimization harness and its best Docker image |
| [3. Compute Quant](tasks/compute-quant/README.md) | What should future GPU capacity cost, and is the supplied reservation a good deal? | 1/3/6/12-month price curve, valuation, and memo |
| [4. 20/20: Beat Astra](tasks/puzzle-design/README.md) | Can you design a puzzle in 20 minutes that Astra cannot solve in 20 minutes? | Puzzle, worked solution, and fair verifier |

**The key distinction:** Task 1 designs the benchmark, keeping the engine and measurement
runner fixed. Task 2 improves the engine through a loop using candidate-chosen development
measurements; we grade its final image offline with a private, black-box benchmark.
Task 2 never grades against the candidate's Task 1 suite.

**Agent starting points:** Task 1 gets a **souped-up, fixed Pi 1.0 harness** so candidates
can focus on benchmark design. Task 2 starts with **bland, stock Pi 1.0** and asks candidates
to build its optimization capabilities. These coding-agent harnesses are separate from the
measurement runner and private grader. See [harness profiles](agent-harness/README.md) and
the [LLM-cheating / protected-no-diff warning](docs/INTEGRITY.md).

Task 3 uses supplied dated evidence; **FV means fair value**. Task 4 uses a pinned solver
and two trusted clocks; invalid puzzles and infrastructure failures are not wins.

> **Draft preview, not a candidate-ready release.** Inference infrastructure still needs
> hardware validation, Compute Quant inputs are synthetic, and Astra's profile/timed runner
> are not yet pinned. See the [public release status](docs/RELEASE_STATUS.md). Nothing here starts
> a timer, launches paid resources, or issues credits.

## Fork and submit

This is intended to be a **public, read-only upstream**: candidates fork it, work on a
branch in their own fork, and submit a pull request. No upstream push access is needed
or granted. See [candidate instructions](CONTRIBUTING.md) before starting.

Forks and PRs are public. **Task 4 solutions, verifiers, and reports go through the
organizer's private submission channel**, never a public commit. Do not start a timed
session until that channel and the frozen solver profile have been supplied.

## Proposed time and resources

| Resource | Task 1 | Task 2 | Task 3 | Task 4 |
| --- | ---: | ---: | ---: | ---: |
| Active effort | 6–10 hours | 24–40 hours | 8–12 hours | 20 minutes |
| Calendar window | One week | Two weeks | One week | One timed session |
| Candidate API credit | $50 | $200 | $50 | $5 |
| Candidate GPU-hours | 12 | 64 | 0 | 0 |
| Organizer grading GPU-hours | 4 | 8 | 0 | 0 |

These are proposals, not spending authorization. Use separate resource ledgers;
no transfers between tasks. GPU time includes idle allocations, setup, and failed runs.
Task 4 separately proposes one organizer-funded Astra attempt with a **20-minute maximum
and $20 API cap**; premature cap exhaustion does not count as puzzle resistance.
See [budget policy](docs/BUDGETS.md) and `budgets.toml`.

## Inference setup — Tasks 1 and 2 only

We use **ZML/LLMD**, the Zig/OpenXLA inference server—not the separate `llm-d` Kubernetes
project. Proposed hardware/model: **one isolated Hot Aisle MI355X** and
**Qwen/Qwen3.6-27B**, with **Qwen/Qwen3-8B** for smoke tests. Both pinned combinations
need a hardware pilot before release. No multi-node or unsupported-model work is required.

Run this on the assigned **Linux AMD GPU host**, not an Apple laptop. You need Docker,
an appropriate AMD driver, Python 3.11+, `uv`, and access to the assigned render device
and `/dev/kfd`. All commands run from the **repository root**.

```bash
uv sync --frozen --extra dev
uv run python -m tools.baseline prepare --model smoke --model-dir /srv/abstract-model
uv run python -m tools.baseline start --model-dir /srv/abstract-model \
  --render-device /dev/dri/renderD128
uv run python -m benchmarks.smoke --out results/smoke.json
uv run python -m tools.baseline stop
```

`renderD128` is an example; verify the assigned device. Preparation pulls the pinned ROCm
image, materializes weights, and builds [`baseline/Dockerfile`](baseline/Dockerfile).
Launch mounts weights read-only, exposes only loopback port 8000, and injects no HF
credential into the server.

Use a separate directory for the target snapshot; mixing snapshots is rejected:

```bash
uv run python -m tools.baseline prepare --model target --model-dir /srv/abstract-target
uv run python -m tools.baseline start --model-dir /srv/abstract-target \
  --render-device /dev/dri/renderD128
uv run python -m benchmarks.smoke --out results/target-smoke.json
uv run python -m tools.baseline stop
```

This is a development launcher, not the hardened measurement runner. Snapshot markers
and response model IDs are bookkeeping, not checksum certificates. The smoke client
checks a completed text stream, not correctness or performance.

### GPU-free checks and planning

These software checks run on a laptop; they do not certify a working GPU assignment.

```bash
uv sync --frozen --extra dev
uv run --frozen ruff check .
uv run --frozen python -m unittest discover -s tests -v
uv run python -m tools.baseline start --model-dir /srv/abstract-model --dry-run
uv run python -m tools.budget estimate --task benchmark-design
uv run python -m tools.budget estimate --task harness-design
uv run python -m tools.budget estimate --task compute-quant
uv run python -m tools.budget estimate --task puzzle-design
```

Dry-run and budget planning require no Docker daemon, weights, or paid APIs. Budget
estimates do not provision resources and require an explicit task.

## Details and repository layout

Start with the linked assignment; consult its contract and rubric before implementation.
[Task 2 evaluation policy](docs/BENCHMARK.md) explains the black-box/offline boundary.
For measurement ideas, see [Etalon §4](https://arxiv.org/html/2407.07000#S4); it is a hint,
not the hidden benchmark specification or a required Task 1 workload.
Inspired by [quantbagel/takehome](https://github.com/quantbagel/takehome) and
[Etalon](https://arxiv.org/abs/2407.07000).

```text
tasks/benchmark-design/   assignment, rubric, suite contract, manifest, design notes
tasks/harness-design/     assignment, rubric, harness contract/log, manifest, notes
tasks/compute-quant/      assignment, rubric, synthetic data, manifest, report
tasks/puzzle-design/      assignment, rubric, timing/verifier protocol, manifest, solution
agent-harness/           plain/enhanced Pi 1.0 profile specifications (draft)
baseline/                shared pinned ROCm image and model lock
benchmarks/              shared measurement primitives and smoke client
docs/                    public policies and draft release status
                         (private authoring materials are not distributed)
tools/                   baseline launcher, task budgets, protected-file integrity check
tests/                   CPU-only regressions/conformance (not candidate suite tests)
budgets.toml             separately scoped proposed allowances
RUBRIC.md                rubric index; no combined score
```
