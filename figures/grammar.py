"""Chart grammar for "Fonts on the Web 2026".

The ONLY style file. Every figure in render.py draws through these helpers so
that frame, palette, type, canvas and the denominator rule stay in one place.

House style: Direction A "Specimen" frame with the A5 "Kettle" scheme
(approved 2026-10-02; prototype figures/proto/proto_a.py, variant 'a5').

  * Canvas 960x540 px (9.6 x 5.4 in @ 100 dpi); PNG 1600 px wide; SVG keeps
    live text (svg.fonttype none).
  * Frame: "Fig. N" + section tag, finding title, deck line, two hairline
    rules; a plot column and a margin column (hairline divider) that holds the
    key and ONE big number with a short caption; a source line at the foot.
  * Type (2026-10-22): one family, Schibsted Grotesk. Weight 600 sets the title,
    700 the big margin number, regular and 500 everything else (tag, deck, unit
    line, ticks, value labels, key, caption, note, source). Before that the house
    used Funnel Display and Funnel Sans (2026-10-02, pairing study v4).
    Text wears ink or muted only, never a series colour.
  * Exactly three series hues, in order: cobalt, cerise, violet. Desktop is
    always cobalt, mobile always cerise. Three-year comparisons colour the
    YEAR (earliest violet, middle cobalt, latest cerise) with categories on
    the axis. No stacks.
  * Every figure declares a denominator (required). It is named in the unit
    label above the plot, and written on the SVG root as data-denominator.
  * No dual axes, ever. save_figure() enforces this.
"""

from __future__ import annotations

import os
import re
import sys
import warnings
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import font_manager  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402
import matplotlib.patheffects as pe  # noqa: E402

# --------------------------------------------------------------------------
# Scheme: A5 Kettle, enamel panel
# --------------------------------------------------------------------------

# Frame polish (on since 2026-10-22): a stronger Figure N tag and the dek at y=96. The heavier
# top rule and the rule-to-rule divider were reversed on 2026-10-23; the rules and the divider
# are drawn as before. FIG_POLISH=0 draws the earlier frame; FIG_OUT redirects the output.
POLISH = os.environ.get("FIG_POLISH", "1") != "0"

GROUND = "#e7e9ee"   # Kettle panel
INK = "#181a23"
MUTED = "#5b5d66"
RULE = INK           # hairline rules and the plot baseline
GRID = "#bcbdc6"     # Kettle line: value gridlines

COBALT = "#2a5cda"   # slot 1 -- cobalt glaze
CERISE = "#ca363a"   # slot 2 -- cerise glaze
VIOLET = "#8a64ab"   # slot 3

# Exactly three hues (2026-10-02): no fourth Kettle colour clears cerise for
# colorblind readers. No figure may draw more than three series colours.
SERIES = [COBALT, CERISE, VIOLET]
DESKTOP, MOBILE = COBALT, CERISE
CLIENT_COLORS = {"desktop": DESKTOP, "mobile": MOBILE}
# Three-year comparisons: earliest violet, middle cobalt, latest cerise.
YEAR_COLORS = [VIOLET, COBALT, CERISE]


def year_colors(years):
    """{year: colour} for exactly three years, earliest -> latest."""
    years = sorted(years)
    if len(years) != 3:
        raise ValueError(f"year_colors takes exactly three years, got {years}")
    return dict(zip(years, YEAR_COLORS))

# --------------------------------------------------------------------------
# Canvas and layout (px on the 960x540 canvas, y measured from the top)
# --------------------------------------------------------------------------

FIG_W_IN, FIG_H_IN = 9.6, 5.4
W_PX, H_PX = 960, 540
SCREEN_DPI = 100
PNG_WIDTH_PX = 1600
PNG_DPI = PNG_WIDTH_PX / FIG_W_IN

L, R = 56, 904                 # text measure
PLOT_L, PLOT_R = 100, 640      # default plot column
MARGIN_L = 676                 # margin column
TOP_RULE, BOTTOM_RULE = 124, 480
PLOT_TOP, PLOT_BOTTOM = 172, 444


