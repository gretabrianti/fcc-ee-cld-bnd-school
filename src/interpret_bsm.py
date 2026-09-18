"""
Task B interpretation: BSM (Heavy Neutral Lepton) claims at 91 GeV and 365 GeV.

For each energy point this script:
  1. builds a toy of the claimed HNL hypothesis at the reported mass, and
     checks that its shape is compatible with the reported excess/peak;
  2. builds one or two toy *alternative* hypotheses (pure combinatorial
     background, or a different mass point) and shows they do NOT reproduce
     the reported shape, as a discriminating cross-check;
  3. prints out explicit callouts for things that only the team can resolve
     with the real fit (e.g. the significance is quoted as 3 different
     numbers across slides 14 and 16 -- 5.79 sigma in the fit box, "7.8 sigma"
     in the text, "7 sigma" as the slide 16 headline).

Figures written to figures/bsm/.
"""
from __future__ import annotations

import os

import matplotlib.pyplot as plt
import numpy as np

from style import apply_base_style, fce_header, PALETTE
from toygen import (
    relativistic_bw_resonance,
    combinatorial_background,
    wrong_pairing_smear,
    rng,
)

FIGDIR = os.path.join(os.path.dirname(__file__), "..", "figures", "bsm")
os.makedirs(FIGDIR, exist_ok=True)


# ---------------------------------------------------------------------------
# 91 GeV: HNL hypothesis, m ~ 40 GeV, reconstructed in m(J1, l1)
# ---------------------------------------------------------------------------

def hnl_91gev(outpath):
    apply_base_style()
    fig, ax = plt.subplots(figsize=(8, 5.5))

    xrange = (8, 62)
    bins = np.linspace(*xrange, 12)
    centers = 0.5 * (bins[:-1] + bins[1:])

    # reported pseudo-data, read off slide 14 (approximate)
    reported = np.array([0, 0, 1, 2, 5, 6, 2, 7, 2, 3, 3])

    # H0: HNL hypothesis, mass ~ 40 GeV, width dominated by detector resolution
    # (long-lived particle -> narrow intrinsic width, reconstruction smearing dominates)
    hnl_toy = relativistic_bw_resonance(3000, 40, 0.5, 6, seed_offset=20)
    hnl_toy = hnl_toy[(hnl_toy > xrange[0]) & (hnl_toy < xrange[1])]
    hnl_hist, _ = np.histogram(hnl_toy, bins=bins)
    hnl_hist = hnl_hist / hnl_hist.max() * reported.max()

    # H1 (alternative, "wrong process"): pure combinatorial jet+lepton
    # background from mis-paired soft objects -- smoothly falling, no peak
    alt_toy = combinatorial_background(3000, xrange[0], xrange[1], 25, seed_offset=21)
    alt_hist, _ = np.histogram(alt_toy, bins=bins)
    alt_hist = alt_hist / alt_hist.max() * reported.max()

    ax.errorbar(centers, reported, yerr=np.sqrt(reported), fmt="o", color="black",
                label="reported pseudo-data (slide 14)")
    ax.plot(centers, hnl_hist, drawstyle="steps-mid", color=PALETTE[0], lw=2,
            label="H0: HNL, m=40 GeV (toy)")
    ax.plot(centers, alt_hist, drawstyle="steps-mid", color=PALETTE[5], lw=2,
            ls="--", label="H1: mis-paired combinatorial bkg (toy, wrong hypothesis)")
    ax.set_xlabel("m(J1, l1) [GeV]")
    ax.set_ylabel("events / bin")
    ax.set_title("91 GeV excess: HNL hypothesis vs. non-resonant alternative")
    ax.legend(fontsize=9)
    fce_header(ax, 91)

    chi2_hnl = np.sum((reported - hnl_hist) ** 2 / np.clip(reported, 1, None))
    chi2_alt = np.sum((reported - alt_hist) ** 2 / np.clip(reported, 1, None))
    ax.text(
        0.02, 0.72,
        f"chi2(H0, HNL) = {chi2_hnl:.1f}\nchi2(H1, combinatorial) = {chi2_alt:.1f}\n"
        f"(lower is better; both computed on the same {len(reported)} toy bins)",
        transform=ax.transAxes, fontsize=8,
        bbox=dict(boxstyle="round", fc="white", ec="gray"),
    )

    fig.tight_layout()
    fig.savefig(outpath)
    plt.close(fig)
    return chi2_hnl, chi2_alt


