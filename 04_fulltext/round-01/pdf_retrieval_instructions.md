# PDF Retrieval Instructions

**Date:** 2026-02-06
**Total Records:** 52
**Records with DOI:** 51 (98.1%)
**Records with PMID:** 12 (23.1%)

---

## Retrieval Strategy Overview

We will use a **tiered approach** to maximize PDF retrieval while minimizing costs:

```
Tier 1: Unpaywall API (free Open Access) → ~40-60% success
Tier 2: PubMed Central (free PMC) → +10-20% success
Tier 3: Institutional Access → +20-30% success
Tier 4: Author Contact → +5-10% success
-----------------------------------------------------
Total Expected Success: 75-100% (39-52 PDFs)
```

---

## Tier 1: Unpaywall API (Automated)

### What is Unpaywall?

- Free, legal API to find Open Access versions of articles
- Does NOT violate copyright (only returns legal OA links)
- Success rate: 40-60% for biomedical literature

### Script Available

Check if script exists:

```bash
ls /Users/htlin/meta-pipe/ma-fulltext-management/scripts/unpaywall_fetch.py
```

If available, run:

```bash
cd /Users/htlin/meta-pipe/tooling/python

# Install dependencies if needed
uv add requests

# Run Unpaywall fetch
uv run ../../ma-fulltext-management/scripts/unpaywall_fetch.py \
  --in-csv ../../04_fulltext/round-01/pdf_retrieval_manifest.csv \
  --out-csv ../../04_fulltext/round-01/unpaywall_results.csv \
  --pdf-dir ../../04_fulltext/round-01/pdfs \
  --email "your.email@example.com"
```

**Expected output:**

- PDFs saved to: `04_fulltext/round-01/pdfs/`
- Results logged to: `04_fulltext/round-01/unpaywall_results.csv`

### If Script Not Available

Use this manual approach for key trials:

```python
import requests

def get_unpaywall_pdf(doi, email):
    """Fetch Open Access PDF URL from Unpaywall API."""
    url = f"https://api.unpaywall.org/v2/{doi}?email={email}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data.get("is_oa"):
            pdf_url = data.get("best_oa_location", {}).get("url_for_pdf")
            return pdf_url
    return None

# Example usage
doi = "10.1200/JCO.24.02086"  # postMONARCH
pdf_url = get_unpaywall_pdf(doi, "your.email@example.com")
if pdf_url:
    print(f"PDF available at: {pdf_url}")
```

---

## Tier 2: PubMed Central (PMC)

### For records with PMID:

1. Check if available in PMC:

   ```
   https://www.ncbi.nlm.nih.gov/pmc/?term=PMID
   ```

2. If "Free PMC article" badge shown:
   - Click "PDF" link in top right
   - Download directly

3. **Bulk check** (for all 12 PMIDs):
   - Create list of PMIDs
   - Use NCBI E-utilities to check PMC availability

### PMC Check Script (if needed):

```bash
# Check single PMID
curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pubmed&id=39265124&linkname=pubmed_pmc&retmode=json"

# If PMC ID returned, article is in PMC (free full-text)
```

---

## Tier 3: Institutional Access

### If You Have University/Hospital Affiliation:

#### Option A: Library Proxy

1. Go to your institution's library website
2. Search for article by DOI or title
3. Access via library proxy (usually auto-login)

#### Option B: VPN

1. Connect to institutional VPN
2. Go to journal website directly
3. Should have automatic access

### Direct Journal Access

**Key Journals for This Review:**

- **Journal of Clinical Oncology (JCO)** - postMONARCH, MAINTAIN
  - https://ascopubs.org/
- **Annals of Oncology** - EMERALD, SOLAR-1
  - https://www.annalsofoncology.org/
- **New England Journal of Medicine (NEJM)** - EMBER-3
  - https://www.nejm.org/

### Download Instructions:

1. Go to journal website
2. Search by DOI (most reliable)
3. Click "Download PDF" or "PDF" button
4. Save to: `/Users/htlin/meta-pipe/04_fulltext/round-01/pdfs/`
5. **Naming convention:** `[RecordID].pdf` (e.g., `KalinskyK202547.pdf`)