def px(x):
    """Horizontal pixels -> figure fraction."""
    return x / W_PX


def py(y_from_top):
    """Vertical pixels from the top -> figure fraction."""
    return 1 - y_from_top / H_PX


def pt(pixels):
    """Pixels on the 960x540 canvas -> points (matplotlib font sizes)."""
    return pixels * 72 / SCREEN_DPI


# --------------------------------------------------------------------------
# Type: Schibsted Grotesk (Google Fonts, fetched and cached by pyfonts)
# --------------------------------------------------------------------------


_FONT_FILES: dict = {}   # weight (400, 500, ...) -> font file, for measuring kerning


def _register(family, weights, italic=False, fallback="sans-serif") -> str:
    try:
        from pyfonts import load_google_font

        for weight in weights:
            path = load_google_font(family, weight=weight).get_file()
            font_manager.fontManager.addfont(path)
            _FONT_FILES[400 if weight == "regular" else int(weight)] = path
        if italic:
            font_manager.fontManager.addfont(
                load_google_font(family, weight="regular", italic=True).get_file()
            )
        return family
    except Exception as exc:  # pragma: no cover - offline with an empty cache
        print(f"WARNING: {family} unavailable ({exc}); falling back to {fallback}.", file=sys.stderr)
        return fallback


SANS = _register("Schibsted Grotesk", ("regular", 500, 600, 700), italic=True)
DISPLAY = SANS                 # title and big number are the same family at heavier weights
TITLE_WEIGHT = 600             # figure title (Funnel Display 500 until 2026-10-22)
NUMBER_WEIGHT = 700            # callout number and unit (Funnel Display 300 until 2026-10-22)

# Schibsted Grotesk sets about 5% taller x-height than Funnel Sans did at one size; K keeps
# the apparent size the figures were built with (it was 0.96 for Funnel Sans).
K = 0.93


def spt(pixels):
    """Body size: canvas pixels -> points, scaled by K."""
    return pt(pixels * K)


SIZE_TICKS = spt(12.5)
SIZE_LABEL = spt(12.5)    # direct labels on series
SIZE_VALUE = spt(12)      # small value labels on bars
SIZE_KEY = spt(13)


def features(texts, tags=("lnum",)) -> None:
    """Font features where the toolchain supports them.

    Lining figures always (not ``tnum``: in Schibsted Grotesk it also widens the punctuation,
    "73 . 9%"). Kerning is switched off on any text that holds a digit: the font's own kerning
    pulls "7." in by 287 units of 2048 and ".1" by 160, so "87.1%" collides. Text without
    digits keeps its kerning. matplotlib applies features to a whole text object, so a line
    of caption that contains a number loses kerning for its words too.
    """
    if hasattr(texts, "set_fontfeatures"):
        texts = [texts]
    for t in texts:
        use = list(tags)
        if any(ch.isdigit() for ch in t.get_text()):
            use.append("-kern")
        try:
            t.set_fontfeatures(use)
        except Exception:
            return


def install_rc() -> None:
    matplotlib.rcParams.update(
        {
            "figure.figsize": (FIG_W_IN, FIG_H_IN),
            "figure.dpi": SCREEN_DPI,
            "figure.facecolor": GROUND,
            "savefig.facecolor": GROUND,
            "savefig.edgecolor": GROUND,
            "axes.facecolor": GROUND,
            "font.family": SANS,
            "text.color": INK,
            "axes.labelcolor": INK,
            "xtick.labelcolor": INK,
            "ytick.labelcolor": INK,
            "lines.solid_capstyle": "round",
            "legend.frameon": False,
            "svg.fonttype": "none",  # keep text live in SVG
        }
    )


install_rc()

# --------------------------------------------------------------------------
# Denominators
# --------------------------------------------------------------------------

