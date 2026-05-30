#!/usr/bin/env python3
"""Build the demo manifest for the meta-pipe web UI.

Scans the bundled example project (``projects/ici-breast-cancer/``) and emits a
self-contained ``demo_manifest.json`` that the static frontend replays stage by
stage. No API keys, no Claude tokens, no live execution.

Narrative fields are bilingual (English / Traditional Chinese) using the small
``{"en": ..., "zh": ...}`` shape; the frontend has a language toggle. Code,
file paths, ``basis`` lines, prompts, medical values and artifact previews stay
in English.

Gates are grounded in meta-pipe's own program in three classes -- pre-run
``prep``, in-pipeline ``program`` (each with a ``basis``), and a separate
``suggestions.json`` (only with ``--with-suggestions``) for gates meta-pipe
lacks that we would add. The suggestions file is our opinion and is kept OFF the
upstream PR.

Run from the repo root:

    uv run web/build_demo_manifest.py                    # PR build (no suggestions)
    uv run web/build_demo_manifest.py --with-suggestions # our deploy build
"""

from __future__ import annotations

import argparse
import csv as _csv
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path


def TL(en: str, zh: str) -> dict:
    """A bilingual narrative string."""
    return {"en": en, "zh": zh}


# --- helpers ---------------------------------------------------------------


def read_text(path: Path, max_chars: int = 2400) -> str:
    if not path.exists():
        return ""
    text = path.read_text(encoding="utf-8", errors="replace").strip()
    if len(text) > max_chars:
        text = text[:max_chars].rstrip() + "\n\n[... truncated for demo ...]"
    return text


def read_head(path: Path, n_lines: int, max_chars: int = 2400) -> str:
    if not path.exists():
        return ""
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    text = "\n".join(lines[:n_lines]).strip()
    if len(text) > max_chars:
        text = text[:max_chars].rstrip() + "\n[... truncated ...]"
    return text


def extract_screen_prompt(repo: Path) -> str:
    src = repo / "tooling/python/ai_screen.py"
    if not src.exists():
        return ""
    text = src.read_text(encoding="utf-8", errors="replace")
    i = text.find("def screen_one(")
    if i == -1:
        return ""
    j = text.find('prompt = f"""', i)
    if j == -1:
        return ""
    start = j + len('prompt = f"""')
    end = text.find('"""', start)
    return text[start:end].strip() if end != -1 else ""


def screening_decision_counts(proj: Path) -> dict:
    f = proj / "03_screening" / "round-01_decisions_ai_screened.csv"
    out = {"columns": ["decision_r1", "decision_r2", "final_decision"], "counts": {}, "total": 0}
    if not f.exists():
        return out
    rows = list(_csv.DictReader(f.open(encoding="utf-8", errors="replace")))
    out["total"] = len(rows)
    for col in out["columns"]:
        c = {"include": 0, "maybe": 0, "exclude": 0}
        for r in rows:
            v = (r.get(col) or "").strip().lower()
            if v in c:
                c[v] += 1
        out["counts"][col] = c
    out["identical"] = len({tuple(sorted(out["counts"][c].items())) for c in out["columns"]}) == 1
    return out


# --- pre-run preparation ----------------------------------------------------


