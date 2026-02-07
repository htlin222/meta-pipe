# Citation Mapping: Superscript to BibTeX Keys

This document maps the superscript citations (¹, ², ³, etc.) in the manuscript to their corresponding BibTeX keys in `references.bib`.

## Citation List

| Superscript | BibTeX Key                                                         | Short Citation                                                      | Location in Manuscript                       |
| ----------- | ------------------------------------------------------------------ | ------------------------------------------------------------------- | -------------------------------------------- |
| ¹           | ref1_tnbc_incidence                                                | Dent et al. 2007                                                    | Introduction (TNBC incidence)                |
| ²           | ref2_tnbc_prognosis                                                | Foulkes et al. 2010                                                 | Introduction (TNBC prognosis)                |
| ³           | ref3_tnbc_biology                                                  | Bianchini et al. 2016                                               | Introduction (TNBC biology)                  |
| ⁴           | ref4_neoadjuvant_standard                                          | Mieog et al. 2007                                                   | Introduction (neoadjuvant standard)          |
| ⁵⁻⁷         | ref5_pcr_surrogate_ctnebc, ref6_pcr_spring, ref7_pcr_tnbc_specific | Cortazar et al. 2014, Spring et al. 2020, von Minckwitz et al. 2012 | Introduction (pCR as surrogate)              |
| ⁸           | ref8_pcr_efs_association                                           | Symmans et al. 2017                                                 | Introduction (pCR-EFS association)           |
| ⁹           | ref9_fda_guidance                                                  | FDA 2020                                                            | Introduction (FDA guidance on pCR)           |
| ¹⁰⁻¹²       | ref10_tils_tnbc, ref11_pdl1_tnbc, ref12_immune_landscape_tnbc      | Adams et al. 2014, Mittendorf et al. 2014, Safonov et al. 2017      | Introduction (TILs and PD-L1 in TNBC)        |
| ¹³⁻¹⁵       | ref13_impassion130, ref14_keynote355, ref15_impassion131           | Schmid et al. 2018, Cortes et al. 2020, Miles et al. 2021           | Introduction (metastatic TNBC ICI trials)    |
| ¹⁶          | ref16_neoadjuvant_immune_priming                                   | Kwa & Adams 2018                                                    | Introduction (immune priming in neoadjuvant) |
| ¹⁷          | ref17_keynote522                                                   | Schmid et al. 2022/2024                                             | Introduction & Results (KEYNOTE-522)         |
| ¹⁸          | ref18_impassion031                                                 | Mittendorf et al. 2020/2025                                         | Introduction & Results (IMpassion031)        |
| ¹⁹          | ref19_geparnuevo                                                   | Loibl et al. 2019/2022                                              | Introduction & Results (GeparNuevo)          |
| ²⁰          | ref20_neotripaPDL1                                                 | Gianni et al. 2022                                                  | Introduction & Results (NeoTRIPaPDL1)        |
| ²¹          | ref21_camrelief                                                    | Chen et al. 2024                                                    | Introduction & Results (CamRelief)           |
| ²²          | ref22_ici_irae                                                     | Postow et al. 2018                                                  | Introduction (irAE)                          |
| ²³          | ref23_prisma2020                                                   | Page et al. 2021                                                    | Methods (PRISMA 2020)                        |
| ²⁴          | ref24_rob2                                                         | Sterne et al. 2019                                                  | Methods (RoB 2 tool)                         |
| ²⁵          | ref25_hartung_knapp                                                | Hartung & Knapp 2001                                                | Methods (Hartung-Knapp adjustment)           |
| ²⁶          | ref26_heterogeneity_interpretation                                 | Higgins et al. 2003                                                 | Methods (heterogeneity interpretation)       |
| ²⁷          | ref27_influential_diagnostics                                      | Viechtbauer & Cheung 2010                                           | Methods (influential diagnostics)            |
| ²⁸          | ref28_publication_bias_small_k                                     | Sterne et al. 2011                                                  | Methods (publication bias with small k)      |
| ²⁹          | ref29_meta_package                                                 | Schwarzer 2024                                                      | Methods (meta R package)                     |
| ³⁰          | ref30_metafor_package                                              | Viechtbauer 2010                                                    | Methods (metafor R package)                  |
| ³¹          | ref31_grade                                                        | Guyatt et al. 2008                                                  | Methods (GRADE)                              |

