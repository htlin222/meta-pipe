# Claude CLI flag inventory (for `ai_screen.py` and friends)

Tools in `tooling/python/` that shell out to the `claude` CLI assume a
specific set of flags exist. This file pins the minimum supported Claude
Code version and documents exactly which flags are load-bearing, so a CLI
upgrade breakage fails fast and loud instead of silently degrading.

## Minimum version

**Claude Code ≥ 2.1.100** (verified on macOS, 2026-04-10).

Check with: `claude --version`

## Required flags

These flags MUST exist in `claude -p --help` or screening will not work:

| Flag              | Purpose                                                                                                                              |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| `-p` / `--print`  | Non-interactive single-shot mode.                                                                                                   |
| `--bare`          | Minimal mode: skip hooks, LSP, plugin sync, auto-memory, CLAUDE.md auto-discovery. Cuts per-call input tokens from ~10k → ~1.5k.    |
| `--output-format` | Use `json` for a stable envelope (`{"result": "..."}`). Falls back to raw stdout if JSON parse fails.                                |
| `--model`         | Pin to `haiku` for screening throughput.                                                                                             |

`ai_screen.py` calls `_assert_claude_cli()` at startup to verify `--bare`
and `--output-format` are both present in the help text and exits with a
clear error if either is missing.

### `--bare` and authentication

`--bare` is load-bearing for per-call cost, but it has a sharp edge:

> Anthropic auth is strictly `ANTHROPIC_API_KEY` or `apiKeyHelper` via
> `--settings` (OAuth and keychain are never read).

In other words, if you're logged in interactively (`claude /login`) but
have no `ANTHROPIC_API_KEY` exported, `--bare` will hit
`"Not logged in · Please run /login"` even though an interactive
`claude` works fine.

`_invoke_claude()` handles this by only adding `--bare` when
`ANTHROPIC_API_KEY` is set in the environment, and printing a one-time
warning if it has to fall back. The fallback still works — it just pays
the full system-prompt overhead. Set `ANTHROPIC_API_KEY` to stay on the
fast path.

## Optional / nice-to-have flags (not required)

- `--no-session-persistence` — disables session save; only works with `--print`.
- `--disable-slash-commands` — belt-and-suspenders on top of `--bare`.

These are not yet wired into the scripts because `--bare` already covers
the primary concern (system-prompt and hook overhead). Add them if profiling
shows further savings.

## Out of scope

Per the 2026-04-10 design decision on issue #38, `ai_screen.py` continues
to use the `claude -p` subprocess model short-term. Swapping to a direct
Anthropic SDK call is a separate, deliberate migration — do not do it as a
drive-by change.

## What to update when upgrading Claude Code

1. Run `claude -p --help` and compare against the "Required flags" table.
2. Update `MIN_CLAUDE_CLI_VERSION` in `ai_screen.py` if a newer version is
   required.
3. If a required flag is renamed or removed, update both `_invoke_claude()`
   and `_assert_claude_cli()` in `ai_screen.py` in the same commit, plus
   this document.
