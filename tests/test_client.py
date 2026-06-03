import json
import unittest
from unittest.mock import patch

from mixfont import Mixfont, MixfontGenerationError

DEFAULT_BASE_URL = "https://api.mixfont.com/v1"


def api_generation(**overrides):
    created_at = overrides.pop("created_at", "2026-06-02T00:00:00.000Z")
    poll_url = overrides.pop("poll_url", None)
    error = overrides.pop("error", None)
    generation = {
        "id": overrides.pop("id", "gen_123"),
        "name": overrides.pop("name", "Demo"),
        "ttf_url": overrides.pop("ttf_url", None),
        "status": overrides.pop("status", "queued"),
        "input_type": overrides.pop("input_type", "text"),
        "glyph_set": overrides.pop("glyph_set", "standard"),
        "progress_percent": overrides.pop("progress_percent", 0),
    }
    generation.update(overrides)

    if poll_url is not None:
        generation["poll_url"] = poll_url

    if error is not None:
        generation["error"] = error

    generation["created_at"] = created_at
    return generation


class FakeResponse:
    def __init__(self, body):
        self._body = json.dumps(body).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        return False

    def read(self):
        return self._body


class MixfontClientTest(unittest.TestCase):
    def test_creates_text_generation(self):
        calls = []

        def fake_urlopen(request, timeout):
            calls.append((request, timeout))
            return FakeResponse(
                api_generation(
                    poll_url=f"{DEFAULT_BASE_URL}/font-generations/gen_123",
                )
            )

        with patch("mixfont.client.urlopen", fake_urlopen):
            client = Mixfont("test-key")
            generation = client.generations.create(
                prompt="A condensed sci-fi display font",
                glyph_set="extended",
            )

        request, timeout = calls[0]

        self.assertEqual(
            request.full_url,
            f"{DEFAULT_BASE_URL}/font-generations/text",
        )
        self.assertEqual(request.get_method(), "POST")
        self.assertEqual(timeout, 30.0)
        self.assertEqual(
            json.loads(request.data.decode("utf-8")),
            {
                "prompt": "A condensed sci-fi display font",
                "glyph_set": "extended",
            },
        )
        self.assertEqual(generation["id"], "gen_123")
        self.assertEqual(
            list(generation.keys()),
            [
                "id",
                "name",
                "ttf_url",
                "status",
                "input_type",
                "glyph_set",
                "progress_percent",
                "poll_url",
                "created_at",
            ],
        )

    def test_creates_image_generation(self):
        calls = []

        def fake_urlopen(request, timeout):
            calls.append(request)
            return FakeResponse(api_generation(input_type="image"))

        with patch("mixfont.client.urlopen", fake_urlopen):
            client = Mixfont("test-key")
            client.generations.create(image_url="https://example.com/reference.png")

        self.assertEqual(
            calls[0].full_url,
            f"{DEFAULT_BASE_URL}/font-generations/image",
        )
        self.assertEqual(
            json.loads(calls[0].data.decode("utf-8")),
            {"image_url": "https://example.com/reference.png"},
        )

    def test_gets_generation(self):
        def fake_urlopen(request, timeout):
            self.assertEqual(
                request.full_url,
                f"{DEFAULT_BASE_URL}/font-generations/gen_123",
            )
            self.assertEqual(request.get_method(), "GET")
            return FakeResponse(api_generation())

        with patch("mixfont.client.urlopen", fake_urlopen):
            client = Mixfont("test-key")
            generation = client.generations.get("gen_123")

        self.assertEqual(generation["id"], "gen_123")

    def test_waits_until_generation_succeeds(self):
        statuses = ["running", "succeeded"]

        def fake_urlopen(request, timeout):
            status = statuses.pop(0)
            return FakeResponse(
                api_generation(
                    status=status,
                    progress_percent=100 if status == "succeeded" else 40,
                    ttf_url=(
                        "https://static.test/demo.ttf"
                        if status == "succeeded"
                        else None
                    ),
                )
            )

        with patch("mixfont.client.urlopen", fake_urlopen):
            client = Mixfont("test-key")
            generation = client.generations.wait(
                "gen_123",
                interval_seconds=0.001,
                timeout_seconds=1,
            )

        self.assertEqual(generation["status"], "succeeded")
        self.assertEqual(generation["name"], "Demo")
        self.assertEqual(generation["ttf_url"], "https://static.test/demo.ttf")
        self.assertEqual(
            list(generation.keys()),
            [
                "id",
                "name",
                "ttf_url",
                "status",
                "input_type",
                "glyph_set",
                "progress_percent",
                "created_at",
            ],
        )

    def test_wait_throws_when_generation_fails(self):
        def fake_urlopen(request, timeout):
            return FakeResponse(
                api_generation(status="failed", error="Could not generate font.")
            )

        with patch("mixfont.client.urlopen", fake_urlopen):
            client = Mixfont("test-key")

            with self.assertRaises(MixfontGenerationError):
                client.generations.wait(
                    "gen_123",
                    interval_seconds=0.001,
                    timeout_seconds=1,
                )


if __name__ == "__main__":
    unittest.main()
