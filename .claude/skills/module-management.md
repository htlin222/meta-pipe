---
name: module-management
description: Validate and maintain module registry. Use after adding new scripts, features, or modules to ensure proper documentation and integration.
---

# Module Management Skill

## Purpose

Ensure every new script, template, or feature is properly registered across all
documentation layers. Prevents "orphan scripts" (undocumented code) and "ghost
references" (docs pointing to non-existent files).

## When to Use

- After adding a new Python script to any `ma-*/scripts/` or `tooling/python/`
- After creating new reference templates in `ma-*/references/`
- After renaming or removing scripts
- Before creating a PR for new features
- When running periodic maintenance

## Validation Layers

Every user-facing script must be registered in **4 layers**:

| Layer | File | Purpose | Required |
| --- | --- | --- | --- |
| 1. Module SKILL.md | `ma-*/SKILL.md` | Module-level documentation | Yes |
| 2. CLAUDE.md | `CLAUDE.md` | Agent instructions (commands reference) | Yes |
| 3. GETTING_STARTED.md | `GETTING_STARTED.md` | User-facing quick-start guide | Yes |
| 4. tests/README.md | `tests/README.md` | Test instructions and expected results | Recommended |

## Workflow: Adding a New Script

### Step 1: Create the script

Place it in the correct module:
- Pipeline scripts → `ma-{module}/scripts/{name}.py`
- Utility/tooling scripts → `tooling/python/{name}.py`

### Step 2: Update Module SKILL.md

In the script's parent module `SKILL.md`:
- Add to **Outputs** section (what files does it produce?)
- Add to **Resources** section (reference the script path)
- Add to **Workflow** section if it changes the process

### Step 3: Update CLAUDE.md

In the relevant `<details>` stage section:
- Add the `uv run` command with all flags
- Include expected output description
- Reference any new templates in `references/`

### Step 4: Update GETTING_STARTED.md

Add a user-friendly command example under the appropriate stage section.

### Step 5: Update tests/README.md

Add a test command using test fixtures:
```bash
uv run ../../ma-{module}/scripts/{name}.py \
  --input ../../tests/fixtures/... \
  --output /tmp/test_output
# Expected: description of expected output
```

Add a row to the Expected Results table.

### Step 6: Run validation

```bash
cd tooling/python
uv run ../../ma-end-to-end/scripts/validate_module_registry.py \
  --root ../.. \
  --out-md ../../09_qa/module_registry_report.md \
  --out-json ../../09_qa/module_registry.json
```

Fix any errors before committing.

### Step 7: Smoke test

Run the new script against test fixtures or real data to verify it works:
```bash
cd tooling/python
uv run ../../ma-{module}/scripts/{name}.py --help
uv run ../../ma-{module}/scripts/{name}.py [args using test fixtures]
```

## Workflow: Adding a New Module

1. Create `ma-{name}/` directory with:
   - `SKILL.md` (with YAML frontmatter: name, description)
   - `scripts/` directory
   - `references/` directory (if templates needed)
2. Follow Steps 2-7 above for each script in the module
3. Add the module to `ma-end-to-end/SKILL.md` pipeline stage list

## Workflow: Removing a Script

1. Check for references: `grep -r "script_name.py" --include="*.md"`
2. Remove from all 4 documentation layers
3. Run validation to confirm no ghost references
4. Delete the script file (use `rip` not `rm`)

## Validation Script Reference

```bash
# Basic check (warnings only for missing test docs)
uv run ../../ma-end-to-end/scripts/validate_module_registry.py --root ../..

# Strict check (all warnings become errors)
uv run ../../ma-end-to-end/scripts/validate_module_registry.py --root ../.. --strict

# Full report output
uv run ../../ma-end-to-end/scripts/validate_module_registry.py \
  --root ../.. \
  --out-md ../../09_qa/module_registry_report.md \
  --out-json ../../09_qa/module_registry.json
```

### Exit codes
- `0` = all checks pass
- `1` = warnings only (missing test docs)
- `2` = errors (orphan scripts or ghost references)

## Checklist Template

When adding a new feature, use this checklist:

- [ ] Script created in correct module
- [ ] Module `SKILL.md` updated (Outputs, Resources, Workflow)
- [ ] `CLAUDE.md` updated (Commands Reference section)
- [ ] `GETTING_STARTED.md` updated (user-facing docs)
- [ ] `tests/README.md` updated (test command + expected results)
- [ ] Smoke test passed
- [ ] `validate_module_registry.py` passes (exit code 0)
