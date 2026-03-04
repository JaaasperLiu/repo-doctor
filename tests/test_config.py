"""Tests for config loading."""

from pathlib import Path

from repo_doctor.config import load_config, merge_config


def test_load_config_missing(tmp_path: Path) -> None:
    cfg = load_config(tmp_path)
    assert cfg == {}


def test_load_config_exists(tmp_path: Path) -> None:
    (tmp_path / ".repo-doctor.yml").write_text(
        "license: apache-2.0\nskip:\n  - lint_config\n"
    )
    cfg = load_config(tmp_path)
    assert cfg["license"] == "apache-2.0"
    assert cfg["skip"] == ["lint_config"]


def test_merge_config_defaults() -> None:
    merged = merge_config({})
    assert merged["license"] == "mit"
    assert merged["skip"] == []
    assert merged["format"] == "both"


def test_merge_config_file_values() -> None:
    cfg = {"license": "apache-2.0", "skip": ["lint_config"]}
    merged = merge_config(cfg)
    assert merged["license"] == "apache-2.0"
    assert merged["skip"] == ["lint_config"]


def test_merge_config_cli_overrides() -> None:
    cfg = {"license": "mit", "skip": ["lint_config"]}
    # Non-default CLI values override config
    merged = merge_config(cfg, license="apache-2.0", skip=["repo_size"])
    assert merged["license"] == "apache-2.0"
    assert merged["skip"] == ["repo_size"]


def test_merge_config_default_cli_keeps_config() -> None:
    cfg = {"license": "apache-2.0", "skip": ["lint_config"]}
    # Default CLI values do NOT override config
    merged = merge_config(cfg, license="mit", skip=None)
    assert merged["license"] == "apache-2.0"
    assert merged["skip"] == ["lint_config"]


def test_merge_config_output_dir() -> None:
    merged = merge_config({}, output_dir=".repo-doctor")
    assert merged["output_dir"] == ".repo-doctor"


def test_merge_config_output_dir_from_file() -> None:
    cfg = {"output_dir": "reports"}
    merged = merge_config(cfg)
    assert merged["output_dir"] == "reports"
