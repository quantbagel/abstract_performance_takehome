"""Small strict SSE parser. Events/chunks are deliberately NOT treated as tokens."""

import json
from collections.abc import Iterable, Iterator
from typing import Any


class StreamProtocolError(ValueError):
    pass


def sse_data(lines: Iterable[str], *, max_event_chars: int = 1_048_576) -> Iterator[str]:
    """Collect SSE data fields, bounding values AND separators (including empty fields)."""
    if max_event_chars <= 0:
        raise ValueError("SSE event size limit must be positive")
    fields: list[str] = []
    size = 0
    for raw in lines:
        line = raw.rstrip("\r\n")
        if not line:
            if fields:
                yield "\n".join(fields)
            fields, size = [], 0
            continue
        name, _, value = line.partition(":")
        if name != "data":  # Also skips comments and non-data fields.
            continue
        value = value.removeprefix(" ")
        size += len(value) + (1 if fields else 0)
        if size > max_event_chars:
            raise StreamProtocolError("SSE event exceeded the size limit")
        fields.append(value)
    # Accept a final event at EOF; the caller still requires an explicit [DONE].
    if fields:
        yield "\n".join(fields)


def decode_payload(payload: str) -> dict[str, Any] | None:
    """None represents [DONE]; invalid JSON/error envelopes fail loudly."""
    if payload == "[DONE]":
        return None
    try:
        event = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise StreamProtocolError("invalid SSE JSON") from exc
    if not isinstance(event, dict):
        raise StreamProtocolError("SSE JSON must be an object")
    if "error" in event:
        raise StreamProtocolError(f"server stream error: {event['error']}")
    return event


def generated_deltas(event: dict[str, Any]) -> list[tuple[str, str]]:
    """Return generated channels only, never role/usage/heartbeat as text."""
    choices = event.get("choices", [])
    if not isinstance(choices, list) or len(choices) > 1:
        raise StreamProtocolError("expected at most one streaming choice")
    if not choices:
        return []
    choice = choices[0]
    if not isinstance(choice, dict):
        raise StreamProtocolError("streaming choice must be an object")
    if choice.get("index", 0) != 0:
        raise StreamProtocolError("unexpected streaming choice index")
    delta = choice.get("delta", {})
    if not isinstance(delta, dict):
        raise StreamProtocolError("streaming delta must be an object")
    generated = []
    for channel in ("reasoning_content", "content"):
        text = delta.get(channel)
        if text is None or text == "":
            continue
        if not isinstance(text, str):
            raise StreamProtocolError(f"{channel} must be text")
        generated.append((channel, text))
    return generated
