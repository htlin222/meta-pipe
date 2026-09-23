#!/usr/bin/env python3
"""
AI-powered screening for meta-analysis projects.
Uses `claude -p` CLI (OAuth) to screen studies against project eligibility criteria.

Supports two stages:
  - abstract (default): screen title/abstract from screening-database.csv
  - fulltext: re-screen included studies against full text (web/PDF) from manifest.csv

Topic-agnostic: reads eligibility.md from any project and applies generic
PICO-based exclusion codes. Outputs conform to the dual-review schema so
the result plugs directly into dual_review_agreement.py.

Usage:
    uv run tooling/python/ai_screen.py --project <name>
    uv run tooling/python/ai_screen.py --project <name> --reviewer 2
    uv run tooling/python/ai_screen.py --project <name> --stage fulltext
    uv run tooling/python/ai_screen.py --project <name> --stage fulltext --reviewer 2
"""

import argparse
import csv
import json as _json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Optional, Dict, List


def _resolve_meta_pipe_root() -> Path:
    """Resolve the meta-pipe repo root.

    Order: $MA_PIPE_ROOT env var → module-relative (tooling/python/../..).
    The assert guards against the script being copied outside the repo.
    """
    env_root = os.environ.get("MA_PIPE_ROOT")
    if env_root:
        root = Path(env_root).resolve()
    else:
        root = Path(__file__).resolve().parent.parent.parent
    assert (root / "projects").is_dir(), (
        f"META_PIPE_ROOT={root} does not contain a projects/ directory. "
        "Set MA_PIPE_ROOT to the repo root."
    )
    return root


META_PIPE_ROOT = _resolve_meta_pipe_root()

MIN_CLAUDE_CLI_VERSION = (2, 1, 0)


def _assert_claude_cli() -> None:
    """Verify `claude` is on PATH and supports the required flags."""
    try:
        help_out = subprocess.run(
            ["claude", "-p", "--help"],
            capture_output=True,
            text=True,
            timeout=15,
        )
    except FileNotFoundError:
        raise SystemExit(
            "ERROR: `claude` CLI not found on PATH. Install Claude Code >= "
            f"{'.'.join(str(x) for x in MIN_CLAUDE_CLI_VERSION)}."
        )
    except subprocess.TimeoutExpired:
        raise SystemExit("ERROR: `claude -p --help` timed out after 15s.")
    if help_out.returncode != 0:
        raise SystemExit(f"ERROR: `claude -p --help` failed: {help_out.stderr.strip()}")
    missing = [
        flag for flag in ("--bare", "--output-format") if flag not in help_out.stdout
    ]
    if missing:
        raise SystemExit(
            "ERROR: installed `claude` CLI is missing required flag(s): "
            f"{', '.join(missing)}. Upgrade to Claude Code >= "
            f"{'.'.join(str(x) for x in MIN_CLAUDE_CLI_VERSION)}. "
            "See tooling/python/CLAUDE_CLI_FLAGS.md."
        )


EXCLUSION_CODES = """\
- P1: Wrong population
- P2: Wrong age group
- I1: Wrong intervention
- I2: Intervention used for wrong indication
- C1: Wrong comparator
- S1: Wrong study design (review/meta-analysis/editorial/commentary)
- S2: Case report or small series below minimum sample size
- S3: Preclinical/in vitro/animal study
- S4: Study protocol without results
- O1: No relevant outcomes reported
- O2: Insufficient follow-up duration
- T1: Outside date range
- T2: Conference abstract too old without full publication
- L1: Language not meeting criteria
- D1: Duplicate or superseded publication
- NONE: No exclusion (use for INCLUDE or MAYBE decisions)"""


_BARE_WARNING_EMITTED = False


