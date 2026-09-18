"""
Task A interpretation: Standard Model samples.

Produces, under figures/sm/:
  01_cutflow_160GeV.png       cutflow tables for the two 160 GeV SM processes
  02_cutflow_365GeV.png       cutflow tables for the five 365 GeV SM processes
  03_massplots_160_365.png    toy mass spectra compared to the slide-quoted peaks
  04_cross_energy_consistency.png
                               lepton-pt and b-tag(>0.7) cut efficiencies,
                               extracted independently at 160 GeV and 365 GeV,
                               shown to be statistically compatible -- these
                               are detector-level quantities and should not
                               depend on sqrt(s)
  05_gap_91GeV.png            expected Z-pole process mix, mapped as a
                               *hypothesis* onto the X1-X5 pie chart on slide 6
                               (Task A was never actually carried out for this
                               energy point in the talk)
  06_gap_240GeV.png           expected ZH-run process mix (Task A is entirely
                               missing for this energy point in the talk)
  07_sm_completeness_check.png
                               stacked SM toy prediction vs. the BSM excesses
                               claimed in Task B, at 91 and 365 GeV, showing
                               the excesses sit above a fully-accounted SM sum

All normalisations are toy-level (arbitrary units calibrated to the
approximate bin heights visible in the presentation's histograms), not
absolute cross-sections read from a generator. See notes/process_mapping.md
for the full reasoning and the assumptions that a human should double-check.
"""
from __future__ import annotations

import os

import matplotlib.pyplot as plt
import numpy as np

from style import apply_base_style, fce_header, PALETTE
from toygen import (
    cutflow,
    compatibility_pull,
    gaussian_resonance,
    relativistic_bw_resonance,
    combinatorial_background,
    rng,
)

FIGDIR = os.path.join(os.path.dirname(__file__), "..", "figures", "sm")
os.makedirs(FIGDIR, exist_ok=True)


# ---------------------------------------------------------------------------
# 1) Cutflow tables, built from the cut definitions quoted in the slides.
#    Per-cut efficiencies are assumptions where the talk gives no number
#    (flagged with a trailing "*"), and taken directly from the talk where it
#    does (91 GeV: 20.9% dilepton inclusive selection; 160 GeV: 1.8% WWgamma
#    candidate selection).
# ---------------------------------------------------------------------------

CUTFLOWS_160 = {
    "Higgs production (nu-nu H, H->bb)": [
        ("preselection", 1.0),
        ("2 jets, b-tag>0.7 *", 0.55),
        ("0 leptons *", 0.85),
        ("MET pt cut *", 0.70),
    ],
    "WW production (semileptonic)": [
        ("preselection", 1.0),
        ("2 jets *", 0.80),
        ("1 lepton *", 0.60),
        ("MET pt > 5 GeV *", 0.90),
    ],
}

CUTFLOWS_365 = {
    "ttbar production": [
        ("preselection", 1.0),
        (">=2 leptons *", 0.35),
        (">=4 jets, b-tag>0.7 *", 0.45),
        ("lepton pt > 20 *", 0.85),
        ("MET pt > 20 *", 0.80),
    ],
    "e+e- -> ff (Z/gamma*)": [
        ("preselection", 1.0),
        (">=2 leptons *", 0.40),
        (">=4 jets, b-tag<0.7 (lead 2) *", 0.50),
        ("lepton pt > 20 *", 0.85),
        ("80 < m(l1,l2) < 100 *", 0.60),
    ],
    "ZZ -> ll qq (X5, t/u-channel e+-)": [
        ("preselection", 1.0),
        (">=2 leptons *", 0.45),
        (">=2 jets, b-tag<0.7 *", 0.55),
        ("lepton/jet pt > 20 *", 0.85),
        ("Z-veto (l1,l2) *", 0.55),
        ("MET pt < 20 *", 0.75),
    ],
    "ZH production": [
        ("preselection", 1.0),
        (">=2 leptons *", 0.30),
        (">=2 jets, b-tag>0.7 *", 0.50),
        ("lepton/jet pt > 20 *", 0.85),
        ("80 < m(l1,l2) < 100 *", 0.60),
        ("MET pt < 10 *", 0.70),
    ],
    "WW production (365 GeV selection)": [
        ("preselection", 1.0),
        (">=0 leptons *", 1.0),
        (">=2 jets, b-tag<0.7 *", 0.65),
        ("lepton/jet pt > 20 *", 0.80),
    ],
}

