#!/usr/bin/env bash
# Preflight: prove the whole pipeline can run BEFORE step 1 submits.
#
#   .demo/preflight.sh [--fix]
#
# The first run of this harness discovered JAGS, rjags, LaTeX and several R
# packages were missing — at hour 1.5, from inside a stage that then had to be
# abandoned. Every one of those was knowable in 30 seconds. So: check them here,
# check that things *load and run* rather than merely being installed, and fail
# loudly with the command that fixes each one.
#
# --fix attempts the repairs it knows how to make.

set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/.." && pwd)"
# shellcheck source=/dev/null
. "$HERE/config.env"

FIX=0
[ "${1:-}" = "--fix" ] && FIX=1

pass=0; warn=0; fail=0
REMEDY=""   # newline-separated; an empty bash 3.2 array trips `set -u`

ok()   { printf '  \033[32m✓\033[0m %s\n' "$1"; pass=$((pass+1)); }
no()   { printf '  \033[31m✗\033[0m %s\n' "$1"; fail=$((fail+1)); [ -n "${2:-}" ] && REMEDY="$REMEDY  • $1 → $2"$'\n'; }
meh()  { printf '  \033[33m!\033[0m %s\n' "$1"; warn=$((warn+1)); [ -n "${2:-}" ] && REMEDY="$REMEDY  • $1 → $2"$'\n'; }
head_() { printf '\n\033[1m%s\033[0m\n' "$1"; }

# --- 1. command-line tools ---------------------------------------------------
head_ "Tools"
for t in jq uv rip R Rscript quarto pandoc herdr git; do
  if command -v "$t" >/dev/null 2>&1; then ok "$t"
  else no "$t missing" "install $t"; fi
done

# --- 2. the worker pane ------------------------------------------------------
head_ "Worker pane ($WORKER_PANE)"
pane_json="$(herdr pane get "$WORKER_PANE" 2>/dev/null)"
if [ -z "$pane_json" ] || [ "$(jq -r '.result.pane.pane_id // ""' <<<"$pane_json")" = "" ]; then
  no "pane $WORKER_PANE not found" "herdr pane list  # then set WORKER_PANE in .demo/config.env"
else
  ok "pane exists"
  agent="$(jq -r '.result.pane.agent // "none"' <<<"$pane_json")"
  [ "$agent" = "claude" ] && ok "runs a claude agent" || no "pane agent is '$agent', not claude" "start Claude Code in that pane"
  st="$(jq -r '.result.pane.agent_status // "unknown"' <<<"$pane_json")"
  case "$st" in
    idle|done) ok "agent is $st" ;;
    working)   meh "agent is mid-turn — the runner will wait it out" ;;
    *)         meh "agent status is '$st'" ;;
  esac
  cwd="$(jq -r '.result.pane.cwd // ""' <<<"$pane_json")"
  [ "$cwd" = "$REPO" ] && ok "pane cwd is the repo" || meh "pane cwd is $cwd, not $REPO"
fi

# --- 3. R: packages must LOAD, not merely be installed -----------------------
head_ "R packages"
r_report="$(Rscript -e '
pkgs <- c("gemtc","rjags","netmeta","meta","metafor","ggplot2","gt","dplyr","tidyr","readr","coda","renv","igraph","dmetar")
for (p in pkgs) {
  okp <- tryCatch({ suppressMessages(library(p, character.only=TRUE)); TRUE }, error=function(e) FALSE)
  cat(p, if (okp) "OK" else "FAIL", "\n")
}' 2>/dev/null)"
while read -r p state; do
  [ -z "$p" ] && continue
  if [ "$state" = "OK" ]; then ok "R: $p"
  else no "R: $p does not load" "Rscript -e 'install.packages(\"$p\")'"; fi
done <<<"$r_report"

# --- 4. JAGS must actually compile a model -----------------------------------
# rjags being installed proves nothing: the CRAN binary links libjags.4, and a
# Homebrew JAGS 5 leaves it unloadable. Compile a trivial model instead.
head_ "JAGS engine (the repo's primary NMA engine is gemtc → rjags → JAGS)"
if Rscript -e 'suppressMessages(library(rjags)); invisible(jags.model(textConnection("model{ y ~ dnorm(mu,1); mu ~ dnorm(0,0.001) }"), data=list(y=1), quiet=TRUE))' >/dev/null 2>&1; then
  ok "JAGS compiles a model through rjags"