# Bare noun that must appear in the unit label for each denominator.
DENOMINATOR_NOUNS = {
    "pages": "pages",
    "requests": "font requests",
    "unique_urls": "font URLs",
    "files": "font files",
}


def _validate_denominator(denominator) -> str:
    if denominator not in DENOMINATOR_NOUNS:
        raise ValueError(
            f"A denominator is required; got {denominator!r}. Choose one of: "
            + ", ".join(sorted(DENOMINATOR_NOUNS))
        )
    return denominator


# --------------------------------------------------------------------------
# The frame
# --------------------------------------------------------------------------


def new_figure(number, section, title, deck, denominator, plot_l=PLOT_L, plot_r=PLOT_R,
               plot_top=PLOT_TOP, client_series=None):
    """Build the Specimen frame and return (fig, ax).

    ``denominator`` is REQUIRED (pages | requests | unique_urls | files).
    ``plot_l`` / ``plot_r`` move the plot column (e.g. for long category labels).
    """
    denominator = _validate_denominator(denominator)
    fig = plt.figure(figsize=(FIG_W_IN, FIG_H_IN), dpi=SCREEN_DPI, facecolor=GROUND)
    fig._almanac_denominator = denominator
    fig._almanac_clients = list(client_series or [])
    fig._almanac_unit = False

    tag = fig.text(px(L), py(30), f"Figure {number}", family=SANS,
                   size=spt(12.5 if POLISH else 13), color=INK, va="top",
                   weight=500 if POLISH else "normal")
    fig.canvas.draw()
    fig.text(tag.get_window_extent().x1 / fig.bbox.width + px(8), py(30), section, family=SANS,
             size=spt(13), color=MUTED, va="top")
    if POLISH:
        fig.add_artist(Rectangle((px(L), py(19)), px(28), 3 / H_PX, color=INK,
                                 transform=fig.transFigure, lw=0))
    fig.text(px(L), py(52), title, family=DISPLAY, weight=TITLE_WEIGHT, size=pt(30),
             color=INK, va="top")
    fig.text(px(L), py(96 if POLISH else 94), deck, family=SANS, size=spt(13.5), color=MUTED,
             va="top", linespacing=1.35)
    for y in (TOP_RULE, BOTTOM_RULE):
        fig.add_artist(Line2D([px(L), px(R)], [py(y), py(y)], color=RULE, lw=0.6,
                              transform=fig.transFigure))
    fig.add_artist(Line2D([px(MARGIN_L - 18)] * 2, [py(TOP_RULE + 22), py(BOTTOM_RULE - 22)],
                          color=RULE, lw=0.4, alpha=0.5, transform=fig.transFigure))

    ax = fig.add_axes([px(plot_l), py(PLOT_BOTTOM), px(plot_r - plot_l),
                       (PLOT_BOTTOM - plot_top) / H_PX], facecolor=GROUND)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(INK)
    ax.spines["bottom"].set_linewidth(0.8)
    ax.tick_params(length=0, labelsize=SIZE_TICKS, labelcolor=INK, pad=6)
    ax.set_axisbelow(True)
    return fig, ax


def unit_label(ax, text) -> None:
    """Italic unit line above the plot; must name the figure's denominator."""
    fig = ax.get_figure()
    noun = DENOMINATOR_NOUNS[fig._almanac_denominator]
    if noun not in text:
        raise ValueError(f"unit label {text!r} does not name its denominator ({noun!r})")
    fig.text(px(L), py(PLOT_TOP - 14), text, ha="left", va="bottom", family=SANS,
             style="italic", size=spt(12), color=MUTED)
    fig._almanac_unit = True


def _grid(ax, axis="y") -> None:
    (ax.yaxis if axis == "y" else ax.xaxis).grid(True, color=GRID, lw=0.6)


