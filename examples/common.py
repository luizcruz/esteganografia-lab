from __future__ import annotations

import json
from typing import Any


def step(title: str, explanation: str, value: Any = None, kind: str = "text") -> dict:
    item = {"title": title, "explanation": explanation, "kind": kind}
    if value is not None:
        item["value"] = value
    return item


def result(steps: list[dict], final: str | None = None, note: str | None = None) -> dict:
    payload = {"steps": steps}
    if final is not None:
        payload["final"] = final
    if note is not None:
        payload["note"] = note
    return payload


def cli_main(run):
    print(json.dumps(run(), ensure_ascii=False, indent=2, default=str))