def build_prep() -> list[dict]:
    return [
        {
            "title": TL("Toolchain installed", "已安裝工具鏈"),
            "detail": TL(
                "uv (Python), R ≥ 4.2 + renv, Quarto, cmake. One-time `bash setup.sh`.",
                "uv（Python）、R ≥ 4.2 + renv、Quarto、cmake。一次性 `bash setup.sh`。"),
            "basis": "README §Requirements, setup.sh",
            "required": True,
        },
        {
            "title": TL("API keys in .env", ".env 內的 API 金鑰"),
            "detail": TL(
                "PubMed key is required; Scopus/Embase, Cochrane, Zotero and an Unpaywall email are optional.",
                "PubMed 金鑰為必填；Scopus/Embase、Cochrane、Zotero 與 Unpaywall email 為選填。"),
            "basis": ".env.example",
            "required": True,
        },
        {
            "title": TL("Research question → TOPIC.txt", "研究問題 → TOPIC.txt"),
            "detail": TL(
                "You write the question into projects/<name>/TOPIC.txt; the pipeline cannot start without it.",
                "你要把研究問題寫進 projects/<name>/TOPIC.txt；沒有它 pipeline 無法啟動。"),
            "basis": "init_project.py, AGENTS.md",
            "required": True,
        },
        {
            "title": TL("Search strategy → queries.txt", "搜尋策略 → queries.txt"),
            "detail": TL(
                "You translate PICO into a database Boolean query by hand and save it as queries.txt (a MeSH-expand helper exists, but the strategy is yours).",
                "你要親手把 PICO 轉成資料庫 Boolean query 存成 queries.txt（有 MeSH 展開工具，但策略要自己擬）。"),
            "basis": "ma-search-bibliography/SKILL.md Step 1",
            "required": True,
        },
        {
            "title": TL("PROSPERO registration (you do this yourself)", "PROSPERO 註冊（需自行完成）"),
            "detail": TL(
                "meta-pipe drafts prospero_registration.md but does not register it. The author's position is that registration is out of scope for the tool — the researcher registers the protocol on PROSPERO themselves before running. We list it here as a real pre-run gate.",
                "meta-pipe 會草擬 prospero_registration.md 但不會幫你註冊。原作的立場是註冊不在工具範圍內——研究者要在跑之前自行上 PROSPERO 註冊。我們把它列為真正的跑前 gate。"),
            "basis": "author's stance; prospero_registration.md is a draft only",
            "required": True,
        },
    ]


# --- in-pipeline gates that exist in meta-pipe today ------------------------


def G(type_, label, detail, basis):
    return {"type": type_, "kind": "program", "label": label, "detail": detail, "basis": basis}


