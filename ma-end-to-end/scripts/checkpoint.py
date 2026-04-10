#!/usr/bin/env python3
"""Create and restore pipeline checkpoints."""

from __future__ import annotations

import argparse
import datetime as dt
import os
import tarfile
from pathlib import Path
from typing import Iterable, List, Optional


EXCLUDE_DIRS = {
    ".git",
    ".venv",
    "__pycache__",
    "renv/library",
    "renv/.cache",
    "tooling/python/.venv",
    "09_qa/checkpoints",
}

EXCLUDE_FILES = {
    ".DS_Store",
}


def should_exclude(path: Path, root: Path) -> bool:
    rel = path.relative_to(root)
    rel_str = str(rel)
    if any(rel_str.startswith(ex) for ex in EXCLUDE_DIRS):
        return True
    if path.name in EXCLUDE_FILES:
        return True
    return False


def iter_paths(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        if should_exclude(path, root):
            continue
        yield path


def safe_extract(tar: tarfile.TarFile, path: Path) -> None:
    for member in tar.getmembers():
        member_path = path / member.name
        if not str(member_path.resolve()).startswith(str(path.resolve())):
            raise SystemExit("Unsafe path in tar archive.")
    tar.extractall(path)


def create_checkpoint(root: Path, name: Optional[str]) -> Path:
    ts = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%d_%H%M%S")
    label = name or f"checkpoint_{ts}"
    checkpoint_dir = root / "09_qa" / "checkpoints"
    checkpoint_dir.mkdir(parents=True, exist_ok=True)
    out_path = checkpoint_dir / f"{label}.tar.gz"

    with tarfile.open(out_path, "w:gz") as tar:
        for path in iter_paths(root):
            if path == out_path:
                continue
            arcname = path.relative_to(root)
            tar.add(path, arcname=str(arcname))
    return out_path


def list_checkpoints(root: Path) -> List[Path]:
    checkpoint_dir = root / "09_qa" / "checkpoints"
    if not checkpoint_dir.exists():
        return []
    return sorted(checkpoint_dir.glob("*.tar.gz"))


def restore_checkpoint(root: Path, checkpoint: Path, yes: bool) -> None:
    if not yes:
        raise SystemExit("Restore requires --yes.")
    if not checkpoint.exists():
        raise SystemExit(f"Missing checkpoint: {checkpoint}")
    with tarfile.open(checkpoint, "r:gz") as tar:
        safe_extract(tar, root)


def main() -> None:
    parser = argparse.ArgumentParser(description="Checkpoint create/restore/list.")
    parser.add_argument("--root", default=None, help="Project root (default: repo root)")
    parser.add_argument("--create", action="store_true", help="Create a checkpoint")
    parser.add_argument("--restore", action="store_true", help="Restore a checkpoint")
    parser.add_argument("--list", action="store_true", help="List checkpoints")
    parser.add_argument("--skip", action="store_true", help="Record a skipped checkpoint")
    parser.add_argument("--name", default=None, help="Checkpoint name (without extension)")
    parser.add_argument("--latest", action="store_true", help="Restore latest checkpoint")
    parser.add_argument("--yes", action="store_true", help="Confirm restore")
    parser.add_argument("--note", default=None, help="Optional note for checkpoint log")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[2]
    root = Path(args.root).resolve() if args.root else repo_root

    actions = [args.create, args.restore, args.list, args.skip]
    if sum(bool(x) for x in actions) != 1:
        raise SystemExit("Choose exactly one of --create, --restore, --list, or --skip.")

    if args.list:
        checkpoints = list_checkpoints(root)
        if not checkpoints:
            print("No checkpoints found.")
            return
        for path in checkpoints:
            size = path.stat().st_size
            mtime = dt.datetime.fromtimestamp(path.stat().st_mtime).isoformat()
            print(f"{path.name}\t{size} bytes\t{mtime}")
        return

    if args.create:
        out_path = create_checkpoint(root, args.name)
        log_path = root / "09_qa" / "checkpoint.log"
        log_path.parent.mkdir(parents=True, exist_ok=True)
        log_lines = [
            f"{dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "")}Z\tcreate\t{out_path.name}",
        ]
        if args.note:
            log_lines.append(f"note: {args.note}")
        log_path.write_text("\n".join(log_lines) + "\n")
        print(f"Created checkpoint: {out_path}")
        return

    if args.restore:
        checkpoints = list_checkpoints(root)
        if args.latest:
            if not checkpoints:
                raise SystemExit("No checkpoints available.")
            checkpoint = checkpoints[-1]
        else:
            if not args.name:
                raise SystemExit("Provide --name or --latest for restore.")
            checkpoint = root / "09_qa" / "checkpoints" / f"{args.name}.tar.gz"
        restore_checkpoint(root, checkpoint, args.yes)
        log_path = root / "09_qa" / "checkpoint.log"
        log_path.parent.mkdir(parents=True, exist_ok=True)
        log_lines = [
            f"{dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "")}Z\trestore\t{checkpoint.name}",
        ]
        if args.note:
            log_lines.append(f"note: {args.note}")
        log_path.write_text("\n".join(log_lines) + "\n")
        print(f"Restored checkpoint: {checkpoint}")
        return

    if args.skip:
        log_path = root / "09_qa" / "checkpoint.log"
        log_path.parent.mkdir(parents=True, exist_ok=True)
        log_lines = [
            f"{dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "")}Z\tskip\t-",
        ]
        if args.note:
            log_lines.append(f"note: {args.note}")
        log_path.write_text("\n".join(log_lines) + "\n")
        print("Recorded checkpoint skip.")
        return


if __name__ == "__main__":
    main()
