#!/usr/bin/env bash
# Archive the current run and start the project clean.
#
#   .demo/reset.sh --yes [--keep-search]
#
# --keep-search carries 02_search/ across, so a rerun can skip the slowest,
# most rate-limited stage and still be a genuine clean run of everything after it.
#
# Nothing is deleted: the old project is moved under projects/_archive/.

set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/.." && pwd)"
# shellcheck source=/dev/null
. "$HERE/config.env"

yes=0; keep_search=0
for a in "$@"; do
  case "$a" in
    --yes) yes=1 ;;
    --keep-search) keep_search=1 ;;
    *) printf 'unknown argument: %s\n' "$a" >&2; exit 2 ;;
  esac
done

pd="$REPO/projects/$PROJECT"
[ -d "$pd" ] || { printf 'projects/%s does not exist — nothing to reset\n' "$PROJECT"; exit 0; }

if [ "$yes" != 1 ]; then
  printf 'This archives projects/%s and re-initializes it.\n' "$PROJECT"
  printf 'Re-run with --yes to proceed.\n'
  exit 1
fi

stamp="$(date +%Y%m%d-%H%M%S)"
archive="$REPO/projects/_archive/$PROJECT-$stamp"
mkdir -p "$(dirname "$archive")"

topic="$(mktemp)"; cp "$pd/TOPIC.txt" "$topic"
search=""
if [ "$keep_search" = 1 ] && [ -d "$pd/02_search" ]; then
  search="$(mktemp -d)"; cp -R "$pd/02_search/." "$search/"
fi

command mv "$pd" "$archive"
printf 'archived → %s\n' "$archive"

( cd "$REPO" && uv run tooling/python/init_project.py --name "$PROJECT" >/dev/null )
command cp "$topic" "$pd/TOPIC.txt"; rm -f "$topic"
printf 'reinitialized projects/%s with its TOPIC.txt\n' "$PROJECT"

if [ -n "$search" ]; then
  mkdir -p "$pd/02_search"
  command cp -R "$search/." "$pd/02_search/"
  rm -rf "$search"
  printf 'carried 02_search/ forward\n'
fi

rm -f "$HERE/CURRENT_STEP"
[ -f "$HERE/run.log" ] && command mv "$HERE/run.log" "$archive/run.log"
printf 'harness state cleared\n\nNext: .demo/preflight.sh && .demo/run.sh\n'
