#!/usr/bin/env python3
"""
Validate Ollama connectivity and API key by calling the models endpoint.

Usage:
  python scripts/check_ollama_api.py
  python scripts/check_ollama_api.py --base-url https://ollama.com/api --api-key <KEY>
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any
from pathlib import Path

import requests

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config.settings import settings


def build_tags_url(base_url: str) -> str:
    base = base_url.rstrip("/")
    if base.endswith("/api"):
        return f"{base}/tags"
    return f"{base}/api/tags"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check Ollama API key and endpoint.")
    parser.add_argument(
        "--base-url",
        default=settings.OLLAMA_BASE_URL,
        help="Ollama base URL (defaults to OLLAMA_BASE_URL).",
    )
    parser.add_argument(
        "--api-key",
        default=settings.OLLAMA_API_KEY,
        help="Ollama API key (defaults to OLLAMA_API_KEY).",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=20,
        help="Request timeout in seconds (default: 20).",
    )
    return parser.parse_args()


def short_json(data: Any, limit: int = 300) -> str:
    text = json.dumps(data, ensure_ascii=True)
    if len(text) <= limit:
        return text
    return f"{text[:limit]}..."


def main() -> int:
    args = parse_args()

    base_url = (args.base_url or "").strip()
    api_key = (args.api_key or "").strip()
    if not base_url:
        print("FAIL: Missing OLLAMA_BASE_URL.")
        return 2
    if not api_key:
        print("FAIL: Missing OLLAMA_API_KEY.")
        return 2

    tags_url = build_tags_url(base_url)
    headers = {"Authorization": f"Bearer {api_key}"}

    print(f"Checking Ollama endpoint: {tags_url}")
    try:
        resp = requests.get(tags_url, headers=headers, timeout=args.timeout)
    except requests.RequestException as exc:
        print(f"FAIL: Network error: {exc}")
        return 3

    if resp.status_code == 200:
        try:
            payload = resp.json()
        except ValueError:
            print("FAIL: HTTP 200 but response is not JSON.")
            return 4

        models = payload.get("models", []) if isinstance(payload, dict) else []
        names = [m.get("name") for m in models if isinstance(m, dict) and m.get("name")]
        print("OK: Ollama API key is valid and endpoint is reachable.")
        print(f"Models visible: {len(names)}")
        if names:
            preview = ", ".join(names[:5])
            print(f"Sample models: {preview}")
        return 0

    if resp.status_code in (401, 403):
        print(f"FAIL: Authentication error ({resp.status_code}). Check OLLAMA_API_KEY.")
        return 5

    if resp.status_code == 404:
        print("FAIL: Endpoint not found (404). Check OLLAMA_BASE_URL.")
        print("Hint: cloud base URL is usually https://ollama.com/api")
        return 6

    body_preview = resp.text[:300].strip()
    if not body_preview:
        body_preview = "<empty>"
    print(f"FAIL: Unexpected status {resp.status_code}. Response: {body_preview}")
    return 7


if __name__ == "__main__":
    raise SystemExit(main())