---

## Tier 4: Author Contact

### When to Use:

- Critical trials still paywalled after Tier 1-3
- e.g., postMONARCH, MAINTAIN, PALMIRA if not retrieved

### Email Template:

**Subject:** Request for full-text: [Article Title]

**Body:**

```
Dear Dr. [Last Name],

I am conducting a systematic review and network meta-analysis on treatment
strategies following progression on CDK4/6 inhibitors in HR+/HER2- metastatic
breast cancer.

Your article "[Title]" published in [Journal] ([Year]) appears highly relevant
to our review. Unfortunately, I do not have institutional access to this journal.

Would you be willing to share a PDF copy of your article? I would be very grateful
for your assistance with our research.

Thank you for your time and consideration.

Best regards,
[Your Name]
[Your Affiliation]
[Your Email]
```

### How to Find Author Emails:

1. Check article first page (corresponding author)
2. PubMed author affiliations
3. Google Scholar profile
4. Institution website
5. ResearchGate / ORCID profile

### Expected Response Time:

- 50% respond within 1 week
- 30% respond within 2-4 weeks
- 20% never respond

---

## Priority List: 10 Key Trials (MUST RETRIEVE)

These trials are critical - use all methods if needed:

| Trial                | Record ID               | DOI                          | Journal    | Priority |
| -------------------- | ----------------------- | ---------------------------- | ---------- | -------- |
| postMONARCH          | KalinskyK202547         | 10.1200/JCO.24.02086         | JCO 2024   | ⭐⭐⭐   |
| MAINTAIN             | KalinskyK2023153        | [Check CSV]                  | [Check]    | ⭐⭐⭐   |
| PALMIRA              | LlombartCussacA202537   | [Check CSV]                  | [Check]    | ⭐⭐⭐   |
| TROPiCS-02           | RugoHS202490            | [Check CSV]                  | [Check]    | ⭐⭐⭐   |
| TROPION-Breast01     | Rugo2024TROPION         | 10.1200/JCO.24.00920         | JCO 2024   | ⭐⭐⭐   |
| EMBER-3              | JhaveriKL202541391667   | [Check CSV]                  | Ann Oncol  | ⭐⭐⭐   |
| EMERALD              | Bidard2022EMERALD       | 10.1200/JCO.22.00338         | JCO 2022   | ⭐⭐⭐   |
| CAPItello-291        | TokunagaE202539379782   | [Check CSV]                  | [Check]    | ⭐⭐⭐   |
| SOLAR-1              | Andre2021SOLAR1         | 10.1016/j.annonc.2020.11.011 | Ann Oncol  | ⭐⭐⭐   |
| BOLERO-2 post-CDK4/6 | Fernandez2021Everolimus | 10.1002/onco.13595           | Oncologist | ⭐⭐⭐   |

**Action:** Retrieve these 10 first before others.

---

## Tracking Retrieval Progress

### Update `pdf_retrieval_manifest.csv` with:

| Column           | Values                                                      | Description                         |
| ---------------- | ----------------------------------------------------------- | ----------------------------------- |
| retrieval_method | `unpaywall` / `pmc` / `institutional` / `author` / `manual` | How PDF was obtained                |
| pdf_path         | `04_fulltext/round-01/pdfs/[RecordID].pdf`                  | File path                           |
| retrieval_status | `success` / `pending` / `paywall` / `not_found`             | Status                              |
| notes            | Free text                                                   | Any issues or special circumstances |

### Example:

| record_id       | retrieval_method | pdf_path                            | retrieval_status | notes                       |
| --------------- | ---------------- | ----------------------------------- | ---------------- | --------------------------- |
| KalinskyK202547 | unpaywall        | 04_fulltext/.../KalinskyK202547.pdf | success          | Open Access via JCO         |
| Finn2016        | institutional    | 04_fulltext/.../Finn2016.pdf        | success          | Downloaded via library      |
| SmithUnknown    | author           | -                                   | pending          | Emailed author 2026-02-06   |
| JonesPaywall    | -                | -                                   | paywall          | Not available, low priority |

