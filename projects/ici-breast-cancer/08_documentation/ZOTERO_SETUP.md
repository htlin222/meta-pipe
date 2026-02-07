# Zotero Reference Management Setup

## TNBC Neoadjuvant Immunotherapy Meta-Analysis

**Purpose**: Set up Zotero for reference management throughout the systematic review
**Time**: 45 minutes
**Date**: 2026-02-07

---

## Why Zotero for Meta-Analysis?

✅ **Free and open-source**
✅ **Excellent BibTeX support** (critical for our pipeline)
✅ **PDF management** with full-text search
✅ **Browser integration** for easy paper capture
✅ **Sync across devices** (optional, 300MB free storage)
✅ **Citation while you write** (Word/LibreOffice plugin)
✅ **Group libraries** for collaboration

---

## Step 1: Install Zotero

### Desktop Application

1. Go to https://www.zotero.org/download/
2. Download Zotero 6 (or latest version) for your OS
3. Install following prompts
4. Open Zotero

### Browser Connector (Highly Recommended)

1. Same download page: https://www.zotero.org/download/
2. Click "Zotero Connector" for your browser (Chrome, Firefox, Safari, Edge)
3. Add extension
4. Pin extension to toolbar (click puzzle icon → pin Zotero)

### Word Processor Plugin (Optional, for manuscript stage)

1. With Zotero open, go to Edit → Preferences → Cite → Word Processors
2. Click "Install Microsoft Word Plugin" (or LibreOffice if preferred)
3. Restart Word

---

## Step 2: Create Zotero Account (for Sync)

1. Go to https://www.zotero.org/user/register/
2. Create account (free)
3. In Zotero desktop: Edit → Preferences → Sync
4. Log in with your credentials
5. Settings:
   - **Sync automatically**: Yes
   - **Sync full-text content**: Yes (if <300MB, else No)
   - **Sync attachments**: Only in "My Library" (not group libraries, to save space)

**Storage**: 300MB free, $20/year for 2GB (usually sufficient for 1-2 meta-analyses)

---

## Step 3: Configure Zotero for Systematic Reviews

### General Settings

Edit → Preferences → General:

- **Automatically take snapshots**: No (we only need PDFs)
- **Automatically tag items with keywords**: Yes
- **Automatically rename attachment files**: Yes (using parent metadata)

### File Management

Edit → Preferences → Advanced → Files and Folders:

- **Base directory**: Leave empty (use Zotero default)
- **Data directory location**: Default (or custom if you have external drive)
- **Linked attachment base directory**: Not needed for this project

### Better BibTeX Plugin (CRITICAL for pipeline)

This plugin dramatically improves BibTeX export quality.

1. Go to https://github.com/retorquere/zotero-better-bibtex/releases/latest
2. Download `zotero-better-bibtex-*.xpi` file (not source code)
3. In Zotero: Tools → Add-ons → Gear icon → Install Add-on From File
4. Select downloaded `.xpi` file
5. Restart Zotero

#### Configure Better BibTeX:

Edit → Preferences → Better BibTeX:

**Citation keys:**

- **Citation key format**: `[auth:lower][year]`
  - Example: `schmid2020`, `mittendorf2020`
- **Force citation key to ASCII**: Yes
- **On conflict**: Keep existing key

**Export:**

- **Fields to omit from export**: `abstract, file`
- **Add URLs to BibTeX export**: No
- **Export unicode as plain text**: No

**Automatic export:**

- We'll set this up per collection later

---

## Step 4: Create Collection Structure

Collections = folders in Zotero

### Create Main Collection

1. Click folder+ icon (New Collection)
2. Name: `TNBC Neoadjuvant ICI Meta-Analysis`
3. Create

### Create Sub-Collections

Right-click main collection → New Subcollection:

1. **00_Search_Results** (raw search results, before screening)
2. **01_Screening_Include** (passed title/abstract screening)
3. **02_Screening_Exclude** (excluded at title/abstract)
4. **03_Fulltext_Include** (final included studies)
5. **04_Fulltext_Exclude** (excluded at full-text stage)
6. **05_Background_References** (not included in review, but relevant for introduction/discussion)
7. **06_Methodology_References** (PRISMA guidelines, statistical methods, etc.)

**Your structure:**

