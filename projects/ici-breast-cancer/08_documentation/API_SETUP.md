# API Setup Guide

## Quick Start (Minimum)

```bash
cp .env.example .env
```

Only **PubMed** is required. Others are optional.

```env
PUBMED_API_KEY=your_key   # https://www.ncbi.nlm.nih.gov/account/
```

---

## All Databases

| Database            | URL                                   | Notes                            |
| ------------------- | ------------------------------------- | -------------------------------- |
| **PubMed**          | https://www.ncbi.nlm.nih.gov/account/ | Free, 10 req/sec with key        |
| **Scopus + Embase** | https://dev.elsevier.com/             | Same key for both                |
| **Cochrane**        | N/A                                   | No public API, use manual export |
| **Zotero**          | https://www.zotero.org/settings/keys  | Free                             |
| **Unpaywall**       | N/A                                   | Just needs email                 |

---

## Details by Database

<details>
<summary><strong>PubMed (NCBI)</strong></summary>

1. Go to https://www.ncbi.nlm.nih.gov/account/
2. Settings → API Key Management → Create
3. Copy to `.env`:

```env
PUBMED_API_KEY=your_36_char_key
```

</details>

<details>
<summary><strong>Scopus & Embase (Elsevier)</strong></summary>

> Both use the same Elsevier API key.

1. Register at https://dev.elsevier.com/
2. Create API Key
3. Copy to `.env`:

```env
SCOPUS_API_KEY=your_elsevier_key
EMBASE_API_KEY=your_elsevier_key
```

**Off-campus?** Contact library for `INST_TOKEN`.

</details>

<details>
<summary><strong>Zotero</strong></summary>

1. Go to https://www.zotero.org/settings/keys
2. Create new private key (enable read/write)
3. Note your User ID on the same page
4. Get Collection Key from URL: `zotero.org/user/collections/XXXXXXXX`

```env
ZOTERO_API_KEY=your_24_char_key
ZOTERO_LIBRARY_TYPE=user
ZOTERO_LIBRARY_ID=1234567
ZOTERO_COLLECTION_KEY=ABCD1234
```

**Test:**

```bash
curl -H "Zotero-API-Key: YOUR_KEY" \
  "https://api.zotero.org/users/YOUR_ID/items?limit=1"
```

</details>

<details>
<summary><strong>Cochrane</strong></summary>

No public API. Use manual export (RIS/BibTeX) from Cochrane Library website.

</details>

<details>
<summary><strong>Unpaywall & LLM</strong></summary>

```env
UNPAYWALL_EMAIL=your_email@example.com

# Optional: LLM for assisted extraction
LLM_API_BASE=https://api.openai.com/v1
LLM_API_KEY=sk-your-key
LLM_MODEL=gpt-4o
```

</details>

---

## Troubleshooting

| Issue         | Fix                             |
| ------------- | ------------------------------- |
| 403 Forbidden | Check subscription / INST_TOKEN |
| Rate limit    | Use API key, add delays         |
| Empty results | Verify institutional access     |
