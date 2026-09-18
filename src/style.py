"""
Shared plot style: puma (https://github.com/umami-hep/puma) with the ATLAS
badge replaced by a "CLD Collaboration" one, dpi=300 everywhere, and no plot
titles (only axis labels/legends -- titles are set to "").

puma is built on top of `atlasify`; every `PlotObject` (HistogramPlot,
VarVsEffPlot, ...) accepts `atlas_brand`/`atlas_first_tag`/`atlas_second_tag`
which we repoint at CLD here. For the handful of plots that don't map onto a
puma plot type (plain bar/line charts) `cld_atlasify()` calls the same
underlying `atlasify` package directly, so every figure in this repo -- puma
or not -- carries the same badge.
"""
from __future__ import annotations

import atlasify

DPI = 300

BRAND = "CLD"
FIRST_TAG = "Collaboration Simulation (toy)"

# puma's own PlotObject defaults atlas_fontsize to `fontsize=10` (see
# puma/plot_base.py __post_init__), well below atlasify's own out-of-the-box
# defaults (16/16/12, tuned for full-page ATLAS figures). cld_atlasify()
# matches puma's 10pt badge explicitly so every figure in this repo -- puma
# histograms and plain-matplotlib bar/line charts alike -- carries the same
# badge size, regardless of figure size.
BADGE_FONTSIZE = 10
BADGE_OFFSET = 7
BADGE_INDENT = 8

PALETTE = {
    "X1": "#3B75AF",
    "X2": "#59A14F",
    "X3": "#A0522D",
    "X4": "#8C8C8C",
    "X5": "#57C2CC",
    "data": "#000000",
    "h0": "#3B75AF",
    "h1": "#E15759",
}


def sqrt_s_tag(energy_gev) -> str:
    return rf"$\sqrt{{s}}$ = {energy_gev} GeV"


def puma_kwargs(energy_gev, **extra):
    """Common kwargs for any puma PlotObject (HistogramPlot, VarVsEffPlot, ...)."""
    kwargs = dict(
        title="",
        atlas_brand=BRAND,
        atlas_first_tag=FIRST_TAG,
        atlas_second_tag=sqrt_s_tag(energy_gev) if energy_gev is not None else None,
        use_atlas_tag=True,
        apply_atlas_style=True,
        dpi=DPI,
    )
    kwargs.update(extra)
    return kwargs


def cld_atlasify(ax, energy_gev=None, subtext_extra=None):
    """Apply the CLD badge to a plain matplotlib Axes (for plots that don't
    map onto a puma plot type, e.g. bar/line charts), at the same size puma
    uses for its own histogram/efficiency plots (see BADGE_FONTSIZE above).
    """
    subtext = sqrt_s_tag(energy_gev) if energy_gev is not None else None
    if subtext_extra:
        subtext = subtext_extra if subtext is None else f"{subtext}\n{subtext_extra}"
    atlasify.atlasify(
        atlas=FIRST_TAG,
        subtext=subtext,
        brand=BRAND,
        axes=ax,
        font_size=BADGE_FONTSIZE,
        label_font_size=BADGE_FONTSIZE,
        sub_font_size=BADGE_FONTSIZE,
        offset=BADGE_OFFSET,
        indent=BADGE_INDENT,
    )


def annotate_note(ax, text):
    """Place a short note just under the CLD / sqrt(s) badge (top-left),
    left-aligned, no box, same font as the rest of the axis text -- reads as
    a third line of the badge. Used for chi2/ndof values and other small
    per-plot facts (e.g. an observed event count) that belong next to the
    badge rather than floating elsewhere on the figure.
    """
    ax.text(
        0.02, 0.84, text,
        transform=ax.transAxes, fontsize=BADGE_FONTSIZE, va="top", ha="left",
    )


annotate_chi2 = annotate_note  # backward-compatible alias


def savefig(fig, path, dpi=DPI):
    fig.savefig(path, dpi=dpi, bbox_inches="tight", pad_inches=0.05)
