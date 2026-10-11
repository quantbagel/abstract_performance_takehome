"""GPU/API-free regressions for the public planning and development utilities."""

import argparse
import json
import math
import tempfile
import tomllib
import unittest
from pathlib import Path
from unittest.mock import patch

import httpx

from benchmarks.metrics import (
    fluid_token_generation_rate,
    fluidity,
    minimum_decode_deadline,
    quantile,
    token_intervals,
)
from benchmarks.smoke import check_stream, positive_seconds, wait_for_model
from benchmarks.streaming import StreamProtocolError, decode_payload, generated_deltas, sse_data
from tools.baseline import build_command, load_lock, prepare, start_command, validate_model_dir
from tools.budget import TASKS, estimate

ROOT = Path(__file__).resolve().parents[1]


class MetricTests(unittest.TestCase):
    def test_burst_slack_accepts_later_delay(self):
        result = fluidity([0.5, 0.01, 0.01, 0.1], 0.5, 0.05)
        self.assertEqual((result.accepted_slots, result.missed_slots), (4, 0))

    def test_long_stall_counts_multiple_slots_and_resets_slack(self):
        result = fluidity([0.1, 0.31, 0.01], 0.1, 0.1)
        self.assertEqual((result.accepted_slots, result.missed_slots), (2, 3))
        self.assertEqual(result.index, 0.4)

    def test_missing_nonfinite_and_negative_timing_rejected(self):
        for trace in ([], [-1], [math.nan], [math.inf]):
            with self.subTest(trace=trace), self.assertRaises(ValueError):
                fluidity(trace, 1, 0.1)
        with self.assertRaises(ValueError):
            fluidity([1], 1, 0.1, ignore_first_token=True)
        with self.assertRaises(ValueError):
            fluidity([1], 1, 0)

    def test_arrivals_require_monotonic_finite_timing(self):
        self.assertEqual(token_intervals([1, 1.25, 1.25]), [1, 0.25, 0])
        for trace in ([], [1, 0.5], [math.nan]):
            with self.subTest(trace=trace), self.assertRaises(ValueError):
                token_intervals(trace)

    def test_linear_quantile(self):
        self.assertEqual(quantile([4, 0, 2], 0.75), 3)
        for values, q in (([], 0.5), ([math.inf], 0.5), ([1], -1), ([1], math.nan)):
            with self.subTest(values=values, q=q), self.assertRaises(ValueError):
                quantile(values, q)

    def test_pinned_etalon_search_golden(self):
        # Source-defined search result, NOT a hidden evaluator parameter/threshold.
        self.assertAlmostEqual(
            minimum_decode_deadline([1, 0.05, 0.05, 0.05]), 0.0502064256918161, places=14
        )

    def test_unresolved_trace_is_not_infinite_speed(self):
        self.assertIsNone(minimum_decode_deadline([1, 0, 0]))
        self.assertIsNone(fluid_token_generation_rate([[1, 0, 0], [1, 0.05]]))

    def test_pathological_search_fails_instead_of_hanging_or_claiming_result(self):
        with self.assertRaisesRegex(ValueError, "precision"):
            minimum_decode_deadline([1, 0.05, 0.05], resolution_s=1e-30)
        with self.assertRaisesRegex(ValueError, "search range"):
            minimum_decode_deadline([1, 2e10])


class StreamingTests(unittest.TestCase):
    def test_comments_crlf_multiline_and_eof(self):
        self.assertEqual(
            list(sse_data([": ping\r\n", "data: first\r\n", "data: second\r\n", "\r\n",
                           "event: ignored", "data: last"])),
            ["first\nsecond", "last"],
        )

    def test_empty_field_flood_is_bounded(self):
        with self.assertRaises(StreamProtocolError):
            list(sse_data(["data:"] * 100, max_event_chars=8))

    def test_event_values_and_limits_are_bounded(self):
        with self.assertRaises(StreamProtocolError):
            list(sse_data(["data: 12345"], max_event_chars=4))
        with self.assertRaises(ValueError):
            list(sse_data([], max_event_chars=0))

    def test_payload_errors_and_done(self):
        self.assertIsNone(decode_payload("[DONE]"))
        for payload in ("not json", "[]", '{"error":"failed"}'):
            with self.subTest(payload=payload), self.assertRaises(StreamProtocolError):
                decode_payload(payload)

    def test_generated_channels_not_role_or_usage(self):
        event = {"choices": [{"delta": {"role": "assistant", "content": "hi",
                                        "reasoning_content": "thinking"}}]}
        self.assertEqual(generated_deltas(event), [("reasoning_content", "thinking"),
                                                 ("content", "hi")])
        self.assertEqual(generated_deltas({"usage": {"completion_tokens": 100}}), [])
        with self.assertRaises(StreamProtocolError):
            generated_deltas({"choices": [{"delta": {"content": 123}}]})