def percent_axis(ax, top, step, axis="y", bottom=0) -> None:
    """Whole-number value ticks (the unit line says 'percent'), gridlines in Kettle line."""
    ticks = list(range(bottom, top + 1, step))
    if axis == "y":
        ax.set_ylim(bottom, top)
        ax.set_yticks(ticks)
        ax.set_yticklabels([str(t) for t in ticks], family=SANS)
        features(ax.get_yticklabels())
    else:
        ax.set_xlim(bottom, top)
        ax.set_xticks(ticks)
        ax.set_xticklabels([str(t) for t in ticks], family=SANS)
        features(ax.get_xticklabels())
    ax.tick_params(axis=axis, labelcolor=MUTED)   # value ticks recede; year and row labels stay ink
    _grid(ax, axis)


def log_kb_axis(ax, ticks, lo, hi, grid_color=None) -> None:
    """Log-scaled x axis in kilobytes, labelled ticks only, vertical gridlines."""
    from matplotlib.ticker import FixedLocator, FuncFormatter, NullFormatter, NullLocator

    ax.set_xscale("log")
    ax.set_xlim(lo, hi)
    ax.xaxis.set_major_locator(FixedLocator(list(ticks)))
    ax.xaxis.set_major_formatter(
        FuncFormatter(lambda v, _pos: f"{v:,.0f} kB" if v >= max(ticks) else f"{v:,.0f}"))
    ax.xaxis.set_minor_locator(NullLocator())
    ax.xaxis.set_minor_formatter(NullFormatter())
    for t in ax.get_xticklabels():
        t.set_family(SANS)
    features(ax.get_xticklabels())
    ax.tick_params(axis="x", labelcolor=MUTED)
    ax.xaxis.grid(True, color=grid_color or GRID, lw=0.6)


def category_axis(ax, ticks, labels, axis="x") -> None:
    if axis == "x":
        ax.set_xticks(list(ticks))
        ax.set_xticklabels(list(labels), family=SANS)
        features(ax.get_xticklabels())
    else:
        ax.set_yticks(list(ticks))
        ax.set_yticklabels(list(labels), family=SANS)
        features(ax.get_yticklabels())


def year_axis(ax, years, step=1) -> None:
    """Integer year ticks laid out backwards from the latest year."""
    years = sorted(set(int(y) for y in years))
    ticks = [y for y in years if (years[-1] - y) % step == 0]
    category_axis(ax, ticks, [str(y) for y in ticks])


def horizontal(ax) -> None:
    """Value axis on x: baseline becomes the left spine, ticks move to the top."""
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(True)
    ax.spines["left"].set_color(INK)
    ax.spines["left"].set_linewidth(0.8)
    ax.xaxis.tick_top()


# --------------------------------------------------------------------------
# Marks and labels (text is ink or muted, never a series colour)
# --------------------------------------------------------------------------


def text(ax, x, y, s, color=INK, size=SIZE_VALUE, **kwargs):
    # In-plot labels knock out the gridlines they sit on (F5 p99 met the 1,000 line).
    kwargs.setdefault("bbox", dict(boxstyle="square,pad=0.12", fc=GROUND, ec="none"))
    t = ax.text(x, y, s, family=SANS, size=size, color=color, **kwargs)
    features(t)
    return t


def line(ax, x, y, client, color=None, markers=False):
    """One client series: desktop thinner beneath, mobile heavier on top.

    Mobile wears a ground-coloured halo so a crossing reads as one line passing over
    another. A gap of more than one year (a year not measured) is bridged by a dashed
    segment at the same colour and weight, never by a solid one.
    """
    col = color or CLIENT_COLORS[client]
    lw, z = (1.8, 3) if client == "desktop" else (2.2, 4)
    kw = dict(color=col, lw=lw, solid_capstyle="round", zorder=z)
    if client == "mobile":
        kw["path_effects"] = [pe.Stroke(linewidth=lw + 2.4, foreground=GROUND), pe.Normal()]
    if markers:
        kw.update(marker="o", markersize=4.6, markeredgecolor=GROUND, markeredgewidth=1.0)
    xs, ys = [float(v) for v in x], [float(v) for v in y]
    runs = [[0]]
    for i in range(1, len(xs)):
        if xs[i] - xs[i - 1] > 1.5:
            runs.append([i])
        else:
            runs[-1].append(i)
    for run in runs:
        ax.plot([xs[i] for i in run], [ys[i] for i in run], **kw)
    for a, b in zip(runs, runs[1:]):
        bridge = {k: v for k, v in kw.items() if k not in ("marker", "markersize", "markeredgecolor",
                                                            "markeredgewidth", "solid_capstyle")}
        ax.plot([xs[a[-1]], xs[b[0]]], [ys[a[-1]], ys[b[0]]], dashes=(2.6, 2.0),
                dash_capstyle="butt", **bridge)