def build_stages(proj: Path, repo: Path) -> list[dict]:
    return [
        {
            "id": "00_intake", "num": "00",
            "name": TL("Topic Intake", "主題評估"), "skill": "/ma-topic-intake",
            "summary": TL(
                "With TOPIC.txt in place, Claude refines the PICO and runs a feasibility assessment.",
                "TOPIC.txt 就緒後，Claude 精修 PICO 並執行可行性評估。"),
            "gates": [
                G("approval",
                  TL("Feasibility assessment (mandatory first step)", "可行性評估（必做的第一步）"),
                  TL("meta-pipe requires a ~4-hour feasibility assessment before any protocol writing or extraction. The operator confirms it passed.",
                     "meta-pipe 要求在撰寫 protocol 或抽取資料前先做約 4 小時的可行性評估。操作者確認通過。"),
                  "AGENTS.md §'When User Says Start' (MANDATORY FIRST STEP)"),
            ],
            "artifacts": [{"name": "TOPIC.txt", "kind": "text", "preview": read_head(proj / "01_protocol/TOPIC.txt", 24)}],
            "metrics": [],
        },
        {
            "id": "01_protocol", "num": "01",
            "name": TL("Protocol", "計畫書"), "skill": "/ma-search-bibliography",
            "summary": TL(
                "PICO formalised to pico.yaml with eligibility criteria. (PROSPERO is a pre-run prep gate, not a step here.)",
                "PICO 形式化為 pico.yaml 並訂出納入條件。（PROSPERO 是跑前 prep gate，不在此步。）"),
            "gates": [],
            "artifacts": [{"name": "pico.yaml", "kind": "code", "preview": read_head(proj / "01_protocol/pico.yaml", 35)}],
            "metrics": [],
        },
        {
            "id": "02_search", "num": "02",
            "name": TL("Search & Dedupe", "搜尋與去重"), "skill": "/ma-search-bibliography",
            "summary": TL(
                "Your queries.txt is run against the database(s) and results are exported to a versioned .bib.",
                "用你的 queries.txt 對資料庫執行搜尋，結果匯出為版本化 .bib。"),
            "gates": [],
            "artifacts": [
                {"name": "SEARCH_COMPLETION_REPORT.md", "kind": "text", "preview": read_head(proj / "02_search/SEARCH_COMPLETION_REPORT.md", 30)},
                {"name": "round-01_pubmed_log.md", "kind": "text", "preview": read_text(proj / "02_search/round-01_pubmed_log.md", 1200)},
            ],
            "metrics": [{"label": TL("Records identified", "找到紀錄"), "value": "122"}, {"label": TL("Source", "來源"), "value": "PubMed/MEDLINE"}],
        },
        {
            "id": "03_screening", "num": "03",
            "name": TL("Title/Abstract Screening", "標題摘要篩選"), "skill": "/ma-screening-quality",
            "summary": TL(
                "Records are screened against PICO by an LLM. The configuration below shows exactly how the two reviewer columns are produced.",
                "由 LLM 依 PICO 篩選紀錄。下方設定顯示兩個 reviewer 欄位實際是怎麼產生的。"),
            "gates": [
                G("checkpoint",
                  TL("Inter-reviewer agreement κ ≥ 0.60 before Stage 04", "進入 Stage 04 前 inter-reviewer κ ≥ 0.60"),
                  TL("meta-pipe gates the 03→04 transition on Cohen's κ. In this finished example the threshold is treated as met.",
                     "meta-pipe 以 Cohen's κ 把關 03→04。在這份完成的範例中視為已達標。"),
                  "ma-end-to-end/SKILL.md §Quality Gates"),
                G("decision",
                  TL("Confirm analysis type: pairwise vs network", "確認分析型別：pairwise vs network"),
                  TL("A genuine fork that changes every downstream stage; meta-pipe names this the Analysis Type Confirmation Gate (Step 8).",
                     "這個分岔會改變所有下游階段；meta-pipe 稱之為 Analysis Type Confirmation Gate（Step 8）。"),
                  "AGENTS.md row 03b; ma-screening-quality/SKILL.md Step 8"),
            ],
            "llm": {
                "source": "tooling/python/ai_screen.py",
                "model": "claude -p --model haiku",
                "prompt": extract_screen_prompt(repo),
                "reviewer_mechanism": TL(
                    "`--reviewer 1` and `--reviewer 2` call the same model with the same prompt and only "
                    "write a different CSV column (Reviewer1_Decision / Reviewer2_Decision). The script even "
                    "prints: \"run with --reviewer 2 for dual review, or have a human fill Reviewer2 columns.\"",
                    "`--reviewer 1` 與 `--reviewer 2` 用同一個 model、同一條 prompt，只是寫入不同的 CSV 欄位"
                    "（Reviewer1_Decision / Reviewer2_Decision）。程式甚至印出："
                    "「run with --reviewer 2 for dual review, or have a human fill Reviewer2 columns.」"),
                "decisions": screening_decision_counts(proj),
            },
            "artifacts": [{"name": "AI_SCREENING_REPORT.md", "kind": "text", "preview": read_head(proj / "03_screening/AI_SCREENING_REPORT.md", 28)}],
            "metrics": [{"label": TL("Screened", "已篩"), "value": "122"}, {"label": TL("Excluded", "排除"), "value": "117"}, {"label": TL("To full-text", "進全文"), "value": "5"}],
        },
        {
            "id": "04_fulltext", "num": "04",
            "name": TL("Full-text Retrieval & Eligibility", "全文取得與資格審查"), "skill": "/ma-fulltext-management",
            "summary": TL(
                "Open-access PDFs are fetched for low-confidence studies via Unpaywall; paywalled PDFs the operator must supply.",
                "低信心研究的 OA PDF 由 Unpaywall 自動抓取；付費 PDF 需操作者自行提供。"),
            "gates": [
                G("upload",
                  TL("Supply paywalled full-text PDFs", "提供付費全文 PDF"),
                  TL("meta-pipe retrieves OA PDFs automatically, but flagged/paywalled studies need the operator to place the PDF in 04_fulltext/. The interface adds an upload box for exactly that step.",
                     "meta-pipe 會自動抓 OA PDF，但被標記/付費的研究需操作者把 PDF 放進 04_fulltext/。介面就為這一步加上傳框。"),
                  "ma-fulltext-management/SKILL.md Phase 2 (Targeted PDF Retrieval)"),
                G("checkpoint",
                  TL("Full-text screening κ ≥ 0.60 before Stage 05", "進入 Stage 05 前全文篩選 κ ≥ 0.60"),
                  TL("The 04→05 transition is gated on full-text screening agreement.",
                     "04→05 的轉換以全文篩選一致性把關。"),
                  "ma-end-to-end/SKILL.md §Quality Gates"),
            ],
            "artifacts": [
                {"name": "round-01_include_list.txt", "kind": "text", "preview": read_head(proj / "04_fulltext/round-01_include_list.txt", 12)},
                {"name": "PHASE4_SUMMARY.md", "kind": "text", "preview": read_head(proj / "04_fulltext/PHASE4_SUMMARY.md", 26)},
            ],
            "metrics": [{"label": TL("Full-text sought", "索取全文"), "value": "5"}, {"label": TL("Included", "納入"), "value": "5"}],
        },
        {
            "id": "05_extraction", "num": "05",
            "name": TL("Data Extraction & RoB", "資料抽取與 RoB"), "skill": "/ma-data-extraction",
            "summary": TL(
                "Structured outcome data are extracted; low-confidence fields are flagged. (A risk-of-bias schema is defined in pico.yaml.)",
                "抽取結構化結果資料；低信心欄位被標記。（pico.yaml 已定義 risk-of-bias schema。）"),
            "gates": [
                G("checkpoint",
                  TL("Extraction completeness — all included studies extracted", "抽取完整性 — 所有納入研究皆已抽取"),
                  TL("meta-pipe gates the 05→06 transition on extraction completeness.",
                     "meta-pipe 以抽取完整性把關 05→06。"),
                  "ma-end-to-end/SKILL.md §Quality Gates"),
            ],
            "artifacts": [
                {"name": "round-01_extraction.csv", "kind": "table", "preview": read_text(proj / "05_extraction/round-01_extraction.csv", 1800)},
                {"name": "round-01_QUICK_STATS.md", "kind": "text", "preview": read_head(proj / "05_extraction/round-01_QUICK_STATS.md", 24)},
            ],
            "metrics": [{"label": TL("Trials", "試驗數"), "value": "5"}, {"label": TL("Patients", "病人數"), "value": "2,402"}],
        },
        {
            "id": "06_analysis", "num": "06",
            "name": TL("Meta-Analysis (R)", "統合分析（R）"), "skill": "/ma-meta-analysis",
            "summary": TL(
                "Random-effects pooling in R (meta/metafor): forest plots, subgroup and sensitivity analyses.",
                "在 R（meta/metafor）做隨機效應合併：forest plot、次群組與敏感度分析。"),
            "gates": [
                G("checkpoint",
                  TL("All figures ≥ 300 DPI before Stage 07", "進入 Stage 07 前所有圖 ≥ 300 DPI"),
                  TL("The 06→07 transition is gated on figure resolution.",
                     "06→07 的轉換以圖檔解析度把關。"),
                  "ma-end-to-end/SKILL.md §Quality Gates"),
            ],
            "artifacts": [
                {"name": "tables_pCR_meta_analysis_results.csv", "kind": "table", "preview": read_text(proj / "06_analysis/tables_pCR_meta_analysis_results.csv", 1200)},
                {"name": "tables_safety_meta_analysis_summary.csv", "kind": "table", "preview": read_text(proj / "06_analysis/tables_safety_meta_analysis_summary.csv", 800)},
            ],
            "metrics": [{"label": "pCR RR", "value": "1.26 (1.16–1.37)"}, {"label": "EFS HR", "value": "0.66 (0.51–0.86)"}, {"label": "I²", "value": "0%"}],
        },
        {
            "id": "07_manuscript", "num": "07",
            "name": TL("Manuscript (Quarto)", "稿件（Quarto）"), "skill": "/ma-manuscript-quarto",
            "summary": TL(
                "Sections, tables, figures and references are assembled and rendered.",
                "組裝並渲染章節、表格、圖與參考文獻。"),
            "gates": [
                G("approval",
                  TL("Approve the manuscript outline before any writing", "撰寫前先核准稿件大綱"),
                  TL("meta-pipe makes Phase 1 (outline + checklist) mandatory and requires operator approval before a single section is written.",
                     "meta-pipe 把 Phase 1（大綱 + 檢核表）設為必做，且要操作者核准後才動筆寫任何一節。"),
                  "ma-manuscript-quarto/SKILL.md Phase 1 (MANDATORY before any writing)"),
            ],
            "artifacts": [{"name": "00_abstract.md", "kind": "text", "preview": read_text(proj / "07_manuscript/00_abstract.md", 2400)}],
            "metrics": [{"label": TL("Word count", "字數"), "value": "~4,900"}, {"label": TL("Tables", "表格"), "value": "3 + 4 supp."}],
        },
        {
            "id": "08_grade", "num": "08",
            "name": TL("GRADE & Peer Review", "GRADE 與同儕審查"), "skill": "/ma-peer-review",
            "summary": TL(
                "GRADE certainty assessment and Summary-of-Findings table are written into the manuscript supplement.",
                "GRADE 證據等級評估與 Summary-of-Findings 表寫入稿件補充資料。"),
            "gates": [],
            "artifacts": [{"name": "SupplementaryTable4_GRADE_Profile.md", "kind": "text", "preview": read_head(proj / "07_manuscript/tables/SupplementaryTable4_GRADE_Profile.md", 30)}],
            "metrics": [{"label": TL("Primary outcome certainty", "主要結果證據等級"), "value": "⊕⊕⊕⊕ HIGH"}],
        },
        {
            "id": "09_qa", "num": "09",
            "name": TL("QA & Submission Prep", "QA 與投稿準備"), "skill": "/ma-publication-quality",
            "summary": TL(
                "Overclaim audit, DOI verification, PRISMA completeness and a final readiness score.",
                "誇大宣稱稽核、DOI 驗證、PRISMA 完整性與最終就緒分數。"),
            "gates": [
                G("checkpoint",
                  TL("PRISMA 27/27 + publication readiness ≥ 95%", "PRISMA 27/27 + 發表就緒 ≥ 95%"),
                  TL("The final gate: validate_pipeline.py / final_qa_report.py block on failures.",
                     "最後一道 gate：validate_pipeline.py / final_qa_report.py 失敗即擋下。"),
                  "ma-end-to-end/SKILL.md §Resources; ma-publication-quality/SKILL.md"),
            ],
            "artifacts": [{"name": "doi_verification_report.md", "kind": "text", "preview": read_text(proj / "09_qa/doi_verification_report.md", 1600)}],
            "metrics": [{"label": TL("Status", "狀態"), "value": "99% complete"}],
        },
    ]