class SmokeTests(unittest.TestCase):
    @staticmethod
    def stream(*, done=True, generated=True, finish="stop"):
        events = [
            {"choices": [{"delta": {"role": "assistant"}}]},
            {"choices": [{"delta": {"content": "hi"} if generated else {},
                          "finish_reason": finish}]},
        ]
        text = "".join("data: " + json.dumps(event) + "\n\n" for event in events)
        return text + ("data: [DONE]\n\n" if done else "")

    def run_stream(self, text, mime="text/event-stream"):
        def handler(request):
            self.assertEqual(request.url.path, "/v1/chat/completions")
            self.assertTrue(json.loads(request.content)["stream"])
            return httpx.Response(200, text=text, headers={"content-type": mime})
        with httpx.Client(transport=httpx.MockTransport(handler)) as client:
            return check_stream(client, "http://localhost", "test-model", 1)

    def test_complete_stream_records_events_but_no_token_count(self):
        result = self.run_stream(self.stream())
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["output"]["content"], "hi")
        self.assertIsNone(result["token_count"])
        self.assertEqual(result["generated_event_count"], 1)

    def test_incomplete_empty_and_unfinished_streams_rejected(self):
        for settings in ({"done": False}, {"generated": False}, {"finish": None}):
            with self.subTest(settings=settings), self.assertRaises(StreamProtocolError):
                self.run_stream(self.stream(**settings))
        with self.assertRaises(StreamProtocolError):
            self.run_stream(self.stream(), mime="application/json")

    def test_readiness_requires_nonempty_model_id(self):
        def handler(request):
            self.assertEqual(request.url.path, "/v1/models")
            return httpx.Response(200, json={"data": [{"id": "test-model"}]})
        with httpx.Client(transport=httpx.MockTransport(handler)) as client:
            self.assertEqual(wait_for_model(client, "http://localhost", 1), "test-model")

    def test_duration_rejects_nan_zero_and_infinity(self):
        for value in ("nan", "inf", "0", "-1"):
            with self.subTest(value=value), self.assertRaises(argparse.ArgumentTypeError):
                positive_seconds(value)


class BaselineTests(unittest.TestCase):
    def setUp(self):
        self.lock = load_lock()

    def test_lock_pins_and_build_context(self):
        command = build_command(self.lock, "test-image")
        self.assertIn("BASE_IMAGE=" + self.lock["image"], command)
        self.assertEqual(command[-1], str(ROOT))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "lock.json"
            path.write_text(json.dumps({**self.lock, "image": "mutable:latest"}))
            with self.assertRaises(ValueError):
                load_lock(path)

    def test_start_uses_readonly_weights_and_loopback(self):
        command = start_command(self.lock, Path("/tmp/model"), "/dev/dri/renderD128",
                                "test-image", "test-container", 8000, render_gid=44)
        self.assertIn("127.0.0.1:8000:8000", command)
        resolved = Path("/tmp/model").resolve()
        self.assertIn(f"type=bind,src={resolved},dst=/models/model,readonly", command)
        self.assertIn("no-new-privileges", command)
        self.assertEqual(command[command.index("--group-add") + 1], "44")
        self.assertNotIn("HF_TOKEN", " ".join(command))

    def test_bad_mount_device_and_port_rejected(self):
        for directory, device, port in (("/tmp/a,b", "/dev/dri/renderD128", 8000),
                                        ("/tmp/model", "/dev/mem", 8000),
                                        ("/tmp/model", "/dev/dri/renderD128", 0)):
            with self.subTest(directory=directory, device=device, port=port):
                with self.assertRaises(ValueError):
                    start_command(self.lock, Path(directory), device, "image", "name", port)

    def test_prepare_dry_run_has_no_download_or_docker_execution(self):
        with tempfile.TemporaryDirectory() as directory:
            model_dir = Path(directory) / "not-created"
            args = argparse.Namespace(model="smoke", model_dir=model_dir,
                                      dry_run=True, image="test-image")
            with patch("tools.baseline.subprocess.run") as run:
                prepare(args, self.lock)
                run.assert_not_called()
            self.assertFalse(model_dir.exists())

    def test_incomplete_and_wrong_snapshot_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            (path / "config.json").write_text("{}")
            marker = path / ".abstract-model.json"
            model = self.lock["models"]["smoke"]
            for contents in ({**model, "status": "preparing"},
                             {**model, "status": "complete", "revision": "0" * 40}):
                marker.write_text(json.dumps(contents))
                with self.subTest(contents=contents), self.assertRaises(ValueError):
                    validate_model_dir(path, self.lock)
            marker.write_text(json.dumps({**model, "status": "complete"}))
            validate_model_dir(path, self.lock)


class BudgetTests(unittest.TestCase):
    def setUp(self):
        self.config = tomllib.loads((ROOT / "budgets.toml").read_text())

    def test_each_task_has_separate_allowance_and_no_official_workload(self):
        caps = {"benchmark-design": (50, 12), "harness-design": (200, 64),
                "compute-quant": (50, 0), "puzzle-design": (5, 0)}
        for task in TASKS:
            with self.subTest(task=task):
                result = estimate(self.config, task)
                self.assertEqual((result["candidate_api_cap_usd"],
                                  result["candidate_gpu_hour_cap"]), caps[task])
                self.assertEqual(result["benchmark"], {})
                self.assertEqual(result["status"], "planning-only-unmeasured")
                json.dumps(result, allow_nan=False)

    def test_cpu_tasks_need_no_quote_and_gpu_costs_are_explicit(self):
        for task in ("compute-quant", "puzzle-design"):
            result = estimate(self.config, task)
            self.assertEqual(result["pricing_status"], "not-needed-no-gpu")
            self.assertEqual(result["candidate_compute_cost_usd"], 0)
        self.assertIsNone(estimate(self.config, "harness-design")["candidate_compute_cost_usd"])
        self.assertEqual(estimate(self.config, "harness-design", 2)["candidate_compute_cost_usd"],
                         128)

    def test_invalid_quotes_and_task_rejected(self):
        for rate in (0, -1, math.inf, math.nan):
            with self.subTest(rate=rate), self.assertRaises(ValueError):
                estimate(self.config, "harness-design", rate)
        with self.assertRaises(ValueError):
            estimate(self.config, "unknown")


if __name__ == "__main__":
    unittest.main()
