# Verification

How every number in the report was tied to a result file, and how to re-check a draft.

| File | What it is |
| --- | --- |
| `source-map-2026.csv` | One row per numbered claim (C001 onward): the section, the claim as worded, the value, the client (desktop or mobile), the denominator, the result file and the cell it comes from, and a status (`matched`, `superseded`, or a note). This is the map the gate reads. |
| `source-map-v7-delta.csv` | The claims added in the October 2026 revision (the intel edits), in the same shape. |
| `claim-sheet-2026.md` | The working sheet behind the maps: each claim with the evidence found for it, the problem if any, and the decision taken. Decisions are lettered: A means the text was changed to the verified value, K means the claim was kept with a caveat, D means a denominator or method was corrected first. The "D5 correction" referred to throughout is the adjustment of CSS-derived figures for the stylesheets the extraction set aside for size, described in the report's Appendix B. |
| `anomaly-google-mobile.md` | The investigation of the two steps in the Google Fonts mobile series, which the report declines to narrate as a trend. |
| `verify_draft_numbers.py` | The gate. Checks a Markdown draft in both directions against the two maps: every mapped value must appear in the text, and every number in the text must trace to a map row or to a cell in a data file. Writes `report-<date>.md`. |
| `report-2026-10-23.md` | The gate's run on the published text. |

Run the gate from the repository root:

```bash
python3 verification/verify_draft_numbers.py --draft report/fonts-on-the-web-2026.md --date YYYY-MM-DD
```

A token the gate calls "weak" matches a cell in a data file but no claim row; a token it calls "uncovered" matches nothing and needs a human to say where it came from. The report lists both.