else
  no "rjags cannot reach a working JAGS" "install JAGS 4.3.x into /usr/local (the CRAN rjags binary links libjags.4.dylib); JAGS 5 is not compatible"
fi

# --- 5. Quarto must actually render a PDF ------------------------------------
head_ "Quarto rendering"
# Test from a neutral directory, the way stage 07 renders (cwd = the manuscript
# folder). Quarto reads .env/.env.example from the CURRENT directory only.
tmp="$(mktemp -d)"
printf -- '---\ntitle: preflight\nformat: html\n---\n\nok\n' > "$tmp/t.qmd"
if ( cd "$tmp" && quarto render t.qmd --to html ) >/dev/null 2>&1; then ok "renders HTML"
else no "cannot render HTML" "check the quarto install"; fi

printf -- '---\ntitle: preflight\nformat: pdf\n---\n\nok\n' > "$tmp/p.qmd"
if ( cd "$tmp" && quarto render p.qmd --to pdf ) >/dev/null 2>&1; then ok "renders PDF"
elif [ "$FIX" = 1 ]; then
  printf '    installing tinytex...\n'; quarto install tinytex --no-prompt >/dev/null 2>&1
  ( cd "$tmp" && quarto render p.qmd --to pdf ) >/dev/null 2>&1 \
    && ok "renders PDF (after installing tinytex)" || no "cannot render PDF" "quarto install tinytex"
else
  no "cannot render PDF — stage 08 asks for index.pdf" "quarto install tinytex   (or .demo/preflight.sh --fix)"
fi

# The trap: quarto's dotenv treats every key in .env.example as required and
# non-empty. With a partially-filled .env in the repo root, any render started
# from there dies before it reads the document. Rendering from the manuscript
# directory is unaffected, which is where stage 07 runs.
if [ -f "$REPO/.env" ] && [ -f "$REPO/.env.example" ]; then
  cp "$tmp/t.qmd" "$REPO/.preflight-quarto.qmd" 2>/dev/null
  if ( cd "$REPO" && quarto render .preflight-quarto.qmd --to html ) >/dev/null 2>&1; then
    ok "quarto also works from the repo root"
  else
    meh "quarto fails from the repo root (empty keys in .env vs .env.example) — render from the manuscript directory, never the repo root"
  fi
  rm -f "$REPO/.preflight-quarto.qmd" "$REPO/.preflight-quarto.html" 2>/dev/null
  rm -rf "$REPO/.preflight-quarto_files" 2>/dev/null
fi
rm -rf "$tmp"

# --- 6. credentials, tested live rather than merely present ------------------
head_ "API credentials (a key in .env is not the same as a key that authenticates)"
if [ -f "$REPO/.env" ]; then
  ok ".env exists"
  # shellcheck source=/dev/null
  set -a; . "$REPO/.env" 2>/dev/null; set +a

  if [ -n "${PUBMED_API_KEY:-}" ]; then
    code="$(curl -s -o /dev/null -w '%{http_code}' "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=cancer&retmax=1&api_key=${PUBMED_API_KEY}")"
    [ "$code" = "200" ] && ok "PubMed key authenticates" || no "PubMed key rejected (HTTP $code)" "check PUBMED_API_KEY"
  else
    meh "PUBMED_API_KEY unset — E-utilities still work, at a lower rate limit"
  fi

  if [ -n "${SCOPUS_API_KEY:-}" ]; then
    code="$(curl -s -o /dev/null -w '%{http_code}' -H "X-ELS-APIKey: ${SCOPUS_API_KEY}" "https://api.elsevier.com/content/search/scopus?query=cancer&count=1")"
    [ "$code" = "200" ] && ok "Scopus key authenticates" \
      || no "Scopus key rejected (HTTP $code)" "check SCOPUS_API_KEY; 401 often means the key is not entitled from this network"
    [ -z "${SCOPUS_INST_TOKEN:-}" ] && meh "SCOPUS_INST_TOKEN unset — off-campus coverage will be reduced"
  else
    meh "SCOPUS_API_KEY unset — PRISMA needs a second database; the run will substitute ClinicalTrials.gov and record a deviation"
  fi

  if [ -n "${UNPAYWALL_EMAIL:-}" ]; then
    # Unpaywall takes an email as its politeness parameter; a malformed one is
    # rejected, so test it rather than trust that the field is filled in.
    if curl -s "https://api.unpaywall.org/v2/10.1056/NEJMoa1814017?email=${UNPAYWALL_EMAIL}" | jq -e '.doi' >/dev/null 2>&1; then
      ok "Unpaywall resolves OA locations"
    else
      no "Unpaywall rejected UNPAYWALL_EMAIL" "check the address in .env"
    fi
  else
    meh "UNPAYWALL_EMAIL unset — stage 04 full-text retrieval degrades to fully-open PDFs only" "set UNPAYWALL_EMAIL in .env"
  fi
