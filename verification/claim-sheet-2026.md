# Fonts on the Web 2026 — Claim Sheet

**What this is.** Every claim in the manuscript, with the evidence behind it. It is the workspace for the claim-by-claim fact check, and it will serve afterward as the reference sheet if any claim needs defending.

- **Text checked:** `drafts/fonts-2026-v2.md` (manuscript v2, 2026-09-04). `vL##` = line in that file.
- **Data:** HTTP Archive crawl 2026-07-01, root pages. Query outputs in `sql/**/*.csv`; multi-year series in `data/multi-year/` and `../fonts_all_years.duckdb` (sheet mirrors); prior chapters in `../fonts-20YY/fonts.md`.
- **Prior map:** `verification/source-map-2026.csv` (C-IDs). This was a mechanical match pass done 9/3–9/4. It is cross-referenced here, but it is not relied on: every claim below is re-checked.

## How to read it

**Numbering.** `S.P.C` = section · paragraph · claim.
- Sections: `0` intro ("The half-web moment") · `1` Delivery · `2` Packaging · `3` Loading · `4` The canon · `5` Capability vs expression · `6` The scale problem · `7` Hygiene list · `8` Closing · `A` Appendix A · `B` Appendix B · `F` figures.
- Paragraphs count every body block in order within the section, including tables, lists, and the method box. Numbering runs straight through H3 subsections. Figure placeholders don't count.
- `S.0.h` is the section title. `S.P.h` is an H3 heading, filed under the first paragraph it introduces.

**Kinds.**
- `N`: 2026 measurement.
- `T`: trend or comparison with an earlier year.
- `X`: external fact (history, spec, industry practice, what an earlier chapter said).
- `I`: interpretation or characterization, meaning language that asserts more than the number itself.
- `M`: method or definition statement.
- `H`: heading.

**Status** (bulletproof, per claim):
- **GREEN**: defensible as written.
- **YELLOW**: publishable with the change noted.
- **RED**: wrong or unsupported as written, and must change.
- ⏳: not yet checked.

**Decision** (filled in during the live session):
- **K**: keep.
- **R**: reword, with the new wording recorded.
- **Q**: add a qualifier or denominator.
- **C**: cut.
- **D**: re-derive, meaning new computation needed.
- **V**: verify externally (cite a source).

---

## Bulletproof assessment (2026-09-30)

**Stage:** Publication (near-final manuscript v2).

**Overall: RED as written. It becomes YELLOW once the eleven HIGH items below are resolved.** None of the problems kills the thesis. Two of them change how its second and third claims have to be argued.

Evidence for every verdict is in `bp-evidence/`:
- `lane-A-s0-s1.md`: sections 0–1
- `lane-B-s2-s3.md`: sections 2–3 and the CSS-pipeline ruling
- `lane-C-s4-s5.md`: sections 4–5 and the script-classifier ruling
- `lane-D-s6-s8-app.md`: sections 6–8, the appendices, and the avar2 and IFT rulings
- `lane-E-external.md`: external facts and prior chapters, with dated sources

Verdicts are written into each claim below (source: `bp-status.txt`; merge with `apply_bp_status.py`).

| Section | GREEN | YELLOW | RED | Total |
|---|--:|--:|--:|--:|
| X working header | 0 | 0 | 1 | 1 |
| 0 The half-web moment | 14 | 21 | 4 | 39 |
| 1 Delivery | 32 | 17 | 12 | 61 |
| 2 Packaging | 31 | 15 | 6 | 52 |
| 3 Loading | 19 | 7 | 13 | 39 |
| 4 The canon | 15 | 14 | 7 | 36 |
| 5 Capability vs expression | 27 | 19 | 9 | 55 |
| 6 Scale problem | 5 | 13 | 12 | 30 |
| 7 Hygiene list | 4 | 4 | 0 | 8 |
| 8 Closing | 7 | 6 | 1 | 14 |
| A / B Appendices | 4 | 6 | 4 | 14 |
| F Figures | 1 | 4 | 5 | 10 |
| **All** | **159** | **126** | **74** | **359** |

Many REDs are one-decimal slips with a one-word fix. The heavy REDs are concentrated in sections 3 (CSS comparability), 4 (the Han classifier), and 6 (IFT and avar2).

### 0. Hypothesis and framing

The three-claim thesis was set in the 9/3 planning round after the data were in. That is normal, but it means the numbers were read through the thesis, and several of the errors below run in the thesis's favour.

- **Claim 1, maturity:** holds, with wording fixes.
- **Claim 2, a centralized workaround:** the core is real for Japanese web fonts. Google serves 96% of Noto Sans JP requests and 79% of variable-font requests.
  - But three of its load-bearing numbers are request-count artifacts. Slicing inflates CJK request counts about 20× relative to page reach, and the top-100 truncation inflates within-service shares.
  - Its "supply-side mechanism" has no page-level evidence, and self-hosted variable fonts supplied about half of variable-font request growth since 2024.
- **Claim 3, the unused spec:** stronger than stated, since no browser shipped IFT by July 2026. But the `@supports` "zero" comes from a broken detector, "unlocked" is false, and avar2 cannot be measured from table sizes.
- **What would change the thesis:** a page-level variable-font-by-service count showing that most variable-font pages get their variable fonts from outside Google.

### 1. Data provenance and methodology

- **Source.** HTTP Archive crawl 2026-07-01. The URL list comes from the Chrome UX Report: Chrome desktop and Android users only, gated by popularity, crawled from the US. The crawl was materialized into `fonts_2026.*` tables. Most query text is byte-identical to 2025, but the execution path changed (a materialized extract, pruned CSS), and there is no same-date equivalence test.
- **The CSS size gate.** It was added after validation, never validated itself, and its gated count was never recorded. Every 2026 CSS figure is therefore a lower bound of unknown margin. The symptom: with identical SQL, several CSS measures fell at once (monospace 64.0 → 46.5%, serif 47.5 → 32.6%, Font Awesome in `@font-face` 38.7 → 30.6%).
- **Family queries** keep only the top 100 families per client × service, which drops 18% of parsed requests from the denominators.
- **The script classifier** counts a script only when a file covers more than 5% of its codepoints. Han and Hangul slices can never qualify.
- **The 2022 baseline crawl was smaller:** 7.3M desktop / 10.3M mobile pages, against 12M+ / 15M+ from 2023 on.
- **Defects in the multi-year CSVs:**
  - The 2020 variable-font row has its clients swapped.
  - Values were rounded to four decimals and then printed to one, which produced six wrong one-decimal values.
- **"Self-hosted"** is SERVICE()'s catch-all bucket. It includes cdnjs, jsDelivr, Wix, Webflow, and Shopify.
- **The IFT detector** matches a substring, and its `@supports` path cannot fire. All CSS walkers skip `@font-face` rules nested inside other rules.
- **Font metadata** carries table sizes only: no avar version, no binaries.

### 2. Editor challenge

- **Double counting.**
  - Color-format shares overlap; the text discloses this.
  - First-party and other-third-party `unicode-range` overlap by about 114k pages; this is fine.
  - Family shares are not double counted, but their denominator is truncated.
- **Universe or subset.** This is the universe of HTTP Archive root pages, not "the web." Name the documented biases (0.7.6).
- **N behind every percentage.** N is large almost everywhere. The small-N claims are all stated as counts, which is right:
  - 2011 mobile: 973 pages
  - IFT: 6–7 pages
  - `font-palette`: 131–400 pages
  - `font-optical-sizing: none`: 620 / 658 pages
- **Outside expert review.** None yet: the reviewer email to Bram Stein and Ivan Ukhov was never sent. Stein wrote the 2015 `local()` anti-pattern article the draft leans on.
- **Subject pushback.** Google Fonts is the main subject of claim 2, and the likely venue is a Google blog. A courtesy check of the slicing and variable-serving descriptions with the Google Fonts team would be prudent.

### 3. Legal and ethical

Low risk. The named entities (Google Fonts, Adobe Fonts, Font Awesome, Next.js) are described factually, not accused of anything. The data are aggregate pages only, with no personal information. "Sloppy self-host pipelines" is a mild pejorative about unnamed site owners.

### 4. Reputational risk

Five worst cases:
1. **An expert debunk (most likely).** Font engineers are the audience, and they will spot the Han threshold artifact, the invalid avar2 inference, the broken `@supports` detector, and slice-inflated request counts. HIGH until fixed.
2. **Press or social criticism of the Noto Sans JP claim.** "A fifth of the world's largest font CDN" is wrong in value and in scope, and Google's own engineers know how slicing inflates request counts. HIGH until fixed.
3. **Prior-chapter authors see "first report" claims** that contradict their own chapters (2019 `local()`, 2022 metric overrides). MEDIUM.
4. **Google as both venue and subject.** Claim 2 casts Google as the web's scale layer. It has to be accurate to survive review by the people it describes. MEDIUM.
5. **A lawsuit or regulator inquiry.** N/A.

None of these is catastrophic if fixed before publication. Several would be embarrassing if not.

### 5. Dataset-specific checks (trends; service comparisons)

- **Time windows are wrong in places.**
  - "Five-year window" is four years.
  - "Largest jump" ignores 2021→22.
  - The 2022 corpus was smaller.
  - Crawl months differ (2020 August, 2022 June).
- **Cherry-picking.** The variable-font table omits 2020, 2021, and 2023, and the omission hides exactly the jump that contradicts the text. It was unintentional, but it will read as selective.
- **Alternative explanations.**
  - The mobile Google discontinuity is handled honestly.
  - The CSS declines are probably pipeline effects.
  - Metric overrides are probably framework defaults.
  - The fall in `local()` is explained by Google Fonts dropping it in November 2020.
- **Service comparisons.** Request shares are sound. Family shares are truncated. Per-page reach and request counts are conflated throughout the CJK argument.

### 6. Narrative and language

Recurring patterns:
- **Absolutes:** "every one of these," "essentially every," "exactly flat," "almost nobody," "a confident zero," "prove."
- **Causal claims without causal evidence:** "privacy- and performance-driven," "the hybrid pattern at work," "deliberate," "the mechanism is supply-side," "pathology clusters in CJK."
- **"First" claims** never checked against earlier chapters.
- **The report's own denominator rule** is broken in about a dozen places.
- **Five headings overclaim:** 1.1.h, 2.8.h, 3.0.h, 4.0.h, 4.5.h.

### 7. Visualization integrity

Ten figures. Baselines and axis directions are sound (grammar.py), and captions are not written yet.
- F1 is clean.
- F2 plots the swapped 2020 row.
- F6 and F8 carry double-rounding label errors.
- F9 labels per-file data as "requests."
- F10's accent color spotlights the Han artifact.
- F4 is desktop-only, which hides the mobile reversal.
- F5's caption says "July" for June and August crawls.
- F7 is correct, and the prose contradicts it.

### 8. Reproducibility

Strong on paper: every 2026 number has its SQL and CSV, the multi-year data are documented, and this sheet plus five evidence logs trace every claim. Weak spots:
- The earlier source map marked about 15 wrong claims "matched," because it checked values and not denominators or wording. B.1.5 must not say "machine-checked."
- The gate count is unlogged, and no data-diary entry records the gate decision.
- Internal file paths appear in the text.
- The key caveats need to move into the story copy: CSS figures are lower bounds, the definition of "self-hosted," and requests versus pages.

### 9. Government records

N/A. The report makes no regulatory or licensing claims about any entity.

### Recommended changes

**HIGH (must fix before publication)**
1. **CSS comparability** (3.3.6, 3.4.2, 3.7.3, 3.7.5, 5.2.3, 4.3.3, B.1.7). Decision D1.
2. **Family shares truncated to the top 100** (1.9–1.10, 5.6.4, 6.2.3, 6.7.4). Decision D2.
3. **Noto Sans JP and slicing** (0.4.2, 1.10.5–1.10.9, 5.6.4–5.6.6, 6.2.3, 6.7.4). Request counts are not reach, and "#1" holds on desktop only. Reframe claim 2 around slicing as the mechanism of centralization, which strengthens it.
4. **Han** (4.5.h, 4.5.1, 4.7.2, 4.7.4, 4.7.5, 6.2.1, F10). The 0.5% is a classifier artifact. Rewrite the scripts section and move the "hook" onto request data.
5. **The variable-font "largest jump"** (0.3.4, 5.5.1, 5.4.6, F2). False. Fix the wording and the swapped 2020 row, and show the full series.
6. **The supply-side mechanism** (5.7.1, 5.7.3). No page-level evidence. Decision D3.
7. **IFT and avar2** (6.4.3, 6.5.3, 6.6.4, 6.6.6, 6.7.1, 8.1.10, A.1.4). "Unlocked" is false, the `@supports` detector is broken, and avar2 is unmeasurable. Rewrite the null section. Decision D4.
8. **Prior-chapter "firsts"** (2.11.1, 3.5.h, 3.5.4, 0.7.3). Metric overrides were measured in 2022 and `local()` in 2019. Both become better stories: a roughly 50× rise, and a collapse from 57% to 10%.
9. **Wrong numbers:**
   - One-decimal slips: 2.2.4, 2.8.2, 3.1.1, 3.1.3, 3.3.1, 3.3.4, 4.3.3, 5.6.4.
   - Figure labels: F6, F8, F9.
   - Trend statements: 2.3.2, 3.2.1, 3.2.3.
10. **Internal contradictions:** 1.5.8 vs 1.4.5; 1.3.4 and 1.3.5 vs the "no mobile trend" pledge; B.1.7 vs the body.
11. **Delete** the working header and the "earlier draft" note (X.0.1, 1.11.1), and remove internal paths (B.1.5, B.1.10).

**MEDIUM (should fix)**
- Define "self-hosted" once, and state denominators and clients wherever they are missing.
- Hedge the unmeasured causes: 1.3.6, 1.7.5, 2.7.9, 2.11.4, 6.3.3.
- Soften the absolutes: 5.3.1, 5.3.2, 6.3.1, 2.10.1, 7.2.5.
- In the method box, add the 2022-corpus caveat and the documented crawl biases.
- Add a dated IFT-status sentence (ChromeStatus; the W3C Candidate Recommendation).
- Send the reviewer email.

**LOW (nice to have)**
- Units: use KiB throughout.
- Quote the 2025 chapter exactly where it is quoted, and say "last three chapters" rather than "years."
- Optional precision: Google splits each CJK family into about 100–125 subsets.
- Tooling cleanup:
  - Roboto appears twice in `styles_family.csv`.
  - `fonts-2026/fonts_all_years.duckdb` is an empty stub.
  - `variable_fonts_pages.csv` is a 0-byte file.

### Cleared claims (159 GREEN)

The core 2026 measurements are sound:
- Adoption and delivery:
  - Font adoption: 88.6% desktop / 87.1% mobile.
  - Variable-font adoption, 48.7% / 50.2%, and the +9-point gain.
  - Hosting shares and combinations.
  - Google's page reach, and its 2023–25 mobile series.
  - Request shares by service.
- Formats and files:
  - Format mix on both series, and WOFF2 by service.
  - Outline formats.
  - Size percentiles.
- CSS and font features:
  - `unicode-range` attribution values.
  - `font-display` levels.
  - OpenType capability and its growth.
  - `tabular-nums` vs `tnum`.
  - Axis data.
  - Color fonts.
  - OFL at 70% of all pages.
- Nulls and advice:
  - IFT page counts.
  - avar prevalence.
  - Hygiene items 1–3 and 7.

Each GREEN claim below names its source row.

### Decisions only you can make

Each of these turns on whether to spend money on BigQuery, which reverses the standing "no new BigQuery spend" rule.
- **D1, CSS comparability:**
  - (a) Count the `_prune_skipped` rows in `pruned_css` and state the undercount, or
  - (b) drop every CSS decline and "steady" comparison, keep the increases as directional, and label CSS figures as lower bounds.
- **D2, family shares:**
  - (a) Re-run the two family queries with per-service totals, or
  - (b) restate them as floors and ranges ("about a fifth," "one in six").
- **D3, the variable-font mechanism:**
  - (a) Run a page-level variable-font-by-service query, or
  - (b) soften the claim to request-level language.
- **D4, IFT `@supports`:**
  - (a) Fix the detector and re-run (also pull the 6–7 IFT pages to see what they are), or
  - (b) drop the `@supports` claim.

All four (a) options run on the materialized `fonts_2026` tables. The one comparable post-hoc query cost about $6. Dry-run each first; one short session could cover all of them.

---

## Excluded from publication

- **X.0.1** · `M` · Working header (vL3–6): "Manuscript v2 — 2026-09-04 writing block … Word target … currently ~5,600 body". Delete before publication. The word count is stale: the file is 4,415 words including appendices.
  - Evidence: vL3–6 working header; `wc -w` = 4,415 words (body vL10–283 = 4,150), not "~5,600 body"; vL5 lists internal C-IDs. [lane A]
  - Bulletproof: **RED**. Internal working notes with a stale word count. Must not ship.
  - Suggested fix: Delete vL3–6.
  - Decision: **A** · deleted in v3 (2026-10-01)

---

## 0 · The half-web moment (vL10–28)

- **0.0.h** · `H` · "The half-web moment". The title frames variable fonts crossing 50% as the year's defining event.
  - Evidence: fonts_variable.csv: 48.69% desktop / 50.21% mobile of root pages. [lane A]
  - Bulletproof: **YELLOW**. "Half-web" is literally true only on mobile. It works as a headline if the body states both clients plainly.
  - Suggested fix: Keep the title; make sure the first mention reads "half of mobile pages, just under half of desktop."
  - Decision: **A** · title kept; body states both clients (0.3.2)

### ¶0.1 (vL12) "In 2011, when the HTTP Archive first paid serious attention…"

- **0.1.1** · `X` · "In 2011, when the HTTP Archive first paid serious attention to web typography"
  - Evidence: The HTTP Archive began crawling in Oct 2010; its reqFont timeseries starts 2010-11-15 (mobile 2011-05-16). No typography-specific focus until the 2019 Web Almanac fonts chapter. [lane E]
  - Bulletproof: **YELLOW**. "First paid serious attention to web typography" misdescribes a request counter.
  - Suggested fix: "In 2011, the HTTP Archive's first full year of data, custom fonts were a specialty…"
  - Decision: **A** · v3: "In 2011, the HTTP Archive's first full year of data, …"
- **0.1.2** · `T` · "custom fonts were a specialty: about 4% of desktop pages (and 2% of mobile) shipped their own faces or used an early service". Prior map C001.
  - Evidence: chart_font_usage_annual.csv, 2011-07-15: desktop 723/16,906 = 4.28%; mobile 20/973 = 2.06%. [lane A]
  - Bulletproof: **YELLOW**. Desktop is solid. The 2011 mobile figure rests on 20 pages out of a 973-page crawl, too thin to quote as a share.
  - Suggested fix: "about 4% of desktop pages" and drop the 2011 mobile figure (or note the mobile crawl was under 1,000 pages).
  - Decision: **A** · v3: mobile 2011 figure dropped
- **0.1.3** · `T` · "Desktop crossed the halfway mark around 2015, mobile shortly after". Prior map C002.
  - Evidence: chart_font_usage_annual.csv: desktop first ≥50% on 2015-02-15 (0.5000); mobile 0.5011 on 2015-08-01. [lane A]
  - Bulletproof: **GREEN**. Both halves of the sentence hold.
  - Decision: **K**
- **0.1.4** · `T` · "By 2020 the figure was over 80%". Prior map C003.
  - Evidence: chart_font_usage_annual.csv 2020-07-01: 81.25% desktop / 80.53% mobile. [lane A]
  - Bulletproof: **GREEN**. "Over 80%" is correct for both clients.
  - Decision: **K**
- **0.1.5** · `N` · "88.6% of desktop root pages and 87.1% of mobile still request at least one web font". Prior map C005, C006.
  - Evidence: sql/performance/fonts.csv: 10,298,910 / 11,628,567 = 88.57% desktop; 87.06% mobile; denominator all root pages. [lane A]
  - Bulletproof: **GREEN**. Exact match.
  - Decision: **K**
- **0.1.6** · `T` · "In the July 2026 crawl the line barely moved" (implies a 2025 value close to 2026)
  - Evidence: 2025-07-01 87.92% / 86.60% → 2026 88.57% / 87.06% (+0.65 / +0.46 pp); same SQL definition. [lane A]
  - Bulletproof: **GREEN**. "Barely moved" is accurate.
  - Decision: **K**
- **0.1.7** · `I` · "Saturation, for the Latin-default web, is the backdrop — not the story."
  - Evidence: No script or commercial segmentation exists in the data; recent YoY +0.76, +0.65 pp. [lane A]
  - Bulletproof: **YELLOW**. "Saturation" is supported. "For the Latin-default web" asserts a segment the crawl does not measure.
  - Suggested fix: "Saturation is the backdrop, not the story." (drop the segment), or flag it as the report's reading.
  - Decision: **A** · v3: "Saturation is the backdrop — not the story."

### ¶0.2 (vL14) "The story in 2026 is what kind of maturity…"

- **0.2.1** · `I` · "The story in 2026 is what kind of maturity we have, and it comes in three claims."
  - Evidence: Structural sentence. [lane A]
  - Bulletproof: **GREEN**. Framing only; each of the three claims is graded on its own.
  - Decision: **K**

### ¶0.3 (vL16) "First, the mature part is genuinely mature."

- **0.3.1** · `I` · "First, the mature part is genuinely mature."
  - Evidence: Rests on 0.3.2–0.3.7. [lane A]
  - Bulletproof: **YELLOW**. The claim stands only once 0.3.4 (largest jump) and 0.3.6 (CSS YoY) are fixed.
  - Suggested fix: No change to this sentence; fix the supporting clauses.
  - Decision: **K**
- **0.3.2** · `N` · "Variable fonts crossed half the web this year — 48.7% of desktop pages and 50.2% of mobile load at least one variable font". Prior map C007. Note that desktop is below 50%.
  - Evidence: 48.686% desktop / 50.209% mobile. [lane A]
  - Bulletproof: **YELLOW**. "Crossed half the web" is true only on mobile; desktop is 1.3 points short.
  - Suggested fix: "Variable fonts reached half the web this year: 50.2% of mobile pages and 48.7% of desktop load at least one."
  - Decision: **A** · v3: "Variable fonts reached half the web this year: 50.2% of mobile pages and 48.7% of desktop…"
- **0.3.3** · `T` · "up about nine points from 2025". Prior map C010.
  - Evidence: 2025 39.43% / 41.30% → 2026 48.69% / 50.21%: +9.26 / +8.91 pp. [lane A]
  - Bulletproof: **GREEN**. "About nine points" holds on both clients.
  - Decision: **K**
- **0.3.4** · `T` · "matching the technology's initial 2019–2020 surge as the largest jump in the series". Prior map C010.
  - Evidence: chart_variable_fonts.csv YoY: 2021→22 +15.70 desktop / +16.28 mobile (12.66% → 28.36%); 2019→20 ≈ +8.7–9.2; 2025→26 +9.26. The 2022 chapter says VF "shot up" in 2022. The CSV's 2020 row is client-swapped (the 2020 chapter says 10.54% desktop / 11.00% mobile). [lane A; spot-checked]
  - Bulletproof: **RED**. False as written. 2021→22 is the largest jump; 2026 is second, roughly tied with 2019→20.
  - Suggested fix: "the biggest single-year gain since 2022's sixteen-point leap." Also fix the swapped 2020 row in chart_variable_fonts.csv and re-render F2.
  - Decision: **A** · v3: "the biggest single-year gain since 2022's sixteen-point leap"; 2020 row un-swapped in chart_variable_fonts.csv (backup .bak-2026-10-01); F2 re-rendered
