#!/usr/bin/env python3
"""
Test runner for meta-analysis pipeline.

Usage:
    uv run tests/run_tests.py           # Run unit tests only
    uv run tests/run_tests.py --all     # Run unit tests + connection tests
    uv run tests/run_tests.py --conn    # Run connection tests only
"""

import subprocess
import sys
import tempfile
from pathlib import Path

# Paths
ROOT = Path(__file__).parent.parent
FIXTURES = ROOT / "tests" / "fixtures"
SCRIPTS = {
    "dedupe": ROOT / "ma-search-bibliography" / "scripts" / "dedupe_bib.py",
    "multi_dedupe": ROOT / "ma-search-bibliography" / "scripts" / "multi_db_dedupe.py",
    "agreement": ROOT / "ma-screening-quality" / "scripts" / "dual_review_agreement.py",
    "build_queries": ROOT / "ma-search-bibliography" / "scripts" / "build_queries.py",
}


def run_cmd(cmd: list[str], desc: str) -> tuple[bool, str]:
    """Run a command and return (success, output)."""
    print(f"\n{'=' * 60}")
    print(f"TEST: {desc}")
    print(f"CMD: {' '.join(cmd)}")
    print("=" * 60)

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=ROOT / "tooling" / "python",
            timeout=60,
        )
        output = result.stdout + result.stderr
        success = result.returncode == 0

        if success:
            print(f"✅ PASSED")
        else:
            print(f"❌ FAILED (exit code {result.returncode})")
            print(output)

        return success, output
    except FileNotFoundError:
        print(f"❌ FAILED: Script not found")
        return False, "Script not found"
    except subprocess.TimeoutExpired:
        print(f"❌ FAILED: Timeout")
        return False, "Timeout"


def test_dedupe():
    """Test single-file deduplication."""
    with tempfile.TemporaryDirectory() as tmpdir:
        out_bib = Path(tmpdir) / "dedupe.bib"
        out_log = Path(tmpdir) / "dedupe.log"

        success, output = run_cmd(
            [
                "uv",
                "run",
                str(SCRIPTS["dedupe"]),
                "--in-bib",
                str(FIXTURES / "02_search" / "results.bib"),
                "--out-bib",
                str(out_bib),
                "--out-log",
                str(out_log),
            ],
            "Deduplicate single BibTeX file",
        )

        if success and out_bib.exists():
            content = out_bib.read_text()
            # Should have 7 entries (8 - 1 duplicate)
            n_entries = content.count("@article{")
            print(f"  Output: {n_entries} entries (expected: 7)")
            return n_entries == 7
        return False


def test_multi_dedupe():
    """Test multi-database deduplication."""
    with tempfile.TemporaryDirectory() as tmpdir:
        out_merged = Path(tmpdir) / "merged.bib"
        out_bib = Path(tmpdir) / "final.bib"
        out_log = Path(tmpdir) / "merge.log"

        success, output = run_cmd(
            [
                "uv",
                "run",
                str(SCRIPTS["multi_dedupe"]),
                "--in-bib",
                str(FIXTURES / "02_search" / "results.bib"),
                "--in-bib",
                str(FIXTURES / "02_search" / "scopus.bib"),
                "--out-merged",
                str(out_merged),
                "--out-bib",
                str(out_bib),
                "--out-log",
                str(out_log),
            ],
            "Merge and deduplicate multi-DB results",
        )

        if success and out_bib.exists():
            content = out_bib.read_text()
            n_entries = content.count("@article{")
            print(f"  Output: {n_entries} entries (expected: 9)")
            return n_entries == 9
        return False


def test_agreement():
    """Test dual-review agreement calculation."""
    with tempfile.TemporaryDirectory() as tmpdir:
        out_md = Path(tmpdir) / "agreement.md"

        success, output = run_cmd(
            [
                "uv",
                "run",
                str(SCRIPTS["agreement"]),
                "--file",
                str(FIXTURES / "03_screening" / "decisions.csv"),
                "--col-a",
                "decision_r1",
                "--col-b",
                "decision_r2",
                "--out",
                str(out_md),
            ],
            "Calculate dual-review agreement",
        )

        if success and out_md.exists():
            content = out_md.read_text()
            print(f"  Output preview: {content[:200]}...")
            # Should contain kappa statistic
            return "kappa" in content.lower() or "agreement" in content.lower()
        return False


def test_fulltext_agreement():
    """Test full-text dual-review agreement calculation."""
    with tempfile.TemporaryDirectory() as tmpdir:
        out_md = Path(tmpdir) / "ft_agreement.md"

        success, output = run_cmd(
            [
                "uv",
                "run",
                str(SCRIPTS["agreement"]),
                "--file",
                str(FIXTURES / "04_fulltext" / "fulltext_decisions.csv"),
                "--col-a",
                "FT_Reviewer1_Decision",
                "--col-b",
                "FT_Reviewer2_Decision",
                "--out",
                str(out_md),
            ],
            "Calculate full-text dual-review agreement",
        )

        if success and out_md.exists():
            content = out_md.read_text()
            print(f"  Output preview: {content[:200]}...")
            return "kappa" in content.lower() or "agreement" in content.lower()
        return False


def test_build_queries():
    """Test query building from PICO."""
    with tempfile.TemporaryDirectory() as tmpdir:
        out_txt = Path(tmpdir) / "queries.txt"

        success, output = run_cmd(
            [
                "uv",
                "run",
                str(SCRIPTS["build_queries"]),
                "--pico",
                str(FIXTURES / "01_protocol" / "pico.yaml"),
                "--out",
                str(out_txt),
            ],
            "Build queries from PICO",
        )

        if success and out_txt.exists():
            content = out_txt.read_text()
            print(f"  Output preview: {content[:200]}...")
            # Should contain population terms
            return "depression" in content.lower() or "MDD" in content
        return False


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("META-PIPE TEST SUITE")
    print("=" * 60)

    tests = [
        ("Deduplication", test_dedupe),
        ("Multi-DB Merge", test_multi_dedupe),
        ("Dual-Review Agreement", test_agreement),
        ("Full-text Agreement", test_fulltext_agreement),
        ("Build Queries", test_build_queries),
    ]

    results = []
    for name, test_fn in tests:
        try:
            passed = test_fn()
        except Exception as e:
            print(f"❌ EXCEPTION: {e}")
            passed = False
        results.append((name, passed))

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    passed = sum(1 for _, p in results if p)
    total = len(results)

    for name, p in results:
        status = "✅" if p else "❌"
        print(f"  {status} {name}")

    print(f"\nTotal: {passed}/{total} passed")

    return 0 if passed == total else 1


def run_connection_tests():
    """Run database connection tests."""
    conn_script = ROOT / "tests" / "test_db_connections.py"
    result = subprocess.run(
        ["uv", "run", str(conn_script)],
        cwd=ROOT / "tooling" / "python",
    )
    return result.returncode == 0


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run meta-pipe tests")
    parser.add_argument(
        "--all", action="store_true", help="Run all tests including connections"
    )
    parser.add_argument("--conn", action="store_true", help="Run connection tests only")
    args = parser.parse_args()

    if args.conn:
        # Connection tests only
        sys.exit(0 if run_connection_tests() else 1)
    elif args.all:
        # Unit tests + connection tests
        unit_result = main()
        print("\n" + "=" * 60)
        print("RUNNING CONNECTION TESTS")
        print("=" * 60)
        conn_result = run_connection_tests()
        sys.exit(0 if unit_result == 0 and conn_result else 1)
    else:
        # Unit tests only (default)
        sys.exit(main())