else
  meh ".env missing — only keyless sources will work" "cp .env.example .env and fill it in"
fi

# --- 7. the prompts must reference things that exist -------------------------
# A typo like `--stage title` for a flag that is spelled `--stage abstract`
# costs a whole stage to discover. Catch it here.
head_ "Prompt lint"
lint_fail=0
while read -r script; do
  [ -f "$REPO/$script" ] || { no "prompts reference missing script: $script" "fix the path in .demo/prompts/"; lint_fail=1; }
done < <(grep -rhoE '(tooling/python|ma-[a-z-]+/scripts)/[a-zA-Z_0-9]+\.py' "$HERE/prompts/" 2>/dev/null | sort -u)

while read -r scr flag; do
  [ -z "$scr" ] && continue
  [ -f "$REPO/$scr" ] || continue
  if ! ( cd "$REPO" && uv run "$scr" --help 2>&1 | grep -q -- "$flag" ); then
    no "prompts pass $flag to $(basename "$scr"), which does not accept it" "$(basename "$scr") --help"
    lint_fail=1
  fi
done < <(grep -rhoE '(tooling/python|ma-[a-z-]+/scripts)/[a-zA-Z_0-9]+\.py(( --?[a-zA-Z-]+)( [^ `]+)?)+' "$HERE/prompts/" 2>/dev/null \
         | awk '{ s=$1; for (i=2;i<=NF;i++) if ($i ~ /^--/) print s, $i }' | sort -u)
[ "$lint_fail" = 0 ] && ok "prompts reference only scripts and flags that exist"

# --- 8. the Stop hook ---------------------------------------------------------
head_ "Stop hook"
if [ -x "$REPO/.claude/hooks/pipeline-progress.sh" ]; then
  if printf '{"session_id":"preflight"}' | bash "$REPO/.claude/hooks/pipeline-progress.sh" >/dev/null 2>&1; then
    ok "hook runs and writes a snapshot"
  else
    no "hook errors" "bash -x .claude/hooks/pipeline-progress.sh < /dev/null"
  fi
else
  no "hook missing or not executable" "chmod +x .claude/hooks/pipeline-progress.sh"
fi
jq -e '.hooks.Stop' "$REPO/.claude/settings.json" >/dev/null 2>&1 \
  && ok "hook is registered in .claude/settings.json" \
  || no "hook not registered" "add the Stop hook to .claude/settings.json"
meh "a worker session started before the hook was last edited keeps the old copy; the runner snapshots on its own regardless"

# --- 9. the project ------------------------------------------------------------
head_ "Project ($PROJECT)"
pd="$REPO/projects/$PROJECT"
[ -d "$pd" ] && ok "project directory exists" || no "projects/$PROJECT missing" "uv run tooling/python/init_project.py --name $PROJECT"
if [ -s "$pd/TOPIC.txt" ] && ! grep -q '<Paste your meta-analysis topic here>' "$pd/TOPIC.txt"; then
  ok "TOPIC.txt is filled in"
else
  no "TOPIC.txt is empty or still the placeholder" "write the research question into projects/$PROJECT/TOPIC.txt"
fi
( cd "$REPO" && uv run tooling/python/project_status.py --project "$PROJECT" >/dev/null 2>&1 ) \
  && ok "project_status.py runs" || no "project_status.py fails" "uv sync in tooling/python"

avail="$(df -g "$REPO" | awk 'NR==2{print $4}')"
[ "${avail:-0}" -ge 5 ] && ok "disk: ${avail}G free" || meh "only ${avail}G free — searches cache tens of MB per round"

# --- verdict -------------------------------------------------------------------
printf '\n\033[1m%d passed, %d warnings, %d failed\033[0m\n' "$pass" "$warn" "$fail"
if [ -n "$REMEDY" ]; then
  printf '\nTo fix:\n%s' "$REMEDY"
fi
[ "$fail" -gt 0 ] && { printf '\n\033[31mPreflight failed — do not start a run.\033[0m\n'; exit 1; }
printf '\n\033[32mPreflight passed.\033[0m\n'