```
└── TNBC Neoadjuvant ICI Meta-Analysis/
    ├── 00_Search_Results/
    ├── 01_Screening_Include/
    ├── 02_Screening_Exclude/
    ├── 03_Fulltext_Include/
    ├── 04_Fulltext_Exclude/
    ├── 05_Background_References/
    └── 06_Methodology_References/
```

---

## Step 5: Import Pilot Studies (Known Key Trials)

Let's add the 5 known key trials to `03_Fulltext_Include` as a starting point.

### Method 1: Import from DOI (Fastest)

1. Select `03_Fulltext_Include` collection
2. Click magic wand icon (Add Item by Identifier)
3. Enter DOI (one per line):

```
10.1056/NEJMoa1910549
10.1016/S1470-2045(20)30689-7
10.1038/s41591-019-0689-1
10.1200/JCO.2019.37.15_suppl.506
10.1038/s41591-024-03320-y
```

4. Click "Add"
5. Wait for metadata retrieval

**Expected imports:**

- KEYNOTE-522 (Schmid et al., NEJM 2020)
- IMpassion031 (Mittendorf et al., Lancet Oncol 2020)
- GeparNuevo (Loibl et al., Nat Med 2019)
- NeoTRIPaPDL1 (Gianni et al., JCO 2019)
- CamRelief (Huang et al., Nat Med 2024)

### Method 2: Browser Connector (for papers you're reading)

1. Open paper webpage (PubMed, journal site, etc.)
2. Click Zotero Connector in browser toolbar
3. Select collection: `03_Fulltext_Include`
4. Click "Save to Zotero"

### Method 3: Import from BibTeX (after search phase)

We'll use this after search is complete.

---

## Step 6: Add PDFs to References

### Automatic PDF Retrieval (if you have institutional access)

1. Select reference(s) in Zotero
2. Right-click → Find Available PDF
3. Zotero will search:
   - Publisher websites (via your IP/proxy)
   - Unpaywall (Open Access)
   - PubMed Central

### Manual PDF Upload

1. Locate PDF file
2. Drag and drop onto reference in Zotero
3. Zotero will attach PDF and rename it

### Verify PDF Attachment

- Look for paperclip icon next to reference
- Click to open PDF
- PDF should open in Zotero's built-in reader

---

## Step 7: Tag and Annotate

### Add Tags

Select reference → Tags tab (right panel) → Add:

**Study-level tags:**

- `RCT_phase3` / `RCT_phase2`
- `included_study`
- `keynote_522` (for landmark trial)

**ICI type:**

- `pembrolizumab`
- `atezolizumab`
- `durvalumab`

**Outcomes reported:**

- `pcr_reported`
- `survival_reported`
- `pdl1_subgroup`

**Data extraction status:**

- `extracted`
- `verified`
- `needs_review`

### Add Notes

Select reference → Notes tab → Add Note:

Example for KEYNOTE-522:

```
KEYNOTE-522 EXTRACTION NOTES

pCR definition: ypT0/Tis ypN0
pCR intervention: 64.8%
pCR control: 51.2%

EFS HR: 0.63 (0.48-0.82), p<0.001

Follow-up: 75.1 months median

Notable:
- PD-L1+ subgroup: stronger benefit
- FDA approved based on this trial
- Updated OS data published Sept 2024
```

---

## Step 8: Set Up Automatic BibTeX Export

This keeps `07_manuscript/references.bib` automatically updated.

### For Main Collection:

1. Right-click `03_Fulltext_Include` collection
2. Select "Export Collection"
3. Format: **Better BibTeX** (not plain BibTeX!)
4. Check "Keep updated" (file will auto-update when you add/modify references)
5. Save as: `/Users/htlin/meta-pipe/07_manuscript/references.bib`

**Result**: Every time you add a paper to `03_Fulltext_Include` or edit its metadata, `references.bib` is automatically updated. No manual export needed! 🎉

---

## Step 9: Import Search Results (After Search Phase)

When you reach Stage 02 (Search), you'll have `02_search/round-01/dedupe.bib`.

### Import to Zotero:

1. Select `00_Search_Results` collection
2. File → Import
3. Choose `02_search/round-01/dedupe.bib`
4. Import options:
   - **Place items in**: New collection? No (already in `00_Search_Results`)
   - **Import collections**: No
5. Click "Import"

**Expected**: ~150-180 references imported