def grid_to(ax, x_end, pad_px=14):
    """Horizontal gridlines that stop just past the last data point, so the label
    gutter on the right carries no grid. Call after the x limits are final."""
    ax.yaxis.grid(False)
    lo, hi = ax.get_xlim()
    stop = min(hi, x_end + pad_px * _data_per_px(ax, "x"))
    for t in ax.get_yticks():
        ax.hlines(t, lo, stop, color=GRID, lw=0.6, zorder=0.5)


def end_dot(ax, x, y, client, color=None, front=False):
    ax.scatter([x], [y], s=22 if client == "desktop" else 26, color=color or CLIENT_COLORS[client],
               zorder=6 if front else 5, edgecolor=GROUND, linewidth=1.6)


def _data_per_px(ax, axis="y"):
    fig = ax.get_figure()
    bbox = ax.get_position()
    if axis == "y":
        lo, hi = ax.get_ylim()
        return (hi - lo) / (bbox.height * fig.bbox.height / fig.dpi * SCREEN_DPI)
    lo, hi = ax.get_xlim()
    return (hi - lo) / (bbox.width * fig.bbox.width / fig.dpi * SCREEN_DPI)


def spread(ys, min_gap):
    """Nudge sorted label positions apart by at least min_gap, re-centred on the mean."""
    order = sorted(range(len(ys)), key=lambda i: ys[i])
    placed = [ys[i] for i in order]
    for i in range(1, len(placed)):
        placed[i] = max(placed[i], placed[i - 1] + min_gap)
    shift = (sum(ys) - sum(placed)) / len(placed)
    out = [0.0] * len(ys)
    for i, p in zip(order, placed):
        out[i] = p + shift
    return out


def end_labels(ax, entries, dx, min_gap_px=18, size=SIZE_LABEL, color=INK, colors=None):
    """Direct labels at series ends. entries = [(x, y, text)]; set ylim first.

    ``colors`` (one per entry) puts a short series-colour line sample before each label,
    so colour and name pair up while the text stays ink."""
    gap = min_gap_px * _data_per_px(ax, "y")
    ys = spread([e[1] for e in entries], gap)
    dpx = _data_per_px(ax, "x")
    shift = 16 * dpx if colors else 0.0
    out = []
    for k, ((x, _, s), y) in enumerate(zip(entries, ys)):
        if colors:
            ax.plot([x + dx, x + dx + 12 * dpx], [y, y], color=colors[k], lw=2.4,
                    solid_capstyle="butt", zorder=6, clip_on=False)
        out.append(text(ax, x + dx + shift, y, s, color=color, size=size, va="center"))
    return out


def columns(ax, x, series, width, gap, label_years=None, pad_px=4):
    """Clustered columns. series = [(values, color)]; label first and last year
    (muted for the first, ink for the latest) unless ``label_years`` says otherwise."""
    n = len(series)
    offsets = [(i - (n - 1) / 2) * (width + gap) for i in range(n)]
    pad = pad_px * _data_per_px(ax, "y")
    idx = label_years if label_years is not None else (0, len(x) - 1)
    for (values, color), off in zip(series, offsets):
        ax.bar([xi + off for xi in x], values, width=width, color=color, zorder=3, linewidth=0)
        for i in idx:
            latest = i == len(x) - 1
            text(ax, x[i] + off, values[i] + pad, f"{values[i]:.1f}", ha="center", va="bottom",
                 color=INK if latest else MUTED, weight=500 if latest else "normal")