- **0.3.5** · `T` · "WOFF2 keeps consolidating."
  - Evidence: chart_formats.csv WOFF2 unique-URL share 59.5 → 65.0 → 68.5% (desktop 2024–26); request share 81.0 → 82.4 → 83.7%. [lane A]
  - Bulletproof: **GREEN**. Both series rise.
  - Decision: **K**
- **0.3.6** · `T` · "`font-display: swap` keeps winning."
  - Evidence: swap 31.8 → 49.5 → 52.6% desktop (2025 is 49.5, see 3.3.1); 2026 value comes from the pruned_css pipeline (see B.1.7, 3.3.6). [lanes A, D]
  - Bulletproof: **YELLOW**. Direction is plausible, but the 2026 CSS figure is from a different, unvalidated extraction than 2022/2025, so the YoY comparison is qualified.
  - Suggested fix: Tie to the CSS-comparability ruling (3.3.6).
  - Decision: **K** · CSS lower-bound caveat added to method box; D5 full gate-effect scan running
- **0.3.7** · `T` · "Self-hosting holds at about seven pages in ten." Prior map C011, C012.
  - Evidence: self-hosted 71.41% / 70.15% (2026) vs 71.68% / 71.63% (2025). SERVICE() labels as "self-hosted" any host that isn't a listed font service, including cdnjs, jsDelivr, Wix, Webflow and Shopify (21 of 64 in a log sample). [lane A]
  - Bulletproof: **YELLOW**. The number holds, but "self-hosting" in this report means "not a known font service," which readers will misread as "own server."
  - Suggested fix: Define it once in the method box ("served from anywhere other than a recognized font service, including public CDNs and site builders") and use "self-hosted" consistently after that.
  - Decision: **A** · "self-hosted" defined once in the method box
- **0.3.8** · `I` · "For Latin text on commercial pages, web fonts are a solved product surface with known best practices."
  - Evidence: No script or commercial segmentation in the data. [lane A]
  - Bulletproof: **YELLOW**. An interpretive claim stated as fact. Defensible as the author's reading of the aggregate numbers.
  - Suggested fix: Mark it as judgment, e.g. "For the Latin-script commercial web that dominates the crawl, web fonts look like a solved product surface."
  - Decision: **A** · v3: "For the Latin-script commercial web that dominates the crawl, web fonts look like…"

### ¶0.4 (vL18) "Second, the scale problem…"

- **0.4.1** · `I` · "the scale problem — the full range of human writing systems, and the multi-megabyte files that serve them — is not unsolved so much as *centralized*"
  - Evidence: Google 79.4% of VF requests; 96% of Noto Sans JP requests are Google-served. The crawl cannot see CJK sites that rely on system fonts. [lane A]
  - Bulletproof: **YELLOW**. Centralization is real for the CJK web fonts the crawl sees. But most CJK text on the web likely uses system fonts, which this data cannot see, so "the scale problem is centralized" overreaches.
  - Suggested fix: "…is, where web fonts are used at all, centralized."
  - Decision: **A** · v3: "…is, where web fonts are used at all, not unsolved so much as centralized."
