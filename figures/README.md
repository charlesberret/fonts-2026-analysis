# Figures — Fonts on the Web 2026

**Denominator rule.** Every figure declares its denominator (`pages`, `requests`, `unique_urls`, `files`) as a required argument to `new_figure()`; `unit_label()` refuses a unit line that does not name it, `save_figure()` refuses a figure without a unit line, and it is written into the SVG root as `data-denominator="…"`. A figure without one will not build.

**Run.** `./.venv/bin/python render.py F1 F2` or `./.venv/bin/python render.py --all` — outputs land in `out/` as `fNN-<slug>.svg` (live `<text>`, `svg.fonttype='none'`) and `fNN-<slug>.png` (1600px wide).

**Palette and type.** `grammar.py` is the only style file — the Direction A "Specimen" frame (Fig. N + section tag, finding title, deck, hairline rules, plot column + margin column with key and one big number, source line) in the A5 Kettle scheme: ground `#e7e9ee`, ink `#181a23`, muted `#5b5d66`, grid `#bcbdc6`; exactly three series hues, cobalt `#2a5cda`, cerise `#ca363a`, violet `#8a64ab` (desktop = cobalt, mobile = cerise; three-year comparisons colour the year: earliest violet, middle cobalt, latest cerise; no stacks). Type is one family, Schibsted Grotesk, via pyfonts (cached): weight 600 sets the title and 700 the margin's big number; regular and 500 set everything else — Figure tag, deck, unit line, ticks, value and end labels, key, caption, note, source — at 0.93 of the base sizes (`grammar.K`). Funnel Display and Funnel Sans were the house faces until 2026-10-22. `grammar.features` asks for lining figures only: `tnum` widens Schibsted's punctuation. The unit after the big number is spaced from the number's ink, not its advance. Text is ink or muted only. 960×540 canvas, no dual axes. Change nothing about a chart's look anywhere else.

**Data.** CSVs are read from `../data/multi-year/` and `../sql/{design,performance}/`; see the data folder's `README.md` for provenance and methodology caveats.

**Anchor guard.** Figures whose numbers are quoted in the report text check the CSV against that number before drawing (`_anchor()` in `render.py`, default tolerance 0.2pp). If a source query changes underneath us, the figure is *not* drawn: `render.py` prints `STOP …` for it, renders the rest, and exits 1. Fix the query or move the prose — never widen the tolerance to make a chart appear.

**Years are never backfilled.** A category only appears for years it was actually measured (unique-URL format mix starts 2024; `font-display` uses 2022 / 2025 / 2026). Missing years are left out, not interpolated. F5 puts a marker on every measured year so the 2021 and 2023 gaps read as gaps.

**Environment.** `.venv/` is a local venv (matplotlib + pandas). Do not install into system python or `~/.venvs/fleet`; rebuild with `python3 -m venv .venv && ./.venv/bin/pip install matplotlib pandas`.

**Numbering.** Figures are numbered 1 to 9 in the order they appear in the draft (renumbered 2026-10-17 from 1, 4, 5, 6, 9, 7, 8, 10, 2). Output files are `fNN-<slug>` from that number, and `build_docx.py` finds each image by it. After a renumbering, delete the old `out/f*` files before rendering, or a stale `f02-…` will be picked up for the wrong chart.
