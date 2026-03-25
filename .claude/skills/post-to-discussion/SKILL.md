---
name: post-to-discussion
description: Share your completed meta-analysis project to the htlin222/meta-pipe GitHub Discussions board. Use when a project reaches a milestone (analysis complete, manuscript drafted) and the user wants to showcase their work.
---

# Post to Discussion

## Overview

Share your meta-analysis project as a GitHub Discussion on [htlin222/meta-pipe](https://github.com/htlin222/meta-pipe/discussions). This lets other users see real examples of completed analyses, learn from different clinical questions, and reuse methodological approaches.

## When to Use

- User says "share", "post", "publish to discussion", or "show and tell"
- A project has completed at least through Stage 06 (analysis)
- User wants to showcase their work to the meta-pipe community

## Prerequisites

1. **GitHub CLI (`gh`)** must be authenticated: `gh auth status`
2. **Project figures committed and pushed** — PNGs are gitignored by default, so use `git add -f` for figures
3. **Project must be on a pushed branch** so image URLs resolve via `raw.githubusercontent.com`

## Workflow

### Step 1: Ensure figures are committed and pushed

```bash
# Force-add PNGs (they're gitignored globally)
git add -f projects/<project-name>/06_analysis/figures/*.png
git add -f projects/<project-name>/06_analysis/tables/*.png
git add -f projects/<project-name>/07_manuscript/figures/*.png

# Commit and push
git commit -m "Add <project-name> figures for discussion post"
git push origin <branch>
```

### Step 2: Get the image base URL

```bash
COMMIT_SHA=$(git rev-parse HEAD)
IMG_BASE="https://raw.githubusercontent.com/htlin222/meta-pipe/${COMMIT_SHA}/projects/<project-name>"
```

### Step 3: Get the Discussion category ID

The repo has these categories:

| Category | ID | Use for |
|----------|-----|---------|
| Show and tell | `DIC_kwDORJgSmM4C4-A3` | Completed projects (default) |
| Ideas | `DIC_kwDORJgSmM4C4-A2` | Project proposals |
| General | `DIC_kwDORJgSmM4C4-A0` | Questions, updates |
| Q&A | `DIC_kwDORJgSmM4C4-A1` | Help requests |

Repository ID: `R_kgDORJgSmA`

### Step 4: Create the discussion via GraphQL

```bash
gh api graphql -f query='
mutation {
  createDiscussion(input: {
    repositoryId: "R_kgDORJgSmA",
    categoryId: "DIC_kwDORJgSmM4C4-A3",
    title: "<Your project title>",
    body: "<Markdown body with images>"
  }) {
    discussion {
      id
      number
      url
    }
  }
}'
```

### Step 5: Update the body (if needed)

```bash
gh api graphql -f query='
mutation {
  updateDiscussion(input: {
    discussionId: "<discussion_id>",
    body: "<updated body>"
  }) {
    discussion { url }
  }
}'
```

## Body Template

Use this Markdown template for the discussion body. Adapt sections based on your project type (pairwise MA, NMA, pooled proportion).

```markdown
## 🔬 <Project Title>

**<One-line summary of the research question and key finding.>**

> Project path: `projects/<project-name>/`

---

### Background

<2-3 sentences: clinical context, why this question matters, gap in literature.>

### Included Studies

| Study | Intervention | N | Primary Outcome |
|-------|-------------|---|-----------------|
| ... | ... | ... | ... |

---

### Figure 1: <Title>

![Figure 1](<IMG_BASE>/07_manuscript/figures/Figure1_xxx.png)

<1-2 sentence caption.>

---

### Figure 2: <Title>

![Figure 2](<IMG_BASE>/07_manuscript/figures/Figure2_xxx.png)

<1-2 sentence caption.>

---

### Key Findings

1. **Finding 1** — ...
2. **Finding 2** — ...
3. **Finding 3** — ...

### Clinical Implications

<Brief actionable summary for clinicians.>

### Methodology

- **Analysis**: <Bayesian NMA / Pairwise MA / Pooled proportion>
- **Software**: R (gemtc/netmeta/meta/metafor)
- **Heterogeneity**: I² = X%
- **Quality**: <SUCRA / GRADE / RoB summary>

### Pipeline

<Which stages were completed, total files, key artifacts.>

---

*Generated with [meta-pipe](https://github.com/htlin222/meta-pipe) — AI-assisted meta-analysis pipeline*
```

## Tips

- **Image sizing**: GitHub renders full-width by default. Use `<img src="..." width="600">` for smaller figures.
- **Large bodies**: Use a shell variable with heredoc and pipe through `jq -Rs .` for proper JSON escaping.
- **Multiple figures**: Include 3-5 key figures max. Link to the repo for supplementary materials.
- **Tags**: GitHub Discussions don't support tags, but you can add hashtags in the body (e.g., `#NMA #DLBCL #oncology`).

## Example

See [Discussion #30: Frontline DLBCL NMA](https://github.com/htlin222/meta-pipe/discussions/30) for a complete example with 5 figures, results tables, and clinical recommendations.

## Pipeline Navigation

| Step | Skill | Stage |
|------|-------|-------|
| Prev | `/ma-peer-review` | 08-09 QA & Review |
| This | `/post-to-discussion` | Share your work |
| All | `/ma-end-to-end` | Full pipeline |
