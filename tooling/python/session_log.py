#!/usr/bin/env python3
"""Track and resume work sessions for meta-analysis projects."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional


def _utc_iso() -> str:
    """Return current UTC time as an ISO-8601 string with a Z suffix.

    Replaces the deprecated ``_utc_iso()`` idiom
    with a timezone-aware equivalent that produces an identical string
    shape (``...+00:00`` normalized to ``...Z``).
    """
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


class SessionLog:
    """Manage session logs for a meta-analysis project."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.log_dir = project_root / "09_qa" / "sessions"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.current_session_path = self.log_dir / "current_session.json"
        self.history_path = self.log_dir / "session_history.jsonl"
        self.stamps_path = self.log_dir / "artifact_stamps.jsonl"

    def append_stamp(
        self,
        stage: str,
        artifact: str,
        generator: str = "ai",
        deviations: Optional[List[str]] = None,
        notes: Optional[str] = None,
    ) -> Dict:
        """Append a provenance record for a pipeline artifact.

        Each line in ``artifact_stamps.jsonl`` records who generated which
        file, at what stage, and any deviations from the strict pipeline
        (e.g., "single-reviewer screening", "PROSPERO deferred"). This is
        the single place a future reader can go to answer "how was this
        artifact produced?" without grep-hunting through scattered
        agreement.md files.

        The stamp is also reflected on the current session (if one is
        active) so it shows up in ``resume``.
        """
        stamp = {
            "timestamp": _utc_iso(),
            "stage": stage,
            "artifact": artifact,
            "generator": generator,
            "deviations": deviations or [],
            "notes": notes or "",
        }
        with open(self.stamps_path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(stamp, ensure_ascii=False) + "\n")

        # Reflect on active session if one exists.
        session = self.get_current_session()
        if session:
            session.setdefault("artifact_stamps", []).append(stamp)
            self.current_session_path.write_text(
                json.dumps(session, indent=2)
            )
        return stamp

    def start_session(self, notes: Optional[str] = None) -> Dict:
        """Start a new work session."""
        session = {
            "session_id": datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S"),
            "start_time": _utc_iso(),
            "end_time": None,
            "stage": None,
            "tasks": [],
            "decisions": [],
            "questions": [],
            "notes": notes or "",
            "files_created": [],
            "files_modified": [],
        }

        self.current_session_path.write_text(json.dumps(session, indent=2))
        print(f"📝 Session started: {session['session_id']}")
        return session

    def get_current_session(self) -> Optional[Dict]:
        """Get current active session."""
        if not self.current_session_path.exists():
            return None
        return json.loads(self.current_session_path.read_text())

    def update_session(
        self,
        stage: Optional[str] = None,
        task: Optional[str] = None,
        decision: Optional[str] = None,
        question: Optional[str] = None,
        file_created: Optional[str] = None,
        file_modified: Optional[str] = None,
    ) -> None:
        """Update current session with new information."""
        session = self.get_current_session()
        if not session:
            print("⚠️  No active session. Start a new session first.")
            return

        if stage:
            session["stage"] = stage
        if task:
            session["tasks"].append({
                "timestamp": _utc_iso(),
                "task": task,
            })
        if decision:
            session["decisions"].append({
                "timestamp": _utc_iso(),
                "decision": decision,
            })
        if question:
            session["questions"].append({
                "timestamp": _utc_iso(),
                "question": question,
            })
        if file_created:
            session["files_created"].append(file_created)
        if file_modified:
            session["files_modified"].append(file_modified)

        self.current_session_path.write_text(json.dumps(session, indent=2))

    def end_session(self, summary: Optional[str] = None) -> None:
        """End current session and archive to history."""
        session = self.get_current_session()
        if not session:
            print("⚠️  No active session to end.")
            return

        session["end_time"] = _utc_iso()
        if summary:
            session["summary"] = summary

        # Append to history
        with open(self.history_path, "a") as f:
            f.write(json.dumps(session) + "\n")

        # Clear current session
        self.current_session_path.unlink()

        print(f"✅ Session ended: {session['session_id']}")
        print(f"   Tasks completed: {len(session['tasks'])}")
        print(f"   Decisions made: {len(session['decisions'])}")

    def get_last_session(self) -> Optional[Dict]:
        """Get the most recent completed session."""
        if not self.history_path.exists():
            return None

        with open(self.history_path, "r") as f:
            lines = f.readlines()
            if not lines:
                return None
            return json.loads(lines[-1])

    def get_resume_summary(self) -> str:
        """Generate a resume summary for the next session."""
        last_session = self.get_last_session()
        if not last_session:
            return "No previous session found. This is a new project."

        summary = []
        summary.append("=" * 60)
        summary.append("📋 LAST SESSION SUMMARY")
        summary.append("=" * 60)
        summary.append("")
        summary.append(f"Session ID: {last_session['session_id']}")
        summary.append(f"Date: {last_session['start_time'][:10]}")
        summary.append(f"Stage: {last_session.get('stage', 'Unknown')}")
        summary.append("")

        if last_session.get("tasks"):
            summary.append("✅ TASKS COMPLETED:")
            for task in last_session["tasks"]:
                summary.append(f"   • {task['task']}")
            summary.append("")

        if last_session.get("decisions"):
            summary.append("🎯 DECISIONS MADE:")
            for decision in last_session["decisions"]:
                summary.append(f"   • {decision['decision']}")
            summary.append("")

        if last_session.get("questions"):
            summary.append("❓ OPEN QUESTIONS:")
            for question in last_session["questions"]:
                summary.append(f"   • {question['question']}")
            summary.append("")

        if last_session.get("files_created"):
            summary.append("📁 FILES CREATED:")
            for file in last_session["files_created"]:
                summary.append(f"   • {file}")
            summary.append("")

        if last_session.get("summary"):
            summary.append("📝 SESSION NOTES:")
            summary.append(f"   {last_session['summary']}")
            summary.append("")

        summary.append("=" * 60)
        summary.append("➡️  SUGGESTED NEXT STEPS:")
        summary.append("=" * 60)
        summary.append("")

        # Suggest next steps based on stage
        stage = last_session.get("stage")
        if stage == "01_protocol":
            summary.append("   1. Review pico.yaml completeness")
            summary.append("   2. Start Stage 02: Literature Search")
        elif stage == "02_search":
            summary.append("   1. Review dedupe.bib records")
            summary.append("   2. Convert to CSV for screening")
            summary.append("   3. Start Stage 03: Title/Abstract Screening")
        elif stage == "03_screening":
            summary.append("   1. Calculate Cohen's kappa (target ≥0.60)")
            summary.append("   2. Export included records")
            summary.append("   3. Start Stage 04: Full-text Retrieval")
        elif stage == "05_extraction":
            summary.append("   1. Validate extraction.csv completeness")
            summary.append("   2. Perform Risk of Bias assessment")
            summary.append("   3. Start Stage 06: Meta-Analysis (R)")
        elif stage == "06_analysis":
            summary.append("   1. Verify all R scripts completed")
            summary.append("   2. Check figures exported at 300 DPI")
            summary.append("   3. Start Stage 07: Manuscript Assembly")
        else:
            summary.append("   Run 'project_status.py' to see current progress")

        summary.append("")
        return "\n".join(summary)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Manage work session logs for meta-analysis projects."
    )
    parser.add_argument(
        "--project",
        required=True,
        help="Project name (in projects/<name>/) or full path",
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Start session
    start_parser = subparsers.add_parser("start", help="Start a new work session")
    start_parser.add_argument("--notes", help="Initial session notes")

    # Update session
    update_parser = subparsers.add_parser("update", help="Update current session")
    update_parser.add_argument("--stage", help="Current stage (e.g., 02_search)")
    update_parser.add_argument("--task", help="Task completed")
    update_parser.add_argument("--decision", help="Decision made")
    update_parser.add_argument("--question", help="Open question")
    update_parser.add_argument("--file-created", help="File created")
    update_parser.add_argument("--file-modified", help="File modified")

    # End session
    end_parser = subparsers.add_parser("end", help="End current session")
    end_parser.add_argument("--summary", help="Session summary")

    # Resume
    resume_parser = subparsers.add_parser("resume", help="Show resume summary")

    # Append artifact provenance stamp
    append_parser = subparsers.add_parser(
        "append",
        help="Append a provenance stamp for a pipeline artifact",
    )
    append_parser.add_argument(
        "--stage", required=True, help="Stage identifier (e.g., 03_screening)"
    )
    append_parser.add_argument(
        "--artifact", required=True, help="Artifact path or identifier"
    )
    append_parser.add_argument(
        "--generator",
        default="ai",
        help="Who produced this artifact (ai, human, hybrid). Default: ai.",
    )
    append_parser.add_argument(
        "--deviation",
        action="append",
        default=[],
        help=(
            "Deviation from strict pipeline (repeatable, e.g. "
            '--deviation "single reviewer" --deviation "PROSPERO deferred")'
        ),
    )
    append_parser.add_argument("--notes", help="Free-text notes")

    args = parser.parse_args()

    # Determine project root
    project_path = Path(args.project)
    if not project_path.is_absolute():
        script_dir = Path(__file__).resolve().parent
        repo_root = script_dir.parent.parent
        project_path = repo_root / "projects" / args.project

    if not project_path.exists():
        print(f"❌ Error: Project not found at {project_path}")
        return

    session_log = SessionLog(project_path)

    if args.command == "start":
        session_log.start_session(notes=args.notes)

    elif args.command == "update":
        session_log.update_session(
            stage=args.stage,
            task=args.task,
            decision=args.decision,
            question=args.question,
            file_created=args.file_created,
            file_modified=args.file_modified,
        )
        print("✅ Session updated")

    elif args.command == "end":
        session_log.end_session(summary=args.summary)

    elif args.command == "resume":
        print(session_log.get_resume_summary())

    elif args.command == "append":
        stamp = session_log.append_stamp(
            stage=args.stage,
            artifact=args.artifact,
            generator=args.generator,
            deviations=args.deviation,
            notes=args.notes,
        )
        print(
            f"✅ Stamped {stamp['artifact']} "
            f"(stage={stamp['stage']}, generator={stamp['generator']})"
        )
        if stamp["deviations"]:
            print(f"   deviations: {', '.join(stamp['deviations'])}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
