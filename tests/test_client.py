import json
import unittest
from unittest.mock import patch

from mixfont import Mixfont, MixfontGenerationError


def api_generation(**overrides):
    generation = {
        "id": "gen_123",
        "status": "queued",
        "input_type": "text",
        "glyph_set": "standard",
        "progress_percent": 0,
        "fonts": [],
        "error": None,
        "created_at": "2026-06-02T00:00:00.000Z",
    }
    generation.update(overrides)
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
                    credits_charged=15,
                    poll_url="https://api.test/v1/font-generations/gen_123",
                )
            )

        with patch("mixfont.client.urlopen", fake_urlopen):
            client = Mixfont("test-key", base_url="https://api.test/v1")
            generation = client.generations.create(
                prompt="A condensed sci-fi display font",
                glyph_set="extended",
                font_name="Demo",
            )

        request, timeout = calls[0]

        self.assertEqual(
            request.full_url,
            "https://api.test/v1/font-generations/text",
        )
        self.assertEqual(request.get_method(), "POST")
        self.assertEqual(timeout, 30.0)
        self.assertEqual(
            json.loads(request.data.decode("utf-8")),
            {
                "prompt": "A condensed sci-fi display font",
                "glyph_set": "extended",
                "font_name": "Demo",
            },
        )
        self.assertEqual(generation["id"], "gen_123")
        self.assertEqual(generation["credits_charged"], 15)

    def test_creates_image_generation(self):
        calls = []

        def fake_urlopen(request, timeout):
            calls.append(request)
            return FakeResponse(api_generation(input_type="image"))

        with patch("mixfont.client.urlopen", fake_urlopen):
            client = Mixfont("test-key", base_url="https://api.test/v1")
            client.generations.create(image_url="https://example.com/reference.png")

        self.assertEqual(
            calls[0].full_url,
            "https://api.test/v1/font-generations/image",
        )
        self.assertEqual(
            json.loads(calls[0].data.decode("utf-8")),
            {"image_url": "https://example.com/reference.png"},
        )

    def test_gets_generation(self):
        def fake_urlopen(request, timeout):
            self.assertEqual(
                request.full_url,
                "https://api.test/v1/font-generations/gen_123",
            )
            self.assertEqual(request.get_method(), "GET")
            return FakeResponse(api_generation())

        with patch("mixfont.client.urlopen", fake_urlopen):
            client = Mixfont("test-key", base_url="https://api.test/v1")
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
                    fonts=(
                        [{"name": "Demo", "url": "https://static.test/demo.ttf"}]
                        if status == "succeeded"
                        else []
                    ),
                )
            )

        with patch("mixfont.client.urlopen", fake_urlopen):
            client = Mixfont("test-key", base_url="https://api.test/v1")
            generation = client.generations.wait(
                "gen_123",
                interval_seconds=0.001,
                timeout_seconds=1,
            )

        self.assertEqual(generation["status"], "succeeded")
        self.assertEqual(generation["fonts"][0]["url"], "https://static.test/demo.ttf")

    def test_wait_throws_when_generation_fails(self):
        def fake_urlopen(request, timeout):
            return FakeResponse(
                api_generation(status="failed", error="Could not generate font.")
            )

        with patch("mixfont.client.urlopen", fake_urlopen):
            client = Mixfont("test-key", base_url="https://api.test/v1")

            with self.assertRaises(MixfontGenerationError):
                client.generations.wait(
                    "gen_123",
                    interval_seconds=0.001,
                    timeout_seconds=1,
                )


if __name__ == "__main__":
    unittest.main()