# ---------------------------------------------------------------------------
# 365 GeV: W mass reconstruction + HNL mass reconstruction, including the
# combinatorial mis-pairing effect noted on slide 20 ("sub-optimal pairing
# might lead to large spread").
# ---------------------------------------------------------------------------

def hnl_365gev(outpath):
    apply_base_style()
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.5))

    # --- W boson mass from (j2+j3), slide 19 ---
    ax = axes[0]
    xrange = (0, 200)
    correct_w = relativistic_bw_resonance(4000, 80.4, 2.1, 8, seed_offset=30)
    # apply the mis-pairing smear the slide already flags as a caveat
    w_toy = wrong_pairing_smear(correct_w, mis_id_fraction=0.5, spread=35, seed_offset=31)
    w_toy = w_toy[(w_toy > xrange[0]) & (w_toy < xrange[1])]
    ax.hist(w_toy, bins=30, range=xrange, color=PALETTE[0], alpha=0.85,
            label="toy: correct pairing (50%) + mis-pairing smear (50%)")
    ax.axvline(80.4, color="black", ls=":", label="m(W) = 80.4 GeV")
    ax.set_xlabel("m(j2, j3) [GeV]")
    ax.set_ylabel("toy events / bin")
    ax.set_title("W boson reconstruction (matches slide 19 broad shape)")
    ax.legend(fontsize=8)

    # --- HNL mass from (j2+j3+l2), slide 20 ---
    ax = axes[1]
    xrange = (0, 300)
    correct_hnl = relativistic_bw_resonance(4000, 150, 3.0, 12, seed_offset=32)
    hnl_toy = wrong_pairing_smear(correct_hnl, mis_id_fraction=0.55, spread=45, seed_offset=33)
    hnl_toy = hnl_toy[(hnl_toy > xrange[0]) & (hnl_toy < xrange[1])]
    ax.hist(hnl_toy, bins=30, range=xrange, color=PALETTE[2], alpha=0.85,
            label="toy: correct pairing (45%) + mis-pairing smear (55%)")
    ax.axvline(150, color="black", ls=":", label="reported m(HNL) ~ 150 GeV")
    ax.set_xlabel("m(j2, j3, l2) [GeV]")
    ax.set_ylabel("toy events / bin")
    ax.set_title("HNL mass reconstruction: broad spread is expected\nfrom 3-body combinatorics, not necessarily a flaw")
    ax.legend(fontsize=8)

    fig.suptitle("FCE (toy, synthetic)  --  CLD, sqrt(s) = 365 GeV",
                 fontsize=12, fontweight="bold", x=0.02, ha="left")
    fig.tight_layout(rect=[0, 0, 1, 0.93])
    fig.savefig(outpath)
    plt.close(fig)


