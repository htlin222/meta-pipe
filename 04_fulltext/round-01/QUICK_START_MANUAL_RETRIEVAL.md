# Quick Start: Manual PDF Retrieval

**Date**: 2026-02-06
**Goal**: Retrieve 42 remaining PDFs (target: 35-40 success)

---

## 📋 Pre-Flight Checklist

- [ ] Institutional library access confirmed
- [ ] VPN connected (if remote)
- [ ] Browser ready (Chrome/Firefox recommended)
- [ ] File manager open to: `/Users/htlin/meta-pipe/04_fulltext/round-01/pdfs/`
- [ ] CSV editor open: `pdf_retrieval_manifest_updated.csv`

---

## 🎯 Today's Target: 9 Key Trials (Priority 1)

### Quick Access Links

Open these in browser tabs (replace with your institutional proxy if needed):

1. **TROPION-Breast01** - https://doi.org/10.1200/JCO.24.00920
   - Save as: `Rugo2024TROPION.pdf`

2. **EMERALD** - https://doi.org/10.1200/JCO.22.00338
   - Save as: `Bidard2022EMERALD.pdf`

3. **postMONARCH** - https://doi.org/10.1200/JCO-24-02086
   - Save as: `KalinskyK202547.pdf`

4. **MAINTAIN** - https://doi.org/10.1200/JCO-24-01865
   - Save as: `LlombartCussacA202537.pdf`

5. **PALMIRA** - https://doi.org/10.1200/JCO.22.02392
   - Save as: `KalinskyK2023153.pdf`

6. **TROPiCS-02** - https://doi.org/10.1016/S1470-2045(23)00071-X
   - Save as: `RugoHS2023146.pdf`

7. **SOLAR-1** - https://doi.org/10.1016/j.annonc.2020.11.011
   - Save as: `Andre2021SOLAR1.pdf`

8. **BOLERO-2 post-CDK** - https://doi.org/10.1002/onco.13595
   - Save as: `Fernandez2021Everolimus.pdf`

9. **EMBER-3** - https://doi.org/10.1016/j.annonc.2025.11.018
   - Save as: `JhaveriKL202541391667.pdf`

---

## ⚡ Fast Workflow (Repeat for Each)

1. **Click DOI link** → Should redirect to journal via institutional proxy
2. **Find "Download PDF" button** → Usually top-right or after abstract
3. **Save to pdfs/ folder** → Use exact filename from list above
4. **Verify PDF opens** → Quick check it's not corrupted
5. **Update CSV** → Change `retrieval_status` to "downloaded"

**Time per PDF**: ~3-5 minutes
**Total time for 9**: ~30-45 minutes

---

## 🆘 Troubleshooting

### "Access Denied" or "Subscribe to Continue"
- ❌ **Not signed in to institutional proxy**
  - Fix: Go to library portal, search for journal, click link
- ❌ **VPN not connected**
  - Fix: Connect to institutional VPN first
- ❌ **Institution doesn't have access**
  - Fix: Try PMC alternative (see below)

### "404 Not Found"
- ❌ **DOI incorrect or article not published yet**
  - Fix: Google search: `[first author] [year] [key words]`

### "PDF Download Not Available"
- ❌ **HTML-only article**
  - Fix: Use browser print → Save as PDF
  - Note in CSV: `retrieval_method = "HTML converted"`

---

## 🔄 PMC Fallback (If Institutional Fails)

For articles with PMID, try PubMed Central:

| Record | PMID | PMC URL |
|--------|------|---------|
| TROPION | 39265124 | https://www.ncbi.nlm.nih.gov/pmc/articles/PMID39265124/pdf/ |
| EMERALD | 35584336 | https://www.ncbi.nlm.nih.gov/pmc/articles/PMID35584336/pdf/ |
| SOLAR-1 | 33246021 | https://www.ncbi.nlm.nih.gov/pmc/articles/PMID33246021/pdf/ |
| BOLERO-2 | 33373062 | https://www.ncbi.nlm.nih.gov/pmc/articles/PMID33373062/pdf/ |
| EMBER-3 | 41391667 | https://www.ncbi.nlm.nih.gov/pmc/articles/PMID41391667/pdf/ |

---

## 📝 Progress Tracking

As you download, check off:

- [ ] 1/9: TROPION-Breast01
- [ ] 2/9: EMERALD
- [ ] 3/9: postMONARCH
- [ ] 4/9: MAINTAIN
- [ ] 5/9: PALMIRA
- [ ] 6/9: TROPiCS-02
- [ ] 7/9: SOLAR-1
- [ ] 8/9: BOLERO-2 post-CDK
- [ ] 9/9: EMBER-3

**When complete**: 10/10 key trials retrieved (including CAPItello already downloaded)

---

## 📊 CSV Update Template

After each download, update `pdf_retrieval_manifest_updated.csv`:

| Field | Value |
|-------|-------|
| `retrieval_status` | `downloaded` |
| `retrieval_method` | `Institutional access` (or `PMC` if fallback) |
| `pdf_path` | `pdfs/[RecordID].pdf` |
| `notes` | Clear any error notes |

**Tip**: Use Excel/LibreOffice for easy editing, save as CSV

---

## ✅ When Done Today

You should have:
- ✅ 9 new PDFs in `pdfs/` folder (total 19/52)
- ✅ All 10 key trials retrieved (100%)
- ✅ CSV updated with retrieval status
- ✅ Ready to continue with Priority 2-3 tomorrow

**Estimated progress**: 37% of total (19/52)

---

## 🚀 Tomorrow's Plan

Once Priority 1 is complete, proceed to:
- **Priority 2** (2 PDFs): Key trial subgroup analyses
- **Priority 3** (10 PDFs): Supporting RCTs

See `PRIORITY_RETRIEVAL_LIST.md` for full details.

**Target end of Week 4**: 35-40 PDFs total (67-77%)

---

## 💡 Pro Tips

1. **Keep DOI links in separate browser tabs** - easier to go back if download fails
2. **Download all first, rename later** - faster workflow
3. **Use download manager** - some browsers have better resume capability
4. **Try different browsers** - Sometimes Firefox works where Chrome doesn't
5. **Check file size** - PDFs should be >200 KB (if <100 KB, likely error page)

---

**Questions? Issues?** Refer to:
- `PDF_RETRIEVAL_REPORT.md` - Detailed analysis
- `PRIORITY_RETRIEVAL_LIST.md` - Full manual retrieval guide
- `fulltext_review_guide.md` - What to do after retrieval

**🎯 Let's get these 9 key trials! Start now.**
