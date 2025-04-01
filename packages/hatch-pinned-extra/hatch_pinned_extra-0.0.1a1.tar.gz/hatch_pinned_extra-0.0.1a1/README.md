# hatch-pinned-extra

[![image](https://img.shields.io/pypi/l/hatch-pinned-extras.svg)](https://pypi.python.org/pypi/hatch-pinned-extra)

Hatch plugin that adds a packaging [_extra_](https://packaging.python.org/en/latest/specifications/core-metadata/#provides-extra-multiple-use) to the wheel metadata with pinned dependencies from [`uv.lock`](https://docs.astral.sh/uv/guides/projects/#uvlock).

## Usage

```toml
# pyproject.toml
[build-system]
requires = [
    "hatchling",
    "hatch-pinned-extra",
]
build-backend = "hatchling.build"

[tool.hatch.metadata.hooks.pinned_extra]
name = "pinned"
```

If your package doesn't have any optional dependencies already, you will need to mark them as _dynamic_:

```toml
# pyproject.toml
[project]
dynamic = [
    "optional-dependencies",
]
```