def alternative_sm_explanation_365(outpath):
    """Check whether the 365 GeV excess (slide 17, sigma=6.46) could plausibly
    be explained by mis-reconstructed SM ZZ/WW instead of a new HNL, using the
    total-system-mass observable from slide 17.
    """
    apply_base_style()
    fig, ax = plt.subplots(figsize=(8, 5.5))

    xrange = (190, 610)
    bins = np.linspace(*xrange, 15)
    centers = 0.5 * (bins[:-1] + bins[1:])
    reported = np.array([0, 0, 3, 6, 8, 24, 4, 2, 1, 0, 0, 0, 0, 0])

    # H0: genuine new resonance (HNL pair / single production) near sqrt(s)
    hnl_sys = relativistic_bw_resonance(3000, 345, 5, 25, seed_offset=40)
    hnl_sys = hnl_sys[(hnl_sys > xrange[0]) & (hnl_sys < xrange[1])]
    hnl_hist, _ = np.histogram(hnl_sys, bins=bins)
    hnl_hist = hnl_hist / hnl_hist.max() * reported.max()

    # H1: mis-reconstructed SM ZZ/WW (already in the Task-A sample list at
    # 365 GeV) with the leptons/jets mismeasured -- total mass should track
    # close to sqrt(s), broad and roughly flat, not peaked at 345 GeV specifically
    sm_misreco = combinatorial_background(3000, xrange[0], xrange[1], 90, seed_offset=41) + 190
    sm_misreco = sm_misreco[(sm_misreco > xrange[0]) & (sm_misreco < xrange[1])]
    sm_hist, _ = np.histogram(sm_misreco, bins=bins)
    sm_hist = sm_hist / sm_hist.max() * reported.max()

    ax.errorbar(centers, reported, yerr=np.sqrt(reported), fmt="o", color="black",
                label="reported pseudo-data (slide 17)")
    ax.plot(centers, hnl_hist, drawstyle="steps-mid", color=PALETTE[0], lw=2,
            label="H0: localised new-physics resonance (toy)")
    ax.plot(centers, sm_hist, drawstyle="steps-mid", color=PALETTE[5], lw=2, ls="--",
            label="H1: mis-reconstructed SM ZZ/WW tail (toy, wrong hypothesis)")
    ax.set_xlabel("(j1+j2+j3+j4+l1+l2).mass [GeV]")
    ax.set_ylabel("events / bin")
    ax.set_title("365 GeV excess: localised resonance vs. mis-reconstructed SM tail")
    ax.legend(fontsize=8)
    fce_header(ax, 365)

    chi2_hnl = np.sum((reported - hnl_hist) ** 2 / np.clip(reported, 1, None))
    chi2_sm = np.sum((reported - sm_hist) ** 2 / np.clip(reported, 1, None))
    ax.text(
        0.02, 0.72,
        f"chi2(H0, resonance) = {chi2_hnl:.1f}\nchi2(H1, SM mis-reco) = {chi2_sm:.1f}",
        transform=ax.transAxes, fontsize=8,
        bbox=dict(boxstyle="round", fc="white", ec="gray"),
    )

    fig.tight_layout()
    fig.savefig(outpath)
    plt.close(fig)
    return chi2_hnl, chi2_sm


def print_human_action_items():
    print("=" * 72)
    print("ITEMS THAT NEED HUMAN ACTION (cannot be resolved from the slides alone):")
    print("-" * 72)
    print(
        "1. 91 GeV significance is inconsistent across the deck:\n"
        "   - slide 14 fit box quotes 5.79 sigma\n"
        "   - slide 14 body text quotes 7.8 sigma\n"
        "   - slide 16 headline quotes 7 sigma\n"
        "   -> re-run/inspect the original fit log to determine which number\n"
        "      (if any) is the final one, and fix the deck before presenting it."
    )
    print(
        "2. Absolute cutflow numbers (N passing events per cut, per sample,\n"
        "   per energy) are not in the deck -- only cut definitions and a\n"
        "   couple of percentages (20.9%, 1.8%). The cutflow tables produced\n"
        "   by this script use ASSUMED per-cut efficiencies (marked with '*').\n"
        "   -> export the real cutflow from fce (aggregate yields only, not\n"
        "      the underlying events) and replace the '*' numbers in\n"
        "      src/interpret_sm.py with the real ones."
    )
    print(
        "3. Task A (SM sample identification) is missing entirely for the\n"
        "   240 GeV working point, and was not shown for 91 GeV in the talk\n"
        "   (only the BSM search was). -> needs to be done by the team; this\n"
        "   repo only provides an expected-composition placeholder."
    )
    print(
        "4. The 240 GeV, 91 GeV luminosity/cross-section assumptions used\n"
        "   anywhere in the real fce analysis (if any absolute yields are\n"
        "   quoted later) should be confirmed against the actual generator\n"
        "   config, since this repo does not use or infer them."
    )
    print("=" * 72)


def main():
    chi2_hnl_91, chi2_alt_91 = hnl_91gev(os.path.join(FIGDIR, "01_hnl_91GeV_hypothesis_test.png"))
    hnl_365gev(os.path.join(FIGDIR, "02_hnl_365GeV_mass_reco.png"))
    chi2_hnl_365, chi2_sm_365 = alternative_sm_explanation_365(
        os.path.join(FIGDIR, "03_hnl_365GeV_alternative_test.png")
    )

    print("BSM interpretation figures written to", FIGDIR)
    print(f"91 GeV: chi2(HNL)={chi2_hnl_91:.1f} vs chi2(combinatorial bkg)={chi2_alt_91:.1f}")
    print(f"365 GeV: chi2(resonance)={chi2_hnl_365:.1f} vs chi2(SM mis-reco)={chi2_sm_365:.1f}")
    print_human_action_items()


if __name__ == "__main__":
    main()