# Numbers explicitly quoted in the talk (used as external validation points,
# not fitted to).
QUOTED = {
    "91 GeV dilepton-inclusive selection": 0.209,
    "160 GeV WWgamma-like (2jet+photon) selection": 0.018,
}


def render_cutflow_table(cutflow_dict, energy_gev, outpath, n_start=1000.0):
    apply_base_style()
    n_proc = len(cutflow_dict)
    fig, axes = plt.subplots(n_proc, 1, figsize=(9, 2.1 * n_proc + 1.0))
    if n_proc == 1:
        axes = [axes]
    for ax, (proc_name, cuts) in zip(axes, cutflow_dict.items()):
        rows = cutflow(n_start, cuts)
        cell_text = [
            [r["cut"], f"{r['n_pass']:.0f}", f"{100*r['rel_eff']:.1f}%", f"{100*r['cum_eff']:.1f}%"]
            for r in rows
        ]
        ax.axis("off")
        ax.set_title(proc_name, fontsize=11, fontweight="bold", loc="left", pad=10)
        tbl = ax.table(
            cellText=cell_text,
            colLabels=["cut", "N pass (toy, N0=1000)", "rel. eff.", "cum. eff."],
            colWidths=[0.42, 0.24, 0.17, 0.17],
            loc="center",
            cellLoc="center",
        )
        tbl.auto_set_font_size(False)
        tbl.set_fontsize(9)
        tbl.scale(1, 1.4)
    fig.suptitle(
        f"Cutflow, sqrt(s) = {energy_gev} GeV  (* = efficiency assumed, not quoted in the talk)",
        fontsize=10,
    )
    fig.subplots_adjust(hspace=0.9, top=0.94, bottom=0.02)
    fig.savefig(outpath)
    plt.close(fig)


# ---------------------------------------------------------------------------
# 2) Toy mass spectra, anchored to the approximate peak positions/widths
#    read off the histograms in the talk.
# ---------------------------------------------------------------------------

def make_mass_plots(outpath):
    apply_base_style()
    fig, axes = plt.subplots(2, 3, figsize=(15, 8))

    specs = [
        ("Higgs (160 GeV)\nm(J1,J2)", relativistic_bw_resonance(4000, 125, 4.1, 8, 1), (60, 160), 160),
        ("WW (160 GeV)\nm(l1,MET,J1,J2)", relativistic_bw_resonance(6000, 153, 2.0, 6, 2), (120, 180), 160),
        ("ttbar (365 GeV)\n(j1+met+l1).mass", relativistic_bw_resonance(5000, 178, 1.4, 20, 3), (0, 400), 365),
        ("e+e->ff (365 GeV)\n(j1+j2).mass", combinatorial_background(4000, 0, 250, 60, 4), (0, 400), 365),
        ("ZZ->llqq X5 (365 GeV)\n(j1+j2).mass", relativistic_bw_resonance(9000, 91, 2.5, 6, 5), (0, 400), 365),
        ("W in HNL chain (365 GeV)\n(j2+j3).mass", relativistic_bw_resonance(3000, 80.4, 2.1, 10, 6), (0, 200), 365),
    ]
    for ax, (title, sample, xrange, e) in zip(axes.flat, specs):
        sample = sample[(sample > xrange[0]) & (sample < xrange[1])]
        ax.hist(sample, bins=40, range=xrange, color=PALETTE[0], alpha=0.85)
        ax.set_title(f"{title}  (sqrt(s)={e} GeV)", fontsize=10)
        ax.set_xlabel("mass [GeV]")
        ax.set_ylabel("toy events / bin")
    fig.suptitle("FCE (toy, synthetic)  --  reconstructed mass observables from the talk",
                 fontsize=12, fontweight="bold", x=0.02, ha="left")
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(outpath)
    plt.close(fig)


# ---------------------------------------------------------------------------
# 3) Cross-energy consistency of *detector-level* cut efficiencies.
#    These toys are built from the same underlying efficiency model at both
#    energies (only kinematics/boost differ), so agreement is expected by
#    construction -- the point is to show the METHOD the team should apply to
#    their real fce cutflow numbers once extracted, and to make explicit that
#    lepton pt>20 and b-tag>0.7 acceptances are supposed to be sqrt(s)-independent.
# ---------------------------------------------------------------------------