### After Screening:

**Move included studies**:

1. After Rayyan screening, identify included studies
2. Select them in `00_Search_Results`
3. Drag to `01_Screening_Include`

**Move excluded studies**:

1. Select excluded studies
2. Drag to `02_Screening_Exclude`
3. Add exclusion reason tag (e.g., `excluded_not_RCT`, `excluded_metastatic`)

---

## Step 10: Full-Text PDF Management

After full-text retrieval (Stage 04), you'll have PDFs in `04_fulltext/round-01/pdfs/`.

### Batch Import PDFs:

**Option A: Drag and drop**

1. Select references in `01_Screening_Include`
2. Open `04_fulltext/round-01/pdfs/` folder
3. Drag matching PDFs onto each reference

**Option B: ZotFile Plugin (Advanced)**

1. Install ZotFile: https://github.com/jlegewie/zotfile/releases
2. Tools → ZotFile Preferences → General Settings:
   - **Source Folder**: `/Users/htlin/meta-pipe/04_fulltext/round-01/pdfs`
   - **Location of Files**: Zotero default
   - **Renaming Format**: `{%a_}{%y_}{%t}`
3. Select all references in `01_Screening_Include`
4. Right-click → Manage Attachments → Attach New File
5. ZotFile will automatically match PDFs by title/DOI

---

## Step 11: Organize PDFs for Reading

### Create Saved Searches (Smart Collections)

#### 1. Papers Without PDFs

1. File → New Saved Search
2. Name: `Missing PDFs`
3. Conditions:
   - **Collection** is `01_Screening_Include`
   - **Attachment File Type** is not `PDF`
4. Save

This shows which papers still need PDF retrieval.

#### 2. Unread Papers

1. File → New Saved Search
2. Name: `To Read`
3. Conditions:
   - **Collection** is `03_Fulltext_Include`
   - **Tag** is not `extracted`
4. Save

This shows which papers still need data extraction.

---

## Step 12: Collaboration Setup (Optional)

If working with co-authors:

### Create Group Library

1. Go to https://www.zotero.org/groups/new/
2. Group Type: **Private** (members-only)
3. Group Name: `TNBC Neoadjuvant ICI MA Team`
4. Description: Internal collaboration for systematic review
5. Create Group

### Invite Members

1. Go to group settings on Zotero website
2. Member Settings → Send Invitations
3. Enter co-author emails
4. Role: **Member** (can read/write) or **Admin**
5. Send

### Sync Group Library

1. In Zotero desktop, group will appear in left sidebar
2. Drag references from "My Library" to group library
3. PDFs will sync (counts toward storage limit)

**Storage caveat**: Group libraries share your storage quota. If >300MB PDFs, consider:

- Upgrade storage ($20/year for 2GB)
- Store PDFs locally only (no sync)
- Share via institutional repository

---

## Step 13: Citation While Writing (Manuscript Stage)

When writing manuscript in Word (Stage 07):

### Insert Citation

1. Place cursor where citation needed
2. Click "Add/Edit Citation" in Word (Zotero toolbar)
3. Search for reference (author, title, or year)
4. Select reference
5. Click Enter

**Example**: (Schmid et al., 2020)

### Insert Bibliography

1. Place cursor where references should go
2. Click "Add/Edit Bibliography"
3. Bibliography auto-generated and auto-updated

### Change Citation Style

1. Click "Document Preferences" in Word
2. Select style:
   - **Vancouver** (numbered, for JAMA Oncology, JCO)
   - **APA 7th** (author-year, for some journals)
   - **Nature** (superscript numbers)
3. All citations instantly reformatted

---

## Step 14: Backup and Maintenance

### Automatic Backup (Recommended)

Zotero auto-saves, but for extra safety:

**Option A: Time Machine / Windows Backup**

