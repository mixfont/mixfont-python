# Publishing

The PyPI package name is `mixfont`.

Before publishing:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip build twine
PYTHONPATH=src python -m unittest discover -s tests
python -m build
python -m twine check dist/*
```

Publish:

```sh
python -m twine upload dist/*
```

Use TestPyPI for a dry run before the first production release:

```sh
python -m twine upload --repository testpypi dist/*
```

PyPI versions are immutable, so a published version cannot be reused.

For automated releases later, configure PyPI trusted publishing from GitHub
Actions instead of storing a long-lived PyPI token.
