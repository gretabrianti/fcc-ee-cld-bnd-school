"""
Shared plot style: puma (https://github.com/umami-hep/puma) with the ATLAS
badge replaced by a "CLD Collaboration" one, dpi=200 everywhere, and no plot
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

DPI = 200

BRAND = "CLD"
FIRST_TAG = "Collaboration Simulation (toy)"

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
    map onto a puma plot type, e.g. bar/line charts)."""
    subtext = sqrt_s_tag(energy_gev) if energy_gev is not None else None
    if subtext_extra:
        subtext = subtext_extra if subtext is None else f"{subtext}\n{subtext_extra}"
    atlasify.atlasify(
        atlas=FIRST_TAG,
        subtext=subtext,
        brand=BRAND,
        axes=ax,
    )


def savefig(fig, path, dpi=DPI):
    fig.savefig(path, dpi=dpi, bbox_inches="tight", pad_inches=0.05)
