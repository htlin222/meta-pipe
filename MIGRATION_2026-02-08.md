# Project Structure Migration Report

**Date**: 2026-02-08
**Status**: ✅ Complete

## Summary

Successfully separated project-specific data from framework code by moving all projects to the `projects/` directory.

## Changes Made

### 1. ✅ File System Changes

**Moved to `projects/legacy/`**:

- `01_protocol/` → `projects/legacy/01_protocol/`
- `02_search/` → `projects/legacy/02_search/`
- `03_screening/` → `projects/legacy/03_screening/`
- `04_fulltext/` → `projects/legacy/04_fulltext/`
- `05_extraction/` → `projects/legacy/05_extraction/`
- `06_analysis/` → `projects/legacy/06_analysis/`
- `07_manuscript/` → `projects/legacy/07_manuscript/`
- `08_reviews/` → `projects/legacy/08_reviews/`
- `09_qa/` → `projects/legacy/09_qa/`
- `TOPIC.txt` → `projects/legacy/TOPIC.txt`
- `feasibility_abstracts.json` → `projects/legacy/feasibility_abstracts.json`

**Created**:

- `projects/.gitkeep` - Ensures projects/ is tracked by Git
- `projects/legacy/README.md` - Explains legacy data

### 2. ✅ Git Configuration

**Updated `.gitignore`**:

```gitignore
# Projects Directory
projects/*
!projects/.gitkeep
!projects/ici-breast-cancer/
!projects/legacy/README.md
```

- All projects are now ignored by Git except documented examples
- Prevents accidental commits of project-specific data

### 3. ✅ Documentation Updates

**AGENTS.md (CLAUDE.md)**:

- ✅ Added project structure overview
- ✅ Updated all command examples to use `projects/<project-name>/`
- ✅ Updated `--root` parameter usage to `../../projects/<project-name>`
- ✅ Updated "When User Says Start" section

**README.md**:

- ✅ Updated Quick Start with project initialization
- ✅ Added Project Structure section
- ✅ Updated "What Claude Does" section
- ✅ Updated Pipeline Overview with project paths

**GETTING_STARTED.md**:

- ✅ Added project structure explanation at top
- ✅ Updated all command examples with new paths
- ✅ Updated project initialization instructions

### 4. ✅ Script Updates

**ma-end-to-end/scripts/init_project.py**:

- ✅ Changed from `--root` to `--name` parameter (required)
- ✅ Auto-creates projects in `projects/<name>/`
- ✅ Added existence check with user confirmation
- ✅ Added helpful next steps output
- ✅ Backward compatible with `--root` for advanced users

**Usage**:

```bash
# New way (recommended)
uv run ma-end-to-end/scripts/init_project.py --name my-meta-analysis

# Old way (still works)
uv run ma-end-to-end/scripts/init_project.py --root projects/my-meta-analysis
```

## New Directory Structure

```
meta-pipe/
├── ma-*/                    # Framework code modules ✅
├── docs/                    # Framework documentation ✅
├── tooling/                 # Shared tools and scripts ✅
├── tests/                   # Test suites ✅
├── .gitignore               # Updated to ignore projects/* ✅
├── AGENTS.md                # Updated with new paths ✅
├── README.md                # Updated with new workflow ✅
├── GETTING_STARTED.md       # Updated with new paths ✅
└── projects/                # All meta-analysis projects ✅
    ├── .gitkeep             # Keeps directory in Git ✅
    ├── legacy/              # Historical data (migrated) ✅
    │   ├── 01_protocol/
    │   ├── 02_search/
    │   ├── ...
    │   ├── TOPIC.txt
    │   └── README.md        # Explains legacy status ✅
    └── ici-breast-cancer/   # Example project (tracked) ✅
```

## Testing

✅ **Test passed**: Created and verified `projects/test-project/`

- All stage folders created correctly
- TOPIC.txt file present
- Cleanup successful

## User Impact

### Before Migration

```bash
# Projects mixed with framework code
meta-pipe/
├── 01_protocol/        # ❌ Project data in root
├── 02_search/          # ❌ Project data in root
├── ma-*/               # Framework code
└── docs/               # Documentation
```

