"""Tests for project_status.py — project stage detection."""

from __future__ import annotations

from pathlib import Path

import pytest

from project_status import STAGES, check_stage_status, get_project_status


class TestCheckStageStatus:
    """Tests for check_stage_status()."""

    def test_nonexistent_stage_dir(self, tmp_path):
        status = check_stage_status(tmp_path, "01_protocol")
        assert status["exists"] is False
        assert status["validated"] is False
        assert status["file_count"] == 0

    def test_validated_protocol_stage(self, tmp_path):
        stage_dir = tmp_path / "01_protocol"
        stage_dir.mkdir()
        (stage_dir / "pico.yaml").write_text("population: cancer\n")
        status = check_stage_status(tmp_path, "01_protocol")
        assert status["exists"] is True
        assert status["validated"] is True
        assert status["file_count"] == 1

    def test_incomplete_protocol_stage(self, tmp_path):
        stage_dir = tmp_path / "01_protocol"
        stage_dir.mkdir()
        (stage_dir / "notes.md").write_text("WIP\n")
        status = check_stage_status(tmp_path, "01_protocol")
        assert status["exists"] is True
        assert status["validated"] is False  # no pico.yaml

    def test_key_files_tracking(self, tmp_path):
        stage_dir = tmp_path / "01_protocol"
        stage_dir.mkdir()
        (stage_dir / "pico.yaml").write_text("x\n")
        status = check_stage_status(tmp_path, "01_protocol")
        assert "pico.yaml" in status["key_files_present"]
        assert "eligibility.md" in status["key_files_missing"]

    def test_last_modified_set(self, tmp_path):
        stage_dir = tmp_path / "01_protocol"
        stage_dir.mkdir()
        (stage_dir / "pico.yaml").write_text("x\n")
        status = check_stage_status(tmp_path, "01_protocol")
        assert status["last_modified"] is not None

    def test_hidden_files_excluded_from_count(self, tmp_path):
        stage_dir = tmp_path / "01_protocol"
        stage_dir.mkdir()
        (stage_dir / "pico.yaml").write_text("x\n")
        (stage_dir / ".hidden").write_text("x\n")
        status = check_stage_status(tmp_path, "01_protocol")
        assert status["file_count"] == 1


class TestGetProjectStatus:
    """Tests for get_project_status()."""

    def test_empty_project(self, tmp_path):
        status = get_project_status(tmp_path)
        assert status["completion_percentage"] == 0
        assert status["current_stage"] == "01_protocol"

    def test_first_stage_complete(self, tmp_path):
        stage_dir = tmp_path / "01_protocol"
        stage_dir.mkdir()
        (stage_dir / "pico.yaml").write_text("x\n")
        status = get_project_status(tmp_path)
        assert status["completion_percentage"] > 0
        assert status["current_stage"] == "02_search"

    def test_all_stages_complete(self, tmp_path):
        """Simulate all stages validated."""
        # Create minimal files for each stage's validation lambda
        (tmp_path / "01_protocol").mkdir()
        (tmp_path / "01_protocol" / "pico.yaml").write_text("x\n")

        (tmp_path / "02_search" / "round-01").mkdir(parents=True)
        (tmp_path / "02_search" / "round-01" / "dedupe.bib").write_text("x\n")

        (tmp_path / "03_screening" / "round-01").mkdir(parents=True)
        (tmp_path / "03_screening" / "round-01" / "decisions.csv").write_text("x\n")

        (tmp_path / "04_fulltext").mkdir(parents=True)
        (tmp_path / "04_fulltext" / "manifest.csv").write_text("x\n")

        (tmp_path / "05_extraction" / "round-01").mkdir(parents=True)
        (tmp_path / "05_extraction" / "round-01" / "extraction.csv").write_text("x\n")

        for d in ("figures", "tables"):
            (tmp_path / "06_analysis" / d).mkdir(parents=True)

        (tmp_path / "07_manuscript").mkdir()
        (tmp_path / "07_manuscript" / "index.qmd").write_text("x\n")

        (tmp_path / "08_reviews").mkdir()
        (tmp_path / "08_reviews" / "grade_summary.csv").write_text("x\n")

        (tmp_path / "09_qa").mkdir()

        status = get_project_status(tmp_path)
        assert status["completion_percentage"] == 100
        assert "complete" in status["next_action"].lower() or "qa" in status["next_action"].lower()

    def test_project_name_from_path(self, tmp_path):
        status = get_project_status(tmp_path)
        assert status["project_name"] == tmp_path.name

    def test_next_action_set(self, tmp_path):
        status = get_project_status(tmp_path)
        assert status["next_action"] is not None
        assert "01_protocol" in status["next_action"]
