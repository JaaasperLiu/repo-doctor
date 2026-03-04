"""Config file loading for .repo-doctor.yml."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def load_config(repo_path: Path) -> dict[str, Any]:
    """Load .repo-doctor.yml from repo root. Returns empty dict if missing."""
    config_path = repo_path / ".repo-doctor.yml"
    if not config_path.exists():
        return {}

    try:
        data = yaml.safe_load(config_path.read_text())
        return data if isinstance(data, dict) else {}
    except (yaml.YAMLError, OSError):
        return {}


def merge_config(
    config: dict[str, Any],
    *,
    only: list[str] | None = None,
    skip: list[str] | None = None,
    format: str = "both",
    strict: bool = False,
    license: str = "mit",
    ci: str = "github-actions",
    readme: str = "standard",
    output_dir: str | None = None,
) -> dict[str, Any]:
    """Merge config file values with CLI flags. CLI flags take precedence."""
    merged: dict[str, Any] = {}

    # Config file values (defaults)
    merged["only"] = config.get("only")
    merged["skip"] = config.get("skip", [])
    merged["format"] = config.get("format", "both")
    merged["strict"] = config.get("strict", False)
    merged["license"] = config.get("license", "mit")
    merged["ci"] = config.get("ci", "github-actions")
    merged["readme"] = config.get("readme", "standard")
    merged["output_dir"] = config.get("output_dir")

    # CLI flag overrides (only override if not default)
    if only is not None:
        merged["only"] = only
    if skip is not None and len(skip) > 0:
        merged["skip"] = skip
    if format != "both":
        merged["format"] = format
    if strict:
        merged["strict"] = strict
    if license != "mit":
        merged["license"] = license
    if ci != "github-actions":
        merged["ci"] = ci
    if readme != "standard":
        merged["readme"] = readme
    if output_dir is not None:
        merged["output_dir"] = output_dir

    return merged
