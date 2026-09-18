"""Shared matplotlib style, loosely echoing the FCE plot look used in the talk
(bold "FCE" tag top-left, "CLD, sqrt(s) = ... GeV" top-right) so figures are
visually consistent with the presentation, without depending on the `fce`
package itself.
"""
from __future__ import annotations

import matplotlib.pyplot as plt

PALETTE = ["#3B75AF", "#59A14F", "#A0522D", "#8C8C8C", "#57C2CC", "#E15759"]


def apply_base_style():
    plt.rcParams.update(
        {
            "figure.dpi": 150,
            "savefig.dpi": 150,
            "font.size": 11,
            "axes.labelsize": 11,
            "axes.titlesize": 12,
            "legend.fontsize": 9,
            "xtick.labelsize": 9,
            "ytick.labelsize": 9,
            "axes.linewidth": 1.0,
            "axes.titlepad": 12,
            "figure.facecolor": "white",
            "savefig.facecolor": "white",
        }
    )


def fce_header(ax, energy_gev, tag="FCE (toy, synthetic)"):
    ax.text(
        0.0,
        1.10,
        tag,
        transform=ax.transAxes,
        fontsize=11,
        fontweight="bold",
        va="bottom",
        ha="left",
    )
    ax.text(
        1.0,
        1.10,
        rf"CLD, $\sqrt{{s}}$ = {energy_gev} GeV",
        transform=ax.transAxes,
        fontsize=10,
        va="bottom",
        ha="right",
    )
