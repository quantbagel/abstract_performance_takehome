# Etalon attribution

`benchmarks/metrics.py` reimplements the playback-slot algorithm audited in
`project-etalon/etalon` at `aeb65b2509e73b5450fb16d7f5fe9fc664431b33`,
`etalon/metrics/metric_utils.py`. Changes include strict input validation, a typed
result, bounded decode-interval search, and rejecting unobservable/all-zero traces.
No upstream evaluation runner is vendored. The accompanying license and notice are
retained for the source algorithm and its attribution.

Paper: https://arxiv.org/abs/2407.07000
Source: https://github.com/project-etalon/etalon
Copyright 2024-onwards Systems for AI Lab, Georgia Institute of Technology.
Apache License 2.0; see LICENSE and NOTICE.txt in this directory.
