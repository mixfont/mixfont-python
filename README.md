<p align="center">
  <img src="https://static.mixfont.com/assets/20260604-033721-image-4hk1jdqm.webp" alt="Mixfont banner" width="1280" />
</p>

<h1 align="center">State-of-the-art AI Font Generation Model</h1>

<p align="center">
  Official Mixfont Python SDK
</p>

<p align="center">
  <a href="https://www.mixfont.com"><img src="https://img.shields.io/badge/Website-mixfont.com-111111" alt="Mixfont website" /></a>
  <a href="https://github.com/mixfont"><img src="https://img.shields.io/badge/GitHub-mixfont-111111" alt="Mixfont GitHub" /></a>
  <a href="https://x.com/mixfont"><img src="https://img.shields.io/badge/X-@mixfont-111111" alt="Mixfont on X" /></a>
</p>

<p align="center">
  <a href="#examples">Examples</a> |
  <a href="#supported-platforms">Supported platforms</a> |
  <a href="#how-font-generation-works">How it works</a> |
  <a href="#model-inputs-and-outputs">Model inputs</a> |
  <a href="#usage">Usage</a>
</p>

<hr />

The official Python SDK for the [Mixfont](https://www.mixfont.com) AI font generation API. It lets you
create AI-generated font files from Python applications and scripts.

Mixfont is a frontier AI lab developing generative AI for fonts. The Mixfont [font generation](https://www.mixfont.com/font-generator) model creates complete, web-safe TTF font files from a natural-language prompt or a public reference image, so applications can turn generated lettering, sketches, logos, or visual references into editable type instead of a flat image. Fonts generated via the API are unique and licensed for commercial use.

For more information, see the [Mixfont website](https://www.mixfont.com) and the [full Mixfont documentation](https://www.mixfont.com/docs).

<hr />

## Examples

These examples show prompt and image inputs paired with generated font files from Mixfont.

<table>
  <thead>
    <tr>
      <th align="left" width="30%">Input</th>
      <th align="left" width="70%">Generated font preview</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        generate a font for a soccer team logo. Make the letterforms soccer themed, bold, and unique.
      </td>
      <td>
        <img src="https://static.mixfont.com/assets/20260604-035208-image-8ttcinix.webp" alt="Cipher Striker Ultra generated font preview" width="480" /><br />
        <a href="https://static.mixfont.com/assets/20260603-224831-font-001-cipherstrikerultra-regular-1uj742pz.ttf">Download Cipher-Striker-Ultra.ttf</a>
      </td>
    </tr>
    <tr>
      <td>
        <img src="https://static.mixfont.com/assets/20260603-230108-image-e3prnt68.webp" alt="Wuthering Heights input example" width="220" />
      </td>
      <td>
        <img src="https://static.mixfont.com/assets/20260604-035246-image-l75vnkaz.webp" alt="Wuthering Heights Display generated font preview" width="480" /><br />
        <a href="https://static.mixfont.com/assets/20260603-230122-font-001-generatedfont-regular-1-yrpido7g.ttf">Download Wuthering-Heights-Display.ttf</a>
      </td>
    </tr>
    <tr>
      <td>
        <img src="https://static.mixfont.com/assets/20260603-210216-image-n06hmmov.webp" alt="Gossamer Editorial Serif input example" width="220" />
      </td>
      <td>
        <img src="https://static.mixfont.com/assets/20260604-035352-image-um7d7s4q.webp" alt="Gossamer Editorial Serif generated font preview" width="480" /><br />
        <a href="https://static.mixfont.com/assets/20260603-212006-font-001-gossamereditorialserif-regular-1-weyynop8.ttf">Download Gossamer-Editorial-Serif.ttf</a>
      </td>
    </tr>
    <tr>
      <td>
        <img src="https://static.mixfont.com/assets/20260603-225224-image-9sw57q4v.webp" alt="HANDY DAN'S Property Maintanence input example" width="220" />
      </td>
      <td>
        <img src="https://static.mixfont.com/assets/20260604-035258-image-hdz1y9zh.webp" alt="Dystopian Brush Stroke Display generated font preview" width="480" /><br />
        <a href="https://static.mixfont.com/assets/20260603-225219-font-001-dystopianbrushstrokedisplay-regular-chnivcf8.ttf">Download Dystopian-Brush-Stroke-Display.ttf</a>
      </td>
    </tr>
    <tr>
      <td>
        <img src="https://static.mixfont.com/assets/20260603-230210-image-5lg2741x.webp" alt="NASA logo input example" width="220" />
      </td>
      <td>
        <img src="https://static.mixfont.com/assets/20260604-035311-image-o2w16gf5.webp" alt="Dissonant Wave Sans generated font preview" width="480" /><br />
        <a href="https://static.mixfont.com/assets/20260603-230230-font-001-dissonantwavesans-regular-z9d7o2ui.ttf">Download Dissonant-Wave-Sans.ttf</a>
      </td>
    </tr>
    <tr>
      <td>
        <img src="https://static.mixfont.com/assets/20260603-230651-image-cgq0gjku.webp" alt="Natural handwriting input example" width="220" />
      </td>
      <td>
        <img src="https://static.mixfont.com/assets/20260604-035322-image-bz6cmt09.webp" alt="Zephyr Ink Script generated font preview" width="480" /><br />
        <a href="https://static.mixfont.com/assets/20260603-230724-font-001-zephyrinkscript-regular-81hj01mq.ttf">Download Zephyr-Ink-Script.ttf</a>
      </td>
    </tr>
  </tbody>
</table>

<br />

## Supported platforms

- Python >= 3.9
- Standard CPython environments with network access

<br />

## How font generation works

Font generation is asynchronous. Start a generation with exactly one input:

- `prompt`: a text description of the font to generate.
- `image_url`: a public HTTPS reference image for the style you want the model to follow.

The create call returns a generation `id` and, when available, a polling URL. Use `mixfont.generations.wait(...)` for built-in polling, or call `mixfont.generations.get(...)` yourself until the status reaches `succeeded`, `failed`, or `cancelled`. When a job succeeds, `ttf_url` contains the generated TTF download URL.

<br />

## Model inputs and outputs

Use text generation when you can describe the type direction, such as category, style, use case, spacing, contrast, or distinctive details. Use image generation when a visual reference is the clearest source of truth, such as a sketch, sign, logo, poster, screenshot, or existing design mockup.

Reference images should be publicly reachable HTTPS URLs that point to JPEG, PNG, or WebP files up to 20 MB. Clear images with readable letterforms, strong contrast, clean edges, and cropped text regions generally produce better results.

Generated font files are returned as TTFs. Download or persist the returned `ttf_url` after the job succeeds, then rehost the file in your own storage before using it in production. Returned TTF URLs are temporary and will be deleted within 24 hours.

<br />

## Create an API key

To start making calls to the API you'll need an API key. If you don't already have a Mixfont account, visit [Mixfont](https://www.mixfont.com) and sign in.

Go to the [Developer Console](https://www.mixfont.com/console/keys) to create your first API key. When calling the API, include the key in the `x-api-key` header for each request.

<img src="https://static.mixfont.com/assets/20260602-212442-image-d3bfvtw5.webp" alt="Developer Console Key Creation Flow" width="1280" />

Make sure to copy the API key to a safe place. The API key will only be visible in the dashboard once. If you lose your key, you'll have to create a new one.

<br />

## Installation

Install it from PyPI:

```sh
pip install mixfont
```

<br />

## Usage

For the full API documentation, see [Mixfont docs](https://www.mixfont.com/docs).

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

<br />

## API

<br />

### Constructor

```py
mixfont = Mixfont(api_key, timeout=30.0)
```

| Argument   | Type    | Description                                              |
| ---------- | ------- | -------------------------------------------------------- |
| `api_key`  | `str`   | Required. Mixfont API key.                               |
| `timeout`  | `float` | Optional request timeout in seconds. Defaults to `30.0`. |

<br />

### `mixfont.generations.create(...)`

Starts a new font generation and returns immediately.

| Argument    | Type                         | Description                                   |
| ----------- | ---------------------------- | --------------------------------------------- |
| `prompt`    | `str`                        | Text prompt for the generated font.           |
| `image_url` | `str`                        | Public HTTPS URL for a JPEG, PNG, or WebP reference image up to 20 MB. |
| `glyph_set` | `"standard"` or `"extended"` | Optional glyph set. Defaults to `standard`.   |

Provide exactly one of `prompt` or `image_url`.

<br />

### Glyph sets

| Glyph set  | Best for                                               | Glyphs | Typical timing |
| ---------- | ------------------------------------------------------ | ------ | -------------- |
| `standard` | English concepting, prototypes, headings, and logos    | 72     | Around 25 seconds on average |
| `extended` | Production candidates for Latin-language text beyond English | 319 | 2-3 minutes |

`standard` includes English letters, numbers, and basic punctuation. `extended` supports all Latin languages, including special characters, and costs more API credits.

<br />

### `mixfont.generations.get(generation_id)`

Fetches the current status of a generation.

<br />

### `mixfont.generations.wait(generation_id, ...)`

Checks the generation until it reaches a terminal status.

| Argument           | Type    | Description                             |
| ------------------ | ------- | --------------------------------------- |
| `interval_seconds` | `float` | Polling interval. Defaults to `5.0`.    |
| `timeout_seconds`  | `float` | Maximum wait time. Defaults to `600.0`. |

`wait` returns the completed generation when it succeeds. It raises an error if
the generation fails, is cancelled, or times out.

<br />

## Best practices

Write specific prompts that describe the type category, visual style, intended use case, and distinctive details.

Start with `standard` when comparing directions, then use `extended` once you have a candidate worth testing more deeply.

Store the generation `id`, original prompt or image URL, and `glyph_set` with each result so your team can compare outputs later.

Test generated fonts in real content, including headings, numbers, punctuation, labels, and the longest strings your product needs to support.

Keep your API key on the server and read it from an environment variable such as `MIXFONT_API_KEY`.

<br />

## Development

```sh
PYTHONPATH=src python3 -m unittest discover -s tests
python3 -m build
```

<br />

## Links

- [Website](https://www.mixfont.com)
- [GitHub](https://github.com/mixfont)
- [X](https://x.com/mixfont)