# --- our suggestions (NOT shipped in the PR) -------------------------------


def build_suggestions() -> list[dict]:
    return [
        {
            "title": TL("Two genuinely independent reviewers + conflict resolution", "兩位真正獨立的 reviewer + 衝突解決"),
            "where": TL("Screening (Stage 03)", "篩選（Stage 03）"),
            "why": TL(
                "meta-pipe's `--reviewer 1/2` runs one model with one prompt and writes two columns; in the example decision_r1 = decision_r2 = final (all 27/63/32). Cochrane Handbook §6.4 expects two independent reviewers and a recorded conflict-resolution step.",
                "meta-pipe 的 `--reviewer 1/2` 是同一個 model、同一條 prompt 寫兩欄；範例中 decision_r1 = decision_r2 = final（全部 27/63/32）。Cochrane Handbook §6.4 要求兩位獨立 reviewer 並記錄衝突解決。"),
        },
        {
            "title": TL("Multi-database search + cross-source de-duplication", "多資料庫搜尋 + 跨來源去重"),
            "where": TL("Search (Stage 02)", "搜尋（Stage 02）"),
            "why": TL(
                "The example searched only PubMed (122 records) and the dedupe step is a no-op. Cochrane Handbook §4.4 expects at least MEDLINE + Embase + CENTRAL.",
                "範例只搜了 PubMed（122 筆），去重步驟形同無作用。Cochrane Handbook §4.4 要求至少 MEDLINE + Embase + CENTRAL。"),
        },
        {
            "title": TL("Risk-of-bias assessment as an enforced gate", "Risk-of-bias 評估作為強制 gate"),
            "where": TL("Extraction / RoB (Stage 05)", "抽取 / RoB（Stage 05）"),
            "why": TL(
                "pico.yaml defines a RoB 2 schema, but no per-study × domain assessment is required before analysis runs. We would gate Stage 06 on a completed RoB matrix.",
                "pico.yaml 定義了 RoB 2 schema，但分析前並不要求逐研究×領域的評估。我們會以完成的 RoB 矩陣把關 Stage 06。"),
        },
        {
            "title": TL("GRADE certainty sign-off gate", "GRADE 證據等級簽核 gate"),
            "where": TL("GRADE (Stage 08)", "GRADE（Stage 08）"),
            "why": TL(
                "GRADE certainty is hand-written with no gate. Downgrade/upgrade judgements should be confirmed before any publication-quality certainty claim is made.",
                "GRADE 由人手寫、無 gate。降級/升級判斷應在做出任何發表級證據等級宣稱前確認。"),
        },
        {
            "title": TL("Search-strategy builder & ≥ 2-database validator", "搜尋策略 builder 與 ≥ 2 資料庫驗證"),
            "where": TL("Search prep", "搜尋準備"),
            "why": TL(
                "queries.txt is authored entirely by hand (only a MeSH-expand helper exists). Nothing validates database coverage or strategy completeness before the search runs.",
                "queries.txt 完全靠人手寫（只有 MeSH 展開工具）。搜尋前沒有任何東西驗證資料庫涵蓋度或策略完整性。"),
        },
    ]