def year_groups(ax, x, series, width, gap, label=None, pad_px=4):
    """Grouped columns, one bar per year inside each category.

    series = [(values, color)] earliest -> latest year. The latest year is
    labelled at every category (ink); ``label(s, i)`` may add earlier-year
    labels (muted) for series s at category i where they do not crowd.
    """
    n = len(series)
    offsets = [(s - (n - 1) / 2) * (width + gap) for s in range(n)]
    pad = pad_px * _data_per_px(ax, "y")
    for s, ((values, color), off) in enumerate(zip(series, offsets)):
        ax.bar([xi + off for xi in x], values, width=width, color=color, zorder=3, linewidth=0)
        latest = s == n - 1
        for i, xi in enumerate(x):
            if latest or (label is not None and label(s, i)):
                text(ax, xi + off, values[i] + pad, f"{values[i]:.1f}", ha="center", va="bottom",
                     color=INK if latest else MUTED, weight=500 if latest else "normal")


# --------------------------------------------------------------------------
# Margin column: key and the one big number
# --------------------------------------------------------------------------


def margin_key(fig, entries, y=None, marker="square"):
    """Glossary key at the head of the margin column. entries = [(label, color)].
    Returns the y (px from top) just below the key."""
    y = TOP_RULE + 26 if y is None else y
    for label, color in entries:
        if marker == "dot":
            fig.add_artist(Line2D([px(MARGIN_L + 5.5)], [py(y + 10.5)], marker="o", markersize=7,
                                  color=color, lw=0, transform=fig.transFigure))
        else:
            fig.add_artist(Rectangle((px(MARGIN_L), py(y + 16)), px(11), 11 / H_PX,
                                     color=color, transform=fig.transFigure, lw=0))
        fig.text(px(MARGIN_L + 20), py(y), label, family=SANS, size=SIZE_KEY, color=INK, va="top")
        y += 22
    return y


def _ink_right_px(s, size_px, weight=NUMBER_WEIGHT) -> float:
    """Right edge of the inked glyphs (not the advance), in canvas pixels."""
    from matplotlib.font_manager import FontProperties
    from matplotlib.textpath import TextPath

    path = TextPath((0, 0), s, size=pt(size_px), prop=FontProperties(family=DISPLAY, weight=weight))
    return path.get_extents().x1 * SCREEN_DPI / 72 + _kern_loss_px(s, size_px, weight)


def _kern_loss_px(s, size_px, weight) -> float:
    """Width added by switching kerning off (``features`` does that for text with digits).

    TextPath measures the kerned string; the figure draws it unkerned, so the unit that
    follows a number would sit too far left. This is the difference, in canvas pixels."""
    path = _FONT_FILES.get(int(weight))
    if not path or not any(ch.isdigit() for ch in s):
        return 0.0
    try:
        from PIL import ImageFont

        font = ImageFont.truetype(path, 2048, layout_engine=ImageFont.Layout.RAQM)
        return (font.getlength(s, features=["-kern"]) - font.getlength(s)) / 2048 * size_px
    except Exception:  # pragma: no cover - PIL without raqm
        return 0.0


def _number_gap(size_px):
    return 5 * size_px / 70


def _fit_number(fig, number, unit, size_px, room_px):
    """Largest size <= size_px at which number + unit fits the margin column."""
    while size_px > 30:
        w = _ink_right_px(number, size_px) + _number_gap(size_px) \
            + _ink_right_px(unit, size_px * 0.4) + 4
        if w <= room_px:
            return size_px
        size_px -= 2
    return size_px


def _bind_last(s):
    """No one-word last line: bind the last two words with a no-break space."""
    head, _, tail = s.rpartition(" ")
    return f"{head}\u00a0{tail}" if head else s


