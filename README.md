<img src="./assets/mixfont-banner.webp" alt="Mixfont banner" width="1280" />

# Mixfont Python client

A Python client for the [Mixfont](https://www.mixfont.com) API. It lets you
generate AI-generated font files from Python applications and scripts. Mixfont is a frontier AI [font generation](https://www.mixfont.com/font-generator) model that allows users to create custom fonts in seconds. For more information, see the [Mixfont website](https://www.mixfont.com) and the [API documentation](https://www.mixfont.com/docs).

## Supported platforms

- Python >= 3.9
- Standard CPython environments with network access

## Installation

Install it from PyPI:

```sh
pip install mixfont
```

## Usage

Import the package:

```py
from mixfont import Mixfont
```

Instantiate the client:

```py
import os

mixfont = Mixfont(api_key=os.environ["MIXFONT_API_KEY"])
```

Create a font generation:

```py
generation = mixfont.generations.create(
    prompt="A condensed sci-fi display font",
    glyph_set="standard",
)

print(generation["id"])
```

Fetch the generation later:

```py
generation = mixfont.generations.get("generation_id")

print(generation["status"], generation["progress_percent"])
```

Or wait for the generation to finish:

```py
result = mixfont.generations.wait(generation["id"])

print(result["fonts"][0]["url"])
```

Create a generation from a reference image:

```py
generation = mixfont.generations.create(
    image_url="https://example.com/reference.png",
)
```

## API

### Constructor

```py
mixfont = Mixfont(api_key, base_url="https://api.mixfont.com/v1", timeout=30.0)
```

| Argument   | Type    | Description                                              |
| ---------- | ------- | -------------------------------------------------------- |
| `api_key`  | `str`   | Required. Mixfont API key.                               |
| `base_url` | `str`   | Optional. Defaults to `https://api.mixfont.com/v1`.      |
| `timeout`  | `float` | Optional request timeout in seconds. Defaults to `30.0`. |

### `mixfont.generations.create(...)`

Starts a new font generation and returns immediately.

| Argument    | Type                         | Description                                   |
| ----------- | ---------------------------- | --------------------------------------------- |
| `prompt`    | `str`                        | Text prompt for the generated font.           |
| `image_url` | `str`                        | Public URL for a reference image.             |
| `glyph_set` | `"standard"` or `"extended"` | Optional glyph set.                           |
| `font_name` | `str`                        | Optional display name for the generated font. |

Provide exactly one of `prompt` or `image_url`.

### `mixfont.generations.get(generation_id)`

Fetches the current status of a generation.

### `mixfont.generations.wait(generation_id, ...)`

Checks the generation until it reaches a terminal status.

| Argument           | Type    | Description                             |
| ------------------ | ------- | --------------------------------------- |
| `interval_seconds` | `float` | Polling interval. Defaults to `5.0`.    |
| `timeout_seconds`  | `float` | Maximum wait time. Defaults to `600.0`. |

`wait` returns the completed generation when it succeeds. It raises an error if
the generation fails, is cancelled, or times out.

## Development

```sh
PYTHONPATH=src python3 -m unittest discover -s tests
python3 -m build
```

## Publishing

See [PUBLISHING.md](./PUBLISHING.md).
