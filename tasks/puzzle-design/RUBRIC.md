# Task 4 rubric — 20/20 puzzle design

**Proposed independent 100-point rubric.** One 20-minute authoring session and one pinned
20-minute Astra solve. Release the solver/tools/resources, timing/submission protocol,
validity criteria, and sandbox before anyone's clock starts.

## Gates before Astra resistance

- Bundle frozen on time, within format/size limits, with a known-valid answer and proof.
- Self-contained, objectively answerable statement; ambiguity/private facts/contradictions
  are not difficulty. More than one valid answer is allowed if the verifier accepts them.
- Deterministic, bounded, fair verifier; correct answer and declared equivalents pass.
  Wrong/malformed answers fail without crashing, hanging, or consulting solver identity.
- No prewritten private instance, payload-padding/crypto-inversion trick, huge blind search
  as sole difficulty, malicious payload, unsafe prompt, secret extraction, or runner attack.

Invalid entries get no resistance credit; we distinguish honest incomplete work from
misrepresentation. Reviewer verification of the supplied solution is not a requirement
that a human discover that solution from scratch within the solver's 20 minutes.

## Scoring

| Area | Points | What matters |
| --- | ---: | --- |
| Resistance to pinned Astra run | 40 | Valid deadline or normal unsuccessful completion without a correct final answer: 40; correct on-time answer: 0 |
| Reasoning depth and construction | 30 | Interesting, auditable reasoning challenge; difficulty not solely compute volume, obscure knowledge, or syntax tricks |
| Clarity and elegance | 20 | Compact sufficient statement, precise conventions/answer format, and satisfying explained solution |
| Verification and reproducibility | 10 | Fair tested verifier, equivalent-answer handling, authoritative timestamps/digests, complete evidence, and honest resource record |

Resistance is deliberately binary for the literal challenge. Design quality can still
be excellent when Astra solves it. We do not turn an unsafe refusal or arbitrary timeout
into an adversarial success.

## Run interpretation

- Pin the same solver profile/model/tool limits for the cohort; no puzzle-specific changes.
- Only the public statement/answer format is exposed; private proof/verifier/report remain
  outside the solver's filesystem and context. One final answer, no hidden-key oracle.
- Record delivery/start/deadline/submission times, transcript/tools, final structured
  answer, resource use, verifier result, and reviewer confirmation of puzzle validity.
- A correct answer at or before the solver deadline solves the puzzle. Later output
  does not count. Server/network receipt semantics must be explicit and consistent.
- Infrastructure failure, premature API-cap exhaustion, or verifier malfunction is
  inconclusive/invalid, not 40 resistance points. Retry only under a published policy.
- One sample demonstrates failure in that run, not a universal theorem about the model.
  Any multi-seed robustness experiment is separately budgeted and not required here.

## Cost

Proposed organizer allowance: one 20-minute solve, $20 API cap, zero GPU-hours, and a
bounded CPU verifier/review allowance. Pilot spend/timing before release; if the profile
cannot reliably use its 20-minute allocation, change the published profile/budget rather
than shortening some candidates' attempts invisibly. No live solver is provisioned here.