### After Migration

```bash
# Clean separation
meta-pipe/
├── ma-*/               # ✅ Framework code only
├── docs/               # ✅ Documentation
└── projects/           # ✅ All projects isolated
    └── my-project/
        ├── 01_protocol/
        ├── 02_search/
        └── ...
```

## Benefits

1. **Clean Git History**: Only framework changes tracked, not project data
2. **Multiple Projects**: Easy to work on multiple meta-analyses simultaneously
3. **Clear Separation**: Framework code vs project data
4. **Better Organization**: Each project self-contained in its own directory
5. **Safer Operations**: Less risk of accidentally deleting/modifying wrong files

## Migration Commands Used

```bash
# 1. Create projects/legacy/
mkdir -p projects/legacy

# 2. Move historical data
command mv 01_protocol 02_search 03_screening 04_fulltext 05_extraction \
           06_analysis 07_manuscript 08_reviews 09_qa \
           TOPIC.txt feasibility_abstracts.json \
           projects/legacy/

# 3. Update .gitignore
# (Added projects/* ignore rules)

# 4. Update documentation
# (Used sed for batch path updates in AGENTS.md)
# (Manual edits for README.md and GETTING_STARTED.md)

# 5. Update init_project.py
# (Added --name parameter, auto-creates in projects/)

# 6. Test
uv run ma-end-to-end/scripts/init_project.py --name test-project
rip projects/test-project/
```

## Next Steps for Users

### Starting a New Project

```bash
# 1. Initialize project
cd /Users/htlin/meta-pipe
uv run tooling/python/init_project.py --name my-meta-analysis

# 2. Edit research question
nano projects/my-meta-analysis/TOPIC.txt

# 3. Launch Claude Code
# Say: "Start project my-meta-analysis"
```

### Working with Existing Legacy Data

The legacy project data is still accessible at `projects/legacy/`:

```bash
# View legacy data
ls projects/legacy/

# If you want to continue working on it:
# 1. Copy to new project structure
cp -r projects/legacy projects/my-continued-work

# 2. Work with it normally
# Say: "Continue project my-continued-work"
```

## Rollback Plan (If Needed)

If migration needs to be reversed:

```bash
# 1. Move files back to root
command mv projects/legacy/* .

# 2. Remove projects/legacy/
rip projects/legacy/

# 3. Restore backup files
command mv AGENTS.md.bak AGENTS.md
command mv GETTING_STARTED.md.bak GETTING_STARTED.md

# 4. Revert .gitignore changes
git checkout .gitignore

# 5. Revert init_project.py
git checkout ma-end-to-end/scripts/init_project.py
```

## Backup Files Created

- `AGENTS.md.bak` (sed created automatically)
- `GETTING_STARTED.md.bak` (sed created automatically)

These can be removed if migration is confirmed successful:

```bash
rip AGENTS.md.bak GETTING_STARTED.md.bak
```

## Verification Checklist

- [x] All stage folders moved to projects/legacy/
- [x] Root directory only contains framework code
- [x] .gitignore updated and tested
- [x] AGENTS.md paths updated and verified
- [x] README.md paths updated and verified
- [x] GETTING_STARTED.md paths updated and verified
- [x] init_project.py updated and tested
- [x] Test project creation successful
- [x] Legacy README.md created with instructions
- [x] projects/.gitkeep added

## Success Criteria

✅ All criteria met:

1. ✅ Root directory clean (only framework code)
2. ✅ Projects isolated in projects/ directory
3. ✅ Git ignores project data (except examples)
4. ✅ Documentation consistent with new structure
5. ✅ init_project.py creates projects correctly
6. ✅ Legacy data preserved and documented
7. ✅ Test project creation works

## Notes

- Migration is **non-destructive** - all data preserved
- Legacy project can still be accessed/continued
- Backup files created automatically by sed
- Changes are **backward compatible** via `--root` parameter

---

**Migration completed successfully on 2026-02-08 22:28 GMT+8**