def main() -> None:
    ap = argparse.ArgumentParser(description="Build demo_manifest.json for the meta-pipe web UI")
    ap.add_argument("--project", default="projects/ici-breast-cancer", help="finished project to replay")
    ap.add_argument("--repo-root", default=str(Path(__file__).resolve().parent.parent), help="meta-pipe repo root")
    ap.add_argument("--with-suggestions", action="store_true",
                    help="also emit suggestions.json (our opinion; keep OFF the upstream PR)")
    args = ap.parse_args()

    repo = Path(args.repo_root).resolve()
    proj = (repo / args.project).resolve()
    web = repo / "web"
    static = web / "static"
    assets = static / "assets"
    assets.mkdir(parents=True, exist_ok=True)

    if not proj.exists():
        raise SystemExit(f"project not found: {proj}")

    prisma_src = proj / "figures/prisma_flow_static.svg"
    if prisma_src.exists():
        shutil.copy2(prisma_src, assets / "prisma_flow_static.svg")

    manifest = {
        "project": {
            "name": proj.name,
            "title": TL(
                "Neoadjuvant Immunotherapy + Chemotherapy vs Chemotherapy Alone for Early TNBC",
                "早期三陰性乳癌之術前免疫治療併化療 vs 單用化療"),
            "subtitle": TL(
                "A systematic review & meta-analysis of randomized controlled trials",
                "隨機對照試驗的系統性回顧與統合分析"),
            "headline": [
                {"label": TL("RCTs", "隨機試驗"), "value": "5"},
                {"label": TL("Patients", "病人數"), "value": "2,402"},
                {"label": "pCR RR", "value": "1.26 (1.16–1.37)"},
                {"label": TL("Certainty", "證據等級"), "value": "⊕⊕⊕⊕ HIGH"},
            ],
            "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        },
        "prep": build_prep(),
        "stages": build_stages(proj, repo),
        "output": {
            "prisma_svg": "assets/prisma_flow_static.svg" if prisma_src.exists() else "",
            "abstract": read_text(proj / "07_manuscript/00_abstract.md", 3000),
            "downloads": [
                {"label": "manuscript.pdf", "note": TL("rendered in live mode via Quarto", "live 模式用 Quarto 渲染")},
                {"label": TL("PRISMA 2020 flow diagram", "PRISMA 2020 流程圖"), "note": TL("shown above", "見上方")},
                {"label": TL("forest plots + SoF table", "forest plot + SoF 表"), "note": TL("produced by stage 06 / 08", "由 stage 06 / 08 產生")},
            ],
        },
    }

    out = static / "demo_manifest.json"
    out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    msg = f"wrote {out.name} ({out.stat().st_size:,} bytes, {len(manifest['stages'])} stages, {len(manifest['prep'])} prep gates)"

    sug = static / "suggestions.json"
    if args.with_suggestions:
        sug.write_text(json.dumps({"suggestions": build_suggestions()}, indent=2, ensure_ascii=False), encoding="utf-8")
        msg += f"; wrote {sug.name} ({len(build_suggestions())} suggestions)"
    else:
        if sug.exists():
            sug.unlink()
        msg += "; suggestions.json omitted (PR build)"
    print(msg)


if __name__ == "__main__":
    main()
