# Organizer-owned measurement utilities

This directory contains shared Etalon metric primitives, strict SSE parsing, and a
completed-stream smoke client. It is **not** the candidate's Task 1 benchmark suite,
Task 1's complete supplied measurement harness, or Task 2's full frozen evaluator.

- **Task 1:** candidate code belongs in `tasks/benchmark-design/suite/`. It may import
  these primitives but cannot modify trusted instrumentation, baseline, or shared tools.
- **Task 2:** the organizer runs a private evaluator offline after submission; no official
  evaluator is supplied to candidates. Candidates modify `tasks/harness-design/harness/`
  and their declared engine/image source, choosing their own development measurements.
  Shared primitives may inform local proxies but do not specify the hidden grader.

The full runner/event schemas/token adapter remain organizer release work. See
[release status](../docs/RELEASE_STATUS.md) and the
[Task 2 black-box evaluation policy](../docs/BENCHMARK.md). A protocol smoke success is not either
assignment's correctness gate or performance score.
