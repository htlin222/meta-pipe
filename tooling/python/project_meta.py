"""Read-only helpers for ``projects/<name>/.ma_meta.json``.

A project's quality mode (``strict`` vs ``draft``) is stored in
``.ma_meta.json`` at the project root. This module is the single place
that reads it — other scripts should import :func:`get_quality_mode`
instead of re-parsing the JSON so a schema change stays in one file.
"""

from __future__ import annotations

import json
from pathlib import Path

DEFAULT_MODE = "strict"
VALID_MODES = ("strict", "draft")


def load_project_meta(project_path: Path) -> dict:
    """Return the parsed .ma_meta.json dict, or an empty dict if missing."""
    meta_path = project_path / ".ma_meta.json"
    if not meta_path.exists():
        return {}
    try:
        return json.loads(meta_path.read_text())
    except (json.JSONDecodeError, OSError):
        return {}


def get_quality_mode(project_path: Path) -> str:
    """Return the quality mode for a project. Defaults to ``strict``.

    Unknown values fall back to ``strict`` — that is the safer default,
    because strict mode fails closed on quality gates.
    """
    meta = load_project_meta(project_path)
    mode = meta.get("quality_mode", DEFAULT_MODE)
    if mode not in VALID_MODES:
        return DEFAULT_MODE
    return mode


def is_draft(project_path: Path) -> bool:
    return get_quality_mode(project_path) == "draft"