def _invoke_claude(prompt: str, timeout: int) -> str:
    """Run `claude -p` and return the result text.

    Uses --bare when ANTHROPIC_API_KEY is set, which skips hooks, LSP,
    plugin sync, auto-memory, and CLAUDE.md auto-discovery — this is a
    stateless single-shot call, not an interactive Claude Code session.
    Cuts per-call input tokens from ~10k (full session context) down to
    ~1.5k (just the prompt).

    --bare explicitly refuses OAuth/keychain auth, so if only an OAuth
    session is available we fall back to non-bare mode with a one-time
    warning. Set ANTHROPIC_API_KEY to get the fast path.

    --output-format json returns a stable envelope: {"result": "<text>", ...}.
    We fall back to raw stdout if parsing fails so a CLI change doesn't
    break screening.
    """
    global _BARE_WARNING_EMITTED

    cmd = ["claude", "-p", "--output-format", "json", "--model", "haiku"]
    if os.environ.get("ANTHROPIC_API_KEY"):
        cmd.insert(2, "--bare")
    elif not _BARE_WARNING_EMITTED:
        print(
            "NOTE: ANTHROPIC_API_KEY not set — falling back to non-bare "
            "`claude -p`. Screening will still work but each call pays the "
            "full system-prompt overhead (~10k input tokens). Set "
            "ANTHROPIC_API_KEY to drop to ~1.5k tokens per call.",
            file=sys.stderr,
        )
        _BARE_WARNING_EMITTED = True

    result = subprocess.run(
        cmd,
        input=prompt,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    if result.returncode != 0:
        raise RuntimeError(f"claude -p failed: {result.stderr.strip()}")
    stdout = result.stdout.strip()
    if not stdout:
        return ""
    try:
        envelope = _json.loads(stdout)
    except _json.JSONDecodeError:
        return stdout
    if isinstance(envelope, dict):
        if envelope.get("is_error"):
            raise RuntimeError(f"claude -p error: {envelope.get('result', envelope)}")
        return str(envelope.get("result") or envelope.get("content") or stdout)
    return stdout


def load_eligibility_criteria(project_path: Path) -> str:
    """Load PICO criteria from project's eligibility.md."""
    eligibility_file = project_path / "01_protocol" / "eligibility.md"
    if eligibility_file.exists():
        return eligibility_file.read_text()
    return ""


def screen_fulltext_one(
    title: str,
    record_id: str,
    doi: str,
    pmid: str,
    eligibility_criteria: str,
    pdf_path: Optional[Path] = None,
    abstract: str = "",
    retrieval_status: str = "",
) -> dict:
    """
    Call `claude -p` to re-screen a study at the full-text stage.
    Uses local PDF text if available, otherwise attempts to use web search.
    Returns dict with decision, reason, confidence, exclusion_code.
    """
    pdf_text = ""
    if pdf_path and pdf_path.exists():
        print(f"   (Extracting text from {pdf_path.name}...)")
        try:
            # The module is extract_pdf_text.py and the function is
            # extract_text_from_pdf. The previous `from llm_extract import
            # extract_pdf_text` named a module that does not exist in this repo,
            # so every downloaded PDF was silently ignored and full-text
            # screening degraded to a web search for every record.
            from extract_pdf_text import extract_text_from_pdf

            _res = extract_text_from_pdf(pdf_path, max_pages=10)
            # returns a dict with metadata, not a bare string
            pdf_text = _res.get("text", "") if isinstance(_res, dict) else str(_res)
            if isinstance(_res, dict) and _res.get("error"):
                print(f"   (PDF extraction reported: {_res['error']})")
        except Exception as e:
            print(f"   (PDF extraction failed: {e})")
            pdf_text = ""

    prompt_context = f"STUDY TO SCREEN:\nRecord ID: {record_id}\nTitle: {title}\nDOI: {doi}\nPMID: {pmid}\n"
    if pdf_text:
        prompt_context += f"\nFULL TEXT CONTENT (first 10 pages):\n{pdf_text[:15000]}\n"
        search_instruction = (
            "2. EVIDENCE AVAILABLE: the full text is provided above. Evaluate ALL "
            "eligibility criteria against it. Reserve UNCLEAR for genuine ambiguity "
            "in the document, not for extraction difficulty."
        )
    elif abstract:
        # No full text could be retrieved, but the abstract is available. Give it to
        # the reviewer and state the rule, instead of asking for a web search that
        # usually fails and yields a meaningless "unable to determine".
        prompt_context += (
            f"\nABSTRACT (no full text could be retrieved):\n{abstract[:6000]}\n"
        )
        search_instruction = (
            "2. EVIDENCE AVAILABLE: ABSTRACT ONLY -- no full text could be retrieved.\n"
            "   Apply the protocol rule for this case:\n"
            "   - EXCLUDE if the abstract shows a HARD, SELF-EVIDENT violation: metastatic/"
            "stage IV population, HER2-negative population, explicitly non-randomised or "
            "single-arm, review/editorial/commentary, a SECONDARY or POOLED analysis of "
            "previously reported trials, protocol without results, or non-breast primary. "
            "Name the criterion.\n"
            "   - UNCLEAR if the abstract is consistent with eligibility but lacks detail only "
            "the full text could supply (arm-level pCR numbers, exact stage distribution).\n"
            "   - Do NOT answer UNCLEAR merely because the full text is unavailable, and do NOT "
            "EXCLUDE for missing arm-level outcome data -- that is reporting depth, not "
            "ineligibility."
        )
    else:
        search_instruction = (
            "2. EVIDENCE AVAILABLE: title only. Answer UNCLEAR unless the title itself shows a "
            "hard violation."
        )

    prompt = f"""You are an expert systematic reviewer performing FULL-TEXT eligibility screening for a meta-analysis.

This study was previously INCLUDED at the title/abstract stage. Your task is to re-evaluate
its eligibility using the FULL TEXT of the article. Be more stringent than abstract screening —
at this stage, the study must clearly satisfy ALL eligibility criteria.

ELIGIBILITY CRITERIA (from the project protocol -- read carefully):
{eligibility_criteria}

{prompt_context}

INSTRUCTIONS:
1. {search_instruction}
3. Pay special attention to: study design details, exact population definitions,
   intervention/comparator specifics, outcome measurement methods, and follow-up duration.
4. If the full text reveals ANY eligibility violation not apparent from the abstract, EXCLUDE.
5. Document the specific reason with reference to which criterion failed.

Respond in this EXACT format (one line each, no markdown, no extra text):
DECISION: [INCLUDE/EXCLUDE]
REASON: [Brief explanation referencing specific full-text content]
CONFIDENCE: [HIGH/MEDIUM/LOW]
EXCLUSION_CODE: [code or NONE]

Exclusion codes:
{EXCLUSION_CODES}
"""

    # 180s: tool use / long full-text prompts need more than the default 120s
    text = _invoke_claude(prompt, timeout=180)

    # Default to UNCLEAR, never to exclude.
    # A parse failure, a timeout, or a full text the model could not reach is a
    # RETRIEVAL/TOOLING outcome, not an eligibility judgement. Defaulting such a
    # record to "exclude" silently converts an infrastructure failure into a
    # PRISMA exclusion-with-reason and drops eligible trials: in a pilot, 6 of 8
    # records defaulted this way, including a neoadjuvant T-DM1 + pertuzumab
    # trial that plainly meets the criteria. Unclear records advance to human
    # adjudication instead.
    parsed = {
        "decision": "unclear",
        "reason": "Unable to determine from available full text — advanced for adjudication",
        "confidence": "LOW",
        "exclusion_code": "NONE",
    }
    for line in text.strip().split("\n"):
        line = line.strip()
        if line.startswith("DECISION:"):
            parsed["decision"] = line.split(":", 1)[1].strip().lower()
        elif line.startswith("REASON:"):
            parsed["reason"] = line.split(":", 1)[1].strip()
        elif line.startswith("CONFIDENCE:"):
            parsed["confidence"] = line.split(":", 1)[1].strip()
        elif line.startswith("EXCLUSION_CODE:"):
            parsed["exclusion_code"] = line.split(":", 1)[1].strip()

    # Anything that is not a clean include/exclude becomes `unclear`, which
    # advances the record rather than silently excluding it.
    if parsed["decision"] not in ("include", "exclude"):
        parsed["decision"] = "unclear"

    return parsed


def screen_batch(records: List[dict], eligibility_criteria: str) -> Dict[int, dict]:
    """Screen several studies in one `claude -p` call.

    One call per record is the most faithful method but is dominated by CLI
    startup (~14s wall for a ~10s model turn), so a large corpus becomes
    infeasible. Batching amortises that startup across K records while still
    requiring a separate, explicitly-keyed judgement per record.

    Returns {position_index: parsed_dict} for whichever records the model
    returned. The caller is responsible for any record missing from the reply --
    it must never be silently dropped.
    """
    blocks = []
    for i, rec in enumerate(records, 1):
        abstract = (rec.get("Abstract") or "").strip()
        blocks.append(
            f"### RECORD {i}\n"
            f"Title: {rec.get('Title', '')}\n"
            f"Authors: {rec.get('Authors', '')}\n"
            f"Journal: {rec.get('Journal', '')}\n"
            f"Year: {rec.get('Year', '')}\n"
            f"Abstract: {abstract[:1200] if abstract else 'NO ABSTRACT AVAILABLE'}"
        )
    joined = "\n\n".join(blocks)

    prompt = f"""You are an expert systematic reviewer screening studies for a meta-analysis.

ELIGIBILITY CRITERIA (from the project protocol -- read carefully):
{eligibility_criteria}

You will screen {len(records)} studies. Judge EACH ONE INDEPENDENTLY on its own
title and abstract. Do not let one record influence another.

{joined}

TASK:
For each record, decide:
1. INCLUDE - clearly meets all eligibility criteria
2. EXCLUDE - clearly violates one or more eligibility criteria
3. MAYBE - uncertain, needs full-text review

When in doubt, prefer MAYBE over EXCLUDE (liberal screening at title/abstract stage).
If a record has no abstract, judge on the title alone and prefer MAYBE unless the
title clearly violates a criterion.

Output EXACTLY one line per record, in this format, no markdown, no extra text:
RECORD <n> | DECISION: <INCLUDE|EXCLUDE|MAYBE> | REASON: <one sentence> | CONFIDENCE: <HIGH|MEDIUM|LOW> | EXCLUSION_CODE: <code or NONE>

You must output exactly {len(records)} lines, numbered 1 to {len(records)}.

Exclusion codes:
{EXCLUSION_CODES}
"""

    timeout = max(120, 25 * len(records))
    text = _invoke_claude(prompt, timeout=timeout)

    out: Dict[int, dict] = {}
    line_re = re.compile(r"RECORD\s*(\d+)\s*\|(.*)", re.I)
    for line in text.strip().splitlines():
        m = line_re.search(line.strip())
        if not m:
            continue
        idx = int(m.group(1))
        if not (1 <= idx <= len(records)) or idx in out:
            continue
        rest = m.group(2)

        def field(name: str, default: str) -> str:
            fm = re.search(rf"{name}\s*:\s*([^|]*)", rest, re.I)
            return fm.group(1).strip() if fm else default

        decision = field("DECISION", "maybe").lower()
        if decision not in ("include", "exclude", "maybe"):
            decision = "maybe"
        out[idx] = {
            "decision": decision,
            "reason": field("REASON", "No reason given"),
            "confidence": (field("CONFIDENCE", "LOW") or "LOW").upper(),
            "exclusion_code": field("EXCLUSION_CODE", "NONE") or "NONE",
        }
    return out


def screen_one(title, abstract, year, authors, journal, eligibility_criteria) -> dict:
    """
    Call `claude -p` to screen a single study.
    Returns dict with decision, reason, confidence, exclusion_code.
    """
    prompt = f"""You are an expert systematic reviewer screening studies for a meta-analysis.

ELIGIBILITY CRITERIA (from the project protocol -- read carefully):
{eligibility_criteria}

STUDY TO SCREEN:
Title: {title}
Authors: {authors}
Journal: {journal}
Year: {year}
Abstract: {abstract[:1500] if abstract else "No abstract available"}

TASK:
Based on ONLY the title and abstract, decide if this study should be:
1. INCLUDE - clearly meets all eligibility criteria
2. EXCLUDE - clearly violates one or more eligibility criteria
3. MAYBE - uncertain, needs full-text review

When in doubt, prefer MAYBE over EXCLUDE (liberal screening at title/abstract stage).

Respond in this EXACT format (one line each, no markdown, no extra text):
DECISION: [INCLUDE/EXCLUDE/MAYBE]
REASON: [Brief explanation in one sentence]
CONFIDENCE: [HIGH/MEDIUM/LOW]
EXCLUSION_CODE: [code or NONE]

Exclusion codes:
{EXCLUSION_CODES}
"""

    text = _invoke_claude(prompt, timeout=60)

    parsed = {
        "decision": "maybe",
        "reason": "Unable to determine",
        "confidence": "LOW",
        "exclusion_code": "NONE",
    }
    for line in text.strip().split("\n"):
        line = line.strip()
        if line.startswith("DECISION:"):
            parsed["decision"] = line.split(":", 1)[1].strip().lower()
        elif line.startswith("REASON:"):
            parsed["reason"] = line.split(":", 1)[1].strip()
        elif line.startswith("CONFIDENCE:"):
            parsed["confidence"] = line.split(":", 1)[1].strip()
        elif line.startswith("EXCLUSION_CODE:"):
            parsed["exclusion_code"] = line.split(":", 1)[1].strip()

    return parsed


def _apply(
    record: dict, res: dict, decision_col: str, reason_col: str, reviewer: int
) -> None:
    record[decision_col] = res["decision"]
    record[reason_col] = (
        f"{res['exclusion_code']}: {res['reason']}"
        if res["exclusion_code"] != "NONE"
        else res["reason"]
    )
    record["Notes"] = (
        record.get("Notes", "") + f" | AI-R{reviewer} confidence={res['confidence']}"
    ).strip(" |")


def _run_batched(
    records: List[dict],
    batch_size: int,
    eligibility: str,
    decision_col: str,
    reason_col: str,
    reviewer: int,
) -> None:
    """Screen in batches, falling back to one-by-one for anything not returned.

    A record the model omits is NEVER left undecided or dropped: it is retried
    individually, and only if that also fails is it recorded as 'maybe' with the
    error captured in the reason column.
    """
    pending = [r for r in records if not r.get(decision_col, "").strip()]
    print(f"Batched screening: {len(pending)} records, batch size {batch_size}")

    done = 0
    repaired = 0
    for start in range(0, len(pending), batch_size):
        chunk = pending[start : start + batch_size]
        try:
            results = screen_batch(chunk, eligibility)
        except Exception as exc:  # noqa: BLE001 - one bad batch must not abort the run
            print(f"   batch error: {exc}")
            results = {}

        missing = []
        for idx, record in enumerate(chunk, 1):
            res = results.get(idx)
            if res is None:
                missing.append(record)
                continue
            _apply(record, res, decision_col, reason_col, reviewer)
            done += 1

        for record in missing:
            repaired += 1
            try:
                res = screen_one(
                    record.get("Title", ""),
                    record.get("Abstract", ""),
                    record.get("Year", ""),
                    record.get("Authors", ""),
                    record.get("Journal", ""),
                    eligibility,
                )
                _apply(record, res, decision_col, reason_col, reviewer)
            except Exception as exc:  # noqa: BLE001
                record[decision_col] = "maybe"
                record[reason_col] = f"AI error: {exc}"
            done += 1

        print(f"   {done}/{len(pending)} screened (individual repairs: {repaired})")

    undecided = [r for r in records if not r.get(decision_col, "").strip()]
    if undecided:
        raise RuntimeError(
            f"{len(undecided)} records left undecided — refusing to write a partial "
            "decisions file (a missing decision corrupts the PRISMA flow)"
        )


def _column_fill_counts(path: Path, fieldnames: List[str]) -> Dict[str, int]:
    """How many non-empty cells each column currently has on disk."""
    if not path.exists():
        return {}
    counts: Dict[str, int] = {c: 0 for c in fieldnames}
    try:
        with open(path, "r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                for col in counts:
                    if (row.get(col) or "").strip():
                        counts[col] += 1
    except Exception:  # noqa: BLE001 - an unreadable prior file just means no guard data
        return {}
    return counts


def _assert_no_column_regression(
    records: List[dict],
    fieldnames: List[str],
    prior_counts: Dict[str, int],
    owned: set,
) -> None:
    """Refuse to write if this pass would blank out a column it does not own.

    Guards the dual-review invariant: a reviewer-2 run must never reduce the
    number of populated Reviewer1_* cells (or Final_*, or any other column).
    Shrinking a column you do not own means data loss, not an update.
    """
    if not prior_counts:
        return
    regressions = []
    for col in fieldnames:
        if col in owned:
            continue
        before = prior_counts.get(col, 0)
        after = sum(1 for r in records if (r.get(col) or "").strip())
        if after < before:
            regressions.append(f"{col}: {before} -> {after} ({before - after} lost)")
    if regressions:
        raise RuntimeError(
            "refusing to write: this pass would reduce populated cells in "
            "column(s) it does not own -- that is data loss, not an update:\n  "
            + "\n  ".join(regressions)
        )


def _write_and_summarise(
    records, fieldnames, output_csv, decision_col, args, round_dir, prior_counts=None
) -> None:
    owned = {
        f"Reviewer{args.reviewer}_Decision",
        f"Reviewer{args.reviewer}_Reason",
        "Notes",
    }
    _assert_no_column_regression(records, fieldnames, prior_counts or {}, owned)

    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    decisions = [r.get(decision_col, "").lower() for r in records]
    total = len(records) or 1
    print(f"\n{'=' * 60}")
    print(f"SCREENING SUMMARY (Reviewer {args.reviewer} = AI)")
    print(f"{'=' * 60}")
    print(f"Total:    {len(records)}")
    for label in ("include", "exclude", "maybe"):
        n = decisions.count(label)
        print(f"  {label}: {n} ({n / total * 100:.1f}%)")
    print(f"{'=' * 60}")
    print(f"\nOutput: {output_csv}")


def run_abstract_screening(args, project_path: Path) -> None:
    """Run title/abstract screening (original Stage 03 behavior)."""
    screening_db = project_path / "03_screening" / "screening-database.csv"
    round_dir = project_path / "03_screening" / args.round

    shard_i = getattr(args, "shard_index", None)
    shard_n = getattr(args, "shard_total", None)
    sharded = shard_i is not None

    if sharded:
        # Shard output is per-shard AND per-reviewer, so concurrent shards and
        # the two reviewers never write the same file. decisions.csv is produced
        # later by merge_screening_shards.py.
        output_csv = (
            round_dir
            / "shards"
            / f"decisions.r{args.reviewer}.shard-{shard_i:03d}-of-{shard_n:03d}.csv"
        )
    else:
        output_csv = round_dir / "decisions.csv"

    if not screening_db.exists():
        print(f"ERROR: {screening_db} not found. Run search stage first.")
        sys.exit(1)

    eligibility = load_eligibility_criteria(project_path)
    if not eligibility:
        print("WARNING: No eligibility.md found. AI will use basic heuristics.")

    output_csv.parent.mkdir(parents=True, exist_ok=True)

    with open(screening_db, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames)
        records = list(reader)

    # MERGE, DO NOT REPLACE.
    # The screening database's reviewer columns are empty by construction. If a
    # reviewer pass always started from it, running --reviewer 2 after
    # --reviewer 1 would write a decisions.csv in which Reviewer1_* is blank,
    # silently destroying half of an independent dual review -- exactly what the
    # kappa is meant to measure. So when the output already exists, seed from it
    # and overlay only the column this pass owns.
    key_col = "RecordID" if "RecordID" in fieldnames else None
    prior_counts = _column_fill_counts(output_csv, fieldnames)
    if output_csv.exists() and key_col:
        with open(output_csv, "r", encoding="utf-8") as f:
            existing = {r.get(key_col, ""): r for r in csv.DictReader(f)}
        merged = 0
        for i, rec in enumerate(records):
            prev = existing.get(rec.get(key_col, ""))
            if prev:
                records[i] = {**rec, **{k: v for k, v in prev.items() if v}}
                merged += 1
        if merged:
            print(
                f"Merging into existing {output_csv.name}: {merged} prior rows carried forward"
            )

    if sharded:
        total_in = len(records)
        # Round-robin (stride) assignment: shard i takes positions i-1, i-1+n, ...
        # Every record lands in exactly one shard, so the shards partition the
        # corpus exactly and merging cannot lose or duplicate a record.
        records = records[shard_i - 1 :: shard_n]
        print(
            f"Shard {shard_i}/{shard_n}: {len(records)} of {total_in} records"
            f" (stride assignment)"
        )

    print(f"Loaded {len(records)} records from {screening_db.name}")
    print(f"Filling Reviewer{args.reviewer} columns (AI screening)")

    decision_col = f"Reviewer{args.reviewer}_Decision"
    reason_col = f"Reviewer{args.reviewer}_Reason"

    batch_size = getattr(args, "batch", 1) or 1
    if batch_size > 1:
        _run_batched(
            records, batch_size, eligibility, decision_col, reason_col, args.reviewer
        )
        _write_and_summarise(
            records, fieldnames, output_csv, decision_col, args, round_dir, prior_counts
        )
        return

    screened = 0
    skipped = 0
    for i, record in enumerate(records, 1):
        if record.get(decision_col, "").strip():
            skipped += 1
            continue

        pmid = record.get("PMID", "")
        title = record.get("Title", "")
        abstract = record.get("Abstract", "")
        year = record.get("Year", "")
        authors = record.get("Authors", "")
        journal = record.get("Journal", "")

        print(f"\n[{i}/{len(records)}] PMID {pmid}")
        print(f"   {title[:80]}...")

        try:
            result = screen_one(title, abstract, year, authors, journal, eligibility)
            record[decision_col] = result["decision"]
            record[reason_col] = (
                f"{result['exclusion_code']}: {result['reason']}"
                if result["exclusion_code"] != "NONE"
                else result["reason"]
            )
            record["Notes"] = (
                record.get("Notes", "")
                + f" | AI-R{args.reviewer} confidence={result['confidence']}"
            ).strip(" |")
            screened += 1

            print(f"   -> {result['decision']} ({result['confidence']})")
            if result["exclusion_code"] != "NONE":
                print(f"      {result['exclusion_code']}: {result['reason']}")

        except Exception as e:
            print(f"   ERROR: {e}")
            record[decision_col] = "maybe"
            record[reason_col] = f"AI error: {e}"
            screened += 1

    _assert_no_column_regression(
        records,
        fieldnames,
        prior_counts,
        {decision_col, reason_col, "Notes"},
    )
    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    decisions = [r.get(decision_col, "").lower() for r in records]
    inc = decisions.count("include")
    exc = decisions.count("exclude")
    may = decisions.count("maybe")
    total = len(records)

    print(f"\n{'=' * 60}")
    print(f"SCREENING SUMMARY (Reviewer {args.reviewer} = AI)")
    print(f"{'=' * 60}")
    print(f"Total:    {total}")
    print(f"Screened: {screened}  (skipped {skipped} already decided)")
    print(f"  include: {inc} ({inc / total * 100:.1f}%)")
    print(f"  exclude: {exc} ({exc / total * 100:.1f}%)")
    print(f"  maybe:   {may} ({may / total * 100:.1f}%)")
    print(f"{'=' * 60}")
    print(f"\nOutput: {output_csv}")

    if args.reviewer == 1:
        print(
            f"\nNext: run with --reviewer 2 for dual review, or have a human fill Reviewer2 columns."
        )
        print(f"Then: uv run ma-screening-quality/scripts/dual_review_agreement.py \\")
        print(
            f"        --file {output_csv} --col-a Reviewer1_Decision --col-b Reviewer2_Decision \\"
        )
        print(f"        --out {round_dir}/agreement.md")


def run_fulltext_screening(args, project_path: Path) -> None:
    """Run full-text eligibility screening (Stage 04b).

    Reads manifest.csv from Stage 04, re-applies eligibility criteria against
    the full text of each included study, and outputs fulltext_decisions.csv.
    This implements PRISMA 2020 item 16 (full-text exclusion with reasons).
    """
    manifest_csv = project_path / "04_fulltext" / "manifest.csv"

    shard_i = getattr(args, "shard_index", None)
    shard_n = getattr(args, "shard_total", None)
    ft_sharded = shard_i is not None
    if ft_sharded:
        output_csv = (
            project_path
            / "04_fulltext"
            / "shards"
            / f"fulltext_decisions.r{args.reviewer}.shard-{shard_i:03d}-of-{shard_n:03d}.csv"
        )
        output_csv.parent.mkdir(parents=True, exist_ok=True)
    else:
        output_csv = project_path / "04_fulltext" / "fulltext_decisions.csv"

    if not manifest_csv.exists():
        print(
            f"ERROR: {manifest_csv} not found. Complete Stage 04 (fulltext retrieval) first."
        )
        sys.exit(1)

    eligibility = load_eligibility_criteria(project_path)
    if not eligibility:
        print("WARNING: No eligibility.md found. AI will use basic heuristics.")

    # Abstracts for records with no retrievable full text: without these the
    # reviewer has nothing to judge and returns "unable to determine".
    abstracts: Dict[str, str] = {}
    sdb = project_path / "03_screening" / "screening-database.csv"
    if sdb.exists():
        with open(sdb, "r", encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                abstracts[row.get("RecordID", "")] = (row.get("Abstract") or "").strip()

    # Read manifest
    with open(manifest_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        manifest_records = list(reader)

    m_by_id = {m.get("record_id", ""): m for m in manifest_records}
    print(f"Loaded {len(manifest_records)} studies from {manifest_csv.name}")
    print(f"Filling FT_Reviewer{args.reviewer} columns (AI full-text screening)")

    # Build or load existing fulltext_decisions.csv
    ft_fieldnames = [
        "record_id",
        "title",
        "doi",
        "pmid",
        "FT_Reviewer1_Decision",
        "FT_Reviewer1_Reason",
        "FT_Reviewer2_Decision",
        "FT_Reviewer2_Reason",
        "FT_Final_Decision",
        "FT_Exclusion_Code",
    ]

    # Load existing decisions if re-running
    existing: dict[str, dict] = {}
    if output_csv.exists():
        with open(output_csv, "r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                rid = row.get("record_id", "").strip()
                if rid:
                    existing[rid] = row

    # Build records list from manifest.
    # Records whose full text could not be retrieved are NOT screened: you cannot
    # assess the eligibility of a paper you cannot read. PRISMA 2020 counts these
    # in the "reports not retrieved" box, which is distinct from "excluded with
    # reasons". Marking them not_retrieved here keeps that distinction intact and
    # avoids spending a web search per record on paper we know is unavailable.
    NOT_RETRIEVABLE = {"unavailable", "registry_only", "pdf_invalid"}
    skipped_unretrieved = 0
    records = []
    for m in manifest_records:
        rid = m.get("record_id", "").strip()
        if not rid:
            continue
        status = (m.get("retrieval_status") or "").strip()
        if status in NOT_RETRIEVABLE:
            row = existing.get(rid) or {k: "" for k in ft_fieldnames}
            row.update(
                {
                    "record_id": rid,
                    "title": m.get("title", ""),
                    "doi": m.get("doi", ""),
                    "pmid": m.get("pmid", ""),
                    "FT_Final_Decision": "not_retrieved",
                    "FT_Exclusion_Code": "NOT_RETRIEVED",
                }
            )
            if not row.get("FT_Reviewer1_Reason"):
                row["FT_Reviewer1_Reason"] = f"full text not retrieved ({status})"
            existing[rid] = row
            skipped_unretrieved += 1
            continue
        if rid in existing:
            records.append(existing[rid])
        else:
            records.append(
                {
                    "record_id": rid,
                    "title": m.get("title", ""),
                    "doi": m.get("doi", ""),
                    "pmid": m.get("pmid", ""),
                    "FT_Reviewer1_Decision": "",
                    "FT_Reviewer1_Reason": "",
                    "FT_Reviewer2_Decision": "",
                    "FT_Reviewer2_Reason": "",
                    "FT_Final_Decision": "",
                    "FT_Exclusion_Code": "",
                }
            )

    if skipped_unretrieved:
        print(
            f"{skipped_unretrieved} records marked not_retrieved (no full text to assess); "
            f"{len(records)} assessable records will be screened"
        )

    if ft_sharded:
        total_in = len(records)
        # Same stride partition as the abstract stage: shard i takes positions
        # i-1, i-1+n, ... so the shards partition the corpus exactly.
        records = records[shard_i - 1 :: shard_n]
        print(f"Shard {shard_i}/{shard_n}: {len(records)} of {total_in} records")

    decision_col = f"FT_Reviewer{args.reviewer}_Decision"
    reason_col = f"FT_Reviewer{args.reviewer}_Reason"

    screened = 0
    skipped = 0
    for i, record in enumerate(records, 1):
        # Skip if this reviewer already decided
        if record.get(decision_col, "").strip():
            skipped += 1
            continue

        rid = record["record_id"]
        title = record.get("title", "")
        doi = record.get("doi", "")
        pmid = record.get("pmid", "")

        # Find matching manifest record for file_path
        manifest_record = next(
            (m for m in manifest_records if m.get("record_id") == rid), {}
        )
        file_path_val = manifest_record.get("file_path", "")
        pdf_path = None
        if file_path_val:
            pdf_path = Path(file_path_val)
            if not pdf_path.is_absolute():
                # manifest file_path may be written relative to the project root
                # ("04_fulltext/pdf/x.pdf") or to 04_fulltext/ ("pdf/x.pdf");
                # accept either rather than silently resolving to a missing file.
                for base in (project_path, project_path / "04_fulltext"):
                    cand = (base / pdf_path).resolve()
                    if cand.exists():
                        pdf_path = cand
                        break
                else:
                    pdf_path = (project_path / "04_fulltext" / pdf_path).resolve()

        print(f"\n[{i}/{len(records)}] {rid}")
        print(f"   {title[:80]}...")

        try:
            result = screen_fulltext_one(
                title,
                rid,
                doi,
                pmid,
                eligibility,
                pdf_path,
                abstract=abstracts.get(rid, ""),
                retrieval_status=(m_by_id.get(rid, {}) or {}).get(
                    "retrieval_status", ""
                ),
            )
            record[decision_col] = result["decision"]
            record[reason_col] = (
                f"{result['exclusion_code']}: {result['reason']}"
                if result["exclusion_code"] != "NONE"
                else result["reason"]
            )
            screened += 1

            print(f"   -> {result['decision']} ({result['confidence']})")
            if result["exclusion_code"] != "NONE":
                print(f"      {result['exclusion_code']}: {result['reason']}")

        except Exception as e:
            print(f"   ERROR: {e}")
            record[decision_col] = "include"
            record[reason_col] = f"AI error (defaulting to include): {e}"
            screened += 1

    # Resolve final decisions (after both reviewers)
    for record in records:
        r1 = record.get("FT_Reviewer1_Decision", "").strip().lower()
        r2 = record.get("FT_Reviewer2_Decision", "").strip().lower()
        if r1 and r2:
            if r1 == "exclude" or r2 == "exclude":
                # Conservative: if either reviewer excludes, mark as exclude
                # (requires conflict resolution by human if disagreed)
                record["FT_Final_Decision"] = "exclude"
                # Use the exclusion reason from whichever reviewer excluded
                if r1 == "exclude":
                    reason = record.get("FT_Reviewer1_Reason", "")
                else:
                    reason = record.get("FT_Reviewer2_Reason", "")
                # Extract exclusion code from reason string
                code = reason.split(":")[0].strip() if ":" in reason else "NONE"
                record["FT_Exclusion_Code"] = code
            else:
                record["FT_Final_Decision"] = "include"
                record["FT_Exclusion_Code"] = "NONE"

    # Write fulltext_decisions.csv.
    # Unsharded runs also emit the not_retrieved rows so the file accounts for
    # every manifest record; sharded runs emit only their own shard, and the
    # merge step restores the full set.
    out_rows = records
    if not ft_sharded:
        screened_ids = {r.get("record_id") for r in records}
        out_rows = records + [v for k, v in existing.items() if k not in screened_ids]
    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=ft_fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(out_rows)

    # Summary
    decisions = [r.get(decision_col, "").lower() for r in records]
    inc = decisions.count("include")
    exc = decisions.count("exclude")
    total = len(records)

    print(f"\n{'=' * 60}")
    print(f"FULL-TEXT SCREENING SUMMARY (Reviewer {args.reviewer} = AI)")
    print(f"{'=' * 60}")
    print(f"Total:    {total}")
    print(f"Screened: {screened}  (skipped {skipped} already decided)")
    print(f"  include: {inc} ({inc / total * 100:.1f}%)" if total else "  include: 0")
    print(f"  exclude: {exc} ({exc / total * 100:.1f}%)" if total else "  exclude: 0")
    print(f"{'=' * 60}")
    print(f"\nOutput: {output_csv}")

    # Check if both reviewers are done
    final_decisions = [r.get("FT_Final_Decision", "").strip() for r in records]
    resolved = sum(1 for d in final_decisions if d)

    if resolved == total and total > 0:
        ft_included = sum(1 for d in final_decisions if d.lower() == "include")
        ft_excluded = sum(1 for d in final_decisions if d.lower() == "exclude")
        print(f"\nFinal decisions resolved: {resolved}/{total}")
        print(f"  -> {ft_included} INCLUDE (proceed to Stage 05 extraction)")
        print(f"  -> {ft_excluded} EXCLUDE (with reasons for PRISMA flow diagram)")
        agreement_out = project_path / "04_fulltext" / "ft_agreement.md"
        print(f"\nNext: compute full-text inter-rater agreement:")
        print(f"  uv run ma-screening-quality/scripts/dual_review_agreement.py \\")
        print(f"    --file {output_csv} \\")
        print(f"    --col-a FT_Reviewer1_Decision --col-b FT_Reviewer2_Decision \\")
        print(f"    --out {agreement_out}")
    elif args.reviewer == 1:
        print(f"\nNext: run with --reviewer 2 for dual review:")
        print(
            f"  uv run tooling/python/ai_screen.py --project {args.project} --stage fulltext --reviewer 2"
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="AI-powered screening for meta-analysis projects (abstract or full-text)"
    )
    parser.add_argument("--project", required=True, help="Project name under projects/")
    parser.add_argument(
        "--stage",
        choices=["abstract", "fulltext"],
        default="abstract",
        help="Screening stage: 'abstract' (default, Stage 03) or 'fulltext' (Stage 04b)",
    )
    parser.add_argument(
        "--reviewer",
        type=int,
        choices=[1, 2],
        default=1,
        help="Which reviewer column to fill (1 or 2, default: 1)",
    )
    parser.add_argument(
        "--round",
        default="round-01",
        help="Screening round directory name (default: round-01)",
    )
    parser.add_argument(
        "--shard",
        default=None,
        metavar="i/n",
        help=(
            "Screen only shard i of n (1-based), e.g. --shard 3/16. Records are "
            "assigned round-robin by position, so every shard sees a comparable "
            "mix. Each shard writes its own file under <round>/shards/ and never "
            "touches <round>/decisions.csv, so N shards can run concurrently. "
            "Screening one record costs ~14s serially, so a large corpus needs "
            "this: run all N shards in parallel, then merge with "
            "merge_screening_shards.py. Omit for the original single-process "
            "behaviour."
        ),
    )
    parser.add_argument(
        "--batch",
        type=int,
        default=1,
        metavar="K",
        help=(
            "Screen K records per `claude -p` call instead of one (default: 1). "
            "Each record still gets its own explicitly-keyed decision; batching "
            "only amortises CLI startup, which dominates single-record cost "
            "(~14s wall for a ~10s model turn). Any record the model omits is "
            "retried individually, and the run aborts rather than write a "
            "decisions file with a missing decision. Use with --shard on large "
            "corpora; K=10-15 is a reasonable range."
        ),
    )
    args = parser.parse_args()

    if args.batch < 1:
        parser.error(f"--batch must be >= 1 (got {args.batch})")

    if args.shard is not None:
        try:
            _i, _n = (int(x) for x in args.shard.split("/", 1))
        except ValueError:
            parser.error(f"--shard must look like i/n (got {args.shard!r})")
        if _n < 1 or not (1 <= _i <= _n):
            parser.error(
                f"--shard i/n requires 1 <= i <= n and n >= 1 (got {args.shard!r})"
            )
        args.shard_index, args.shard_total = _i, _n
    else:
        args.shard_index, args.shard_total = None, None

    _assert_claude_cli()

    project_path = META_PIPE_ROOT / "projects" / args.project

    if args.stage == "fulltext":
        run_fulltext_screening(args, project_path)
    else:
        run_abstract_screening(args, project_path)


if __name__ == "__main__":
    main()