def wrap_px(fig, s, width_px, **props):
    """Greedy word wrap measured in canvas pixels (never breaks on hyphens)."""
    renderer = fig.canvas.get_renderer()
    probe = fig.text(0, 0, "", **props)
    lines, cur = [], ""
    for word in s.split(" "):  # NBSP (\u00a0) binds a number to its unit
        trial = f"{cur} {word}".strip()
        probe.set_text(trial)
        if cur and probe.get_window_extent(renderer).width * SCREEN_DPI / fig.dpi > width_px:
            lines.append(cur)
            cur = word
        else:
            cur = trial
    if cur:
        lines.append(cur)
    probe.remove()
    return "\n".join(lines)


def _bottom_px(fig, artist):
    fig.canvas.draw()
    return (fig.bbox.height - artist.get_window_extent().y0) * SCREEN_DPI / fig.dpi


# Callout sizing (2026-10-20). Each graphic's callout is sized to fill its margin column:
# the big number takes the widest size that fits, the caption (the takeaway) takes the
# largest size that still fits beneath it, and the note stays visibly smaller than the
# caption, so size carries the hierarchy. Sizes are px on the 960x540 canvas.
NUMBER_MAX, NUMBER_MIN = 120, 52
CAPTION_MAX, CAPTION_MIN = 21.0, 15.0
NOTE_MIN, NOTE_RATIO = 12.5, 1.3          # note = caption / 1.3, never under 12.5
CAPTION_PITCH, NOTE_PITCH = 1.3, 1.35      # fixed baseline-to-baseline pitch, times the rendered size


def _set_lines(fig, block, y_px, pitch_px, color, **props):
    """One fig.text per wrapped line at a fixed baseline pitch; returns (artists, bottom_px).

    A multi-line matplotlib text sets each line from its own glyph height, so the pitch
    wobbles. Here the first baseline is ``y_px`` and every later one is ``pitch_px`` lower."""
    arts = []
    for i, ln in enumerate(block.split("\n")):
        t = fig.text(px(MARGIN_L), py(y_px + i * pitch_px), ln, color=color, va="baseline", **props)
        features(t)
        arts.append(t)
    return arts, _bottom_px(fig, arts[-1])


def _draw_callout(fig, number, unit, caption, note, y, size_px, cap_px):
    """Draw one candidate callout; return (artists, bottom_px)."""
    k = size_px / 70
    width = R - MARGIN_L - 6
    art = [fig.text(px(MARGIN_L), py(y), number, family=DISPLAY, weight=NUMBER_WEIGHT,
                    size=pt(size_px), color=INK, va="top")]
    features(art[0])
    unit_x = MARGIN_L + _ink_right_px(number, size_px) + _number_gap(size_px)
    art.append(fig.text(px(unit_x), py(y + 16 * k), unit, family=DISPLAY, weight=NUMBER_WEIGHT,
                        size=pt(28 * k), color=INK, va="top"))
    features(art[1])
    props = dict(family=SANS, size=spt(cap_px))
    cap_arts, bottom = _set_lines(fig, wrap_px(fig, _bind_last(caption), width, **props),
                                  y + 92 * k + 0.95 * cap_px * K, CAPTION_PITCH * cap_px * K, INK, **props)
    art += cap_arts
    if note:
        note_px = max(NOTE_MIN, cap_px / NOTE_RATIO)
        nprops = dict(family=SANS, style="italic", size=spt(note_px))
        n_arts, bottom = _set_lines(fig, wrap_px(fig, _bind_last(note), width, **nprops),
                                    bottom + 0.9 * cap_px + 0.95 * note_px * K,
                                    NOTE_PITCH * note_px * K, MUTED, **nprops)
        art += n_arts
    return art, bottom