---

## File Naming & Organization

### PDF Naming Convention:

```
[RecordID].pdf
```

**Examples:**

- `KalinskyK202547.pdf` (postMONARCH)
- `Rugo2024TROPION.pdf` (TROPION-Breast01)
- `Bidard2022EMERALD.pdf` (EMERALD main paper)

### Directory Structure:

```
04_fulltext/round-01/
├── pdfs/
│   ├── KalinskyK202547.pdf
│   ├── Rugo2024TROPION.pdf
│   └── ... (50+ PDFs)
├── fulltext_decisions.csv
├── pdf_retrieval_manifest.csv
├── unpaywall_results.csv (if using Unpaywall)
└── fulltext_review_guide.md
```

---

## Quality Checks

### After Retrieval, Verify:

1. **PDF readable:**
   - Open each PDF
   - Check it's not corrupted
   - Verify it's the correct article (match title/authors)

2. **Not a scanned image:**
   - Text should be selectable
   - If scanned, may need OCR (use Adobe Acrobat or online tool)

3. **Complete article:**
   - Has Methods, Results, Discussion sections
   - Check for supplementary materials link (may need separate download)

4. **Correct version:**
   - Prefer final published version over preprint
   - Note if preprint only available

---

## Troubleshooting

### Issue: DOI Not Recognized by Unpaywall

**Solution:**

- Try CrossRef API: `https://api.crossref.org/works/[DOI]`
- Check if DOI is correct in CSV
- Try journal website directly

### Issue: PDF Behind Paywall, No Institutional Access

**Options:**

1. Contact authors (Tier 4)
2. Check if preprint available (bioRxiv, medRxiv)
3. Use Google Scholar "All versions" link (may have repository copy)
4. Last resort: Exclude if not critical trial

### Issue: Supplementary Materials Needed

**Where to Find:**

- Journal website (often under "Supplements" tab)
- Sometimes hosted on publisher's data repository
- Contact authors if critical data in supplements

---

## Expected Timeline

| Day  | Task                             | PDFs Retrieved (Cumulative) |
| ---- | -------------------------------- | --------------------------- |
| 1    | Tier 1: Unpaywall API            | 20-30 PDFs (~40-60%)        |
| 2    | Tier 2: PMC check                | 25-35 PDFs                  |
| 3-5  | Tier 3: Institutional access     | 35-45 PDFs                  |
| 7-14 | Tier 4: Author contact responses | 40-50 PDFs                  |

**Target:** ≥45 PDFs retrieved (≥87%)

---

## Next Steps After Retrieval

Once PDFs retrieved:

1. ✅ Update `pdf_retrieval_manifest.csv` with retrieval status
2. ✅ Verify all 10 key trials retrieved
3. ✅ Begin full-text review using `fulltext_review_guide.md`
4. ✅ Update `fulltext_decisions.csv` with review decisions
5. ✅ Proceed to Stage 05 (Data Extraction) for included studies

---

## Commands Summary

```bash
# Check if Unpaywall script exists
ls /Users/htlin/meta-pipe/ma-fulltext-management/scripts/unpaywall_fetch.py

# If yes, run Unpaywall
cd /Users/htlin/meta-pipe/tooling/python
uv run ../../ma-fulltext-management/scripts/unpaywall_fetch.py \
  --in-csv ../../04_fulltext/round-01/pdf_retrieval_manifest.csv \
  --out-csv ../../04_fulltext/round-01/unpaywall_results.csv \
  --pdf-dir ../../04_fulltext/round-01/pdfs \
  --email "your.email@example.com"

# Check retrieval progress
wc -l /Users/htlin/meta-pipe/04_fulltext/round-01/pdfs/*.pdf
ls -lh /Users/htlin/meta-pipe/04_fulltext/round-01/pdfs/

# Count successful retrievals
grep "success" /Users/htlin/meta-pipe/04_fulltext/round-01/pdf_retrieval_manifest.csv | wc -l
```

---

**Document Version:** 1.0
**Date:** 2026-02-06
**Status:** Ready for PDF retrieval
