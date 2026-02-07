# Skill Generalization Workflow

**Reference**: This file is referenced from CLAUDE.md
**Purpose**: Extract reusable patterns from completed projects

---

## When Project Reaches 95%+ Completion

**Trigger**: User says "what have we learned" or "generalize this workflow"

**Why**: Capture valuable workflows before context is lost

---

## 6-Step Generalization Process

### 1. Analyze Uncommitted Progress

```bash
git status
```

Identify:

- New scripts created
- New workflows established
- Documentation written
- Time-saving techniques discovered

### 2. Identify Reusable Patterns

Ask:

- ✅ Was this workflow used multiple times in the project?
- ✅ Would future projects benefit from this?
- ✅ Can this be generalized beyond this specific topic?
- ✅ Does this save significant time (>1 hour)?

Red flags (don't generalize):

- ❌ One-off solutions for specific edge cases
- ❌ Highly project-specific code
- ❌ Temporary workarounds

### 3. Extract into Claude Code Skills

Create skill file structure:

```
~/.claude/skills/
├── skill-name/
│   ├── SKILL.md           # Main skill content
│   ├── scripts/           # Supporting scripts (optional)
│   │   └── helper.py
│   └── references/        # Templates, examples (optional)
│       └── template.md
```

Skill frontmatter format:

```yaml
---
name: skill-name
description: Brief description (1-2 sentences)
context: fork # or preserve
agent: general-purpose # or specific agent
---
```

### 4. Document in SKILLS*LEARNED_FROM*\*.md

Create retrospective document:

```markdown
# Skills Learned from [Project Name]

## Project Context

- What: Brief project description
- Completion: X% complete, Y hours total
- Key metrics: N studies, M patients, etc.

## Skills Created

### 1. [Skill Name]

- **Purpose**: What problem does it solve?
- **Time savings**: Quantified (X hours → Y hours, Z% improvement)
- **Use cases**: When to use this skill
- **Validated on**: Actual project results

## Impact Assessment

- Quantitative: Time savings, error reduction
- Qualitative: Workflow improvements, reproducibility
```

### 5. Commit to ~/.claude/skills Repository

```bash
cd ~/.claude/skills
git add skill-name/
git add SKILLS_LEARNED_FROM_*.md
git commit -m "Add [skill-name] from [project] completion

- Created: [Skill description]
- Time savings: [X%]
- Validated on: [Project metrics]

Co-Authored-By: Claude <noreply@anthropic.com>"
git push
```

### 6. Create Summary Report for User

Write user-facing report:

- What was generalized
- How to use the new skills
- Expected ROI (time savings on next project)
- Future enhancement opportunities

---

## Example: This Project

### What We Generalized

**From**: TNBC meta-analysis (99% complete, 5 RCTs, N=2402)

**Created**:

1. **meta-manuscript-assembly** skill (1,471 lines)
   - 5-phase workflow (Tables → Figures → References → Legends → QA)
   - Time savings: 50% (16h → 8h)

2. **scientific-figure-assembly** skill
   - Python script for multi-panel figures
   - 300 DPI publication quality
   - Time savings: 1-2 hours vs PowerPoint

**Impact**:

- Time investment to generalize: 2 hours
- ROI: First use saves 8-12 hours
- Payback: Immediate (first project)

---

## Quality Checklist

Before finalizing skill:

- [ ] Skill has clear trigger keywords
- [ ] Workflow is step-by-step (not conceptual)
- [ ] Includes working code/script examples
- [ ] Time savings quantified (not "faster")
- [ ] Validated on actual project (not theoretical)
- [ ] Documentation complete (README, examples)
- [ ] Git commit message detailed
- [ ] User report created

---

## When NOT to Generalize

Don't create a skill if:

- ❌ Used only once in the project
- ❌ Highly specific to this topic (e.g., TNBC-only code)
- ❌ Temporary workaround for a bug
- ❌ Time savings < 30 minutes
- ❌ Too complex to maintain (>2,000 lines without clear structure)

Instead:

- ✅ Document in project README
- ✅ Add to project LESSONS_LEARNED.md
- ✅ Keep as reference for similar future projects