def cross_energy_consistency(outpath):
    apply_base_style()

    true_lepton_eff, true_lepton_eff_unc = 0.85, 0.02
    true_btag_eff, true_btag_eff_unc = 0.75, 0.02

    g160 = rng(10)
    g365 = rng(11)
    n_toy = 500
    lep_eff_160 = np.clip(g160.normal(true_lepton_eff, true_lepton_eff_unc, n_toy), 0, 1).mean()
    lep_eff_365 = np.clip(g365.normal(true_lepton_eff, true_lepton_eff_unc, n_toy), 0, 1).mean()
    btag_eff_160 = np.clip(g160.normal(true_btag_eff, true_btag_eff_unc, n_toy), 0, 1).mean()
    btag_eff_365 = np.clip(g365.normal(true_btag_eff, true_btag_eff_unc, n_toy), 0, 1).mean()

    stat_unc = true_lepton_eff_unc  # same order for both quantities here

    pull_lep = compatibility_pull(lep_eff_160, stat_unc, lep_eff_365, stat_unc)
    pull_btag = compatibility_pull(btag_eff_160, stat_unc, btag_eff_365, stat_unc)

    fig, ax = plt.subplots(figsize=(7, 5))
    labels = ["lepton pt>20 eff.", "b-tag>0.7 eff."]
    x = np.arange(len(labels))
    width = 0.32
    ax.bar(x - width / 2, [lep_eff_160, btag_eff_160], width, yerr=stat_unc,
           label="160 GeV toy", color=PALETTE[0], capsize=4)
    ax.bar(x + width / 2, [lep_eff_365, btag_eff_365], width, yerr=stat_unc,
           label="365 GeV toy", color=PALETTE[2], capsize=4)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel("efficiency")
    ax.set_ylim(0, 1.15)
    ax.set_title("Cross-energy consistency (toy)")
    ax.text(
        0.02, 0.95,
        f"pull(lepton) = {pull_lep:.2f}$\\sigma$\npull(b-tag) = {pull_btag:.2f}$\\sigma$",
        transform=ax.transAxes, fontsize=9, va="top",
        bbox=dict(boxstyle="round", fc="white", ec="gray"),
    )
    ax.legend(loc="upper right", bbox_to_anchor=(0.98, 0.80))
    fce_header(ax, "160 & 365")
    fig.tight_layout()
    fig.savefig(outpath)
    plt.close(fig)
    return dict(
        lep_eff_160=lep_eff_160, lep_eff_365=lep_eff_365,
        btag_eff_160=btag_eff_160, btag_eff_365=btag_eff_365,
        pull_lep=pull_lep, pull_btag=pull_btag,
    )


# ---------------------------------------------------------------------------
# 4) Gap fillers for 91 GeV and 240 GeV: Task A was never carried out for
#    these energies in the talk. These panels are *expected* compositions
#    from standard FCC-ee Z-pole / ZH-run physics, explicitly not fitted to
#    or extracted from any data, meant as a checklist for the team.
# ---------------------------------------------------------------------------

def gap_panel_91(outpath):
    apply_base_style()
    # Hypothesis mapping onto the slide-6 pie chart fractions (X1=45%, X2=30%,
    # X3=15%, X4=8%, X5=2%), reasoned from cross-section hierarchy at the Z
    # pole and from X1 dominating the "Dilepton" sub-selection (82%) -- see
    # notes/process_mapping.md for the argument.
    labels = ["X1: Bhabha e+e-(gamma)\n(t-channel, dominates\ndilepton selection)",
              "X2: Z -> qqbar\n(hadronic, absent from\ndilepton selection)",
              "X3: Z -> mumu/tautau\n(genuine leptonic Z)",
              "X4: gamma-gamma ->\nhadrons (low activity)",
              "X5: rare leptonic Z\nflavour / other"]
    fractions = [45, 30, 15, 8, 2]
    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.barh(labels, fractions, color=PALETTE[:5])
    ax.set_xlabel("hypothesised fraction of total sample [%]")
    ax.set_title(
        "91 GeV: Task A not carried out in the talk (hypothesis only, not a claim)",
        fontsize=10,
    )
    fce_header(ax, 91)
    fig.tight_layout(rect=[0, 0, 1, 0.88])
    fig.savefig(outpath)
    plt.close(fig)


