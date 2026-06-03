<img src="./assets/mixfont-banner.webp" alt="Mixfont banner" width="1280" />

# Mixfont Python client

A Python client for the [Mixfont](https://www.mixfont.com) API. It lets you
create AI-generated font files from Python applications and scripts.

Mixfont is a frontier AI lab developing generative AI for fonts. The Mixfont [font generation](https://www.mixfont.com/font-generator) model creates complete, web-safe TTF font files from a natural-language prompt or a public reference image, so applications can turn generated lettering, sketches, logos, or visual references into editable type instead of a flat image. Fonts generated via the API are unique and licensed for commercial use.

For more information, see the [Mixfont website](https://www.mixfont.com) and the [full Mixfont documentation](https://www.mixfont.com/docs).

## Supported platforms

- Python >= 3.9
- Standard CPython environments with network access

## How font generation works

Font generation is asynchronous. Start a generation with exactly one input:

- `prompt`: a text description of the font to generate.
- `image_url`: a public HTTPS reference image for the style you want the model to follow.

The create call returns a generation `id` and, when available, a polling URL. Use `mixfont.generations.wait(...)` for built-in polling, or call `mixfont.generations.get(...)` yourself until the status reaches `succeeded`, `failed`, or `cancelled`. When a job succeeds, `ttf_url` contains the generated TTF download URL.

## Model inputs and outputs

Use text generation when you can describe the type direction, such as category, style, use case, spacing, contrast, or distinctive details. Use image generation when a visual reference is the clearest source of truth, such as a sketch, sign, logo, poster, screenshot, or existing design mockup.

Reference images should be publicly reachable HTTPS URLs that point to JPEG, PNG, or WebP files up to 20 MB. Clear images with readable letterforms, strong contrast, clean edges, and cropped text regions generally produce better results.

Generated font files are returned as TTFs. Download or persist the returned `ttf_url` after the job succeeds, then rehost the file in your own storage before using it in production. Returned TTF URLs are temporary and will be deleted within 24 hours.

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

print(result["ttf_url"])
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
mixfont = Mixfont(api_key, timeout=30.0)
```

| Argument   | Type    | Description                                              |
| ---------- | ------- | -------------------------------------------------------- |
| `api_key`  | `str`   | Required. Mixfont API key.                               |
| `timeout`  | `float` | Optional request timeout in seconds. Defaults to `30.0`. |

### `mixfont.generations.create(...)`

Starts a new font generation and returns immediately.

| Argument    | Type                         | Description                                   |
| ----------- | ---------------------------- | --------------------------------------------- |
| `prompt`    | `str`                        | Text prompt for the generated font.           |
| `image_url` | `str`                        | Public HTTPS URL for a JPEG, PNG, or WebP reference image up to 20 MB. |
| `glyph_set` | `"standard"` or `"extended"` | Optional glyph set. Defaults to `standard`.   |

Provide exactly one of `prompt` or `image_url`.

### Glyph sets

| Glyph set  | Best for                                               | Glyphs | Typical timing |
| ---------- | ------------------------------------------------------ | ------ | -------------- |
| `standard` | English concepting, prototypes, headings, and logos    | 72     | Around 25 seconds on average |
| `extended` | Production candidates for Latin-language text beyond English | 319 | 2-3 minutes |

`standard` includes English letters, numbers, and basic punctuation. `extended` supports all Latin languages, including special characters, and costs more API credits.

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

## Best practices

- Write specific prompts that describe the type category, visual style, intended use case, and distinctive details.
- Start with `standard` when comparing directions, then use `extended` once you have a candidate worth testing more deeply.
- Store the generation `id`, original prompt or image URL, and `glyph_set` with each result so your team can compare outputs later.
- Test generated fonts in real content, including headings, numbers, punctuation, labels, and the longest strings your product needs to support.
- Keep your API key on the server and read it from an environment variable such as `MIXFONT_API_KEY`.

## Development

```sh
PYTHONPATH=src python3 -m unittest discover -s tests
python3 -m build
```

## Publishing

See [PUBLISHING.md](./PUBLISHING.md).