- Zotero data location:
  - Mac: `/Users/[username]/Zotero/`
  - Windows: `C:\Users\[username]\Zotero\`
- Include in system backup

**Option B: Manual Export**

- File → Export Library
- Format: **Zotero RDF** (preserves everything)
- Save to external drive monthly

**Option C: Git (for BibTeX only)**

- The `references.bib` in `07_manuscript/` is already in git
- Commit regularly: `git commit -m "Add 2 new references"`

### Regular Maintenance

**Weekly during active phases:**

- Verify PDFs attached correctly
- Check for duplicate entries (Duplicate Items view)
- Update citation keys if needed
- Tag new papers
- Add extraction notes

**Before manuscript submission:**

- Verify all cited papers are in `03_Fulltext_Include`
- Check DOIs are correct
- Ensure journal abbreviations follow target journal style
- Export final `references.bib`

---

## Workflow Summary

### Stage 02 (Search)

→ Import `dedupe.bib` to `00_Search_Results`

### Stage 03 (Screening)

→ After Rayyan: Move included to `01_Screening_Include`, excluded to `02_Screening_Exclude`

### Stage 04 (Full-Text)

→ Retrieve PDFs, attach to references in `01_Screening_Include`
→ After full-text review: Move final included to `03_Fulltext_Include`, excluded to `04_Fulltext_Exclude`

### Stage 05 (Extraction)

→ Read PDFs from `03_Fulltext_Include`, extract data
→ Add notes to each reference
→ Tag as `extracted` when complete

### Stage 07 (Manuscript)

→ Auto-export from `03_Fulltext_Include` → `references.bib`
→ Cite papers in Word/LibreOffice using Zotero plugin
→ Auto-generate bibliography

---

## Keyboard Shortcuts (Zotero Desktop)

- **Ctrl/Cmd + N**: New item
- **Ctrl/Cmd + Shift + A**: Add by identifier (DOI/PMID)
- **Ctrl/Cmd + Shift + C**: New collection
- **Ctrl/Cmd + F**: Search library
- **Delete**: Move to trash (not permanent)
- **Ctrl/Cmd + Shift + Delete**: Permanent delete
- **Spacebar**: Open PDF in reader

---

## Troubleshooting

### Issue: Can't retrieve PDFs automatically

- **Check**: Are you on institutional network or VPN?
- **Check**: Is paper Open Access? (Use Unpaywall)
- **Solution**: Manually download from journal website

### Issue: Duplicate entries

- **Solution**: View → Duplicate Items → Merge duplicates
- **Tip**: Better BibTeX prevents duplicates by citation key

### Issue: BibTeX export missing fields

- **Ensure**: Using Better BibTeX (not plain BibTeX)
- **Check**: Export preferences → Fields to omit

### Issue: References not syncing

- **Check**: Preferences → Sync → Auto-sync enabled
- **Check**: Storage quota not exceeded
- **Solution**: Manually sync (green arrow icon)

### Issue: Word plugin not working

- **Solution**: Restart Word, reinstall plugin from Zotero preferences

---

## Advanced Tips

### 1. Full-Text Search Across All PDFs

- Zotero automatically indexes PDF text
- Use search bar: "immune checkpoint" finds all papers mentioning this

### 2. Related Items

- Select reference → Related tab → Add related
- Links papers (e.g., main trial + updated follow-up)

### 3. Timeline View

- View → Timeline
- Visualizes when studies were published (useful for temporal trends)

### 4. Generate Reports

- Select collection → Generate Report from Items
- Creates HTML summary of all papers (good for team meetings)

---

## Resources

- **Zotero Documentation**: https://www.zotero.org/support/
- **Better BibTeX Guide**: https://retorque.re/zotero-better-bibtex/
- **Zotero Forums**: https://forums.zotero.org/
- **Video Tutorials**: https://www.zotero.org/support/screencast_tutorials

---

## Timeline

- **Initial setup**: 45 minutes (today)
- **Import pilot studies**: 15 minutes (today)
- **Daily use during screening**: 5-10 minutes
- **PDF management**: 2-3 hours (Stage 04)
- **Citation during writing**: Ongoing (Stage 07)

---

## Success Checklist

- [ ] Zotero desktop installed
- [ ] Browser connector installed
- [ ] Better BibTeX plugin installed and configured
- [ ] Collection structure created (00-06 subcollections)
- [ ] Pilot studies imported (5 key trials)
- [ ] PDFs attached to pilot studies
- [ ] Automatic export configured to `07_manuscript/references.bib`
- [ ] Tags and notes added to ≥1 study (practice)
- [ ] Saved searches created (Missing PDFs, To Read)
- [ ] Backup strategy decided

---

**Version**: 1.0
**Date**: 2026-02-07
**Last updated**: Initial setup for TNBC neoadjuvant ICI meta-analysis
