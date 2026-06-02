from __future__ import annotations

import json
import math
import time
from typing import Any, Dict, Optional
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from mixfont.errors import (
    MixfontAPIError,
    MixfontError,
    MixfontGenerationCancelledError,
    MixfontGenerationError,
    MixfontTimeoutError,
)

DEFAULT_BASE_URL = "https://api.mixfont.com/v1"
DEFAULT_WAIT_INTERVAL_SECONDS = 5.0
DEFAULT_WAIT_TIMEOUT_SECONDS = 10 * 60.0

JsonObject = Dict[str, Any]


class Mixfont:
    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = 30.0,
    ) -> None:
        api_key = api_key.strip()

        if not api_key:
            raise MixfontError("A Mixfont API key is required.")

        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self.generations = GenerationsClient(self)

    def _request(
        self,
        method: str,
        path: str,
        *,
        body: Optional[JsonObject] = None,
    ) -> JsonObject:
        data = None if body is None else json.dumps(body).encode("utf-8")
        headers = {
            "Accept": "application/json",
            "User-Agent": "mixfont-python/0.1.0",
            "x-api-key": self._api_key,
        }

        if data is not None:
            headers["Content-Type"] = "application/json"

        request = Request(
            f"{self._base_url}{path}",
            data=data,
            headers=headers,
            method=method,
        )

        try:
            with urlopen(request, timeout=self._timeout) as response:
                return _read_json_body(response)
        except HTTPError as error:
            body_data = _read_json_body(error)
            raise MixfontAPIError(
                _read_error_message(body_data)
                or f"Mixfont request failed with status {error.code}.",
                status_code=error.code,
                body=body_data,
            ) from None
        except URLError as error:
            raise MixfontError(f"Mixfont request failed: {error.reason}") from error


class GenerationsClient:
    def __init__(self, client: Mixfont) -> None:
        self._client = client

    def create(
        self,
        *,
        prompt: Optional[str] = None,
        image_url: Optional[str] = None,
        glyph_set: Optional[str] = None,
        font_name: Optional[str] = None,
    ) -> JsonObject:
        has_prompt = _has_text(prompt)
        has_image_url = _has_text(image_url)

        if has_prompt == has_image_url:
            raise MixfontError("Provide exactly one of prompt or image_url.")

        body: JsonObject = {}
        path = "/font-generations/text"

        if has_prompt:
            body["prompt"] = prompt
        else:
            body["image_url"] = image_url
            path = "/font-generations/image"

        if glyph_set is not None:
            body["glyph_set"] = glyph_set

        if font_name is not None:
            body["font_name"] = font_name

        return self._client._request("POST", path, body=body)

    def get(self, generation_id: str) -> JsonObject:
        generation_id = _normalize_generation_id(generation_id)

        return self._client._request(
            "GET",
            f"/font-generations/{quote(generation_id, safe='')}",
        )

    def wait(
        self,
        generation_id: str,
        *,
        interval_seconds: float = DEFAULT_WAIT_INTERVAL_SECONDS,
        timeout_seconds: float = DEFAULT_WAIT_TIMEOUT_SECONDS,
    ) -> JsonObject:
        _validate_positive_number(interval_seconds, "interval_seconds")
        _validate_positive_number(timeout_seconds, "timeout_seconds")

        started_at = time.monotonic()
        last_generation: Optional[JsonObject] = None

        while time.monotonic() - started_at <= timeout_seconds:
            last_generation = self.get(generation_id)
            status = last_generation.get("status")

            if status == "succeeded":
                return last_generation

            if status == "failed":
                raise MixfontGenerationError(
                    last_generation.get("error") or "Font generation failed.",
                    generation=last_generation,
                )

            if status == "cancelled":
                raise MixfontGenerationCancelledError(
                    "Font generation was cancelled.",
                    generation=last_generation,
                )

            elapsed_seconds = time.monotonic() - started_at
            remaining_seconds = timeout_seconds - elapsed_seconds

            if remaining_seconds <= 0:
                break

            time.sleep(min(interval_seconds, remaining_seconds))

        raise MixfontTimeoutError(
            f"Timed out waiting for Mixfont generation {generation_id}.",
            generation=last_generation,
        )


def _has_text(value: Optional[str]) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _normalize_generation_id(generation_id: str) -> str:
    generation_id = generation_id.strip()

    if not generation_id:
        raise MixfontError("A Mixfont generation id is required.")

    return generation_id


def _validate_positive_number(value: float, name: str) -> None:
    if not math.isfinite(value) or value <= 0:
        raise MixfontError(f"{name} must be a positive number.")


def _read_json_body(response: Any) -> JsonObject:
    raw_body = response.read()

    if not raw_body:
        return {}

    try:
        body = json.loads(raw_body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return {}

    return body if isinstance(body, dict) else {}


def _read_error_message(body: JsonObject) -> Optional[str]:
    error = body.get("error")

    if isinstance(error, str) and error.strip():
        return error

    return None
