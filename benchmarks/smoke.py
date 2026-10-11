"""Development connectivity/protocol check. No correctness gate or performance score."""

import argparse
import json
import math
import time
from pathlib import Path
from typing import Any

import httpx

from benchmarks.streaming import StreamProtocolError, decode_payload, generated_deltas, sse_data


def positive_seconds(value: str) -> float:
    number = float(value)
    if not math.isfinite(number) or number <= 0:
        raise argparse.ArgumentTypeError("duration must be finite and positive")
    return number


def wait_for_model(client: httpx.Client, base_url: str, wait_s: float) -> str:
    deadline = time.monotonic() + wait_s
    last_error = "no readiness response"
    while time.monotonic() < deadline:
        try:
            response = client.get(
                base_url + "/v1/models", timeout=min(5.0, deadline - time.monotonic())
            )
            response.raise_for_status()
            models = response.json().get("data", [])
            model = (
                models[0].get("id")
                if isinstance(models, list) and models and isinstance(models[0], dict) else None
            )
            if not isinstance(model, str) or not model:
                raise StreamProtocolError("readiness response has no usable model id")
            return model
        except (httpx.HTTPError, ValueError, AttributeError, TypeError) as exc:
            last_error = str(exc)
            time.sleep(min(0.25, max(0.0, deadline - time.monotonic())))
    raise TimeoutError(f"model not ready after {wait_s}s: {last_error}")


def check_stream(
    client: httpx.Client, base_url: str, model: str, timeout_s: float
) -> dict[str, Any]:
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": "Reply with a short greeting."}],
        "temperature": 0,
        "max_tokens": 64,
        "stream": True,
    }
    started = time.monotonic()
    events = []
    output = {channel: [] for channel in ("content", "reasoning_content")}
    done = False
    finish_reason = first_generated_text_s = None
    payload_chars = generated_event_count = 0
    with client.stream(
        "POST", base_url + "/v1/chat/completions", json=payload, timeout=timeout_s
    ) as response:
        response.raise_for_status()
        if "text/event-stream" not in response.headers.get("content-type", ""):
            raise StreamProtocolError("response is not text/event-stream")
        first_headers_s = time.monotonic() - started

        def bounded_lines():
            for line in response.iter_lines():
                if time.monotonic() - started > timeout_s:
                    raise TimeoutError("stream exceeded total smoke request timeout")
                yield line

        for raw in sse_data(bounded_lines()):
            payload_chars += len(raw)
            if payload_chars > 8_388_608 or len(events) >= 10_000:
                raise StreamProtocolError("smoke stream exceeded its bounded capture limit")
            received_s = time.monotonic() - started
            event = decode_payload(raw)
            if event is None:
                done = True
                break
            deltas = generated_deltas(event)  # Events are not model tokens.
            events.append({"received_s": received_s, "payload": event})
            if deltas:
                if first_generated_text_s is None:
                    first_generated_text_s = received_s
                generated_event_count += 1
                for channel, text in deltas:
                    output[channel].append(text)
            choices = event.get("choices", [])
            if choices and choices[0].get("finish_reason") is not None:
                finish_reason = choices[0]["finish_reason"]
    if not done or finish_reason not in ("stop", "length") or not generated_event_count:
        raise StreamProtocolError(
            "stream needs generated text, stop/length finish reason, and [DONE]"
        )
    return {
        "status": "ok",
        "kind": "protocol-smoke-only-not-a-performance-score",
        "model": model,
        "first_headers_s": first_headers_s,
        "first_generated_text_s": first_generated_text_s,
        "completed_stream_s": time.monotonic() - started,
        "finish_reason": finish_reason,
        "generated_event_count": generated_event_count,
        "token_count": None,
        "output": {channel: "".join(parts) for channel, parts in output.items()},
        "events": events,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    parser.add_argument("--wait-seconds", type=positive_seconds, default=900.0)
    parser.add_argument("--request-timeout-seconds", type=positive_seconds, default=120.0)
    parser.add_argument("--out", type=Path, default=Path("results/smoke.json"))
    args = parser.parse_args()
    url = args.base_url.rstrip("/")
    try:
        # Don't silently route local traffic through the user's HTTP_PROXY.
        with httpx.Client(trust_env=False) as client:
            model = wait_for_model(client, url, args.wait_seconds)
            result = check_stream(client, url, model, args.request_timeout_seconds)
    except (httpx.HTTPError, ValueError, TimeoutError) as exc:
        result = {"status": "error", "kind": "protocol-smoke-only", "error": str(exc)}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "artifact": str(args.out)}))
    return 0 if result["status"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
