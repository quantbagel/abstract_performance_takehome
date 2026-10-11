# Task 2 — Optimized image contract

This contract applies to [Task 2: harness design](../tasks/harness-design/README.md).
Task 1 evaluates the fixed serving image and submits a benchmark suite, not an optimized
engine image. Task 2 uses candidate-chosen development measurements, but its official
private evaluator runs offline after submission and cannot be replaced by a Task 1 suite.

## The output we want

**One runnable `linux/amd64` OCI image of ZML/LLMD, named by SHA-256 digest**, plus its
reproducible source/build recipe. A fork URL, launch script, remote endpoint, or claim
of faster inference is not a substitute for the image. We preload and run the image
ourselves on the frozen MI355X environment, with a private benchmark after submission.

A minimal build path is already included:

```bash
docker build --platform linux/amd64 -f baseline/Dockerfile \
  -t abstract-llmd-baseline:local .
```

This wraps the pinned upstream ROCm image without changing the engine. Candidates can
start from it for configuration/packaging changes. Engine/kernel changes require source
access supplied equally by the organizer; the public ZML checkout inspected during
authoring did not contain the complete LLMD server. Its commit hash is **not** proof of
the release image's LLMD source provenance. Resolve access/licensing before promising
source-level optimization or a from-source baseline build.

## Runtime ABI (provisional until baseline pilot)

- Fixed container entrypoint; accepts appended arguments
  `--io-impl=zio --model=/models/model`. This preserves the inspected upstream ABI.
- Serves port 8000 on the container interface, with OpenAI-compatible streaming.
- `/v1/models` for development readiness; full runner also requires a valid completed
  generation. The pilot must validate these endpoints and response/model IDs.
- `/models/model` is the organizer's pinned snapshot, mounted **read-only** as real files.
- No credentials, HF token, package installation, runtime weight download, or paid API
  is necessary. Images must start with egress disabled.
- Fresh writable container layer and bounded ephemeral state every launch. No persistent
  candidate cache or access to the host filesystem apart from authorized mounts.
- Only the assigned GPU device, published CPU/RAM/shm limits, and client network access.
- Graceful SIGTERM and bounded shutdown. No privileged mode or host-driver replacement.
- Same prompt semantics, greedy behavior, output channels, completeness, and tokenizer.

Organizer-owned runtime constraints must not be arbitrary candidate-supplied Docker
flags. A candidate can declare approved environment/engine arguments in its manifest;
we review them and apply the same resource/isolation constraints regardless of image.
The initial example manifest has no arbitrary host mounts or executable shell commands.

## Build and registry requirements

Copy [the Task 2 example](../tasks/harness-design/submission.example.json) to
`tasks/harness-design/submission.json`, retaining `task=harness-design`. Paths are
repository-root-relative. Include:

- Image registry digest, platform, human source commit, Dockerfile path/build arguments.
- Upstream base image and full source references for any modified engine components.
- Weight/model revision matching the baseline; any allowed conversion artifacts declared.
- Build provenance including compiler/runtime versions, licenses, and generated caches.
- Experiment record and report paths. No secrets or signed registry-download URLs.

Pin every base image and source dependency. Build on a clean CPU builder with declared
resources; disclose any GPU-assisted compilation and charge it to the compute budget.
Rebuild verification means equivalent source/behavior and traceable provenance; exact
byte-for-byte digest reproduction is required only if the published build is deterministic.
Both digests are retained if timestamps make the rebuilt image differ.

Push to an organizer-accessible registry and make the source available. Registry pulls,
compressed/unpacked image bytes, extraction/container-creation times, and cold weight
fetches are recorded separately, not folded into engine startup. Do not bake weights,
request answers, secrets, or hidden traces into the image. Model-independent or
model-specific compiled artifacts are allowed only under the published cohort policy,
from declared source and pinned target, without expected-answer data.

## Black-box, offline evaluation

Initial grading uses held-out prompts, arrivals, and output tasks on the **same pinned
model**. The evaluator and grading workload are not distributed or queryable during
optimization. Generalization means a real serving improvement, not trace-specific behavior.
A hidden model is **not** an additional mandatory stage in v1; it changes compilation,
source-support, and compute requirements too much to promise before the pilot.

We may re-execute selected kept development experiments by image digest, preserving
their declared local workload and runtime conditions. That harness review is separate
from private final-image grading; no hidden benchmark digest/report is required in the
candidate manifest. Keep images accessible until review completes. Registry/storage
allowance is part of the resource policy.