def gap_panel_240(outpath):
    apply_base_style()
    labels = ["ZH signal\n(e+e- -> ZH)", "WW\n(background)", "e+e- -> ff / ZZ\n(background)"]
    fractions = [15, 55, 30]  # illustrative hierarchy only, NOT extracted from data
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.bar(labels, fractions, color=PALETTE[:3])
    ax.set_ylabel("expected fraction [%] (illustrative)")
    ax.set_title(
        "240 GeV: Task A entirely missing from the talk (expected mix only)",
        fontsize=10,
    )
    fce_header(ax, 240)
    fig.tight_layout(rect=[0, 0, 1, 0.88])
    fig.savefig(outpath)
    plt.close(fig)


# ---------------------------------------------------------------------------
# 5) SM-completeness check behind the Task-B excesses.
# ---------------------------------------------------------------------------

def sm_completeness_check(outpath):
    apply_base_style()
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    # 91 GeV: m(J1,l1) tail, SM stack vs reported excess shape (slide 14)
    ax = axes[0]
    bins = np.linspace(8, 62, 12)
    sm_stack = np.array([0.2, 0.2, 0.2, 0.3, 0.3, 0.3, 0.3, 0.3, 0.2, 0.1, 0.1])
    excess = np.array([1, 1, 2, 5, 6, 7, 2, 2, 3, 3])
    centers = 0.5 * (bins[:-1] + bins[1:])
    ax.bar(centers, sm_stack, width=(bins[1] - bins[0]), color=PALETTE[1],
           alpha=0.85, label="summed SM toy prediction")
    ax.errorbar(centers[: len(excess)], excess, yerr=np.sqrt(excess), fmt="o",
                color="black", label="reported pseudo-data (slide 14)")
    ax.set_xlabel("m(J1, l1) [GeV]")
    ax.set_ylabel("events / bin (toy)")
    ax.set_title("91 GeV: excess sits above summed SM prediction")
    ax.legend(fontsize=8)

    # 365 GeV: total system mass, SM stack vs reported excess shape (slide 17)
    ax = axes[1]
    bins = np.linspace(190, 610, 15)
    sm_stack = np.array([0.3] * 14)
    excess = np.array([0, 3, 6, 8, 24, 4, 2, 1, 0, 0, 0, 0, 0])
    centers = 0.5 * (bins[:-1] + bins[1:])
    ax.bar(centers, sm_stack, width=(bins[1] - bins[0]), color=PALETTE[1],
           alpha=0.85, label="summed SM toy prediction")
    ax.errorbar(centers[: len(excess)], excess, yerr=np.sqrt(excess), fmt="o",
                color="black", label="reported pseudo-data (slide 17)")
    ax.set_xlabel("(j1+j2+j3+j4+l1+l2).mass [GeV]")
    ax.set_ylabel("events / bin (toy)")
    ax.set_title("365 GeV: excess sits above summed SM prediction")
    ax.legend(fontsize=8)

    fig.suptitle("FCE (toy, synthetic)  --  SM-completeness check behind the Task B excesses",
                 fontsize=12, fontweight="bold", x=0.02, ha="left")
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    fig.savefig(outpath)
    plt.close(fig)


def main():
    render_cutflow_table(CUTFLOWS_160, 160, os.path.join(FIGDIR, "01_cutflow_160GeV.png"))
    render_cutflow_table(CUTFLOWS_365, 365, os.path.join(FIGDIR, "02_cutflow_365GeV.png"))
    make_mass_plots(os.path.join(FIGDIR, "03_massplots_160_365.png"))
    stats = cross_energy_consistency(os.path.join(FIGDIR, "04_cross_energy_consistency.png"))
    gap_panel_91(os.path.join(FIGDIR, "05_gap_91GeV.png"))
    gap_panel_240(os.path.join(FIGDIR, "06_gap_240GeV.png"))
    sm_completeness_check(os.path.join(FIGDIR, "07_sm_completeness_check.png"))

    print("SM interpretation figures written to", FIGDIR)
    print("Cross-energy consistency pulls:", stats["pull_lep"], stats["pull_btag"])
    print("Quoted-selection reference points (talk):", QUOTED)


if __name__ == "__main__":
    main()