---

## Usage Instructions

### For Journal Submission

When formatting for journal submission (e.g., Lancet Oncology), you will need to:

1. **Convert superscripts to citation numbers**: Replace superscripts (¹, ², ³) with standard citation format per journal style
2. **Apply journal citation style**: Most journals use numbered citations in order of appearance
3. **Format references**: Convert BibTeX to journal-specific format (usually Vancouver or AMA style for medical journals)

### Example Conversion

**Current format** (manuscript):

```markdown
Triple-negative breast cancer (TNBC)... accounts for approximately 15–20% of all breast cancers.¹
```

**Lancet Oncology format**:

```
Triple-negative breast cancer (TNBC)... accounts for approximately 15–20% of all breast cancers.1
```

**Reference list format** (Lancet style):

```
1. Dent R, Trudeau M, Pritchard KI, et al. Triple-negative breast cancer: clinical features and patterns of recurrence. Clin Cancer Res 2007; 13: 4429–34.
```

---

## BibTeX to Journal Format Conversion

### Option 1: Manual Conversion

- Export BibTeX entries from reference manager (Zotero, Mendeley, EndNote)
- Apply Lancet Oncology CSL style
- Copy formatted references to manuscript

### Option 2: Pandoc Conversion

```bash
# Convert markdown to Word with citations
pandoc manuscript.md --bibliography=references.bib --csl=lancet.csl -o manuscript.docx
```

### Option 3: LaTeX Conversion

```latex
\documentclass{article}
\usepackage[backend=biber,style=numeric,sorting=none]{biblatex}
\addbibresource{references.bib}

\begin{document}
% Manuscript content with \cite{ref1_tnbc_incidence}
\printbibliography
\end{document}
```

---

## Citation Integrity Checklist

- [x] All 31 citations have corresponding BibTeX entries
- [x] All BibTeX entries have DOI for verification
- [x] Primary trial citations (refs 17-21) include update notes
- [ ] Verify all DOIs resolve correctly
- [ ] Cross-check citation numbers match references
- [ ] Ensure no citations are out of sequence
- [ ] Verify all author names spelled correctly
- [ ] Check journal abbreviations match target journal style

---

## Key Trial References (Quick Reference)

### Primary Included Trials (5 RCTs)

1. **KEYNOTE-522** (ref17_keynote522)
   - Schmid P, et al. N Engl J Med. 2022;386:556-567 (EFS)
   - Schmid P, et al. N Engl J Med. 2024;391:515-525 (OS update)
   - DOI: 10.1056/NEJMoa2112651

2. **IMpassion031** (ref18_impassion031)
   - Mittendorf EA, et al. Lancet. 2020;396:1090-1100 (pCR)
   - Mittendorf EA, et al. Lancet Oncol. 2025 (EFS update, in press)
   - DOI: 10.1016/S0140-6736(20)31953-X

3. **GeparNuevo** (ref19_geparnuevo)
   - Loibl S, et al. Ann Oncol. 2019;30:1279-1288 (pCR)
   - Loibl S, et al. Ann Oncol. 2022;33:382-390 (OS update)
   - DOI: 10.1093/annonc/mdz158

4. **NeoTRIPaPDL1** (ref20_neotripaPDL1)
   - Gianni L, et al. Ann Oncol. 2022;33:534-543
   - DOI: 10.1016/j.annonc.2022.02.004

5. **CamRelief** (ref21_camrelief)
   - Chen X, et al. Lancet. 2024;403:2371-2383
   - DOI: 10.1016/S0140-6736(24)00526-8

---

## Status

- **BibTeX file created**: ✅ `/Users/htlin/meta-pipe/07_manuscript/references.bib`
- **Citation mapping complete**: ✅ All 31 citations mapped
- **Ready for journal formatting**: ⏳ Requires conversion to target journal style
- **Next step**: Apply Lancet Oncology CSL style using Pandoc or reference manager

---

**Last updated**: 2026-02-07