- **0.4.2** · `N` · "The single largest variable-font family on the web by traffic is not Roboto; it is Noto Sans JP." Prior map C151, C152.
  - Evidence: fonts_variable_family.csv VF requests. Desktop: Noto Sans JP 23.4% > Roboto 21.3%. Mobile: Roboto 4,858,934 (21.65%) > Noto Sans JP 4,620,657 (20.59%). Noto Sans JP averages ~28 VF requests per page that uses it (Google's unicode-range slices), Roboto ~1.4; by pages Roboto reaches ~18× more. [lane A; lane D concurs on mobile]
  - Bulletproof: **RED**. False on mobile. On desktop, "largest by traffic" is an artifact of slicing: request count measures files fetched, not reach.
  - Suggested fix: Reframe: "By request count on desktop, the busiest variable-font family is Noto Sans JP. Google splits it into dozens of subset files per page, which is exactly the centralized workaround this report describes." Drop "on the web" and "by traffic."
  - Decision: **A** · v3: slicing made the point ("By request count on desktop, the busiest variable-font family isn't Roboto but Noto Sans JP, which Google splits…"). D2 re-run: Noto Sans JP 26.5 VF requests/page vs Roboto 1.4; Roboto on 17× more VF pages
- **0.4.3** · `I` · "East Asian typography at web scale happens overwhelmingly on Google's infrastructure"
  - Evidence: Noto Sans JP: Google 4.37M requests vs 180K self-hosted (96% Google). Korean leaders include self-hosted Pretendard (325K). No Chinese-specific signal. [lane A]
  - Bulletproof: **YELLOW**. Supported for Japanese; weaker for Korean; silent on Chinese.
  - Suggested fix: "Japanese web typography, where it uses web fonts, runs overwhelmingly on Google's infrastructure."
  - Decision: **A** · v3: "Japanese web typography, where it uses web fonts, runs overwhelmingly on Google's infrastructure"
- **0.4.4** · `X` · "which fragments and subsets those enormous fonts so that individual sites don't have to"
  - Evidence: Live CSS2 API probe (2026-09-30): Noto Sans JP served as 124 unicode-range slices, Noto Sans SC as 101; AIGA 2018-08-09 describes Google's frequency-based CJK slicing. [lane E]
  - Bulletproof: **GREEN**. Accurate. Optional precision: "slices each CJK family into roughly 100–125 subsets."
  - Decision: **K**
- **0.4.5** · `I` · "The workaround works. It is also a workaround."
  - Evidence: No CJK performance data. [lane A]
  - Bulletproof: **YELLOW**. "The workaround works" asserts an outcome the data doesn't measure. Fine as an author's judgment if framed that way.
  - Suggested fix: Keep the second sentence; soften the first ("It is a workaround that evidently scales").
  - Decision: **A** · v3: "It is a workaround that evidently scales. It is also a workaround."

### ¶0.5 (vL20) "Third, the technology designed to solve that problem properly…"

- **0.5.1** · `I` · "the technology designed to solve that problem properly — Incremental Font Transfer — remains a measured zero"
  - Evidence: 6 desktop / 7 mobile pages (see 6.5.1 for detector caveats). [lanes A, D]
  - Bulletproof: **YELLOW**. "Measured zero" vs 6–7 pages is a near-zero. "Properly" is editorial.
  - Suggested fix: "remains, in practice, a measured zero (six desktop and seven mobile pages)."
  - Decision: **A** · v3: "remains, in practice, a measured zero"
- **0.5.2** · `N` · "The opt-in appears on six desktop pages and seven mobile pages". Prior map C013.
  - Evidence: styles_font_tech_incremental.csv: 6 desktop / 7 mobile pages. The query matches the substring "incremental" in top-level @font-face `src` only. [lanes A, D]
  - Bulletproof: **YELLOW**. The count is right, but what it counts is broader than the spec opt-in (legacy keywords, URLs containing the word) and misses nested rules. It is still tiny either way.
  - Suggested fix: "An `@font-face` source mentioning incremental transfer appears on six desktop pages and seven mobile pages."
  - Decision: **A** · D4 re-run (fixed detector): exactly one site writes tech(incremental) — store.gs1us.org (VTEX), on ordinary Gotham WOFF2 files; the other 5–6 old hits were URL substrings (e.g. autoincremental.es); @supports font-tech(incremental) = 0 (now measured). v3: "exactly one site in the entire crawl … attached to ordinary WOFF2 files"
- **0.5.3** · `N` · "out of more than eleven million". Prior map C014.
  - Evidence: Denominators 11,628,567 desktop / 15,539,089 mobile. [lane A]
  - Bulletproof: **GREEN**. "More than eleven million" is true for both.
  - Decision: **superseded** by the 0.5.2 rewrite (crawl sizes now stated per client)
- **0.5.4** · `X` · "it is the pre-launch baseline against which 2027 can be read". This assumes IFT had not launched as of July 2026.
  - Evidence: IFT: W3C Candidate Recommendation Snapshot 2025-07-31, CR Draft 2025-11-18. ChromeStatus "Proposed" (Intent to Prototype 2026-04-28), no flag or origin trial. Firefox and Safari: no signal. [lane E]
  - Bulletproof: **YELLOW**. "Pre-launch" is true; say which launch.
  - Suggested fix: "the baseline from before any browser ships it."
  - Decision: **A** · v3: "the baseline from before any browser ships it"

### ¶0.6 (vL22) "Maturity, a centralized workaround, and an unused spec."

- **0.6.1** · `I` · "Maturity, a centralized workaround, and an unused spec."
  - Evidence: Summary sentence. [lane A]
  - Bulletproof: **YELLOW**. Inherits 0.3.4 and 0.4.2; fine once those are fixed.
  - Suggested fix: No change needed after upstream fixes.
  - Decision: **K**
- **0.6.2** · `I` · "why so many measurements in this report keep pointing at the same empty column"
  - Evidence: Only IFT (and the inferred avar2 null) is literally empty. [lane A]
  - Bulletproof: **YELLOW**. "So many measurements … keep pointing at the same empty column" overstates what is one or two nulls.
  - Suggested fix: "why several measurements point at the same gap."
  - Decision: **A** · v3: "why several measurements in this report point at the same gap"

### ¶0.7 (vL24) Method box: "How to read these numbers."

- **0.7.1** · `M` · "Every metric here names its denominator"
  - Evidence: Unstated denominator or client: combos table, both family lists, "by traffic", 0.7.4, 1.8.x, A.1.2/A.1.3. [lane A]
  - Bulletproof: **RED**. The report states a rule it breaks in at least a dozen places. That is the first thing a hostile reader tests.
  - Suggested fix: Either fix every instance (claim sheet flags each) or soften to "Each metric names its denominator where it matters."
  - Decision: **A** · rule kept; each missing denominator/client fixed section by section
- **0.7.2** · `M` · "Page shares are percentages of the ~11.6M desktop / ~15.5M mobile root pages in the July 1, 2026 crawl" (asserts one universal page denominator)
  - Evidence: 27 queries normalize on all pages; others use VF pages, parsed fonts, distinct URLs or requests. CSS numerators are floors (pruned_css gate, nested @font-face skipped). [lanes A, D]
  - Bulletproof: **YELLOW**. Not a universal denominator.
  - Suggested fix: "Unless noted, page shares are percentages of…" plus a line that CSS figures are lower bounds.
  - Decision: **A** · v3: "Unless noted, page shares are…"; "Figures derived from CSS are lower bounds (see Method)." Revisit when D5 lands
- **0.7.3** · `X` · "Format mix is reported on distinct font URLs for year-over-year comparison (the convention the 2025 chapter settled on)"
  - Evidence: The 2025 chapter (L34, L112) calls its 65% WOFF2 figure "requests", though it is the distinct-URL share; L494 says "files". It never states a unique-URL convention. [lanes A, B, E]
  - Bulletproof: **RED**. "The convention the 2025 chapter settled on" is false. 2025 used the series but mislabeled it.
  - Suggested fix: "Format mix is reported on distinct font URLs (the series behind the 2025 chapter's 65% WOFF2 figure, which that chapter loosely called requests)."
  - Decision: **A** · v3: "(the series behind the 2025 chapter's 65% WOFF2 figure, which that chapter loosely called requests)"
- **0.7.4** · `N` · "WOFF2 is 68.5% of unique URLs but 83.7% of requests, and both are true". Prior map C218.
  - Evidence: fonts_format_file.csv desktop: woff2 15,547,224 / 22,701,662 = 68.48% of distinct URLs; 52,773,718 / 63,045,145 = 83.71% of requests. [lane A]
  - Bulletproof: **YELLOW**. Numbers exact; client unstated.
  - Suggested fix: Add "(desktop)".
  - Decision: **A** · v3: "on desktop, WOFF2 is 68.5%…"
- **0.7.5** · `M` · "Variable-font axis figures distinguish axes present in files from axes set in CSS, whose denominator is only the pages that use `font-variation-settings` at all"
  - Evidence: Axis-in-CSS denominator = 96,144 desktop pages with font-variation-settings. [lane A]
  - Bulletproof: **GREEN**. Accurate description of the method.
  - Decision: **K**
- **0.7.6** · `X` · "The crawl visits root pages of sites worldwide but skews toward the commercial, Latin-script web"
  - Evidence: The HA URL list comes from CrUX: Chrome desktop and Android only (no iOS), popularity-gated, crawled from US data centers. No source supports "commercial, Latin-script". [lane E]
  - Bulletproof: **YELLOW**. The documented biases are different from, and stronger than, the one asserted.
  - Suggested fix: Name the documented biases (Chrome-user popularity lists, no iOS, US-based crawl); keep "Latin-script" only as the report's inference.
  - Decision: **A** · v3: documented crawl biases (Chrome-popular sites, desktop + Android, fetched from the US); "likely … Latin-script" marked as inference
- **0.7.7** · `M` · "that bias matters most in the script-coverage section, and we say so there"
  - Evidence: vL183 and vL197 discuss the file-vs-population bias. [lane A]
  - Bulletproof: **GREEN**. The promise is kept.
  - Decision: **K** · folded into the 0.7.6 sentence

### ¶0.8 (vL28) "The remaining ~12% of pages…"

- **0.8.1** · `N` · "The remaining ~12% of pages". Prior map C022.
  - Evidence: No-font pages 11.43% desktop / 12.94% mobile. [lane A]
  - Bulletproof: **GREEN**. "~12%" sits between the two clients.
  - Decision: **K**
- **0.8.2** · `I` · "are not a secret avant-garde of system-font purists so much as a mix of minimal sites, broken configs, and places where typography was never a product requirement"
  - Evidence: No query characterizes pages without web fonts. [lane A]
  - Bulletproof: **YELLOW**. A plausible but unmeasured description, stated as fact.
  - Suggested fix: Hedge ("are probably less a secret avant-garde … than…") or cut.
  - Decision: **A** · v3: hedged ("are probably less a secret avant-garde … than …")
- **0.8.3** · `I` · "Growth from here is residual."
  - Evidence: +0.76 / +0.65 pp in the last two years. [lane A]
  - Bulletproof: **GREEN**. "Residual" growth matches.
  - Decision: **K**
- **0.8.4** · `I` · "The interesting variation is *how* fonts arrive."
  - Evidence: Framing. [lane A]
  - Bulletproof: **GREEN**. Transitional sentence.
  - Decision: **K**

---

## 1 · Delivery (vL32–68)

- **1.0.h** · `H` · "Delivery: a self-hosting plateau, and Google on half the map"
  - Evidence: self-hosted 71.4% / 70.2%, flat vs 2025; Google 53.7% / 51.9%. [lane A]
  - Bulletproof: **GREEN**. Both halves of the heading hold.
  - Decision: **K**

### ¶1.1 (vL36) "About seven in ten pages serve at least one font from their own origin…"

- **1.1.h** · `H` · "The architecture of hosting has stabilized"
  - Evidence: Desktop combos moved ≤1.5 pp YoY; mobile combos moved 2.2–3.5 pp. [lane A]
  - Bulletproof: **YELLOW**. "Stabilized" is true for desktop only.
  - Suggested fix: Scope to desktop, or keep and let 1.3 say mobile shifted.
  - Decision: **A** · v3: "…has stabilized on desktop"
- **1.1.1** · `N` · "About seven in ten pages serve at least one font from their own origin (71.4% desktop, 70.2% mobile)". Prior map C023. Check what SERVICE() calls "self-hosted".
  - Evidence: 71.409% desktop / 70.151% mobile. SERVICE() "self-hosted" = not a listed service, including cdnjs, jsDelivr, Wix, Webflow. [lane A]
  - Bulletproof: **YELLOW**. The number is right; "from their own origin" is wrong for an unknown share of those pages.
  - Suggested fix: "About seven in ten pages load at least one font from somewhere other than a font service (71.4% desktop, 70.2% mobile)."
  - Decision: **A** · v3: "About seven in ten pages self-host at least one font (71.4% desktop, 70.2% mobile)"
- **1.1.2** · `T` · "the same ballpark as 2025". Prior map C012.
  - Evidence: −0.27 pp desktop / −1.48 pp mobile vs 2025. [lane A]
  - Bulletproof: **GREEN**. "Same ballpark" holds.
  - Decision: **K** · scoped "on desktop"
- **1.1.3** · `T` · "the leveling-off of a climb that ran from 67% in 2022". Prior map C024.
  - Evidence: Desktop 67.1 → 71.7 → 71.4; mobile 67.4 → 71.6 → 70.2. The 2022 corpus is smaller (7.3M desktop / 10.3M mobile vs 12M+ / 15M+ from 2023). [lane A]
  - Bulletproof: **YELLOW**. Desktop leveling is fine. Mobile fell 1.5 points this year, and the 2022 baseline is a different-size crawl.
  - Suggested fix: "levelling off (desktop) or slipping (mobile) after a climb from 67% in 2022."
  - Decision: **A** · v3: desktop leveling; mobile shift stated as level (¶1.3)
- **1.1.4** · `I` · "the web's habits look almost architectural"
  - Evidence: Rhetorical. [lane A]
  - Bulletproof: **GREEN**. Figure of speech, no factual load.
  - Decision: **K**

### ¶1.2 (vL38–42) Hosting-combinations table (2026)

- **1.2.1** · `N` · Google + self-hosted: 35.2% desktop / 34.0% mobile. Prior map C025.
  - Evidence: fonts_services.csv: 35.209% / 33.973% of all root pages. [lane A]
  - Bulletproof: **GREEN**. Exact.
  - Decision: **K**
- **1.2.2** · `N` · Self-hosted only: 32.2% / 32.9%. Prior map C027.
  - Evidence: 32.227% / 32.865%. [lane A]
  - Bulletproof: **GREEN**. Exact.
  - Decision: **K**
- **1.2.3** · `N` · Google only: 14.3% / 14.5%. Prior map C029.
  - Evidence: 14.297% / 14.457%. [lane A]
  - Bulletproof: **GREEN**. Exact.
  - Decision: **K**
- **1.2.4** · `M` · The table's denominator is unstated: all root pages, or pages with fonts?
  - Evidence: Denominator = all root pages, including the 11–13% with no fonts. [lane A]
  - Bulletproof: **YELLOW**. The reader can't tell from the table.
  - Suggested fix: Header "Share of all root pages (2026)".
  - Decision: **A** · v3 header: "Pattern (share of all root pages, 2026)"

### ¶1.3 (vL44) "Three combinations cover four-fifths of pages…"

- **1.3.1** · `N` · "Three combinations cover four-fifths of pages". Prior map C031.
  - Evidence: 81.73% desktop / 81.30% mobile of all pages. [lane A]
  - Bulletproof: **GREEN**. "Four-fifths" is right.
  - Decision: **K**
- **1.3.2** · `N` · "everything else — Adobe hybrids, Font Awesome CDN mixes, Japanese hosts — is a long tail of one-percent slices". Prior map C032.
  - Evidence: Adobe/FA combinations 0.4–1.2%; fontplus.jp 0.069%; typesquare 0.022%. [lane A]
  - Bulletproof: **YELLOW**. "One-percent slices" fits Adobe/FA. The Japanese hosts are ~100× smaller.
  - Suggested fix: "a long tail of slices of about one percent or less."
  - Decision: **A** · v3: "slices of about one percent or less"
- **1.3.3** · `T` · "Exclusive self-hosting has risen ten points on desktop since 2022 (22.0% → 32.2%)". Prior map C054.
  - Evidence: chart_service_combos.csv desktop self-only 21.99% (2022) → 32.23% (2026), +10.24 pp. [lane A]
  - Bulletproof: **GREEN**. Correct. The 2022-corpus caveat applies to all "since 2022" claims; handle it once in the method box.
  - Decision: **K**
- **1.3.4** · `T` · "but the year-over-year move has slowed to a crawl"
  - Evidence: Desktop self-only YoY: +4.58, +0.94, +3.97, +0.75 pp. Mobile's last step −3.52 pp. [lane A]
  - Bulletproof: **RED**. Not a steady slowdown (2024→25 was +3.97), and on mobile the trend reversed.
  - Suggested fix: "…but it barely moved on desktop this year (+0.75 points) and fell on mobile."
  - Decision: **A** · v3: "it barely moved on desktop this year (+0.8 points)"
  - Correction 2026-10-16 (weak-trace recount): **+0.7 points** in v8 — 3,747,534/11,628,567 − 3,826,767/12,155,048 = +0.74 pp; +0.8 came from subtracting the rounded 4-decimal shares. `verification/weak-trace-2026-10-16.tsv`.
- **1.3.5** · `T` · "hybrid Google-plus-self remains the single most common recipe"
  - Evidence: Mobile self-only led 2023–2025 (e.g. 36.39% vs 31.74%); Google+self regained the mobile lead in 2026. [lane A]
  - Bulletproof: **YELLOW**. "Remains" is true on desktop only.
  - Suggested fix: "…remains the single most common recipe on desktop."
  - Decision: **A** · v3: "remains the single most common recipe on desktop"; + "Mobile shares shifted by 2–3.5 points this year, in step with the Google-mobile discontinuity below."
- **1.3.6** · `I` · "The privacy- and performance-driven migration off CDNs is real over a five-year window; it is not, in 2026, a stampede." This attributes a cause, and 2022–2026 spans four years, not five.
  - Evidence: 2022–2026 spans four years. No data on motives (privacy/performance). Mobile Google +0.4 pp since 2022. [lane A]
  - Bulletproof: **RED**. The window is wrong and the causal attribution is unmeasured. It also sits oddly with 1.5.8.
  - Suggested fix: "The migration off font CDNs is real on desktop over four years; it is not, in 2026, a stampede." (Drop "privacy- and performance-driven" or attribute it to prior chapters or external sources.)
  - Decision: **A** · v3: "The migration off font CDNs, which the 2022 chapter tentatively tied to browser cache partitioning and GDPR, is real on desktop over four years…" (2022 chapter L77, L93)

### ¶1.4 (vL50) "Counting any page that fetches a font from Google's infrastructure…"

- **1.4.h** · `H` · "Google Fonts: a level, not a slope"
  - Evidence: Desktop 59.8 → 55.6 → 56.8 → 53.6 → 53.7. [lane A]
  - Bulletproof: **YELLOW**. "A level, not a slope" is the right ruling for mobile 2026, but desktop does have a 2022–25 slope, which the next paragraph says.
  - Suggested fix: Keep; make sure 1.4.5 and 1.5.8 don't contradict it.
  - Decision: **K** · heading rules on mobile; desktop slope stated in 1.4.3
- **1.4.1** · `M` · "Counting any page that fetches a font from Google's infrastructure"
  - Evidence: SERVICE() Google regex over font file URLs. [lane A]
  - Bulletproof: **GREEN**. Accurate.
  - Decision: **K**
- **1.4.2** · `N` · "Google appears on 53.7% of desktop and 51.9% of mobile pages". Prior map C034.
  - Evidence: 6,240,417 / 11,628,567 = 53.665% desktop; 51.922% mobile. [lane A]
  - Bulletproof: **GREEN**. Exact.
  - Decision: **K**
- **1.4.3** · `T` · "The desktop number is exactly flat against 2025". Prior map C035.
  - Evidence: 53.645% (2025) → 53.665% (2026), +0.02 pp. [lane A]
  - Bulletproof: **YELLOW**. Effectively flat, but "exactly" invites a check that shows 53.6 vs 53.7.
  - Suggested fix: "essentially flat against 2025 (53.6% → 53.7%)."
  - Decision: **A** · v3: "essentially flat against 2025 (53.6% → 53.7%) and down six points from 59.8% in 2022"
- **1.4.4** · `T` · "(and down from 59.8% in 2022)". Prior map C194.
  - Evidence: 59.776% (2022). [lane A]
  - Bulletproof: **GREEN**. Correct (2022-corpus caveat handled globally).
  - Decision: **K**
- **1.4.5** · `T` · "a long, slow decline that has stalled"
  - Evidence: 59.8 → 55.6 → 56.8 → 53.6 → 53.7 (2022–26 desktop). [lane A]
  - Bulletproof: **YELLOW**. Down six points, but not monotonic (2024 rose).
  - Suggested fix: "down six points since 2022, and flat this year."
  - Decision: **A** · folded into 1.4.3 ("down six points"); "long, slow decline that has stalled" removed

### ¶1.5 (vL52) "Mobile needs a more careful sentence."

- **1.5.1** · `T` · "Our own multi-year series had mobile Google at 46–47.5% for three consecutive crawls (2023–2025)". Prior map C037.
  - Evidence: Mobile Google 46.27 / 47.53 / 47.21% (2023–25). [lane A]
  - Bulletproof: **GREEN**. Exact.
  - Decision: **K**
- **1.5.2** · `T` · "the 2026 crawl reads 51.9%, back at the 2022 level". Prior map C195.
  - Evidence: 51.92% (2026) vs 51.51% (2022). [lane A]
  - Bulletproof: **GREEN**. Exact.
  - Decision: **K**
- **1.5.3** · `T` · "while desktop did not move at all"
  - Evidence: Desktop +0.02 pp. [lane A]
  - Bulletproof: **GREEN**. Correct.
  - Decision: **K**
- **1.5.4** · `M` · "The methodology is unchanged." Check whether SERVICE() and the pipeline are the same in the 2025 and 2026 queries.
  - Evidence: SERVICE() and services SQL identical to 2025. 2026 ran through execute_materialized.py against fonts_2026.font_requests/root_pages; history ran on crawl.requests; no same-date equivalence test. [lane A]
  - Bulletproof: **YELLOW**. "Methodology unchanged" is true of the query text, not the execution path.
  - Suggested fix: "The query definition is unchanged (2026 ran on a materialized extract of the same tables)."
  - Decision: **A** · v3: "The query definition is unchanged (2026 ran on a materialized extract of the same crawl tables)."
- **1.5.5** · `I` · "We could not identify a mechanism — crawl composition, service-detection edge cases, and real product shifts are all candidates"
  - Evidence: Mobile self-only −3.5 pp, Google-only +2.5 pp; Roboto mobile VF requests +62%. [lane A]
  - Bulletproof: **GREEN**. The honest statement holds. The data localize the shift without explaining it.
  - Decision: **K**
- **1.5.6** · `I` · "this report declines to narrate a mobile trend in either direction"
  - Evidence: 1.3.5, 1.5.2 ("back at the 2022 level") and 1.5.8 still characterize mobile movement. [lane A]
  - Bulletproof: **YELLOW**. The pledge is broken by neighbouring sentences.
  - Suggested fix: Audit mobile trend language in §1 (1.3.4, 1.3.5, 1.5.8).
  - Decision: **A** · mobile trend sentences in §1 now level-only (1.3.5)
- **1.5.7** · `N` · "Google's fonts touch more than half of pages on both clients"
  - Evidence: 53.67% / 51.92%. [lane A]
  - Bulletproof: **GREEN**. Correct on both clients.
  - Decision: **K**
- **1.5.8** · `I` · "reports of the CDN's decline remain, at minimum, premature". Compare 1.4.5 ("a long, slow decline").
  - Evidence: Desktop Google −6.1 pp since 2022; 1.4.5 itself says "a long, slow decline". [lane A]
  - Bulletproof: **RED**. Internal contradiction: the paragraph above documents the decline this sentence calls premature.
  - Suggested fix: "…and reports of the CDN's collapse are premature: it still reaches more than half of pages."
  - Decision: **A** · v3: "…and reports of the CDN's collapse are premature."

### ¶1.6 (vL54) "Adobe Fonts sits at…"

- **1.6.1** · `N` · "Adobe Fonts sits at 4.0% desktop / 3.2% mobile". Prior map C038.
  - Evidence: Adobe 3.993% / 3.243% of pages. [lane A]
  - Bulletproof: **GREEN**. Exact.
  - Decision: **K**
- **1.6.2** · `N` · "the Font Awesome CDN at 3.0% / 2.6%". Prior map C040.
  - Evidence: fontawesome.com 2.968% / 2.607%. [lane A]
  - Bulletproof: **GREEN**. Exact.
  - Decision: **K**
- **1.6.3** · `N` · "most FA traffic is self-hosted"
  - Evidence: Font Awesome family requests: 4,327,761 "self-hosted" vs 750,172 FA CDN (85.2% desktop, 87.7% mobile). "Self-hosted" includes cdnjs and jsDelivr copies of FA. [lane A]
  - Bulletproof: **YELLOW**. True in the report's own sense of "self-hosted," misleading in the ordinary sense.
  - Suggested fix: "most Font Awesome traffic comes from somewhere other than Font Awesome's own CDN."
  - Decision: **A** · v3: "most Font Awesome traffic, 85% of it, doesn't come from Font Awesome's own CDN" (4,327,761 vs 750,172 desktop)
- **1.6.4** · `N` · "Every other commercial host is noise at web scale."
  - Evidence: Next listed service is fontplus.jp at 0.069% of pages. [lane A]
  - Bulletproof: **GREEN**. "Noise" fits. Only listed services are detectable.
  - Decision: **K**

### ¶1.7 (vL58) "Weigh by font *requests* rather than pages…"

- **1.7.h** · `H` · "Request volume, and who serves what"
  - Evidence: Heading. [lane A]
  - Bulletproof: **GREEN**. Descriptive.
  - Decision: **K**
- **1.7.1** · `I` · "self-hosting and Google nearly split the pipe"
  - Evidence: 49.30% self-hosted vs 45.19% Google of desktop requests. [lane A]
  - Bulletproof: **GREEN**. "Nearly split" fits.
  - Decision: **K**
- **1.7.2** · `N` · "roughly 49% of desktop font requests are self-hosted". Prior map C041.
  - Evidence: fonts_format_file_by_service.csv: 31,080,146 / 63,045,145 = 49.30% (desktop). [lane A]
  - Bulletproof: **GREEN**. Exact.
  - Decision: **K**
- **1.7.3** · `N` · "and 45% come from Google". Prior map C042.
  - Evidence: 45.19% desktop. [lane A]
  - Bulletproof: **GREEN**. Exact.
  - Decision: **K**
- **1.7.4** · `N` · "with Adobe around 4%". Prior map C043.
  - Evidence: 4.06% desktop. [lane A]
  - Bulletproof: **GREEN**. Exact.
  - Decision: **K**
- **1.7.5** · `I` · "The divergence from page share is the hybrid pattern at work — a page pulls five families from Google while also shipping a local icon set." This is an explanatory example.
  - Evidence: No families-per-page data. Requests per font-using page: Google 4.57 vs self-hosted 3.74; slicing multiplies Google requests. [lane A]
  - Bulletproof: **RED**. A causal explanation with no evidence, and a measurable alternative (slicing) points elsewhere.
  - Suggested fix: Replace with what the data show: "Pages that use Google fetch more font files per page (4.6 vs 3.7), partly because Google splits large families into subsets."
  - Decision: **A** · v3: "on desktop, pages using Google fetch 4.6 font files from it on average, versus 3.7 from self-hosted origins, partly because Google splits large families into subsets" (28.49M/6.24M; 31.14M/8.30M)
  - Correction 2026-10-16 (weak-trace recount): **3.8** in v8 — 31,140,937/8,303,836 = 3.750; the 3.7 came from a request count (31,080,146) found in no CSV. `verification/weak-trace-2026-10-16.tsv`.

### ¶1.8 (vL60) "Google's files are almost boringly clean…"

- **1.8.1** · `N` · "about 98% of Google font requests are WOFF2". Prior map C045.
  - Evidence: Google woff2 97.93% of Google requests (desktop). [lane A]
  - Bulletproof: **GREEN**. Exact. Client unstated; add "desktop" for consistency.
  - Decision: **K** · "(desktop)" added
- **1.8.2** · `N` · "Self-hosted traffic is messier — roughly 70% WOFF2 by request". Prior map C046.
  - Evidence: self-hosted woff2 69.50% (desktop requests). [lane A]
  - Bulletproof: **GREEN**. "Roughly 70%" correct.
  - Decision: **K**
- **1.8.3** · `N` · "with WOFF around 12%". Prior map C047.
  - Evidence: woff 12.00%. [lane A]
  - Bulletproof: **GREEN**. Exact.
  - Decision: **K**
- **1.8.4** · `N` · "mislabeled `application/octet-stream` around 9%". Prior map C048.
  - Evidence: octet-stream 9.00%. The 2024 chapter traces much of it to cdnjs and Wix. [lane A]
  - Bulletproof: **GREEN**. Correct; "mislabeled" is fair (font files served with a generic type).
  - Decision: **K**
- **1.8.5** · `N` · "and raw TTF around 5%". Prior map C049.
  - Evidence: ttf 5.44%. [lane A]
  - Bulletproof: **GREEN**. "Around 5%" correct.
  - Decision: **K**
- **1.8.6** · `X` · "Same lecture as the last three years: if you self-host, you own the mistakes." Check that the prior chapters said so.
  - Evidence: 2022 L127/L846, 2024 L160–172 and 2025 L108/L166 all make the self-hosting point. [lanes A, E]
  - Bulletproof: **YELLOW**. Right point, wrong unit: there was no 2023 chapter.
  - Suggested fix: "Same lecture as the last three chapters."
  - Decision: **A** · v3: "Same lecture as the last three chapters"

### ¶1.9 (vL62) "Within each host's family-tagged traffic…"

- **1.9.1** · `M` · "Within each host's family-tagged traffic". The share of requests with a blank family name is undisclosed.
  - Evidence: fonts_family_by_service.sql has `QUALIFY rank <= 100` per client × service; shares were computed against the top-100 sum, which truncates 18.1% of parsed requests. Self-hosted blank-family share 8.3–13.1% is undisclosed. [lane A; spot-checked: Google desktop top-100 sum 22,939,931 vs ~28.5M Google requests]
  - Bulletproof: **RED**. The "within-service" shares are not shares of each host's traffic. All numbers in 1.10 inherit an upward bias.
  - Suggested fix: Either re-run the family query with per-service totals (cheap, on the materialized table; needs your OK on spend), or restate as floors/ranges against all requests of that service.
  - Decision: **D→A** · D2 re-run (fonts_family_by_service_totals.csv) with full per-service totals; v3 states the basis: desktop, share of each host's requests carrying a family name; self-hosted blank family 9.6% of parsed
- **1.9.2** · `I` · "the leaders say a great deal about what each channel is *for*"
  - Evidence: Rank order is robust even where shares are not. [lane A]
  - Bulletproof: **GREEN**. Framing.
  - Decision: **K**

### ¶1.10 (vL64–66) Family-by-service list

- **1.10.1** · `I` · "Self-hosted origins are icon-heavy."
  - Evidence: Icon families 40.4% of the self-hosted top-100 (≤33% once the truncated tail is counted). [lane A]
  - Bulletproof: **GREEN**. "Icon-heavy" holds.
  - Decision: **K**
- **1.10.2** · `N` · "Font Awesome alone is 25% of self-hosted family-tagged requests". Prior map C050.
  - Evidence: Font Awesome 4,327,761 self-hosted requests; the provable tail is ≥3.63M, so the share is ≤20.9% desktop / ≤18.9% mobile. [lane A]
  - Bulletproof: **RED**. 25% is inflated by the truncated denominator.
  - Suggested fix: "Font Awesome alone is about a fifth of self-hosted family-tagged requests" (or re-run for exact).
  - Decision: **A** · exact: Font Awesome 17.9% of self-hosted named-family requests (desktop; mobile 18.3%)
- **1.10.3** · `N` · "Poppins (7.2%), Roboto (6.9%), Open Sans, Montserrat, and Inter (4.0%) follow". This implies ranks 2–6 in that order. Prior map C196.
  - Evidence: Desktop order Poppins > Roboto > Open Sans > Montserrat > Inter is right; corrected values ≤5.9 / ≤5.7 / ≤3.3%. Mobile order has Montserrat before Open Sans. [lane A]
  - Bulletproof: **RED**. Printed percentages are inflated. The order is desktop-only.
  - Suggested fix: Drop the percentages or re-run; name the families without numbers, "(desktop)".
  - Decision: **A** · exact: Poppins 5.0, Roboto 4.9, Open Sans 3.5, Montserrat 3.3, Inter 2.8 (desktop order; mobile has Montserrat before Open Sans)
- **1.10.4** · `I` · "Self-hosting on the public web is mostly 'we vendored the icon kit and a few brand sans faces.'"
  - Evidence: Icons + the six sans faces ≤58.6% desktop / ≤52.7% mobile of self-hosted requests. [lane A]
  - Bulletproof: **YELLOW**. "Mostly" is marginal. "Brand sans faces" are actually Google's OFL families, vendored.
  - Suggested fix: "Self-hosting on the public web is largely 'we vendored the icon kit and a few Google sans faces.'"
  - Decision: **A** · v3: "largely 'we vendored the icon kit and a few Google sans faces.'"
- **1.10.5** · `I` · "Google's head is global."
  - Evidence: Noto Sans JP #1 by requests; by pages Roboto is ~18–23× larger. [lane A]
  - Bulletproof: **YELLOW**. "Global head" is a request-count artifact of slicing.
  - Suggested fix: Tie to the slicing explanation (see 0.4.2).
  - Decision: **A** · v3: "Google's head is global — by requests."
- **1.10.6** · `N` · "Noto Sans JP is 19.1% of Google's family-tagged requests". Prior map C051. Unicode-range slicing may inflate request counts for CJK families.
  - Evidence: Noto Sans JP 4,371,509 desktop Google requests / top-100 sum 22,939,931 = 19.06%; / all Google requests (~28.5M) = 15.3% floor. Estimated true within-parsed share ~16–17% desktop, ~15% mobile. [lane A; spot-checked]
  - Bulletproof: **RED**. 19.1% is an upper bound, not the share.
  - Suggested fix: "roughly one in six Google font requests in the crawl (desktop)" or re-run for the exact share.
  - Decision: **A** · exact: Noto Sans JP 17.5% of Google named-family requests (desktop; mobile 15.3%); reaches 1.4% of pages vs Roboto 20.7%; ~26.8 requests per page
- **1.10.7** · `I` · "nearly a fifth of the world's largest font CDN is one Japanese family". The data measures a share of crawl requests, not of the CDN's own traffic.
  - Evidence: ≤~17% of Google crawl requests; slice-inflated; measured over crawl requests, not the CDN's own traffic. [lane A]
  - Bulletproof: **RED**. Wrong value ("nearly a fifth") and wrong scope ("the world's largest font CDN").
  - Suggested fix: "roughly one in six of the Google Fonts requests in this crawl is a slice of one Japanese family."
  - Decision: **A** · "world's largest font CDN" phrasing removed; scoped "in the crawl"
- **1.10.8** · `N` · "followed by Roboto (14.8%), Poppins (9.3%), Open Sans, Montserrat, Lato, and Noto Serif JP". Prior map C052, C197.
  - Evidence: Ranks 2–7 match on both clients; Roboto ≥11.9%, Poppins ~7.5% (floors). [lane A]
  - Bulletproof: **YELLOW**. Order right, printed percentages are upper bounds.
  - Suggested fix: Drop the percentages or re-run.
  - Decision: **A** · exact: Roboto 13.6, Poppins 8.5; Open Sans, Montserrat, Lato, Noto Serif JP unnumbered
- **1.10.9** · `I` · "CJK is not a footnote on Google Fonts; it is a co-headliner."
  - Evidence: CJK families ≥28.7% of Google requests; Noto Sans JP on ~1.2% of pages. [lane A]
  - Bulletproof: **YELLOW**. "Co-headliner" holds by requests, not by reach.
  - Suggested fix: "CJK is a co-headliner on Google Fonts by request volume."
  - Decision: **A** · v3: "By requests, CJK is a co-headliner on Google Fonts; by reach, it is a specialist." CJK families ≈32.7% desktop / 29.2% mobile of Google named-family requests (top-100 families, pattern-classified; a floor)
- **1.10.10** · `I` · "Adobe is a premium head with a long tail"
  - Evidence: Rank-100 Adobe family has 3,358 requests; tail ≈0.72M. [lane A]
  - Bulletproof: **GREEN**. "Long tail" holds.
  - Decision: **K**
- **1.10.11** · `N` · "Proxima Nova alone is about 26% of Adobe's tagged requests". Prior map C053.
  - Evidence: Proxima Nova 457,617 requests; floor 17.9% of all Adobe requests; ≈18.5% at Adobe's ~97% parse rate. [lane A]
  - Bulletproof: **RED**. 26% is inflated by the top-100 denominator.
  - Suggested fix: "Proxima Nova alone is almost a fifth of Adobe's requests."
  - Decision: **A** · exact: Proxima Nova 18.3% (desktop; mobile 17.7%)
- **1.10.12** · `N` · "then Futura PT (11%) and a scatter of licensed classics". Prior map C198.
  - Evidence: Futura PT Web floor 7.5%, estimate ≈7.8%. [lane A]
  - Bulletproof: **RED**. 11% inflated.
  - Suggested fix: "then Futura PT (about 8%)."
  - Decision: **A** · exact: Futura PT Web 7.7%

### ¶1.11 (vL68) Correction note

- **1.11.1** · `M` · "(An earlier draft of this analysis reported these family shares against all font requests rather than within each service, understating the leaders by factors of two to thirty — the corrected within-service figures above are the meaningful ones.)" Prior map C199. This is a note about an unpublished draft.
  - Evidence: As computed the ratios are 2.4× / 3.2× / 31.4× (mobile Adobe 39.6×), but the "corrected" figures are themselves inflated (1.9.1). [lane A]
  - Bulletproof: **RED**. A note about an unpublished draft, whose numbers are wrong anyway.
  - Suggested fix: Cut the parenthetical entirely.
  - Decision: **C** · cut (note about an unpublished draft)

---

## 2 · Packaging (vL72–117)

- **2.0.h** · `H` · "Packaging: WOFF2 keeps winning; the long tail still bites"
  - Evidence: WOFF2 unique-URL share 59.5 → 65.0 → 68.5%; desktop p99 854 KiB. [lane B]
  - Bulletproof: **GREEN**. Both halves hold.
  - Decision: **K**

### ¶2.1 (vL76) "On the unique-URL series (the chapter convention):"

- **2.1.h** · `H` · "Formats"
  - Evidence: Label. [lane B]
  - Bulletproof: **GREEN**. —
  - Decision: **K**
- **2.1.1** · `M` · "On the unique-URL series (the chapter convention)". See 0.7.3.
  - Evidence: See 0.7.3. [lanes B, E]
  - Bulletproof: **YELLOW**. "The chapter convention" leans on the same false premise.
  - Suggested fix: "On the distinct-URL series:"
  - Decision: **A** · v3: "On the distinct-URL series:" (consistent with 0.7.3)

### ¶2.2 (vL78–83) Format table (distinct font URLs, desktop; 2024 / 2025 / 2026)

- **2.2.1** · `T` · WOFF2: 59.5% / 65.0% / 68.5%. Prior map C055.
  - Evidence: WOFF2 12,445,367/20,915,237 = 59.50% (2024); 15,086,270/23,195,141 = 65.04% (2025); 15,547,224/22,701,662 = 68.48% (2026). SQL identical 2024–26. [lane B]
  - Bulletproof: **GREEN**. Exact and comparable.
  - Decision: **K**
- **2.2.2** · `T` · WOFF: 19.8% / 16.0% / 13.7%. Prior map C056.
  - Evidence: WOFF 19.80 / 15.97 / 13.68%. [lane B]
  - Bulletproof: **GREEN**. Exact.
  - Decision: **K**
- **2.2.3** · `T` · TTF: 6.9% / 6.7% / 6.6%. Prior map C057.
  - Evidence: TTF 6.94 / 6.67 / 6.64%. [lane B]
  - Bulletproof: **GREEN**. Exact.
  - Decision: **K**
- **2.2.4** · `T` · octet-stream: 7.5% / 6.7% / 5.9%. Prior map C058.
  - Evidence: 2025 octet-stream 1,542,382 / 23,195,141 = 6.6496%. [lane B]
  - Bulletproof: **RED**. Double-rounding error: 6.6, not 6.7 (the multi-year builder rounds to 4 decimals first).
  - Suggested fix: 7.5 / 6.6 / 5.9.
  - Decision: **A** · v3: 2025 octet-stream 6.6 (was 6.7, double rounding); chart_formats.csv patched to 0.066496 from raw counts (backup .bak-2026-10-01); F6 re-rendered

### ¶2.3 (vL85) "Mobile tracks desktop almost exactly…"

- **2.3.1** · `N` · "Mobile tracks desktop almost exactly." Prior map C059.
  - Evidence: Mobile within 0.18 pp of desktop on all four formats. [lane B]
  - Bulletproof: **GREEN**. "Almost exactly" is right.
  - Decision: **K**
- **2.3.2** · `T` · "WOFF2 gained three to four points of unique-URL share for the second straight year". Prior map C060. The table itself shows +5.5 for 2024→2025 and +3.5 for 2025→2026.
  - Evidence: WOFF2 unique-URL gains: desktop +5.54 (2024→25) then +3.44 (2025→26); mobile +5.42, +3.26. [lane B]
  - Bulletproof: **RED**. Only this year's gain was three to four points; last year's was five and a half.
  - Suggested fix: "WOFF2 gained another three and a half points of unique-URL share, after five and a half the year before."
  - Decision: **A** · v3: "WOFF2 gained another three and a half points of unique-URL share, after five and a half the year before"
- **2.3.3** · `T` · "WOFF keeps giving ground"
  - Evidence: WOFF URL share 19.8 → 16.0 → 13.7%; request share 8.1 → 7.1 → 6.1%. [lane B]
  - Bulletproof: **GREEN**. Holds on both series.
  - Decision: **K**
- **2.3.4** · `T` · "TTF is stubbornly flat"
  - Evidence: TTF 6.94 → 6.67 → 6.64%. [lane B]
  - Bulletproof: **GREEN**. "Stubbornly flat" is right.
  - Decision: **K**
- **2.3.5** · `T` · "misconfigured MIME types improved only slightly"
  - Evidence: octet-stream 7.49 → 6.65 → 5.92%. [lane B]
  - Bulletproof: **GREEN**. "Only slightly" is fair.
  - Decision: **K**
- **2.3.6** · `N` · "and remain almost entirely a self-hosting phenomenon"
  - Evidence: "Self-hosted" = 99.78% of octet-stream requests and 99.99% of octet-stream URLs, but "self-hosted" is SERVICE()'s catch-all bucket, including generic CDNs. The 2024 chapter traces much of it to cdnjs and Wix. [lane B]
  - Bulletproof: **YELLOW**. The finding is right; the label overstates "self".
  - Suggested fix: "…remain almost entirely a problem outside the font services."
  - Decision: **A** · v3: "almost entirely a problem outside the font services"

### ¶2.4 (vL87) "By request volume, WOFF2's arc is longer and higher…"

- **2.4.1** · `T` · "73.9% (2019) → 78.4% (2022) → 82.4% (2025) → 83.7% (2026) on desktop". Prior map C062. Check comparability across years.
  - Evidence: Request share 73.86 / 78.42 / 82.35 / 83.71%, same MIME/extension formula each year. 2022 is a June crawl. [lane B]
  - Bulletproof: **GREEN**. Comparable series. Note the crawl month in the F5 caption.
  - Decision: **K** · F5 caption must not say "July" for 2020 (Aug) / 2022 (June)
- **2.4.2** · `I` · "because high-traffic hosts amplify the modern format"
  - Evidence: Google: 27.9M WOFF2 requests from 132,592 URLs; self-hosted: 21.6M from 15.25M URLs. [lane B]
  - Bulletproof: **GREEN**. Amplification by high-traffic hosts is directly shown.
  - Decision: **K**
- **2.4.3** · `I` · "Both series are true; they answer different questions."
  - Evidence: — [lane B]
  - Bulletproof: **GREEN**. Accurate framing.
  - Decision: **K**

### ¶2.5 (vL92) "Inside the files, outline technology is even more settled…"

- **2.5.1** · `N` · "TrueType `glyf` outlines in 92–93% of parsed fonts". Prior map C063.
  - Evidence: glyf 92.08% desktop / 92.82% mobile of distinct parsed font URLs. [lane B]
  - Bulletproof: **GREEN**. Exact.
  - Decision: **K**
- **2.5.2** · `N` · "PostScript CFF at 7–8%". Prior map C064.
  - Evidence: CFF 7.88% / 7.14%. [lane B]
  - Bulletproof: **GREEN**. Exact.
  - Decision: **K**
- **2.5.3** · `N` · "CFF2 and SVG outlines rounding errors". Prior map C064.
  - Evidence: CFF2 0.04%, SVG 0.02%. [lanes B, E]
  - Bulletproof: **YELLOW**. SVG is the OpenType color-glyph table, not an outline format.
  - Suggested fix: "CFF2 and SVG-table glyphs are rounding errors."
  - Decision: **A** · v3: "CFF2 and SVG-table glyphs rounding errors"
- **2.5.4** · `I` · "outline technology is even more settled"
  - Evidence: glyf 90.5% (2022) → 91.5% (2024) → 92.1% (2026). [lane B]
  - Bulletproof: **GREEN**. "Even more settled" holds.
  - Decision: **K**

### ¶2.6 (vL96–101) Size-percentile table (font transfer size)

- **2.6.h** · `H` · "Sizes: calm middle, vicious tail"
  - Evidence: p50 34.5 KiB vs p99 854 KiB. [lane B]
  - Bulletproof: **GREEN**. Holds.
  - Decision: **K**
- **2.6.1** · `N` · p50: 34.5 KB desktop / 35.3 KB mobile. Prior map C066.
  - Evidence: fonts_size.csv p50 35,328 B = 34.5 KiB desktop; 36,184 B = 35.3 KiB mobile. [lane B]
  - Bulletproof: **GREEN**. Exact (KiB).
  - Decision: **A** · units → SI kB (ruling 2026-10-01): p50 35.3 / 36.2 kB
- **2.6.2** · `N` · p75: 75.4 KB / 75.4 KB. Prior map C067.
  - Evidence: p75 77,160 B = 75.4 KiB. [lane B]
  - Bulletproof: **GREEN**. Exact.
  - Decision: **A** · p75 77.2 kB both clients
- **2.6.3** · `N` · p90: 122 KB / 117 KB. Prior map C068.
  - Evidence: p90 125,324 B = 122 KiB; 119,637 B = 117 KiB. [lane B]
  - Bulletproof: **GREEN**. Exact.
  - Decision: **A** · p90 125.3 / 119.6 kB
- **2.6.4** · `N` · p99: 854 KB / 680 KB. Prior map C069.
  - Evidence: p99 874,708 B = 854 KiB; 696,072 B = 680 KiB. [lane B]
  - Bulletproof: **GREEN**. Exact.
  - Decision: **A** · p99 874.7 / 696.1 kB
- **2.6.5** · `M` · Unstated: is the size distribution per request or per distinct file? Is KB 1000 or 1024 bytes?
  - Evidence: Per distinct parsed font URL, using respBodySize; "KB" = KiB (÷1024). [lane B]
  - Bulletproof: **YELLOW**. "Font transfer size" is imprecise, and the unit and per-file basis go unstated.
  - Suggested fix: Header: "Font file size, per distinct font URL (KiB)."
  - Decision: **A** · v3 header: "font file size, per distinct font file"; units kB; F9 relabeled (denominator files, kB) and re-rendered

### ¶2.7 (vL103) "The median has held in the mid-30s KB for years…"

- **2.7.1** · `T` · "The median has held in the mid-30s KB for years". Prior map C070 (prior-year).
  - Evidence: Comparable desktop medians: 38.7 KiB (2024) → 35.4 (2025) → 34.5 (2026); 2022 was per-request, so it isn't comparable. [lane B]
  - Bulletproof: **YELLOW**. The median is falling, not holding, and "for years" rests on three comparable points.
  - Suggested fix: "The median has drifted down, from about 39 KiB in 2024 to 34.5 KiB now."
  - Decision: **A** · v3: "The median has drifted down, from about 40 kB in 2024 to 35 kB now" (comparable p50: 39.6 → 36.2 → 35.3 kB)
- **2.7.2** · `N` · "three-quarters of files stay under ~75 KB"
  - Evidence: p75 = 75.4 KiB, per distinct file. [lane B]
  - Bulletproof: **GREEN**. "Three-quarters of files" is the right unit.
  - Decision: **A** · v3: "three-quarters of files stay under ~77 kB"
- **2.7.3** · `N` · "The 99th percentile is another world — nearly a megabyte on desktop"
  - Evidence: 854 KiB = 0.87 MB; p99 rising 637 → 758 → 854 KiB. [lane B]
  - Bulletproof: **GREEN**. "Nearly a megabyte" is fair; the rising p99 is worth adding.
  - Decision: **A** · v3: "nearly 0.9 MB on desktop"
- **2.7.4** · `N` · "WOFF2's median transfer is ~31 KB". Prior map C072.
  - Evidence: WOFF2 median 31,548 B = 30.8 KiB. [lane B]
  - Bulletproof: **GREEN**. "~31" right.
  - Decision: **A** · v3: "~31.5 kB"
- **2.7.5** · `N` · "raw TTF's is ~58 KB". Prior map C073.
  - Evidence: TTF median 59,545 B = 58.1 KiB. [lane B]
  - Bulletproof: **GREEN**. "~58" right.
  - Decision: **A** · v3: "~59.5 kB"
- **2.7.6** · `N` · "Google's median WOFF2 (~17 KB) is half the size of self-hosted WOFF2 (~32 KB)". Prior map C074, C075.
  - Evidence: Google WOFF2 median 17,468 B (17.1 KiB); self-hosted 32,212 B (31.5 KiB; "32" is the SI value); ratio 0.54. [lane B]
  - Bulletproof: **YELLOW**. The comparison holds; the units mix KiB and kB.
  - Suggested fix: "(~17 KiB) … (~31 KiB)."
  - Decision: **A** · v3: "Google's median WOFF2 (~17.5 kB) is about half the size of self-hosted WOFF2 (~32.2 kB)"
- **2.7.7** · `I` · "which is what aggressive subsetting looks like in a table"
  - Evidence: The size gap is real; no query isolates subsetting. [lane B]
  - Bulletproof: **YELLOW**. Causal claim a step beyond the data (plausible given Google's slicing).
  - Suggested fix: "which is consistent with aggressive subsetting."
  - Decision: **A** · v3: "which is consistent with aggressive subsetting"
- **2.7.8** · `I` · "typical fonts are fine; pathological fonts are still catastrophic"
  - Evidence: p50 34.5 vs p99 854 KiB, p99 growing. [lane B]
  - Bulletproof: **GREEN**. Fair characterization.
  - Decision: **K**
- **2.7.9** · `I` · "pathology clusters in CJK faces, unsubsetted families, and sloppy self-host pipelines". Check whether any data identifies what the p99 files are.
  - Evidence: Self-hosted non-WOFF2 p99 1–4.7 MB by format. Adobe-hosted `opentype`-MIME files have p25 921 KB, above the overall p99, and make up ≥27% of the desktop p99 tail. CJK and "unsubsetted" are unmeasured (fonts_size_by_country.csv is empty; no size-by-script query). Google's Material Symbols is an uncut ~4 MB WOFF2. [lanes B, E]
  - Bulletproof: **RED**. Two of the three named causes are unmeasured, and a measured major contributor (Adobe) is omitted.
  - Suggested fix: "…and the tail is dominated by self-hosted non-WOFF2 files and, surprisingly, Adobe-served OpenType files." Drop CJK unless measured.
  - Decision: **A** · v3: "the measured tail is dominated by self-hosted non-WOFF2 files and, unexpectedly, Adobe-served OpenType files: 71,000 of them, with a median of 1.6 MB, make up more than a quarter of the heaviest 1%" (fonts_size_by_service.csv: Adobe opentype n=71,316, p25 921,491 B > overall p99 874,708 B)

### ¶2.8 (vL109) "`unicode-range` — the CSS descriptor that splits a family…"

- **2.8.h** · `H` · "Subsetting: mostly inherited, rarely authored"
  - Evidence: 61% of unicode-range pages inherit it from Google only; non-Google unicode-range on 24.1% of all pages (39% of unicode-range pages). [lane B]
  - Bulletproof: **YELLOW**. "Mostly inherited" holds; "rarely authored" does not.
  - Suggested fix: "Subsetting: mostly inherited."
  - Decision: **A** · v3: "Subsetting: mostly inherited"
- **2.8.1** · `X` · "`unicode-range` — the CSS descriptor that splits a family into script- or block-specific subsets so browsers fetch only what a page needs"
  - Evidence: CSS Fonts 4 §4.5: the descriptor declares a face's character coverage, which browsers use as a download hint. Google's CJK slices are frequency-based, not by Unicode block. [lane E]
  - Bulletproof: **YELLOW**. Mostly right; "splits" misattributes the splitting to the descriptor.
  - Suggested fix: "the CSS descriptor that tells the browser which characters each pre-split font file covers, so it fetches only what a page needs."
  - Decision: **A** · v3: "the CSS descriptor that tells the browser which characters each pre-split font file covers, so it fetches only what a page needs"
- **2.8.2** · `N` · "appears in the CSS of 61.9% of desktop pages (61.7% mobile)". Prior map C076.
  - Evidence: 7,191,956 / 11,628,567 = 61.847% desktop; mobile 61.7%. [lane B]
  - Bulletproof: **RED**. Rounds to 61.8, not 61.9.
  - Suggested fix: 61.8%.
  - Decision: **A** · D5-corrected: 63.5% desktop / 63.4% mobile (published 61.8 + gate delta 1.65)
- **2.8.3** · `T` · "up from 53–56% when it was measured in 2019". Prior map C200. Still open: check against the 2019 chapter.
  - Evidence: 2019 query 06_14.sql, all-pages denominator: 52.9% desktop / 56.0% mobile. 2020 measured 37–38% with a different query that double-counts pages. 2026 comes from the new pipeline (the direction holds as a floor). [lanes B, E]
  - Bulletproof: **YELLOW**. The number is right; the comparison needs scoping.
  - Suggested fix: "up from 53–56% of pages in 2019, the last comparable measurement."
  - Decision: **A** · v3: "up from 53–56% of pages in 2019, the last comparable measurement"
- **2.8.4** · `I` · "At face value that says range-based subsetting is default craft."
  - Evidence: Rhetorical setup. [lane B]
  - Bulletproof: **GREEN**. —
  - Decision: **K**

### ¶2.9 (vL111) "Attribution says otherwise."

- **2.9.1** · `N` · "37.7% of all pages get their `unicode-range` rules solely from Google Fonts' generated CSS". Prior map C201.
  - Evidence: google_css_only 4,388,804 = 37.74% of all root pages (desktop). [lane B]
  - Bulletproof: **GREEN**. Exact. A floor: Google CSS that is inlined or self-hosted counts as first-party.
  - Decision: **A** · D5-corrected: 38.2% (37.7 + 0.43)
- **2.9.2** · `I` · "subsetting they inherited by pasting a `<link>` tag, not subsetting they wrote"
  - Evidence: Follows from the host definition. [lane B]
  - Bulletproof: **GREEN**. Fair.
  - Decision: **K**
- **2.9.3** · `N` · "Author-side usage — any `unicode-range` in non-Google CSS — covers 24.1% of pages". Prior map C202. "Non-Google" includes other third-party CSS.
  - Evidence: 24.11% = first-party 10.25% + other third-party 14.84% (overlap ~114k pages). "Other third-party" has no host breakdown and could include Bunny Fonts, jsDelivr/Fontsource, cdnjs and Typekit generated CSS. [lane B]
  - Bulletproof: **YELLOW**. "Author-side" is not established; much of it may be other services' generated CSS.
  - Suggested fix: "Any `unicode-range` in non-Google CSS covers 24.1% of pages; first-party stylesheets alone, 10.3%."
  - Decision: **A** · v3: "Any unicode-range in non-Google CSS covers 26.3% of pages" ("author-side" dropped)
- **2.9.4** · `N` · "and first-party stylesheets proper just 10.3%". Prior map C203.
  - Evidence: 10.25%, exact-host floor. [lane B]
  - Bulletproof: **GREEN**. Exact.
  - Decision: **A** · D5-corrected first-party 11.6%
- **2.9.5** · `N` · "Roughly three of every five pages that 'use' the web's main subsetting primitive are actually using Google's automation of it". Prior map C204.
  - Evidence: 4,388,804 / 7,191,956 = 61.0%. [lane B]
  - Bulletproof: **GREEN**. "Three of every five" right.
  - Decision: **K** · ~60% of unicode-range pages Google-only after correction

### ¶2.10 (vL113) "That reframing matters for the scale story later…"

- **2.10.1** · `I` · "the technique that makes giant fonts practical exists, is proven, and is overwhelmingly deployed *by one infrastructure provider on authors' behalf*"
  - Evidence: Google-only 61%, any Google 76.5% of unicode-range pages. [lane B]
  - Bulletproof: **YELLOW**. "Overwhelmingly" overstates 61–77%.
  - Suggested fix: "mostly deployed by one infrastructure provider on authors' behalf."
  - Decision: **A** · v3: "mostly deployed"

### ¶2.11 (vL117) "First report for this series…"

- **2.11.h** · `H` · "Metric overrides: a quiet CLS toolkit"
  - Evidence: Label. [lane B]
  - Bulletproof: **GREEN**. —
  - Decision: **K**
- **2.11.1** · `X` · "First report for this series". Check that no earlier chapter reported these descriptors.
  - Evidence: The 2022 chapter (L314–328) reported all four descriptors (ascent-override 0.11% / 0.20%, size-adjust 0.05% / 0.13%); the 2024 and 2025 sheets measured them. Desktop size-adjust: 0.05% (2022) → 1.04% → 1.81% → 2.86% (2026). [lanes B, E; spot-checked]
  - Bulletproof: **RED**. False: not the first report. The real story is a ~50× rise since 2022.
  - Suggested fix: "First measured here in 2022 at a fraction of a percent, the descriptors … now each appear on about 3% of pages."
  - Decision: **A** · v3: "First measured in this series in 2022 at a fraction of a percent … roughly fifty times more" (2022 chapter L314–328; desktop size-adjust 0.05 → 1.04 → 1.81 → 2.86%); 2026 value TK after D5
- **2.11.2** · `X` · "the `@font-face` descriptors that reshape a fallback font to match the web font's metrics"
  - Evidence: CSS Fonts 4 example: "override the metrics of a local fallback font … reduces layout shifting." [lane E]
  - Bulletproof: **YELLOW**. Mostly right; "reshape" is loose.
  - Suggested fix: "resize and re-space a fallback font to match the web font's metrics."
  - Decision: **A** · v3: "resize and re-space a fallback font"
- **2.11.3** · `N` · "`size-adjust`, `ascent-override`, `descent-override`, `line-gap-override` — each appear on about 2.8–3.0% of pages". Prior map C077.
  - Evidence: Desktop 2.71–2.86%, mobile 2.76–2.96%. [lane B]
  - Bulletproof: **YELLOW**. The range is 2.7–3.0, not 2.8–3.0.
  - Suggested fix: "about 3% of pages (2.7–3.0%)."
  - Decision: **A** · D5-corrected: each descriptor 2.8–3.0% desktop → "about 3%"
- **2.11.4** · `I` · "a coherent, deliberate technique aimed squarely at layout shift". Is this deliberate authoring or framework output (for example next/font)?
  - Evidence: The four descriptor counts sit within 5.2% of each other; an "Inter Fallback" family appears on 61,218 pages. Next.js next/font (`adjustFontFallback`, on by default), Nuxt Fontaine and Astro emit all four automatically. [lanes B, E]
  - Bulletproof: **RED**. "Deliberate technique" is unsupported; the evidence points to framework defaults.
  - Suggested fix: "a coherent technique aimed at layout shift, which mostly arrives by default through frameworks such as Next.js."
  - Decision: **A** · v3: "It is a coherent technique aimed squarely at layout shift, and it mostly arrives by default through frameworks such as Next.js."
- **2.11.5** · `I` · "worth tracking from here on"
  - Evidence: Tracked since 2022. [lane B]
  - Bulletproof: **YELLOW**. "From here on" implies a new series.
  - Suggested fix: Fold into the 2.11.1 fix.
  - Decision: **C** · "worth tracking from here on" folded into the 2022→2026 rise

---

## 3 · Loading (vL121–156)

- **3.0.h** · `H` · "Loading: swap wins harder; preload finally grows". "Finally" conflicts with 3.2.3, "preload rose every measured year".
  - Evidence: Preload 9.80 → 9.73 → 10.97 → 12.04 → 14.70% (desktop 2022–26). [lane B]
  - Bulletproof: **YELLOW**. "Finally" is wrong; preload has grown since 2023. The news is that preload overtook dns-prefetch.
  - Suggested fix: "Loading: swap wins harder; preload passes dns-prefetch."
  - Decision: **A** · v3: "Loading: swap wins harder; preload passes dns-prefetch"

### ¶3.1 (vL125–130) Resource-hint table (desktop pages; 2022 / 2025 / 2026)

- **3.1.h** · `H` · "Resource hints"
  - Evidence: Label. [lane B]
  - Bulletproof: **GREEN**. —
  - Decision: **K**
- **3.1.1** · `T` · `preconnect`: 11.2% / 18.3% / 20.3%. Prior map C081.
  - Evidence: 2025 preconnect 2,217,946 / 12,154,967 = 18.247%. F7 already shows 18.2. [lane B]
  - Bulletproof: **RED**. Double-rounding error.
  - Suggested fix: 11.2 / 18.2 / 20.3.
  - Decision: **A** · v3 table: 2025 preconnect 18.2 (raw 2,217,946/12,154,967); chart_resource_hints.csv patched; F7 re-rendered
- **3.1.2** · `T` · `preload`: 9.8% / 12.0% / 14.7%. Prior map C082.
  - Evidence: preload 9.80 / 12.04 / 14.70%. [lane B]
  - Bulletproof: **GREEN**. Exact.
  - Decision: **K**
- **3.1.3** · `T` · `dns-prefetch`: 17.9% / 14.6% / 13.6%. Prior map C083.
  - Evidence: 2022 dns-prefetch 1,303,500 / 7,302,838 = 17.849%. F7 shows 17.8. [lane B]
  - Bulletproof: **RED**. Double-rounding error.
  - Suggested fix: 17.8 / 14.6 / 13.6.
  - Decision: **A** · v3 table: 2022 dns-prefetch 17.8 (raw 1,303,500/7,302,838); CSV patched
- **3.1.4** · `T` · `prefetch`: 0.06% / 0.6% / 0.7%. Prior map C084.
  - Evidence: prefetch 0.059 / 0.636 / 0.696%. [lane B]
  - Bulletproof: **GREEN**. Right at the printed precision.
  - Decision: **K**
- **3.1.5** · `M` · Unstated: are these hints to font hosts or for font resources only, or every hint on the page? The 2024 column is omitted even though F7 has 2024 data.
  - Evidence: Counts only font-related hints (font URL, as=font, or a known font host), over all root pages. The 2022 column is a re-run using the narrower 2024 definition and differs from the 2022 chapter's printed 30/21/16%. [lane B]
  - Bulletproof: **YELLOW**. Definition unstated; 2022 values disagree with the published 2022 chapter.
  - Suggested fix: Title "Font-related resource hints"; footnote the 2022 re-run.
  - Decision: **A** · v3: table titled "Font-related hint"; note on the definition and the 2022 re-run

### ¶3.2 (vL132) "The hierarchy of intent is stable…"

- **3.2.1** · `I` · "The hierarchy of intent is stable: open the connection early, fetch critical faces early, stop relying on DNS-only hints." In 2022, dns-prefetch ranked first.
  - Evidence: 2022: dns-prefetch 17.8% ranked first. Preconnect overtook it in 2023; preload passed it in 2026. [lane B]
  - Bulletproof: **RED**. The ranking changed twice; "stable" is false.
  - Suggested fix: "The order of intent has flipped since 2022: preconnect now leads, preload has overtaken dns-prefetch, and DNS-only hints keep fading."
  - Decision: **A** · v3: "The order of intent has flipped since 2022: preconnect now leads, preload has overtaken dns-prefetch, and DNS-only hints keep fading."
- **3.2.2** · `T` · "Preconnect has nearly doubled since 2022". Prior map C087.
  - Evidence: 20.28 / 11.23 = 1.81×. [lane B]
  - Bulletproof: **GREEN**. "Nearly doubled" holds.
  - Decision: **K**
- **3.2.3** · `T` · "preload rose every measured year"
  - Evidence: Preload fell 2022→2023: desktop 9.80 → 9.73, mobile 9.76 → 9.58. [lane B; spot-checked]
  - Bulletproof: **RED**. False: it has risen every year since 2023, not every measured year.
  - Suggested fix: "preload has risen every year since 2023."
  - Decision: **A** · v3: "preload has risen every year since 2023"
- **3.2.4** · `T` · "dns-prefetch continues its slow fade"
  - Evidence: dns-prefetch 17.85 → 16.00 → 15.43 → 14.57 → 13.64%. [lane B]
  - Bulletproof: **GREEN**. A slow fade, as stated.
  - Decision: **K** · folded into "DNS-only hints keep fading"

### ¶3.3 (vL138–144) font-display table (desktop pages; 2022 / 2025 / 2026)

- **3.3.h** · `H` · "font-display"
  - Evidence: Label. [lane B]
  - Bulletproof: **GREEN**. —
  - Decision: **K**
- **3.3.1** · `T` · `swap`: 31.8% / 49.6% / 52.6%. Prior map C088.
  - Evidence: 2025 swap 6,022,669 / 12,155,048 = 49.549%. [lane B]
  - Bulletproof: **RED**. Double-rounding: 49.5, not 49.6.
  - Suggested fix: 31.8 / 49.5 / 52.6.
  - Decision: **A** · D5-corrected swap 55.7% (2026); 2025 49.5
- **3.3.2** · `T` · `block`: 16.2% / 24.7% / 20.9%. Prior map C089.
  - Evidence: block 16.22 / 24.67 / 20.91%. [lane B]
  - Bulletproof: **GREEN**. Values exact (see 3.4.2 for the YoY problem).
  - Decision: **A** · D5-corrected block 24.5% (flat vs 24.7)
- **3.3.3** · `T` · `auto`: 9.1% / 9.1% / 7.7%. Prior map C090.
  - Evidence: auto 9.14 / 9.05 / 7.70%. [lane B]
  - Bulletproof: **GREEN**. Exact.
  - Decision: **A** · auto 8.4%
- **3.3.4** · `T` · `fallback`: 2.2% / 5.1% / 3.7%. Prior map C091.
  - Evidence: 2025 fallback 613,481 / 12,155,048 = 5.047%. [lane B]
  - Bulletproof: **RED**. Double-rounding: 5.0, not 5.1.
  - Suggested fix: 2.2 / 5.0 / 3.7.
  - Decision: **A** · fallback 3.9% (2025 5.0)
- **3.3.5** · `T` · `optional`: 0.3% / 0.4% / 0.4%. Prior map C092.
  - Evidence: optional 0.27 / 0.37 / 0.38%. [lane B]
  - Bulletproof: **GREEN**. Exact.
  - Decision: **K**
- **3.3.6** · `M` · Unstated: the denominator (all pages or pages with @font-face), and whether the 2026 value comes from the pruned-CSS pipeline. The latter matters because hyphens YoY was dropped for exactly that reason.
  - Evidence: Denominator is all root pages. All 2026 CSS figures come from pruned_css, whose size gate (serialized AST >350,000 B or >8,000 rules → emptied) was added after the Jul 26–27 validation and never validated. The gated count was never recorded (rows carry `_prune_skipped`, uncounted). With 2025 and 2026 SQL identical, several CSS measures dropped at once: monospace 64.0 → 46.5%, serif 47.5 → 32.6%, Font Awesome in @font-face 38.7 → 30.6%, while pages with web fonts rose. [lanes B, C, D; spot-checked the `_prune_skipped` marker]
  - Bulletproof: **RED**. Every 2026 CSS share is a lower bound of unknown margin. Increases can stand in direction; declines and "steady" claims cannot be read. This is the report's largest methodological exposure.
  - Suggested fix: DECISION: (a) count `_prune_skipped` rows on pruned_css (one BigQuery query) and state the undercount; or (b) drop every CSS decline/"steady" YoY and label CSS figures as lower bounds.
  - Decision: **D→A** · D5 full scan (pruned_css_gate_effect.csv; 17.08 TiB billed): corrected = published + pages found only in gated sheets; method stated in box and Appendix B; F8 re-rendered with corrected 2026 values

### ¶3.4 (vL146) "`swap` is more entrenched than ever…"

- **3.4.1** · `T` · "`swap` is more entrenched than ever"
  - Evidence: swap 2.2 → 10.3 → 31.8 → 44.3 → 49.5 → 52.6%. [lane B]
  - Bulletproof: **GREEN**. The rise holds even as a lower bound.
  - Decision: **A** · v3: "up six points to 55.7%"
- **3.4.2** · `T` · "`block` receded about four points from its 2025 peak". Prior map C095.
  - Evidence: block 24.67 → 20.91%; 2025 is the series maximum. [lane B]
  - Bulletproof: **RED**. The decline crosses the pipeline change, so it can't be read (3.3.6).
  - Suggested fix: Drop the YoY ("block sits around a fifth of pages") unless 3.3.6(a) clears it.
  - Decision: **A** · v3: "block held at about a quarter of pages" (the 4-point drop was the gate)
- **3.4.3** · `X` · "consistent with the earlier finding that block is largely an icon-font default rather than a body-text philosophy"
  - Evidence: 2024 chapter L383 (top ten block fonts all icon fonts); 2025 L222 (~70% of block is icon fonts). 2026: block top ten = nine icon fonts + one blank; Font Awesome on 14.7% of pages. [lanes B, E]
  - Bulletproof: **GREEN**. Accurate, with prior-chapter and 2026 support. Optional: name the chapters.
  - Decision: **K**
- **3.4.4** · `I` · "swap for text, block for icons, and say so explicitly"
  - Evidence: swap top five are text faces; block top ten are icon fonts. [lane B]
  - Bulletproof: **GREEN**. Advice grounded in the data.
  - Decision: **K**

### ¶3.5 (vL152) "`local()` sources."

- **3.5.h** · `H` · "Two first-time baselines". The subsection covers three items (local, optical sizing, and hyphens/text-wrap). Check that neither baseline was measured before.
  - Evidence: 2019 chapter (L614–623, query 06_16.sql, same definition): `local()` on 56.05% desktop / 58.66% mobile. Google Fonts stopped emitting `local()` in Nov 2020. [lanes B, E; spot-checked]
  - Bulletproof: **RED**. `local()` is not a first-time baseline; only optical sizing is.
  - Suggested fix: Retitle "A collapse and a baseline"; see 3.5.4.
  - Decision: **A** · v3: "A collapse and a baseline"
- **3.5.1** · `N` · "About 9.5% of desktop and 11.1% of mobile pages include `local()` in an `@font-face` `src` list". Prior map C096.
  - Evidence: 1,106,143 = 9.51% desktop; 1,728,515 = 11.12% mobile. [lane B]
  - Bulletproof: **GREEN**. Exact. A fall from 56–59% is far too large to be a pipeline artifact.
  - Decision: **A** · D5-corrected: 11.3% desktop / 13.0% mobile → "about 11% … and 13%"
- **3.5.2** · `X` · "Several performance guides now recommend dropping `local()`"
  - Evidence: Bram Stein (2015) argues against `local()` for web fonts; web.dev "Best practices for fonts" (2022) is silent; web.dev 2019 still demos `local()`; Chrome's 2023 CLS guidance uses `local()` deliberately for fallback faces. [lane E]
  - Bulletproof: **RED**. "Several guides now recommend dropping" isn't established, and current guidance runs partly the other way.
  - Suggested fix: "Performance writers have warned against `local()` for loading web fonts since at least 2015, while newer layout-shift guidance deliberately uses `local()` to build metric-matched fallbacks."
  - Decision: **A** · v3: "Performance writers have warned against local() for loading web fonts since at least 2015 … while newer layout-shift guidance deliberately uses it to build metric-matched fallbacks" (Stein 2015; Chrome 2023 CLS guidance)
- **3.5.3** · `X` · "locally installed fonts can differ from the web font in version and metrics, and the match fails silently when names drift"
  - Evidence: Stein 2015: installed versions differ in version, metrics and features. The harm is a successful but wrong match. [lane E]
  - Bulletproof: **YELLOW**. The mechanism is slightly misdescribed.
  - Suggested fix: "…when names match, the browser silently uses whatever version the user has installed."
  - Decision: **A** · v3: "when names match, the browser silently uses whatever version the user has installed"
- **3.5.4** · `I` · "Whether that advice is being followed cannot be answered without a baseline; now there is one."
  - Evidence: A 2019 baseline exists: 56–59% of pages. 2026: 9.5–11.1%. [lanes B, E]
  - Bulletproof: **RED**. False, and it misses the story: the advice (or Google's change) has been followed at scale.
  - Suggested fix: "It has been, at scale: `local()` fell from 56–59% of pages in 2019 to about 10%, mostly because Google Fonts stopped emitting it in late 2020; much of what remains is framework-generated fallback faces."
  - Decision: **A** · v3: "down from 56–59% in 2019, mostly because Google Fonts stopped emitting it in late 2020 … some of what remains is likely those fallback faces"

### ¶3.6 (vL154) "`font-optical-sizing`."

- **3.6.1** · `I` · "Explicit control of the optical-size axis is rare"
  - Evidence: ~0.63% of pages set any explicit value. [lane B]
  - Bulletproof: **GREEN**. "Rare" fits.
  - Decision: **K**
- **3.6.2** · `N` · "`auto` — a no-op restatement of the default — on 0.6% of pages". Prior map C103.
  - Evidence: auto on 72,092 pages = 0.62% desktop. [lane B]
  - Bulletproof: **GREEN**. Exact.
  - Decision: **A** · corrected 0.7%
- **3.6.3** · `N` · "`none`, the deliberate opt-out, on only about six hundred pages in the entire crawl". Prior map C206. Which client, or both combined?
  - Evidence: none on 620 desktop / 658 mobile pages. [lane B]
  - Bulletproof: **YELLOW**. "About six hundred pages in the entire crawl" is per client, not the whole crawl.
  - Suggested fix: "about six hundred pages on each client."
  - Decision: **A** · v3: "fewer than a thousand pages on each client" (871 desktop corrected)
- **3.6.4** · `X` · "Browsers do this work invisibly"
  - Evidence: CSS Fonts 4: `auto` "may" apply opsz; automatic opsz ships in Chrome 79+, Firefox 62+, Safari 13.1+ (MDN). [lane E]
  - Bulletproof: **YELLOW**. True for fonts that have an opsz axis.
  - Suggested fix: "Browsers do this work invisibly for fonts with an optical-size axis."
  - Decision: **A** · v3: "for fonts with an optical-size axis"
- **3.6.5** · `I` · "essentially nobody overrides them"
  - Evidence: none on 0.005% of pages. [lane B]
  - Bulletproof: **GREEN**. "Essentially nobody" holds.
  - Decision: **K**
- **3.6.6** · `N` · "a hundred-odd distinct design-system custom properties (`--heading-3-font-optical-sizing` and kin) piping the value through tokens". Prior map C207.
  - Evidence: 105 desktop / 108 mobile distinct custom property names (110 across both), clustered in a handful of design systems. [lane B]
  - Bulletproof: **GREEN**. "A hundred-odd" is right.
  - Decision: **K**
- **3.6.7** · `I` · "a small but genuine trace of variable-font fluency inside design systems, if not yet on the open web"
  - Evidence: The tokens were found on crawled public root pages. [lane B]
  - Bulletproof: **YELLOW**. "If not yet on the open web" contradicts the source.
  - Suggested fix: "…a small but genuine trace of variable-font fluency inside a handful of design systems."
  - Decision: **A** · v3: "inside a handful of design systems"

### ¶3.7 (vL156) "`hyphens: auto` appears on 6.6%…"

- **3.7.1** · `N` · "`hyphens: auto` appears on 6.6% of desktop pages in 2026". Prior map C097.
  - Evidence: 765,848 = 6.59% desktop. [lane B]
  - Bulletproof: **GREEN**. Exact.
  - Decision: **A** · D5-corrected hyphens auto 10.5% (2025 10.6) — flat; v3 restores the comparison
- **3.7.2** · `N` · "with `none` and `manual` around 3% each". Prior map C205.
  - Evidence: none 3.21%, manual 3.11%. [lane B]
  - Bulletproof: **GREEN**. Exact.
  - Decision: **A** · none 4.1%, manual 3.4% → "around 3–4% each"
- **3.7.3** · `M` · "this measurement uses a new CSS-extraction pipeline, so we do not compare it against earlier chapters"
  - Evidence: hyphens SQL is identical in 2025 and 2026, validated MATCH on the sample, and produced in the same run as every other CSS metric. [lane B]
  - Bulletproof: **RED**. The rationale is true, but it applies to all CSS metrics, not just hyphens. Singling out hyphens is inconsistent (B.1.7).
  - Suggested fix: Resolve with 3.3.6; then state the rule once for all CSS figures.
  - Decision: **A** · "new pipeline, so we do not compare" sentence removed (gate corrected)
- **3.7.4** · `T` · "`text-wrap: pretty` continues its quiet climb (~2.2%)". Prior map C100. This is a YoY claim from the same pipeline 3.7.3 disqualifies.
  - Evidence: text-wrap: pretty 1.71% (2025) → 2.24% (2026). [lane B]
  - Bulletproof: **YELLOW**. The increase can stand directionally; "continues its climb" rests on one prior year.
  - Suggested fix: "text-wrap: pretty rose to ~2.2% (from 1.7% in 2025)."
  - Decision: **A** · v3: "pretty rose to 2.8% (from 1.7%)"
- **3.7.5** · `T` · "with `balance` steady around 2.5%". Prior map C099. Also YoY.
  - Evidence: balance 2.67% → 2.46% (−8%). [lane B]
  - Bulletproof: **RED**. It slipped rather than held steady, and declines across the pipeline can't be read.
  - Suggested fix: "with `balance` around 2.5%" (no YoY claim).
  - Decision: **A** · v3: "balance more than doubled to 6.9%" (2025 2.7)

---

## 4 · The canon (vL160–199)

- **4.0.h** · `H` · "The canon: icons, five sans faces, and open licenses". The table lists six sans faces, counting Lato.
  - Evidence: Table ranks 2–8 hold six sans faces: Roboto, Open Sans, Montserrat, Poppins, Inter, Lato. [lane C]
  - Bulletproof: **RED**. "Five" is wrong.
  - Suggested fix: "The canon: icons, a handful of sans faces, and open licenses."
  - Decision: **A** · v3: "icons, a handful of sans faces, and open licenses"

### ¶4.1 (vL162) "The most common `font-family` names…"

- **4.1.1** · `I` · "The most common `font-family` names on desktop pages are not a museum of typographic diversity"
  - Evidence: styles_family.sql counts only the `font-family` descriptor inside @font-face rules. [lane C]
  - Bulletproof: **YELLOW**. These are the most-declared web font families, not the most common `font-family` names on pages.
  - Suggested fix: "The most-declared web font families (in `@font-face` rules) on desktop pages…"
  - Decision: **A** · v3: "The most-declared web font families (in @font-face rules)"

### ¶4.2 (vL164–173) CSS family table (≈ page share, desktop)

- **4.2.1** · `N` · Font Awesome 30.6%. Prior map C104.
  - Evidence: styles_family.csv desktop Font Awesome 3,554,593 / 11,628,567 = 30.57% of all root pages. [lane C]
  - Bulletproof: **GREEN**. Exact (a CSS floor; see 3.3.6).
  - Decision: **A** · D5-corrected Font Awesome 35.3%
- **4.2.2** · `N` · Roboto 21.6%. Prior map C105.
  - Evidence: Roboto 21.62%. [lane C]
  - Bulletproof: **GREEN**. Exact. The CSV duplicates the Roboto row (same count twice); the value is unaffected.
  - Decision: **K** · at least
- **4.2.3** · `N` · Open Sans 15.5%. Prior map C106.
  - Evidence: Open Sans 15.48%. [lane C]
  - Bulletproof: **GREEN**. Exact.
  - Decision: **K** · at least
- **4.2.4** · `N` · Montserrat 11.8%. Prior map C107.
  - Evidence: Montserrat 11.81%. [lane C]
  - Bulletproof: **GREEN**. Exact.
  - Decision: **K** · at least
- **4.2.5** · `N` · swiper-icons 10.9%. Prior map C108.
  - Evidence: swiper-icons 10.88%. [lane C]
  - Bulletproof: **GREEN**. Exact.
  - Decision: **K** · at least
- **4.2.6** · `N` · Poppins 10.5%. Prior map C109.
  - Evidence: Poppins 10.46%. [lane C]
  - Bulletproof: **GREEN**. Exact.
  - Decision: **K** · at least
- **4.2.7** · `N` · Inter 8.7%. Prior map C110.
  - Evidence: Inter 8.67%. [lane C]
  - Bulletproof: **GREEN**. Exact.
  - Decision: **K** · at least
- **4.2.8** · `N` · Lato 8.1%. Prior map C111.
  - Evidence: Lato 8.11%; ranks 1–8 contiguous, nothing omitted (#9 Roboto Slab 5.78%). [lane C]
  - Bulletproof: **GREEN**. Exact.
  - Decision: **K** · at least
- **4.2.9** · `M` · Unstated: what counts as "declaring" a family (the `font-family` property, the @font-face `font-family` descriptor, or both), and how Font Awesome variants are merged.
  - Evidence: @font-face descriptor only; Font Awesome variants merged by regex `(?i)font\s?awesome` after stripping weight suffixes; base = all root pages. [lane C]
  - Bulletproof: **YELLOW**. The definition is unstated in the prose.
  - Suggested fix: Say "declared in `@font-face`" in the table header.
  - Decision: **A** · header: "≈ share of pages declaring it (desktop; at least)"

### ¶4.3 (vL175) "Icon kits and Google-era UI sans faces still run the web…"

- **4.3.1** · `I` · "Icon kits and Google-era UI sans faces still run the web"
  - Evidence: Top 8 = 2 icon kits + 6 Google sans faces, by declaration share. [lane C]
  - Bulletproof: **YELLOW**. "Run the web" overstates declaration data.
  - Suggested fix: "…still dominate the web's font declarations."
  - Decision: **A** · v3: "still dominate the web's font declarations"
- **4.3.2** · `T` · "with Inter completing its climb from designer darling to default stack citizen". This needs Inter's history.
  - Evidence: Inter: 1.17% (2022, rank 50) → 3.83% (2024, #17) → 6.70% (2025, #9) → 8.67% (2026, #7). [lane C]
  - Bulletproof: **YELLOW**. The climb is real and continuing; "completing" is unsupported.
  - Suggested fix: "with Inter still climbing: from about 1% of pages in 2022 to nearly 9% today."
  - Decision: **A** · v3: "Inter still climbing: from about 1% of pages in 2022 to nearly 9% today"
- **4.3.3** · `N` · "`sans-serif` on ~81% of pages, `monospace` on ~47%, `serif` on ~33%, `system-ui` on ~12.5%". Prior map C112.
  - Evidence: styles_family_system.csv: sans-serif 80.63%, monospace 46.46%, serif 32.58%, system-ui 12.49%. [lane C]
  - Bulletproof: **RED**. monospace is ~46%, not ~47%. All four are CSS floors, and monospace dropped from 64.0% in 2025, a pipeline-suspect move.
  - Suggested fix: "~46%".
  - Decision: **A** · D5-corrected generics: sans-serif ~86, monospace ~60, serif ~40, system-ui ~14.5
- **4.3.4** · `I` · "System generics remain universal scaffolding"
  - Evidence: Only sans-serif (80.6%) is near-universal. [lane C]
  - Bulletproof: **YELLOW**. "Universal scaffolding" overstates the other three.
  - Suggested fix: "`sans-serif` remains near-universal scaffolding."
  - Decision: **A** · v3: "sans-serif remains near-universal scaffolding"

### ¶4.4 (vL179) "Where license metadata is readable…"

- **4.4.1** · `N` · "the SIL Open Font License is everywhere — roughly 70% of pages in the license query's universe touch at least one OFL face". Prior map C113. What is the universe?
  - Evidence: fonts_license.csv OFL 8,131,758 / 11,628,567 = 69.93% (mobile 70.60%); the base is all root pages. [lanes C, D]
  - Bulletproof: **YELLOW**. The number is right; "the license query's universe" misdescribes the base, and "everywhere" overstates.
  - Suggested fix: "roughly 70% of all pages load at least one OFL-licensed font."
  - Decision: **A** · v3: "roughly 70% of all pages load at least one OFL-licensed font (69.9% desktop, 70.6% mobile)"; "license query's universe" and "everywhere" removed
- **4.4.2** · `T` · "up from ~64% in 2025". Prior map C114 (prior-year).
  - Evidence: 2025 sheet OFL 63.54% desktop / 64.89% mobile; identical SQL and base. [lane C]
  - Bulletproof: **GREEN**. Comparable (font metadata, not the CSS pipeline).
  - Decision: **K**
- **4.4.3** · `N` · "Google's vendor footprint (~37%) and Font Awesome's (~27%) tower over everything else". Prior map C115, C116. What is the denominator, and what is #3?
  - Evidence: fonts_foundry: GOOG 36.85%, AWSM 27.39% of all pages; blank 17.36%; #3 named vendor `pyrs` 13.74%. common.sql maps FontForge's default vendor ID `PfEd` to Font Awesome. [lane C]
  - Bulletproof: **YELLOW**. Unit unstated; the Font Awesome figure is an upper bound.
  - Suggested fix: "fonts carrying Google's vendor ID reach ~37% of pages; Font Awesome's, up to ~27%."
  - Decision: **A** · v3: "fonts carrying Google's vendor ID reach ~37% of pages, and Font Awesome's up to ~27%, while the next named vendor reaches 13.7%" ('up to': PfEd→AWSM mapping in common.sql)
- **4.4.4** · `N` · "named designers are mostly blank fields"
  - Evidence: fonts_designer: 78.49% of all pages load at least one font with a blank designer field; top named designer Dave Gandy 10.87%. [lane C]
  - Bulletproof: **YELLOW**. The share of blank fields is not measured; the page-level fact is.
  - Suggested fix: "most pages load at least one font whose designer field is blank."
  - Decision: **A** · v3: "most pages (78%) load at least one font whose designer field is blank"
- **4.4.5** · `I` · "The commons, in other words, is not a bazaar — it is a small number of very large donors."
  - Evidence: GOOG, AWSM and OFL page shares support concentration. [lane C]
  - Bulletproof: **YELLOW**. Supported; the AWSM figure is inflated by the PfEd mapping.
  - Suggested fix: Keep; fix 4.4.3.
  - Decision: **K**

### ¶4.5 (vL183) "Among font *files* with script metadata…"

- **4.5.h** · `H` · "Scripts: Latin majority, Han almost absent"
  - Evidence: A font counts as Han only if it covers >5% of the 98,408 Han codepoints (>4,920 ideographs). Google's CJK slices hold a few hundred characters each, so they can never qualify. Only 0.34% of desktop Noto Sans JP requests classify as Han. Kana (1.5%) outranks Han (0.5%). [lanes C, D]
  - Bulletproof: **RED**. "Han almost absent" is a classifier artifact.
  - Suggested fix: "Scripts: Latin majority; Han arrives in slices."
  - Decision: **A** · v3: "Scripts: Latin majority; Han arrives in slices"
- **4.5.1** · `M` · "Among font *files* with script metadata (not pages, not people — the denominator matters nowhere more than here)". Are these distinct files or requests? What is the classification rule?
  - Evidence: Script is inferred from cmap coverage (>5% of the script's codepoints); there is no "script metadata". The base is 19,534,422 distinct parsed URLs, including unclassified ones. [lane C]
  - Bulletproof: **RED**. Misdescribes both the method and the unit.
  - Suggested fix: "Among distinct font URLs, classified by the characters they contain (a script counts when a file covers more than 5% of it)."
  - Decision: **A** · v3: "Among distinct font URLs, classified by the characters each file contains — a script counts when a file covers more than 5% of it"

### ¶4.6 (vL185–195) Script table (desktop share of fonts)

- **4.6.1** · `N` · Latin 57%. Prior map C117.
  - Evidence: fonts_script.csv Latin 57.22%. [lane C]
  - Bulletproof: **GREEN**. Exact.
  - Decision: **K**
- **4.6.2** · `N` · Private Use Area (icons) 50%. Prior map C118.
  - Evidence: PUA 49.64%; any single PUA codepoint counts; Roboto, Inter and Proxima Nova are in the PUA top 10. [lane C]
  - Bulletproof: **YELLOW**. "(icons)" overstates.
  - Suggested fix: "Private Use Area (mostly icons)".
  - Decision: **A** · row: "Private Use Area (mostly icons)"
- **4.6.3** · `N` · Cyrillic 13%. Prior map C119.
  - Evidence: Cyrillic 13.04%. [lane C]
  - Bulletproof: **GREEN**. Exact.
  - Decision: **K**
- **4.6.4** · `N` · Greek 8%. Prior map C120.
  - Evidence: Greek 8.04%. [lane C]
  - Bulletproof: **GREEN**. Exact.
  - Decision: **K**
- **4.6.5** · `N` · Emoji 2.5%. Prior map C121.
  - Evidence: Emoji 2.47%; the "Emoji" script includes digits, #, *, © and ® (qualifies at >71 codepoints). [lane C]
  - Bulletproof: **YELLOW**. These are not emoji fonts.
  - Suggested fix: "Emoji-range symbols".
  - Decision: **A** · row: "Emoji-range symbols"
- **4.6.6** · `N` · Katakana / Hiragana ~1.5% each. Prior map C122.
  - Evidence: Katakana 1.51%, Hiragana 1.48%. [lane C]
  - Bulletproof: **GREEN**. Exact.
  - Decision: **K**
- **4.6.7** · `N` · Hebrew / Devanagari ~1%. Prior map C123.
  - Evidence: Hebrew 1.24%, Devanagari 1.04%. [lane C]
  - Bulletproof: **GREEN**. Exact.
  - Decision: **K**
- **4.6.8** · `N` · Hangul / Arabic <1%. Prior map C124.
  - Evidence: Hangul 0.94%, Arabic 0.74%; only 8.98% of Noto Sans KR requests classify as Hangul. [lane C]
  - Bulletproof: **YELLOW**. Hangul is depressed by the same threshold artifact.
  - Suggested fix: Footnote with the Han fix.
  - Decision: **A** · row "Hangul (near-complete sets)* / Arabic" + footnote: only 9% of Noto Sans KR requests classify as Hangul
- **4.6.9** · `N` · Han ~0.5%. Prior map C125.
  - Evidence: Han 94,999 / 19,534,422 = 0.49% desktop (0.39% mobile). [lane C]
  - Bulletproof: **YELLOW**. The value is right only as "files with a near-complete Han set".
  - Suggested fix: Label the row "Han (near-complete sets)".
  - Decision: **A** · row: "Han (near-complete sets)", unbolded

### ¶4.7 (vL197) "Han script — the writing system of well over a billion readers…"

- **4.7.1** · `X` · "Han script — the writing system of well over a billion readers"
  - Evidence: Chinese characters used by ~1.47 billion people, second only to Latin script. [lane E]
  - Bulletproof: **GREEN**. "Well over a billion" holds.
  - Decision: **K**
- **4.7.2** · `N` · "appears in half a percent of the fonts in the global crawl mix"
  - Evidence: 0.49% = URLs covering >4,920 Han codepoints. Han characters appear in far more files (every Japanese and Chinese slice). [lane C]
  - Bulletproof: **RED**. Implies Han is rare in fonts; the opposite is true.
  - Suggested fix: "only half a percent of font files carry a near-complete Han set."
  - Decision: **A** · v3: "appears as a near-complete set in only half a percent of the font files … it does not mean Han is rare in fonts: it means Han rarely arrives whole"
- **4.7.3** · `I` · "That is not a census of the Chinese web; it is a statement about *files*"
  - Evidence: It is about files, but only complete Han files. [lane C]
  - Bulletproof: **YELLOW**. Half right.
  - Suggested fix: Fold into 4.7.2.
  - Decision: **A** · folded into 4.7.2 ("not a census of the Chinese or Japanese web")
- **4.7.4** · `I` · "full Han faces are enormous, rarely self-hosted, and served (when they are served) through centralized infrastructure that this per-file metric barely sees". Check how the script classifier treats Google's CJK slice files.
  - Evidence: Google's slices are seen but scored not-Han by the 5% threshold. [lane C]
  - Bulletproof: **RED**. The cause is misstated: the metric sees the files, but its threshold can't classify them.
  - Suggested fix: "…because Han reaches the web as hundreds of small slices, each far too partial for this per-file classifier to count."
  - Decision: **A** · v3: cause restated (>4,920 ideographs needed; Google slices carry a few hundred; <1% of Noto Sans JP requests register as Han; why Katakana outranks Han)
- **4.7.5** · `I` · "the gap between them is the strongest data hook in this report for what comes at the end"
  - Evidence: The population/file-prevalence gap is mostly the method artifact. [lane C]
  - Bulletproof: **RED**. The "strongest data hook" rests on an artifact.
  - Suggested fix: Re-anchor on request data: Japanese families are ~1/6–1/5 of Google Fonts requests, arriving ~28 slices per page.
  - Decision: **A** · v3: hook re-anchored on request data: "Japanese families alone are more than a quarter of Google Fonts' family-tagged requests in the crawl, at about 27 subset files per page that uses Noto Sans JP" (28.5% desktop, top-100 classified, floor; 4,371,509 / 163,334 = 26.8)

---

## 5 · Capability versus expression (vL203–235)

- **5.0.h** · `H` · "Capability versus expression"
  - Evidence: Heading. [lane C]
  - Bulletproof: **GREEN**. —
  - Decision: **K**

### ¶5.1 (vL207) "About 68% of parsed fonts carry GSUB/GPOS…"

- **5.1.h** · `H` · "OpenType: the files got better; authors still rarely drive"
  - Evidence: Files improved 61.7% → 67.8%; 10.5% of pages set font-feature-settings. [lane C]
  - Bulletproof: **YELLOW**. "Rarely drive" is in tension with one page in ten.
  - Suggested fix: "OpenType: the files got better; authors mostly leave it to defaults."
  - Decision: **A** · v3: "authors mostly leave it to defaults"
- **5.1.1** · `N` · "About 68% of parsed fonts carry GSUB/GPOS layout tables (67.8% desktop / 67.4% mobile)". Prior map C126. Does this mean either table or both?
  - Evidence: fonts_feature_opentype 13,243,279 / 19,534,422 = 67.79% desktop, 67.44% mobile; GSUB or GPOS; distinct URLs. [lane C]
  - Bulletproof: **GREEN**. Exact. Say "GSUB or GPOS".
  - Decision: **K**
- **5.1.2** · `T` · "up from roughly 61–62% in 2025". Prior map C127 (prior-year). Check that the denominator matches the 2025 one.
  - Evidence: 2025 sheet 61.67% / 61.50%; identical SQL and unit. [lane C]
  - Bulletproof: **GREEN**. Comparable (font metadata, not CSS).
  - Decision: **K**
- **5.1.3** · `T` · "Feature tags keep spreading"
  - Evidence: Desktop kern 44.40 → 49.84%, liga 42.94 → 44.76%, frac 32.52 → 38.40%, mark 17.29 → 21.80%. [lane C]
  - Bulletproof: **GREEN**. "Keep spreading" holds.
  - Decision: **K**
- **5.1.4** · `N` · "`kern` on ~50% of the parsed sample, `liga` ~45%, `frac` and `locl` ~38%, figure features ~22%, mark positioning ~22%". Prior map C128–C132.
  - Evidence: kern 49.84, liga 44.76, frac 38.40, locl 38.28, tnum 22.60, pnum 22.05, mark 21.80%. [lane C]
  - Bulletproof: **GREEN**. Exact. "Figure features" = tnum and pnum, each ~22%.
  - Decision: **K**

### ¶5.2 (vL209) "Authors, meanwhile, mostly trust defaults."

- **5.2.1** · `I` · "Authors, meanwhile, mostly trust defaults."
  - Evidence: 89.5% of pages set no feature settings; 92.9% no font-variant-*. [lane C]
  - Bulletproof: **GREEN**. Holds.
  - Decision: **K**
- **5.2.2** · `N` · "About 10.5% of desktop pages set any `font-feature-settings`". Prior map C133.
  - Evidence: styles_feature_control: font-feature-settings 1,217,445 / 11,628,567 = 10.47%. [lane C]
  - Bulletproof: **GREEN**. Exact (CSS floor).
  - Decision: **A** · D5-corrected 13.7%
- **5.2.3** · `T` · "(flat-to-down vs 2025)". Prior map C134 (prior-year). Pipeline comparability applies here too.
  - Evidence: 2025 11.86% desktop / 11.17% mobile → 2026 10.47%; identical SQL. [lane C]
  - Bulletproof: **RED**. −1.4 points is "down", not "flat-to-down", and declines across the pipeline change can't be read (3.3.6).
  - Suggested fix: Drop the YoY.
  - Decision: **A** · v3: "up from 11.9% in 2025" (was "flat-to-down")
- **5.2.4** · `N` · "~7% use `font-variant` properties". Prior map C135.
  - Evidence: font-variant 7.13% desktop / 6.91% mobile (longhands only). [lane C]
  - Bulletproof: **GREEN**. Exact.
  - Decision: **A** · D5-corrected ~9% (9.3)
- **5.2.5** · `T` · "(up from ~5–6%)". Prior map C136 (prior-year). Pipeline comparability applies here too.
  - Evidence: 2025 5.49% / 5.18%. [lane C]
  - Bulletproof: **GREEN**. An increase, so it holds directionally as a floor.
  - Decision: **A** · "up from ~5.5%"
- **5.2.6** · `N` · "The features people toggle by hand are the classics — `kern`, `liga`, `tnum`"
  - Evidence: Tags in font-feature-settings: kern 2.11%, liga 1.85%, tnum 0.70%, palt 0.66%. [lane C]
  - Bulletproof: **GREEN**. The three named are the top three.
  - Decision: **K**
- **5.2.7** · `N` · "`font-variant-numeric: tabular-nums` now appears on ~4.7% of pages". Prior map C141.
  - Evidence: tabular-nums 540,367 = 4.65% desktop (2025: 3.26%). [lane C]
  - Bulletproof: **GREEN**. "~4.7%" holds.
  - Decision: **A** · "at least 4.7%" (not covered by D5)
- **5.2.8** · `N` · "comfortably ahead of low-level `tnum`"
  - Evidence: 4.65% vs tnum 0.70% = 6.6× (2025: 3.5×). [lane C]
  - Bulletproof: **GREEN**. "Comfortably ahead" holds.
  - Decision: **K**
- **5.2.9** · `I` · "which is the healthy direction: the human-readable CSS is winning for numbers"
  - Evidence: The ratio is widening. [lane C]
  - Bulletproof: **GREEN**. Supported.
  - Decision: **K**

### ¶5.3 (vL211) "The gap is the story…"

- **5.3.1** · `I` · "essentially every text face users see can ligate and kern". Compare 5.1.4: kern ~50%, liga ~45%.
  - Evidence: Kern-capable (GPOS kern or legacy kern table) = 50.72% of distinct font URLs; no text-only or request-weighted cut exists. [lane C]
  - Bulletproof: **RED**. About half, not "essentially every".
  - Suggested fix: "about half the font files in the crawl can kern, and nearly as many ligate."
  - Decision: **A** · v3: "about half the font files in the crawl can kern, and nearly as many ligate" (kern-capable 50.72%, liga 44.76% of distinct URLs)
- **5.3.2** · `I` · "almost nobody hand-authors a typographic feature stylesheet". Compare 5.2.2: 10.5% of pages.
  - Evidence: 10.47% of pages set font-feature-settings; 7.13% use font-variant-*. [lane C]
  - Bulletproof: **RED**. One page in ten is not "almost nobody".
  - Suggested fix: "only about one page in ten hand-authors a typographic feature stylesheet."
  - Decision: **A** · v3: "only about one page in seven hand-authors a typographic feature stylesheet"
- **5.3.3** · `I` · "Capability ships in the files; expression waits on tooling and defaults."
  - Evidence: Capability is about half. [lane C]
  - Bulletproof: **YELLOW**. Holds once 5.3.1 is fixed.
  - Suggested fix: —
  - Decision: **K**

### ¶5.4 (vL215–221) Variable-font adoption table

- **5.4.h** · `H` · "Variable fonts: the headline — and its mechanism"
  - Evidence: The "mechanism" has no page-level support (5.7.1). [lane C]
  - Bulletproof: **YELLOW**. The heading promises more than the evidence gives.
  - Suggested fix: Depends on the 5.7 decision.
  - Decision: **K** · mechanism now measured (D3)
- **5.4.1** · `T` · 2019: 1.8% / 1.9%. Prior map C142.
  - Evidence: 2019 1.82% / 1.87% (2019 SQL counts gvar only). [lane C]
  - Bulletproof: **GREEN**. Right; the definition difference is negligible.
  - Decision: **K**
- **5.4.2** · `T` · 2022: 28.4% / 29.1%. Prior map C144.
  - Evidence: 2022 28.36% / 29.13%. [lane C]
  - Bulletproof: **GREEN**. Exact.
  - Decision: **K**
- **5.4.3** · `T` · 2024: 32.8% / 34.0%. Prior map C146.
  - Evidence: 2024 32.77% / 33.99%. [lane C]
  - Bulletproof: **GREEN**. Exact.
  - Decision: **K**
- **5.4.4** · `T` · 2025: 39.4% / 41.3%. Prior map C147.
  - Evidence: 2025 39.43% / 41.30%. [lane C]
  - Bulletproof: **GREEN**. Exact.
  - Decision: **K**
- **5.4.5** · `N` · 2026: 48.7% / 50.2%. Prior map C148.
  - Evidence: fonts_variable 5,661,443 / 11,628,567 = 48.69%; mobile 50.21%. [lane C]
  - Bulletproof: **GREEN**. Exact.
  - Decision: **K**
- **5.4.6** · `M` · The table omits 2020 and 2023 (dropped in v2; C143, C145), even though 0.3.4 and 5.5.1 lean on the 2019–2020 jump. Check whether the whole series uses one comparable definition.
  - Evidence: 2022–26 use one SQL. The table omits 2020 (10.54% / 11.00%), 2021 (12.66% / 12.85%) and 2023 (28.75% / 30.04%). The 2020 row in chart_variable_fonts.csv is client-swapped (and a September crawl). [lanes A, C; spot-checked]
  - Bulletproof: **RED**. Omitting 2021 hides the largest jump (2021→22), which the text then contradicts.
  - Suggested fix: Show the full series 2019–2026; fix the swapped 2020 row; re-render F2.
  - Decision: **A** · v3 table shows every year 2019–2026 (2020 row corrected: 10.5 / 11.0)

### ¶5.5 (vL225) "Half the web now loads variable fonts…"

- **5.5.1** · `T` · "Half the web now loads variable fonts, after a nine-point jump — as large as any in the series". Prior map C150.
  - Evidence: 2021→22: +15.70 desktop / +16.28 mobile; 2025→26: +9.26 / +8.91. [lanes A, C]
  - Bulletproof: **RED**. False; see 0.3.4.
  - Suggested fix: "after a nine-point jump, the biggest since 2022."
  - Decision: **A** · v3: "after a nine-point jump — the biggest since 2022's sixteen-point leap"
- **5.5.2** · `I` · "'half the web adopted variable fonts' and 'half the web *chose* variable fonts' are different sentences, and the data supports the first far more than the second"
  - Evidence: Support is request-side only. [lane C]
  - Bulletproof: **YELLOW**. The distinction is right; the evidence for "far more than the second" is request share, not pages.
  - Suggested fix: Keep, grounded in the fixed 5.6–5.7.
  - Decision: **K** · now backed by page-level D3

### ¶5.6 (vL227) "Look at where variable-font traffic comes from."

- **5.6.1** · `N` · "Google serves 79.4% of variable-font requests — from just 1.2% of the distinct variable-font URLs in the crawl". Prior map C159. Which client?
  - Evidence: 12,921,267 / 16,264,853 = 79.44% of VF requests; 29,019 / 2,450,960 URLs = 1.18% (desktop); mobile 79.4% / 1.1%. [lane C]
  - Bulletproof: **YELLOW**. Exact; client unstated.
  - Suggested fix: Add "(desktop)".
  - Decision: **A** · v3: "On desktop, Google serves 79.4%…" (mobile 79.4 / 1.1)
- **5.6.2** · `N` · "Self-hosting is the mirror image: 20.5% of VF requests, but 98.8% of unique variable files". Prior map C160. Distinct URLs are not distinct fonts.
  - Evidence: 20.52% of VF requests; 2,420,432 URLs = 98.75%; 1.38 requests per self-hosted URL. [lane C]
  - Bulletproof: **YELLOW**. "Unique variable files" are distinct URLs; the same font self-hosted on many origins counts many times.
  - Suggested fix: "…but 98.8% of distinct variable-font URLs."
  - Decision: **A** · v3: "98.8% of distinct variable-font URLs"
- **5.6.3** · `I` · "the long tail of experimental, branded, and bespoke variables lives on origin servers and barely moves the traffic needle"
  - Evidence: No VF-by-service-by-family query exists. The visible non-Google VFs are library or platform fonts (Inter, Geist, Pretendard, Wix Madefor). [lane C]
  - Bulletproof: **RED**. "Experimental, branded, and bespoke" is unsupported, and the visible evidence points the other way.
  - Suggested fix: "the long tail of variable files on other hosts, many of them copies of the same open-source families, barely moves the traffic needle."
  - Decision: **A** · v3: "the long tail of variable files on other hosts, many of them copies of the same open-source families"
- **5.6.4** · `N` · "Noto Sans JP (23.4%) and Roboto (21.3%) are together 45% of all VF request volume". Prior map C151, C152, C208. The slicing caveat applies.
  - Evidence: Roboto 3,455,630 / 16,264,853 = 21.246% (not 21.3); Noto Sans JP 23.40%; sum 44.65%. On mobile Roboto is #1. [lane C]
  - Bulletproof: **RED**. One wrong decimal; desktop-only ordering; slice-inflated.
  - Suggested fix: "Noto Sans JP (23.4%) and Roboto (21.2%) are together 45% of desktop VF request volume."
  - Decision: **A** · v3: "on desktop, Noto Sans JP (23.4%) and Roboto (21.2%) are together 45% of VF request volume (on mobile, Roboto leads)"
- **5.6.5** · `N` · "with Open Sans, Montserrat, and Inter rounding the top five to about two-thirds". Prior map C209.
  - Evidence: Top five = 63.46% desktop / 62.43% mobile. [lane C]
  - Bulletproof: **YELLOW**. "About two-thirds" rounds up.
  - Suggested fix: "nearly two-thirds."
  - Decision: **A** · v3: "nearly two-thirds" (63.5%)
- **5.6.6** · `I` · "the playlist is concentrated even by playlist standards"
  - Evidence: Noto Sans JP ≈ 27.8 VF requests per declaring page vs Roboto 1.37. [lane C]
  - Bulletproof: **YELLOW**. The concentration is real but inflated by slicing.
  - Suggested fix: Mention slicing where the concentration is stated.
  - Decision: **A** · v3: "Noto Sans JP's share is mostly slices — about 26 files per page against Roboto's 1.4" (fonts_variable_family_totals.csv: 3,806,479/143,791; 3,455,630/2,465,217)

### ¶5.7 (vL229) "The mechanism of the half-web moment, then…"

- **5.7.1** · `I` · "The mechanism of the half-web moment, then, is largely *supply-side*". This is a causal claim resting on request share, not page attribution.
  - Evidence: No page-level VF-by-service data. Self-hosted supplied 39% of VF request growth 2025→26 and 49% of 2024→26. The 2020 chapter already credited Google's serving for that year's surge. [lanes C, E; spot-checked the 2020 chapter]
  - Bulletproof: **RED**. The page-level causal claim is unsupported, and the request trend partly contradicts it.
  - Suggested fix: DECISION: (a) run a page-level VF-by-service query; or (b) soften: "Google's delivery accounts for most variable-font traffic, but self-hosted variables supplied nearly half the growth since 2024."
  - Decision: **D→A** · D3 (pages_variable_by_service.csv): 72.4% desktop / 72.3% mobile of VF pages get VFs only from Google; of those with a visible Google CSS URL, 99% requested 2+ weights or a range. v3 states it with numbers
- **5.7.2** · `X` · "Google Fonts progressively serves its most popular families — including its CJK flagships — as variable files"
  - Evidence: Live probe: a single weight gets a static file; a 400;700 request gets a variable file (wght 100–900). Noto Sans JP [wght] added to google/fonts 2022-05-05. [lane E]
  - Bulletproof: **YELLOW**. Mostly true, but variable serving depends on the embed requesting more than one weight.
  - Suggested fix: "Google Fonts serves variable files, CJK included since 2022, whenever a page requests more than one weight."
  - Decision: **A** · v3: "exactly when Google Fonts serves a variable file (CJK families included, since 2022)"
- **5.7.3** · `I` · "half the web inherits the technology the way it inherits `unicode-range`: by linking to Google"
  - Evidence: No page-level attribution. [lane C]
  - Bulletproof: **RED**. Unsupported as stated.
  - Suggested fix: Depends on the 5.7.1 decision.
  - Decision: **A** · v3: "Most of the half of the web that loads variable fonts inherits the technology the way it inherits unicode-range: by linking to Google" ("half the web" narrowed to "most of the half")
- **5.7.4** · `I` · "That is genuine adoption (the bytes and the rendering pipeline are real), but it is adoption as infrastructure, not as design practice."
  - Evidence: Only 0.83% of pages set variation settings, which supports the design half. [lane C]
  - Bulletproof: **YELLOW**. The design half is supported; the infrastructure half rests on 5.7.1.
  - Suggested fix: Keep, after the 5.7.1 fix.
  - Decision: **K**

### ¶5.8 (vL231) "The axis data completes the picture."

- **5.8.1** · `N` · "Inside variable *files*, weight is ubiquitous — `wght` on 85.7% of the axis sample". Prior map C161. What is the axis sample?
  - Evidence: wght 2,100,462 / 2,450,960 = 85.70% of distinct VF URLs (98.75% of which are self-hosted). [lane C]
  - Bulletproof: **YELLOW**. The denominator is unnamed; "inside variable files" is mostly self-hosted URLs.
  - Suggested fix: "…`wght` in 85.7% of distinct variable-font URLs."
  - Decision: **A** · v3: "wght in 85.7% of distinct variable-font URLs"
- **5.8.2** · `N` · "`opsz` at 10%, `wdth` at 8%, everything else at 1% or less". Prior map C162–C164.
  - Evidence: opsz 10.22%, wdth 8.35%, YTLC 1.04%, slnt 1.00%. [lane C]
  - Bulletproof: **GREEN**. "At 1% or less" is right at the printed precision.
  - Decision: **K**
- **5.8.3** · `M` · "among the minority of pages that set `font-variation-settings` at all". The size of that minority is not stated.
  - Evidence: Pages setting variation settings: 96,144 = 0.83% desktop; 140,032 = 0.90% mobile. [lane C]
  - Bulletproof: **YELLOW**. The size of the minority matters and is unstated.
  - Suggested fix: "among the 0.8% of pages that set…"
  - Decision: **A** · v3: "among the roughly 1% of pages" (0.83% published, scaled by D5 gate delta ≈1.06%)
- **5.8.4** · `N` · "the ranking is `wght` 52%, then `FILL` 45%, `opsz` 38%, `GRAD` 34%". Prior map C165–C168.
  - Evidence: wght 52.31%, FILL 44.52%, opsz 38.22%, GRAD 33.96% of 96,144 pages. [lane C]
  - Bulletproof: **GREEN**. Exact.
  - Decision: **K**
- **5.8.5** · `I` · "that middle cluster is still Google's Material Symbols icon font, not a renaissance of parametric typography"
  - Evidence: FILL and GRAD appear in only 0.26% / 0.31% of VF files; Material Symbols is declared on 69,674 pages (≥ 42,800 FILL pages). Material Symbols' axes: FILL 0–1, GRAD −50–200, opsz 20–48, wght 100–700. The 2025 chapter (L458) said the same. [lanes C, E]
  - Bulletproof: **GREEN**. Circumstantial but strong.
  - Decision: **K**
- **5.8.6** · `N` · "Animation of variation axes: 0.22% of pages". Prior map C171.
  - Evidence: 26,126 / 11,628,567 = 0.2247%; the metric also counts font-weight transitions on static fonts. [lane C]
  - Bulletproof: **YELLOW**. "Animation of variation axes" overstates.
  - Suggested fix: "Animating font weight or variation settings: 0.22% of pages."
  - Decision: **A** · v3: "Animating font weight or variation settings: at least 0.22% of pages"
- **5.8.7** · `X` · "The 2025 verdict — *high technical integration, early creative exploration*"
  - Evidence: 2025 chapter L460: "supported by high levels of technical integration, but still in an early phase of creative exploration." [lanes C, E]
  - Bulletproof: **YELLOW**. The italics imply a quote; it is a paraphrase.
  - Suggested fix: Quote it exactly, or drop the italics.
  - Decision: **A** · v3: exact 2025 quote
- **5.8.8** · `T` · "holds with the integration half now covering half the web and the exploration half essentially unmoved"
  - Evidence: Variation-settings pages 0.58% → 0.83% (+43%); animation 0.30% → 0.22% (a decline across the pipeline). [lane C]
  - Bulletproof: **YELLOW**. The exploration half did move; "essentially unmoved" is wrong in direction if not in scale.
  - Suggested fix: "…and the exploration half still under one percent of pages."
  - Decision: **A** · v3: "the exploration half still around one percent of pages"

### ¶5.9 (vL235) "Color fonts remain on 0.05–0.06% of pages…"

- **5.9.h** · `H` · "Color fonts: still a laboratory"
  - Evidence: 0.057% of pages. [lane C]
  - Bulletproof: **GREEN**. Fair.
  - Decision: **K**
- **5.9.1** · `N` · "Color fonts remain on 0.05–0.06% of pages". Prior map C173.
  - Evidence: fonts_color: 6,616 = 0.0569% desktop; 7,661 = 0.0493% mobile. [lane C]
  - Bulletproof: **GREEN**. "0.05–0.06%" right.
  - Decision: **K**
- **5.9.2** · `T` · "one in two thousand, flat year over year". Prior map C174.
  - Evidence: 2025 0.0558% / 0.0477%. [lane C]
  - Bulletproof: **GREEN**. Flat, and a 1-in-2,000 figure.
  - Decision: **K**
- **5.9.3** · `N` · "Noto Color Emoji is ~61% of the color-family sample". Prior map C176.
  - Evidence: Noto Color Emoji 9,037 of 14,729 color-font requests = 61.36%. [lane C]
  - Bulletproof: **YELLOW**. The denominator is requests, not "the color-family sample".
  - Suggested fix: "~61% of color-font requests."
  - Decision: **A** · v3: "~61% of color-font requests"
- **5.9.4** · `N` · "SVG ~52%, COLRv0 ~31%, COLRv1 ~19%". Prior map C177–C179.
  - Evidence: SVG 51.85%, COLRv0 31.46%, COLRv1 19.24% of 3,913 distinct color URLs. [lane C]
  - Bulletproof: **GREEN**. Exact.
  - Decision: **K**
- **5.9.5** · `M` · "shares overlap slightly, since some fonts carry more than one color table"
  - Evidence: Shares sum to 108.99% desktop / 105.42% mobile. [lane C]
  - Bulletproof: **GREEN**. "Overlap slightly" is fair.
  - Decision: **K**
- **5.9.6** · `T` · "with COLRv1 a few points up on 2025: migration, not breakout". Prior map C179.
  - Evidence: COLRv1 16.93% → 19.24% desktop (+2.3); mobile 16.08% → 17.16% (+1.1). [lane C]
  - Bulletproof: **YELLOW**. "A few points" is desktop only.
  - Suggested fix: "a couple of points up on desktop."
  - Decision: **A** · v3: "a couple of points up on 2025 on desktop (+2.3; mobile +1.1)"
- **5.9.7** · `N` · "`font-palette` appears on a few hundred pages in the entire crawl, against several thousand color-font pages". Prior map C182.
  - Evidence: font-palette on 109–368 desktop pages and 114–400 mobile (per-value sums are upper bounds); color-font pages 6,616 / 7,661. [lane C]
  - Bulletproof: **GREEN**. "A few hundred" vs "several thousand" holds. The two populations are not joined.
  - Decision: **A** · v3: "set on only a few hundred pages at all"
- **5.9.8** · `N` · "theming a color font is roughly a 2% practice within an already-0.06% world". Prior map C210. Check the numerator: font-palette pages are not necessarily color-font pages.
  - Evidence: Custom palette identifiers on 131 / 6,616 = 1.98% desktop, 1.81% mobile; all font-palette values 5.56%. The populations are not joined. [lane C]
  - Bulletproof: **YELLOW**. "About 2%" holds only for custom identifiers, and only as a ratio of unjoined counts.
  - Suggested fix: "A few hundred pages set `font-palette` at all, and about 130 define custom palettes, against several thousand color-font pages."
  - Decision: **A** · v3: "about 130 define custom palettes, against several thousand color-font pages"
- **5.9.9** · `I` · "The custom `--palette` identifiers that do appear prove `@font-palette-values` has real users; there are just extraordinarily few of them." Prior map C211.
  - Evidence: 61 distinct --identifiers on ≤131 pages; @font-palette-values rules not parsed. [lane C]
  - Bulletproof: **YELLOW**. "Prove" is too strong.
  - Suggested fix: "indicate."
  - Decision: **A** · "indicate" (was "prove")

---

## 6 · The scale problem and the empty column (vL239–259)

- **6.0.h** · `H` · "The scale problem and the empty column"
  - Evidence: IFT count is 6/7 pages; the `@supports` check and avar2 were never directly measured. [lane D]
  - Bulletproof: **YELLOW**. "The empty column" is a near-empty column plus two unmeasured cells.
  - Suggested fix: Keep the heading if 6.5–6.7 are fixed to say so; or "the scale problem and the near-empty column."
  - Decision: **K** · IFT column is now measured empty (D4); avar2 bounded (D6)

### ¶6.1 (vL241) "Put the uncomfortable numbers in one place:"

- **6.1.1** · `I` · "Put the uncomfortable numbers in one place"
  - Evidence: Framing. [lane D]
  - Bulletproof: **GREEN**. Transitional.
  - Decision: **K**

### ¶6.2 (vL243–247) Numbered list

- **6.2.1** · `N` · "Han script coverage: ~0.5% of fonts in the global file mix". Prior map C183.
  - Evidence: Han 94,999 / 19,534,422 = 0.49%, counting only files with >4,920 Han codepoints; Google's slices can't qualify. [lanes C, D]
  - Bulletproof: **RED**. As an "uncomfortable number" it is an artifact.
  - Suggested fix: Replace with: "Japanese families: roughly one in six Google Fonts requests, arriving as ~28 slices per page."
  - Decision: **A** · v3: "Han reaches the web in slices: only 0.5% of font files carry a near-complete Han set, while Japanese families are more than a quarter of Google Fonts' family-tagged requests in the crawl."
- **6.2.2** · `N` · "p99 font transfer: ~0.85 MB on desktop". Prior map C184.
  - Evidence: fonts_size.csv p99 = 874,708 bytes (distinct URLs, desktop) = 854 KiB = 0.87 MB (decimal) = 0.83 MiB. [lane D]
  - Bulletproof: **YELLOW**. The value is right; the units drift ("KB" in the table is KiB, "~0.85 MB" mixes conventions).
  - Suggested fix: Use one unit convention throughout (e.g. "854 KiB" or "0.87 MB").
  - Decision: **A** · v3: "p99 font file size: ~0.87 MB on desktop" (SI units)
- **6.2.3** · `N` · "Noto Sans JP is simultaneously the #1 variable-font family on the web and a fifth of Google Fonts' own traffic". Prior map C216. The data covers crawl requests, not the CDN's own traffic.
  - Evidence: VF families: desktop Noto Sans JP 23.4% > Roboto; mobile Roboto 21.65% > Noto Sans JP 20.59%. Share of Google requests 19.1% desktop / 16.8% mobile against the truncated top-100 denominator (floor 15.3% desktop). [lanes A, D]
  - Bulletproof: **RED**. "#1 on the web" is desktop-only; "a fifth of Google Fonts' own traffic" has the wrong value and the wrong scope (crawl requests, not the CDN's traffic), and both counts are slice-inflated.
  - Suggested fix: "Noto Sans JP is the busiest variable-font family by request count on desktop, and roughly one in six Google Fonts requests in the crawl."
  - Decision: **A** · v3: "Noto Sans JP: the busiest variable-font family by request count on desktop, and 17.5% of Google Fonts' family-tagged requests in the crawl, from just 1.4% of pages."
- **6.2.4** · `N` · "Subsetting via `unicode-range`: on ~62% of pages, but authored outside Google's generated CSS on only ~24%". Prior map C217.
  - Evidence: 61.85% any unicode-range; 24.11% in non-Google CSS (desktop). [lane D]
  - Bulletproof: **YELLOW**. Numbers exact. "Authored outside Google's generated CSS" overstates: non-Google CSS includes other third-party generated CSS (see 2.9.3).
  - Suggested fix: "…but present outside Google's generated CSS on only ~24%."
  - Decision: **A** · v3: "on ~63% of pages, but present outside Google's generated CSS on only ~26%"
- **6.2.5** · `I` · "Variable fonts ship axes almost nobody sets."
  - Evidence: Only 0.83% of pages set `font-variation-settings` (1.7% of VF pages); weight is set everywhere through `font-weight`. [lane D]
  - Bulletproof: **YELLOW**. True for axes set through the low-level property, but `wght` is set on nearly every VF page via `font-weight`.
  - Suggested fix: "Variable fonts ship axes that almost nobody sets directly: under 1% of pages use `font-variation-settings`."
  - Decision: **A** · v3: "about 1% of pages use font-variation-settings"

### ¶6.3 (vL249) "Every one of these points at the same architecture…"

- **6.3.1** · `I` · "Every one of these points at the same architecture: the web's hard typography — the giant scripts, the aggressive subsetting, the variable CJK files — is handled by one CDN's automation."
  - Evidence: Of the five items: two support the one-CDN claim (Noto Sans JP, unicode-range), one only indirectly, one is silent (axes), and one contradicts it (p99 tail: 99% of distinct URLs are non-Google; self-hosted p99 is 1–4.7 MB by format). [lane D]
  - Bulletproof: **RED**. "Every one of these points at the same architecture" is false; the megabyte tail is a self-hosting problem.
  - Suggested fix: "Three of these point at the same architecture…" and move the p99 point to a self-hosting sentence.
  - Decision: **A** · v3: "Most of these point at the same architecture… (The megabyte tail is the exception: it is a self-hosting problem.)"
- **6.3.2** · `I` · "That is the scale layer the web actually has in 2026. It works, at the price of centralization"
  - Evidence: Centralization supported (Noto Sans JP 96% Google-served; Google 79.4% of VF requests). "It works" not measured. [lane D]
  - Bulletproof: **YELLOW**. Half measured, half judgment.
  - Suggested fix: Mark "it works" as judgment, or cut.
  - Decision: **A** · v3: "It evidently scales, at the price of centralization"
- **6.3.3** · `I` · "the sites least able to self-host a 10 MB Han face are exactly the sites most dependent on Google's pipeline". Includes the external size figure "10 MB Han face".
  - Evidence: Noto Sans JP VF TTF 9.6 MB (WOFF2 4.35 MB); Noto Sans SC 17.8 MB; static pan-CJK OTF 16.4 MB. No data on which sites can or can't self-host. [lanes D, E]
  - Bulletproof: **RED**. "10 MB" is fair; "exactly the sites least able … are … most dependent" is an unsupported causal claim.
  - Suggested fix: "a site that wants Japanese web type without Google must self-host a multi-megabyte file (Noto Sans JP is ~4 MB even as WOFF2), and slice it itself."
  - Decision: **A** · v3: "a site that wants Japanese web type without Google must self-host a multi-megabyte file (Noto Sans JP is about 4 MB even as WOFF2) and slice it itself" (lane E: Noto Sans JP VF WOFF2 4.35 MB)
- **6.3.4** · `I` · "the subsetting expertise embodied in that pipeline exists *as infrastructure* rather than as widespread craft"
  - Evidence: Google-only unicode-range 37.7% of pages vs first-party 10.3%; Google WOFF2 median 17 KB vs 32 KB self-hosted. [lane D]
  - Bulletproof: **YELLOW**. Supported directionally; 24% of pages do carry non-Google unicode-range, so "rather than widespread craft" is a little strong.
  - Suggested fix: "exists mostly as infrastructure rather than as widespread craft."
  - Decision: **A** · v3: "exists mostly as infrastructure" — recheck against D5 unicode-range correction

### ¶6.4 (vL251) "Incremental Font Transfer is the spec-track answer…"

- **6.4.1** · `X` · "Incremental Font Transfer is the spec-track answer — let a browser fetch only the glyph and variation data it needs, from any host, incrementally"
  - Evidence: IFT spec: a patch map lists patch URLs; Rieger (Aug 2025): patches are static files, "host these files as per usual". [lane E]
  - Bulletproof: **YELLOW**. Mostly right; "from any host" needs the static-patch detail (CORS applies).
  - Suggested fix: "…fetch only the glyph, layout and variation data it needs, as static patches that any server or CDN can host."
  - Decision: **A** · v3: "fetch only the glyph, layout and variation data it needs, as static patches that any server or CDN can host"
- **6.4.2** · `X` · "The 2025 chapter called it next year's story."
  - Evidence: fonts-2025/fonts.md L146, L508: IFT data next year "may" arrive; "may have data". [lane D]
  - Bulletproof: **YELLOW**. The paraphrase drops the 2025 chapter's hedge.
  - Suggested fix: "The 2025 chapter flagged it as a story to watch this year."
  - Decision: **A** · v3: "The 2025 chapter flagged it as a story to watch this year."
- **6.4.3** · `X` · "The July 2026 crawl walked up to that door and found it unlocked but unused". "Unlocked" implies shipping browser support.
  - Evidence: No shipping browser in July 2026: Chrome Intent to Prototype 2026-04-28, no flag or origin trial; Firefox and Safari no signal. Browsers skip unsupported tech() sources. By contrast, avar2 shipped in all three engines by May 2026. [lane E]
  - Bulletproof: **RED**. "Unlocked" is false: nothing could open that door.
  - Suggested fix: "…found the door still locked: the spec is ready (Candidate Recommendation, 2025), but no browser ships support." Consider moving "unlocked but unused" to avar2, which shipped but can't be measured here.
  - Decision: **A** · v3: "found it still locked: the spec has been a W3C Candidate Recommendation since 2025, but no browser shipped support (Chrome had only announced an intent to prototype, in April 2026)"; "unlocked but unused" moved to avar2

### ¶6.5 (vL253–255) IFT list

- **6.5.1** · `N` · "`tech(incremental)` in `@font-face` src: 6 desktop pages, 7 mobile pages". Prior map C185. Check that the spec keyword is correct and what the query matched.
  - Evidence: Query matches `src` containing the substring "incremental" in top-level @font-face only. This catches tech(incremental), legacy incremental-patch/-range/-auto keywords and URLs containing the word, and misses faces nested in @media/@supports. There is no page list, so the 6/7 pages are unidentified. [lane D]
  - Bulletproof: **YELLOW**. The order of magnitude is safe; the precise meaning of "6 pages" is not.
  - Suggested fix: "`@font-face` sources mentioning incremental transfer: 6 desktop pages, 7 mobile pages." Optionally pull the page list (tiny query) to see if they're test pages.
  - Decision: **A** · D4 (styles_font_tech_incremental_v2.csv): one site writes tech(incremental) (store.gs1us.org, VTEX, ordinary Gotham WOFF2); other old hits were URL substrings (e.g. autoincremental.es). v3 bullet leaves the site unnamed
- **6.5.2** · `N` · "about 0.00005% of the web". Prior map C212.
  - Evidence: 6 / 11,628,567 = 0.0000516%; 7 / 15,539,089 = 0.0000450%. [lane D]
  - Bulletproof: **GREEN**. Arithmetic correct.
  - Decision: **C** · "about 0.00005%" dropped (now one site)
- **6.5.3** · `N` · "`@supports font-tech(incremental)` feature detection: zero pages". Prior map C213.
  - Evidence: The `@supports` detector in styles_font_tech_incremental.sql cannot fire. Lane D ran its JavaScript locally on an IFT face wrapped in `@supports font-tech(incremental)` and it returned nothing, even though pruned_css keeps those blocks. [lane D]
  - Bulletproof: **RED**. "Zero pages" is a detector failure, not a measurement.
  - Suggested fix: Remove the bullet (and from A.1.4), or fix the detector and re-run (small query; your call on spend).
  - Decision: **A** · D4: @supports font-tech(incremental) = 0 pages with a fixed detector that walks nested rules (27/27 node tests)
- **6.5.4** · `M` · "IFT polyfills: not detectable in our extraction (which keeps font binaries and CSS, not script bodies)". Does the extraction really keep font *binaries*?
  - Evidence: fonts_2026.font_requests (sql/materialize/font_requests.sql L13–24) holds request rows, HAR payload with the crawler's `_font_details` metadata, and summary; there is no body or binary column. [lane D]
  - Bulletproof: **RED**. "Keeps font binaries" is factually wrong.
  - Suggested fix: "…(which keeps font request records, parsed font metadata and CSS, not script bodies)."
  - Decision: **A** · v3: "keeps font request records, parsed font metadata and CSS, not script bodies"
- **6.5.5** · `N` · "and no signature of one surfaced anywhere else in the data". What was searched? Would IFT/IFTX table tags in parsed fonts count?
  - Evidence: No IFT/IFTX tag among the 67 table tags in fonts_size_by_table.csv, but that query has `HAVING count > 1000`. No other search is documented. [lane D]
  - Bulletproof: **YELLOW**. Directionally true, but "no signature surfaced anywhere" implies a search that wasn't systematically run. The table-tag check has a floor of 1,000 fonts.
  - Suggested fix: "and no IFT font table appears among the table tags seen in more than a thousand fonts."
  - Decision: **A** · v3: "no IFT font table appears among the table tags seen in more than a thousand fonts"

### ¶6.6 (vL257) "And one companion baseline from the file side: avar2…"

- **6.6.1** · `X` · "avar2 — the extended axis-mapping table that underpins some of the more ambitious variable-font futures"
  - Evidence: avar v2 is standardized in ISO/IEC 14496-22 5th ed. (FDIS), not OpenType 1.9.1. Rendering support: Chrome 148 (2026-05-05); Firefox and Safari already shipping. [lane E]
  - Bulletproof: **YELLOW**. Fair description; lacks standard and support context, which matters for the argument.
  - Suggested fix: Add "(standardized through ISO's Open Font Format; supported in all major browsers since May 2026)."
  - Decision: **A** · v3: "standardized through ISO's Open Font Format and rendered by all major browsers since May 2026" (Chrome 148 release notes 2026-05-05; ChromeStatus lists Firefox/Safari shipping)
- **6.6.2** · `N` · "An `avar` table of some kind rides on about 10.7% of parsed fonts on desktop (11.1% mobile)". Prior map C214. Is the denominator parsed fonts or requests?
  - Evidence: 2,094,240 / 19,534,422 = 10.72% desktop; 2,863,512 / 25,875,765 = 11.07% mobile; distinct parsed font URLs. [lane D]
  - Bulletproof: **GREEN**. Exact; "parsed fonts" is the right noun.
  - Decision: **K**
- **6.6.3** · `N` · "the size distribution (median 42 bytes, 99th percentile 72 bytes)". Prior map C215.
  - Evidence: fonts_size_by_table.csv avar sizes desktop p10–p99: 22 / 34 / 42 / 46 / 50 / 72 bytes (mobile median 44). No max or p999 exists. [lane D]
  - Bulletproof: **GREEN**. Numbers exact.
  - Decision: **C** · percentiles replaced by the max (D6)
- **6.6.4** · `I` · "is consistent only with version 1's simple segment maps; avar2's variation stores would be orders of magnitude larger". A p99 does not rule out the top 1%. Check the actual minimum size of avar2.
  - Evidence: avar v1 = 8 + 2N + 4K bytes (N axes, K map entries): 22 B = 1-axis default, 50 B = 3-axis default, 72 B = 2 axes with 15 entries. A minimal avar v2 adds 8 B of offsets plus a ~31 B ItemVariationStore, so ≈49–82 B, inside the observed band. ~20,942 desktop / 28,635 mobile tables sit above p99, unobserved. [lane D; lane E to confirm v2 size]
  - Bulletproof: **RED**. "Consistent only with version 1" and "orders of magnitude larger" are both false. The size data can't distinguish v2 from v1 at small sizes, and can't see the top 1% at all.
  - Suggested fix: "The size distribution shows no sign of avar2 through the 99th percentile, but the crawl records table sizes only, so avar2 is effectively unmeasured."
  - Decision: **D→A** · D6 (fonts_avar_size_tail.csv): max avar table in the crawl = 200 B on both clients; 0 tables > 200 B; 2,832 desktop > 100 B; p99.9 108 B, p99.99 198 B. Shipped avar2 tables are tens of kB (Amstelvar 58,318 B). v3 states the bound and the version caveat
- **6.6.5** · `M` · "No direct version field reaches the crawl's metadata, so this is an indirect null"
  - Evidence: No 2026 query reads an avar version field; the payload schema isn't in the repo. [lane D]
  - Bulletproof: **YELLOW**. Probably true, but unverified from the repo.
  - Suggested fix: Confirm against the crawler's font-parser source or one sample payload, or say "the metadata we queried carries table sizes only."
  - Decision: **A** · v3: "The metadata records sizes, not versions"
- **6.6.6** · `I` · "but it is a confident one: effectively zero avar2, effectively zero IFT"
  - Evidence: avar2 not excluded (6.6.4); `@supports` unmeasured (6.5.3). [lane D]
  - Bulletproof: **RED**. "A confident one: effectively zero avar2" is unsupported. The IFT half is fine at 6–7 pages.
  - Suggested fix: "effectively zero IFT; avar2, so far, beyond the crawl's reach."
  - Decision: **A** · v3: "no font in the crawl looks like a real one: effectively zero avar2, effectively zero IFT" (now backed by D4 + D6)

### ¶6.7 (vL259) "None of this is a failure of measurement…"

- **6.7.1** · `I` · "None of this is a failure of measurement, and it is not quite a failure of the technology either."
  - Evidence: The `@supports` result is a detector failure; the table-tag check has a floor; avar2 can't be measured from sizes. [lane D]
  - Bulletproof: **RED**. "None of this is a failure of measurement" is contradicted by the evidence.
  - Suggested fix: "Only part of this is a measurement limit; most of it is a technology that hasn't shipped."
  - Decision: **A** · v3: "Little of this is a failure of measurement…"
- **6.7.2** · `I` · "Specs precede toolchains; toolchains precede hosts; hosts precede the long tail."
  - Evidence: Aphorism. [lane D]
  - Bulletproof: **GREEN**. Opinion, clearly framed.
  - Decision: **K**
- **6.7.3** · `I` · "in 2026 the decentralized answer to the scale problem has not begun shipping"
  - Evidence: 6 desktop / 7 mobile pages already mention incremental transfer. [lane D]
  - Bulletproof: **YELLOW**. "Has not begun shipping" vs a handful of opt-ins.
  - Suggested fix: "has barely begun shipping."
  - Decision: **K** · accurate after D4 (no real IFT deployment)
- **6.7.4** · `N` · "while the centralized answer quietly serves a fifth of the largest font CDN's traffic in Japanese"
  - Evidence: Noto Sans JP 19.1% / 16.8% of Google top-100 family requests (floor 15.3% desktop); all Japanese families 22.2% / 20.6%, same denominator issue. [lane D; lane A for the denominator]
  - Bulletproof: **RED**. Wrong value and wrong scope (crawl request share, slice-inflated, not "the largest CDN's traffic").
  - Suggested fix: "…while the centralized answer serves roughly one in six Google Fonts requests in this crawl in Japanese."
  - Decision: **A** · v3: "serves more than a quarter of Google Fonts' family-tagged requests in the crawl in Japanese"
- **6.7.5** · `I` · "Watch for three things in 2027: a non-zero `tech(incremental)` count, host support (Google's own pipeline is the obvious first mover), and measurable byte savings on CJK delivery". The count is already non-zero (6–7 pages).
  - Evidence: The count is already non-zero (6/7 pages); no per-script byte metric exists to watch savings. [lane D]
  - Bulletproof: **RED**. "A non-zero count" is already met.
  - Suggested fix: "a count in the hundreds rather than single digits, host support…, and measurable byte savings on CJK delivery (which would need a new per-script size query)."
  - Decision: **A** · v3: "the first production pages serving real IFT fonts"

---

## 7 · What to do with a mature stack (vL263–273)

### ¶7.1 (vL265) "A 2026 hygiene list, each line grounded in a number above:"

- **7.1.1** · `M` · "each line grounded in a number above"
  - Evidence: Five of seven items grounded in body numbers; #2 partly (icon rationale is external advice); #4 not measured. [lane D]
  - Bulletproof: **YELLOW**. "Each line grounded in a number above" is not quite true.
  - Suggested fix: "most lines grounded in a number above," or fix #4.
  - Decision: **A** · v3: "most lines grounded in a number above"

### ¶7.2 (vL267–273) Hygiene list

- **7.2.1** · `N` · "Ship WOFF2 with a correct `font/*` MIME type — on your own origin especially, where ~30% of request volume still isn't WOFF2 and mislabeled octet-stream persists". Prior map C186.
  - Evidence: Self-hosted non-WOFF2 = 30.50% desktop / 30.69% mobile of self-hosted requests; octet-stream 9.0%. [lane D]
  - Bulletproof: **GREEN**. "~30%" holds; advice is standard.
  - Decision: **A** · v3: "when you self-host especially"
- **7.2.2** · `I` · "`font-display: swap` for text; `block` only for icon fonts that should never flash placeholder boxes"
  - Evidence: styles_font_display_by_family: the top-10 `block` families are all icon fonts (Font Awesome on 14.7% of pages); the top `swap` families are text faces. [lane D]
  - Bulletproof: **GREEN**. The data directly support the advice.
  - Decision: **K**
- **7.2.3** · `T` · "Preconnect and preload critical faces — the still-growing minority practices"
  - Evidence: Font-related hints: preconnect 18.25 → 20.28%, preload 12.04 → 14.70% (desktop 2025 → 2026). [lane D]
  - Bulletproof: **GREEN**. "Still-growing minority" holds (preconnect was flat 2024→25, grew this year).
  - Decision: **K**
- **7.2.4** · `I` · "Use variable fonts as consolidated multi-weight files — that is what half the web already does". Multi-weight use itself is not measured.
  - Evidence: Only "≥1 VF on the page" and axes-in-file are measured; multi-weight consolidation is not. [lane D]
  - Bulletproof: **YELLOW**. "That is what half the web already does" is unmeasured.
  - Suggested fix: Cut that clause: "Use variable fonts as consolidated multi-weight files; explore other axes when design calls for them."
  - Decision: **A** · v3: "which is, in effect, what most variable-font pages already get from Google when they ask for more than one weight" (D3)
- **7.2.5** · `I` · "If you self-host, subsetting is on you. `unicode-range` on your pages is very likely Google's CSS, not yours"
  - Evidence: Among unicode-range pages: Google-only 61.0%; any Google 76.5%. [lane D]
  - Bulletproof: **YELLOW**. "Very likely" slightly overstates.
  - Suggested fix: "is likely Google's CSS, not yours."
  - Decision: **A** · "likely"
- **7.2.6** · `N` · "Consider metric overrides … the 3% of pages doing this are onto something". Prior map C219.
  - Evidence: Each override descriptor 2.71–2.86% desktop; next/font emits all four by default; "Inter Fallback" on 61,218 pages. [lanes B, D, E]
  - Bulletproof: **YELLOW**. "Onto something" credits authors for what frameworks mostly do.
  - Suggested fix: "…the 3% of pages doing this, mostly via framework defaults, show it can be automatic."
  - Decision: **A** · v3: "mostly via framework defaults, show it can be automatic"
- **7.2.7** · `I` · "Don't plan a 2026 product around IFT — plan to watch it, and to notice if your CJK strategy is quietly a bet on one CDN"
  - Evidence: IFT 6/7 pages; Noto Sans JP 96% Google-served. [lane D]
  - Bulletproof: **GREEN**. Advice consistent with the data.
  - Decision: **K**

---

## 8 · Closing (vL277–281)

### ¶8.1 (vL279) "The 2025 chapter closed on convergence and refinement…"

- **8.1.1** · `X` · "The 2025 chapter closed on convergence and refinement."
  - Evidence: fonts-2025/fonts.md L506: "convergence and refinement." [lane D]
  - Bulletproof: **GREEN**. Accurate paraphrase.
  - Decision: **K**
- **8.1.2** · `N` · "web fonts on ~88% of pages". Prior map C187.
  - Evidence: 88.57% / 87.06%. [lane D]
  - Bulletproof: **GREEN**. "~88%" correct.
  - Decision: **K**
- **8.1.3** · `N` · "variable fonts on half"
  - Evidence: 48.69% / 50.21%. [lane D]
  - Bulletproof: **GREEN**. "On half" is fair in a recap.
  - Decision: **K**
- **8.1.4** · `T` · "WOFF2 at 68.5% of unique URLs and rising"
  - Evidence: Unique-URL WOFF2 59.5 → 65.04 → 68.48% (desktop). [lane D]
  - Bulletproof: **GREEN**. Correct.
  - Decision: **K**
- **8.1.5** · `N` · "swap past 52%"
  - Evidence: swap 52.61% desktop / 52.92% mobile of all root pages; pruned_css figure, so a floor. [lane D]
  - Bulletproof: **YELLOW**. Value fine; carries the CSS-floor caveat.
  - Suggested fix: None beyond the global CSS-floor note.
  - Decision: **A** · "swap past 55%" (corrected)
- **8.1.6** · `N` · "OFL touching seven in ten pages". This drops the "license query's universe" qualifier from 4.4.1.
  - Evidence: OFL 69.93% desktop / 70.60% mobile; the license query's "universe" is all root pages. [lane D]
  - Bulletproof: **GREEN**. Correct as written. It is 4.4.1's qualifier that misleads.
  - Decision: **K**
- **8.1.7** · `I` · "a solved surface with a boringly consistent leaderboard"
  - Evidence: Family rank order matches 2025, but the 2026 levels are 2–3.5× the 2025 chapter's (Font Awesome 8.5–9.3% → 30.6%), a pipeline or definition difference. [lane D]
  - Bulletproof: **YELLOW**. "Consistent leaderboard" is true of ranks only.
  - Suggested fix: Tie to the §4 comparability fix.
  - Decision: **K** · ranks match 2025; levels not compared (Appendix B)
- **8.1.8** · `I` · "the hard problems — CJK scale, subsetting, variable delivery — solved in practice by one provider's automation, visible in every table where Noto Sans JP or Google's generated CSS appears"
  - Evidence: Google 79.4% of VF requests; Google on 61% of unicode-range pages; Noto Sans JP 96% Google. [lane D]
  - Bulletproof: **YELLOW**. "Solved in practice" is unmeasured; "every table" overstated.
  - Suggested fix: "handled in practice by one provider's automation, visible wherever Noto Sans JP or Google's generated CSS appears."
  - Decision: **A** · v3: "handled in practice by one provider's automation, visible wherever Noto Sans JP or Google's generated CSS appears"
- **8.1.9** · `N` · "Incremental Font Transfer at six pages". Prior map C188.
  - Evidence: 6 desktop / 7 mobile pages. [lane D]
  - Bulletproof: **YELLOW**. Desktop figure only; detector caveats (6.5.1).
  - Suggested fix: "Incremental Font Transfer on six or seven pages."
  - Decision: **A** · v3: "Incremental Font Transfer opted into by a single site (on ordinary files)" (D4)
- **8.1.10** · `N` · "avar2 at zero". Prior map C188. The evidence is an indirect null.
  - Evidence: No avar2 measurement exists (6.6.4). [lane D]
  - Bulletproof: **RED**. Cannot be "zero."
  - Suggested fix: Cut "avar2 at zero," or "avar2 not yet measurable."
  - Decision: **A** · v3: "avar2 effectively absent though every major browser renders it" (D6: max avar 200 B)
- **8.1.11** · `I` · "the decentralized future still entirely in front of us"
  - Evidence: 6/7-page trace exists. [lane D]
  - Bulletproof: **YELLOW**. "Entirely" overstated by a hair.
  - Suggested fix: "almost entirely in front of us."
  - Decision: **K** · accurate after D4

### ¶8.2 (vL281) "Maturity is not completion."

- **8.2.1** · `I` · "For the Latin-default commercial web, fonts are done in the way plumbing is done."
  - Evidence: Consistent with the aggregate maturity numbers. [lane D]
  - Bulletproof: **GREEN**. Author's conclusion, clearly framed.
  - Decision: **K**
- **8.2.2** · `I` · "the megabyte tail that still sneaks into every crawl"
  - Evidence: Self-hosted p99 ranges 1.0–4.7 MB by format; 2024 p99 ~776 KB (prior map C071). [lane D]
  - Bulletproof: **GREEN**. Holds.
  - Decision: **K**
- **8.2.3** · `I` · "the web is waiting on infrastructure the July 2026 corpus cannot yet see, while leaning on infrastructure it can see everywhere it looks"
  - Evidence: IFT is partly seen; Google on 53.7% / 51.9% of pages. [lane D]
  - Bulletproof: **YELLOW**. "Everywhere it looks" overstated.
  - Suggested fix: Rhetorical; soften or keep as a flourish, knowingly.
  - Decision: **K** · deliberate flourish

---

## A · Appendix A — Featured stats (vL285–290)

- **A.1.1** · `N` · "50% — mobile pages loading a variable font (48.7% desktop)". Prior map C190.
  - Evidence: 50.21% mobile / 48.69% desktop. [lane D]
  - Bulletproof: **GREEN**. Exact.
  - Decision: **K**
- **A.1.2** · `N` · "71% — pages self-hosting at least one font". Prior map C191. The client is unstated.
  - Evidence: 71.41% desktop; 70.15% mobile. [lane D]
  - Bulletproof: **YELLOW**. Client unstated; "self-hosting" definition (see 0.3.7).
  - Suggested fix: "71% — desktop pages loading at least one font from outside the font services."
  - Decision: **A** · v3: "71% — desktop pages self-hosting at least one font"
- **A.1.3** · `N` · "38% — pages whose only `unicode-range` subsetting comes from Google's generated CSS". Prior map C192. The client is unstated.
  - Evidence: 37.74% desktop; 37.12% mobile. [lane D]
  - Bulletproof: **YELLOW**. Client unstated.
  - Suggested fix: "38% — desktop pages whose only…"
  - Decision: **A** · "38% — desktop pages…" (38.2% corrected)
- **A.1.4** · `N` · "0% — measurable IFT adoption (6–7 pages; `@supports` count: zero)". Prior map C193.
  - Evidence: 6/7 pages OK; the `@supports` count was never measured (6.5.3). [lane D]
  - Bulletproof: **RED**. Contains a false measurement.
  - Suggested fix: "0% — measurable IFT adoption (six desktop and seven mobile pages)."
  - Decision: **A** · v3: "0% — measurable IFT adoption (one site's opt-in, on ordinary WOFF2 files; @supports count: zero)" (follows from D4)

---

## B · Appendix B — Method & sources (vL292–294)

- **B.1.1** · `N` · "root pages (11,628,567 desktop / 15,539,089 mobile)". Prior map C189.
  - Evidence: The `total` column in every page-normalized CSV = COUNT(DISTINCT page) from root_pages: 11,628,567 / 15,539,089. [lane D]
  - Bulletproof: **GREEN**. Internally consistent. No independent cross-check against HA's published counts.
  - Decision: **K**
- **B.1.2** · `M` · "Font binaries via `fonts_2026.font_requests`". Are these binaries, or request records plus parsed metadata?
  - Evidence: font_requests.sql L13–24 selects no body. [lane D]
  - Bulletproof: **RED**. "Font binaries" is wrong.
  - Suggested fix: "Font request records and parsed font metadata via…"
  - Decision: **A** · v3: "font request records and the crawler's parsed font metadata"
- **B.1.3** · `M` · "CSS via the `fonts_2026.pruned_css` materialization (font-relevant AST slices; pathological mega-sheets gated empty)". How many sheets or pages were gated?
  - Evidence: Gates: serialized AST >350,000 bytes, or >8,000 top-level rules, plus JS caps. The number of gated sheets or pages is logged nowhere, and the gate was never validated (the sample rebuild omits it). [lane D]
  - Bulletproof: **YELLOW**. The description is true; it hides an undercount of unknown size in every CSS figure.
  - Suggested fix: Count the gated sheets/pages (one small BigQuery query; your call on spend) and state it; or state plainly that CSS figures are lower bounds of unknown margin.
  - Decision: **A** · v3 Appendix B: gate stated (2.9% of stylesheets, 44% of pages) and corrected by full scan
- **B.1.4** · `M` · "Format YoY on distinct-URL proportions; request-volume series labeled where used"
  - Evidence: chart_formats.csv proportion_unique vs proportion_request, both labeled. [lane D]
  - Bulletproof: **GREEN**. Accurate.
  - Decision: **A** · v3: restated in plain language
- **B.1.5** · `M` · "Every number in this manuscript is keyed to its source CSV, column, and denominator in `verification/source-map-2026.csv`". This points at the internal path; the claim sheet supersedes it.
  - Evidence: The map has 220 rows; row C220 is stale; C213, C215, C216 and C188 are wrong ("matched"). [lane D]
  - Bulletproof: **RED**. "Machine-checked" overstates a map that marked several wrong claims as matched. The internal path is meaningless to readers.
  - Suggested fix: Point to the published methods/replication page and this claim sheet; drop "machine-checked."
  - Decision: **A** · v3: "Every figure is traced to its query, result table, and denominator in a claim-by-claim verification sheet, available with the queries." ("machine-checked" and internal path removed)
- **B.1.6** · `M` · "Multi-year series from Web Almanac sheet mirrors (`fonts_all_years.duckdb`) and `data/multi-year/chart_*.csv`"
  - Evidence: Provenance true per data/multi-year/README.md. The fonts-2026/ copy of the DuckDB is an empty stub; the real one is one directory up. [lane D]
  - Bulletproof: **YELLOW**. Internal paths; fine for a replication appendix, not for readers.
  - Suggested fix: Name the sources (Web Almanac spreadsheets 2019–2025) rather than local files.
  - Decision: **A** · v3: "published spreadsheets of the Web Almanac fonts chapters (2019–2025)"; no local paths
- **B.1.7** · `M` · "Known limits: `hyphens`/CSS-property figures use the 2026 pruned-CSS pipeline and are not compared against earlier chapters". Compare 3.3, 3.7.4, 5.2.3, and 5.2.5, which do compare.
  - Evidence: At least nine passages compare pruned_css figures with earlier years: vL16, 109, 121, 138–148, 146, 156, 175, 209, 231. [lane D]
  - Bulletproof: **RED**. The stated limitation is false as written, and the comparability problem it points to is thesis-level (see CSS ruling).
  - Suggested fix: Depends on the CSS-comparability decision (3.3.6).
  - Decision: **A** · v3 Appendix B: residual 2025→2026 CSS declines reported as levels; @layer parser caveat
- **B.1.8** · `M` · "script coverage is a per-file metric"
  - Evidence: fonts_script counts COUNT(DISTINCT url) over parsed fonts; a script is assigned when a font covers >5% of that script's codepoints. [lane D]
  - Bulletproof: **YELLOW**. "Per-file" is right; the 5% threshold, which drives the Han result, is undisclosed.
  - Suggested fix: Add the threshold.
  - Decision: **A** · v3: "a script counts when a file covers more than 5% of its characters"
- **B.1.9** · `M` · "host attribution for `unicode-range` uses exact host matching (first-party is a floor)"
  - Evidence: Exact NET.HOST equality in styles_unicode_range_by_source.sql; fonts.googleapis.com also exact-matched. [lane D]
  - Bulletproof: **GREEN**. Accurate. Note Google-only is also a floor (locally copied Google CSS counts as first-party).
  - Decision: **K** · restated
- **B.1.10** · `M` · "The Google Fonts mobile series carries an unexplained 2025→2026 discontinuity documented in `verification/anomaly-google-mobile.md`; no mobile trend claim is made." This points at an internal path.
  - Evidence: Note values match chart_services.csv; v2 states levels only for mobile. [lane D]
  - Bulletproof: **YELLOW**. Accurate, but an internal file path.
  - Suggested fix: Describe the discontinuity in a sentence instead of pointing to the internal file.
  - Decision: **A** · v3: discontinuity described in one sentence; internal path removed

---

## F · Figures (placeholders in v2; rendered files in `figures/out/`)

- **F.1** · F1 "web font adoption, 2011–2026 — share of root pages" (vL26) · `f01-font-usage-over-time`
  - Evidence: f01 SVG data-denominator="pages"; all 32 plotted points equal chart_font_usage_annual.csv to 0.01 pp. [lane A]
  - Bulletproof: **GREEN**. Faithful to data. Minor: mixed July dates across years; early mobile samples are tiny (see 0.1.2).
  - Decision: **K**
- **F.2** · F2 "variable font adoption, 2019–2026 — share of root pages" (vL223) · `f02-variable-font-adoption`
  - Evidence: f02 SVG denominator = pages; plotted values equal chart_variable_fonts.csv, whose 2020 row is client-swapped. The chart visibly shows the 2021→22 jump that contradicts 5.5.1. [lane C]
  - Bulletproof: **RED**. Plots a data error.
  - Suggested fix: Fix the CSV row and re-render.
  - Decision: **A** · 2020 row un-swapped; re-rendered 2026-10-01
- **F.4** · F4 "hosting combinations, 2022–2026 — share of desktop pages" (vL46) · `f04-hosting-combinations`
  - Evidence: f04 data-denominator="pages"; all 15 labels equal chart_service_combos.csv (desktop). [lane A]
  - Bulletproof: **YELLOW**. Accurate but desktop-only, which hides the 2026 mobile reversal the text discusses. The 2022 corpus differs.
  - Suggested fix: Caption should say "desktop" and note mobile diverged in 2026.
  - Decision: **A** · caption (when written): "desktop"; note that mobile diverged in 2026
- **F.5** · F5 "WOFF2 share of font requests, 2019–2026" (vL89) · `f05-woff2-request-share`
  - Evidence: denominator = requests (correct); labels 83.7 / 83.3 correct. [lane B]
  - Bulletproof: **YELLOW**. "July crawls" is wrong for 2020 (August) and 2022 (June).
  - Suggested fix: Caption: "mid-year crawls" or list the months.
  - Decision: **A** · caption (when written): crawl months, not "July"
- **F.6** · F6 "format mix among distinct font URLs, 2024–2026" (vL90) · `f06-format-mix-unique-urls`
  - Evidence: denominator = unique_urls (correct); 2025 octet label shows 6.7. [lane B]
  - Bulletproof: **RED**. Double-rounding error: 6.6.
  - Suggested fix: Recompute labels from raw counts; re-render.
  - Decision: **A** · 2025 octet label fixed (6.6); re-rendered 2026-10-01
- **F.7** · F7 (optional) "resource hints, 2022–2026" (vL134) · `f07-resource-hints`
  - Evidence: denominator = pages; labels match the counts (18.2, 17.8) and show the 2023 preload dip; no prefetch series. [lane B]
  - Bulletproof: **YELLOW**. The figure is right; the prose disagrees with it (3.1.1, 3.1.3, 3.2.1, 3.2.3). No prefetch.
  - Suggested fix: Keep; fix the prose; footnote the 2022 re-run definition.
  - Decision: **A** · labels confirmed (18.2 / 17.8); prose now agrees with the figure; caption should say "font-related" and note the 2022 re-run
- **F.8** · F8 "font-display values, 2022 / 2025 / 2026" (vL148) · `f08-font-display`
  - Evidence: denominator = pages; 2026 labels correct; 2025 auto shows "9.0" (should be 9.1) and fallback "5.1" (should be 5.0); a code comment wrongly says 2024 wasn't measured. [lane B]
  - Bulletproof: **RED**. Two wrong labels.
  - Suggested fix: Recompute from raw counts; re-render.
  - Decision: **A** · 2025 labels fixed (swap 49.5, auto 9.1, fallback 5.0) from raw counts; re-rendered. YoY still subject to D5
- **F.9** · F9 "font transfer size percentiles, 2026" (vL105) · `f09-size-percentiles`
  - Evidence: Labels correct, but the SVG denominator, title and axis say "requests"; the data is distinct parsed font files. [lane B]
  - Bulletproof: **RED**. Wrong denominator on the chart.
  - Suggested fix: Relabel "per distinct font file (KiB)"; re-render.
  - Decision: **A** · relabeled: per distinct font file, SI kB, denominator=files; re-rendered
- **F.10** · F10 "script coverage among font files, 2026" (vL199) · `f10-script-coverage`
  - Evidence: denominator = files, bars equal the CSV; the unit is distinct URLs; the Han bar is accent-coloured, spotlighting the classifier artifact. [lane C]
  - Bulletproof: **RED**. The chart's emphasis promotes the artifact.
  - Suggested fix: Rethink after the 4.5–4.7 decision; at minimum remove the Han accent and footnote the 5% threshold.
  - Decision: **A** · re-rendered 2026-10-01: no Han accent; Han/Hangul labeled "near-complete sets"; PUA "(mostly icons)"; "Emoji-range symbols"; x-label states the >5% rule; source "distinct font URLs"
- **F.11** · F11 (optional) "most-declared font families, 2026" (vL177). Not rendered.
  - Evidence: Not rendered; would come from styles_family.csv (@font-face declarations). [lane C]
  - Bulletproof: **YELLOW**. N/A until built.
  - Suggested fix: If built, title it "most-declared @font-face families".
  - Decision: **K** · not rendered; if built, title "most-declared @font-face families"