def margin_number(fig, number, unit, caption, note=None, y=None, size_px=None):
    """ONE big number in the margin column, a caption under it, an optional note.

    Sized per graphic to fill the column: the number is Schibsted Grotesk Bold at the
    widest size that fits (at most ``size_px`` if given, else NUMBER_MAX); the caption is
    the largest size from CAPTION_MAX down to CAPTION_MIN that fits beneath it; the note
    is smaller than the caption. If nothing fits, the number shrinks a step and the
    search repeats, down to NUMBER_MIN; then the build stops. The unit is spaced from
    the number's ink, not its advance, so open figures (7) do not leave a hole.
    """
    y = TOP_RULE + 24 if y is None else y
    limit = BOTTOM_RULE - 14
    size = _fit_number(fig, number, unit, NUMBER_MAX if size_px is None else size_px, R - MARGIN_L)
    while size >= NUMBER_MIN:
        cap_px = CAPTION_MAX
        while cap_px >= CAPTION_MIN:
            art, bottom = _draw_callout(fig, number, unit, caption, note, y, size, cap_px)
            if bottom <= limit:
                return
            for a in art:
                a.remove()
            cap_px -= 0.5
        size -= 4
    raise ValueError(f"margin callout cannot fit the column: {caption!r} / {note!r}")


def source_note(fig, text) -> None:
    """Source line under the bottom rule, full measure; two lines at most.

    Steps the size down (to 11 px at the least) rather than leave a widow of
    one or two words on the second line.
    """
    size_px = 12 * K
    while True:
        props = dict(family=SANS, size=pt(size_px))
        body = wrap_px(fig, text, R - L - 8, **props)
        lines = body.split("\n")
        widow = len(lines) == 2 and len(lines[1].split()) < 3
        if (len(lines) <= 2 and not widow) or size_px <= 11.0:
            break
        size_px -= 0.25
    if len(lines) > 2:
        raise ValueError(f"source line runs past two lines: {text!r}")
    t = fig.text(px(L), py(BOTTOM_RULE + 10), body, color=MUTED, va="top", linespacing=1.25, **props)
    features(t)


# --------------------------------------------------------------------------
# Saving
# --------------------------------------------------------------------------

_SVG_ROOT_RE = re.compile(r"<svg\b[^>]*>", re.DOTALL)


def _assert_no_dual_axes(fig) -> None:
    boxes = []
    for ax in fig.axes:
        b = ax.get_position()
        key = (round(b.x0, 4), round(b.y0, 4), round(b.x1, 4), round(b.y1, 4))
        if key in boxes:
            raise ValueError("Dual axes detected: the house grammar forbids twinned axes.")
        boxes.append(key)


def _inject_svg_denominator(path: Path, denominator: str) -> None:
    markup = path.read_text(encoding="utf-8")
    match = _SVG_ROOT_RE.search(markup)
    if not match:
        raise ValueError(f"Could not find an <svg> root element in {path}")
    root = match.group(0)
    if "data-denominator=" in root:
        new_root = re.sub(r'data-denominator="[^"]*"', f'data-denominator="{denominator}"', root)
    else:
        new_root = root[:-1].rstrip() + f' data-denominator="{denominator}">'
    path.write_text(markup[: match.start()] + new_root + markup[match.end():], "utf-8")


def save_figure(fig, number, slug, out_dir=None) -> tuple[Path, Path]:
    """Write out/fNN-<slug>.svg (live text) and .png (1600 px wide)."""
    denominator = getattr(fig, "_almanac_denominator", None)
    if denominator is None:
        raise ValueError("Figure was not built with new_figure(); no denominator recorded.")
    if not getattr(fig, "_almanac_unit", False):
        raise ValueError("Figure has no unit_label(); the denominator must be named on the plot.")
    _assert_no_dual_axes(fig)

    out_dir = Path(out_dir or os.environ.get("FIG_OUT") or Path(__file__).resolve().parent / "out")
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = f"f{int(number):02d}-{slug}"
    svg_path, png_path = out_dir / f"{stem}.svg", out_dir / f"{stem}.png"
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        fig.savefig(svg_path, format="svg", dpi=SCREEN_DPI)
        fig.savefig(png_path, format="png", dpi=PNG_DPI)
    _inject_svg_denominator(svg_path, denominator)
    plt.close(fig)
    return svg_path, png_path
