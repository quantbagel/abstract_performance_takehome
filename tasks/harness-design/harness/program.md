# Task 2 — Optimization playbook template

Replace/extend this with your own informed search strategy.

- Start from bland Pi 1.0.0: stock prompt/tools, no supplied enhanced agent/optimizer.
- Build your harness enhancements here (or in a declared Pi-derived fork/overlay), not
  by editing the organizer's protected baseline, tools, tests, or environment locks.
- The artifact is an optimized ZML/LLMD image on the assigned AMD GPU.
- Never change the pinned model snapshot/tokenizer, baseline lock, or host policy.
- Choose your own development workloads and correctness checks for keep/revert decisions.
- Official grading is private and offline after submission: no released grader or live oracle.
- Local measurements (including a Task 1 suite) are evidence, not official scores.
- Hint: [Etalon §4](https://arxiv.org/html/2407.07000#S4), not a hidden-test specification.
- Read the image contract and available budgets before proposing experiments.
- Profile first. Identify prefill, decode scheduling, kernels, loading/compilation,
  container/runtime initialization, and client-observability bottlenecks separately.
- Make a small attributable change, retain its exact patch and provenance, and measure.
- Do not substitute mean tokens/s for fluidity or readiness for engine startup.
- Correctness and complete output are gates. No faster-but-wrong or trace-specific wins.
- Noise is evidence against a premature keep; do not change local tests to hide regressions.
- Bound builds/launches/measurements; keep last-good state and enough final-run reserve.
- On failure preserve logs/reproducer, clean up, restore, and try the next hypothesis.
- Ship the actual image you measured, by digest, with unsuccessful experiments included.
- Run `python -B -m tools.check_integrity --base takehome-start`; protected diffs must
  be empty. Record the starter commit and result, alongside your own harness changes.
