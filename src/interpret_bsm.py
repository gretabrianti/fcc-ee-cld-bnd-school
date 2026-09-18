"""
Task B interpretation: BSM (Heavy Neutral Lepton) claims at 91 GeV and 365 GeV.

Every figure is written to its own file under figures/bsm/, dpi=300, no plot
titles, styled with `puma` (CLD badge). See CODE_EXPLAINED.md for what each
figure means and how to read it.

For each energy point this script:
  1. builds a toy of the claimed HNL hypothesis at the reported mass and
     compares it, together with a toy "wrong hypothesis", to the reported
     pseudo-data -- a shape-level validation;
  2. independently recomputes the discovery significance from the reported
     pseudo-data under three different statistical treatments (see
     toygen.py for why there are three) and checks whether the excess still
     clears the discovery/evidence thresholds under the most conservative
     one -- a statistical validation of whether the claim holds up;
  3. prints the human action items that can't be resolved from the slides
     alone.
"""
from __future__ import annotations

import logging
import os

import matplotlib.pyplot as plt
import numpy as np
import puma

logging.getLogger("puma").setLevel(logging.ERROR)

import slide_readings as sl
import style
from interpret_sm import edges_from_centers, toy_vs_data_histogram
from toygen import (
    relativistic_bw_resonance,
    combinatorial_background,
    wrong_pairing_smear,
    background_relative_uncertainty,
    counting_significance,
    poisson_excess_significance,
    significance_with_bkg_uncertainty,
    global_significance,
    chi2_between,
    met_like,
    three_way_pairing_toy,
)

FIGDIR = os.path.join(os.path.dirname(__file__), "..", "figures", "bsm")
os.makedirs(FIGDIR, exist_ok=True)


# ---------------------------------------------------------------------------
# 1) Shape-level hypothesis tests: H0 (claimed BSM hypothesis) vs H1
#    (plausible wrong hypothesis) vs reported pseudo-data, with a proper
#    Data/H0 ratio panel.
# ---------------------------------------------------------------------------

def hypothesis_test_plot(h0_values, h1_values, data_centers, data_values, xlabel,
                          h0_label, h1_label, energy_gev, outpath):
    edges = edges_from_centers(data_centers)
    n_bins = len(data_centers)

    h0_raw, _ = np.histogram(h0_values, bins=edges)
    h1_raw, _ = np.histogram(h1_values, bins=edges)
    total_data = data_values.sum()
    h0_counts = h0_raw * (total_data / h0_raw.sum()) if h0_raw.sum() > 0 else np.zeros(n_bins)
    h1_counts = h1_raw * (total_data / h1_raw.sum()) if h1_raw.sum() > 0 else np.zeros(n_bins)

    plot = puma.HistogramPlot(
        **style.puma_kwargs(
            energy_gev, n_ratio_panels=1, ylabel="Events / bin",
            ylabel_ratio=["Data / H0"], xlabel=xlabel, figsize=(6.5, 5.5),
            leg_loc="upper right", ymin_ratio=[0], ymax_ratio=[3],
        )
    )
    plot.add(
        puma.Histogram(values=h0_counts, bin_edges=edges, norm=False, histtype="step",
                        colour=style.PALETTE["h0"], linewidth=2, label=h0_label),
        key="h0", reference=True,
    )
    plot.add(
        puma.Histogram(values=h1_counts, bin_edges=edges, norm=False, histtype="step",
                        colour=style.PALETTE["h1"], linewidth=2, linestyle="--", label=h1_label),
        key="h1",
    )
    plot.add(
        puma.Histogram(values=data_values.astype(float), bin_edges=edges, norm=False, is_data=True,
                        colour=style.PALETTE["data"], label="pseudo-data"),
        key="data",
    )
    plot.draw()
    chi2_h0, ndof_h0, chi2ndof_h0 = chi2_between(data_values, h0_counts)
    chi2_h1, ndof_h1, chi2ndof_h1 = chi2_between(data_values, h1_counts)
    style.annotate_chi2(
        plot.axis_top,
        rf"$\chi^2$/ndof(H0) = {chi2_h0:.1f}/{ndof_h0} = {chi2ndof_h0:.2f}"
        "\n"
        rf"$\chi^2$/ndof(H1) = {chi2_h1:.1f}/{ndof_h1} = {chi2ndof_h1:.2f}",
    )
    plot.savefig(outpath)
    plt.close("all")
    return chi2_h0, chi2_h1


def single_histogram_plot(values, xrange, xlabel, energy_gev, outpath, colour_key, label,
                           vline=None, vline_label=None):
    edges = np.linspace(*xrange, 31)
    counts, _ = np.histogram(values, bins=edges)

    plot = puma.HistogramPlot(
        **style.puma_kwargs(
            energy_gev, ylabel="Toy events / bin", xlabel=xlabel, figsize=(6, 5),
            leg_loc="upper right" if vline is None else "lower right",
        )
    )
    plot.add(
        puma.Histogram(values=counts, bin_edges=edges, norm=False, histtype="stepfilled",
                        colour=style.PALETTE[colour_key], alpha=0.75, label=label),
        key="h",
    )
    plot.draw()
    if vline is not None:
        ax = plot.axis_top
        ax.axvline(vline, color="black", ls=":", lw=1.5)
        ymax = ax.get_ylim()[1]
        ax.text(vline, ymax * 0.5, f"  {vline_label}", fontsize=9, ha="left", va="center", rotation=90)
    plot.savefig(outpath)
    plt.close("all")


def pairing_comparison_plot(naive_values, constrained_values, xrange, xlabel, energy_gev,
                             outpath, target_mass=None, target_label=None):
    """Overlay the 'naive' (fixed, unconstrained jet assignment) and
    'constrained' (pick the 3-way pairing closest to m_W) toy reconstructions
    -- see toygen.three_way_pairing_toy. A cleaner, narrower constrained peak
    demonstrates the resolution improvement a kinematic pairing constraint
    would buy over just reading off a default jet ordering.
    """
    edges = np.linspace(*xrange, 31)
    naive_counts, _ = np.histogram(naive_values, bins=edges)
    constrained_counts, _ = np.histogram(constrained_values, bins=edges)

    plot = puma.HistogramPlot(
        **style.puma_kwargs(energy_gev, ylabel="Toy events / bin", xlabel=xlabel,
                             figsize=(6, 5), leg_loc="upper right")
    )
    plot.add(
        puma.Histogram(values=naive_counts, bin_edges=edges, norm=False, histtype="step",
                        colour=style.PALETTE["h1"], linewidth=2,
                        label="naive (fixed jet slot, no constraint)"),
        key="naive",
    )
    plot.add(
        puma.Histogram(values=constrained_counts, bin_edges=edges, norm=False, histtype="stepfilled",
                        colour=style.PALETTE["h0"], alpha=0.7,
                        label=r"constrained (closest to $m_W$)"),
        key="constrained",
    )
    plot.draw()
    if target_mass is not None:
        ax = plot.axis_top
        ax.axvline(target_mass, color="black", ls=":", lw=1.5)
        ymax = ax.get_ylim()[1]
        ax.text(target_mass, ymax * 0.5, f"  {target_label}", fontsize=9, ha="left",
                 va="center", rotation=90)
    plot.savefig(outpath)
    plt.close("all")


# ---------------------------------------------------------------------------
# 2) Significance validation: recompute the discovery significance from the
#    reported pseudo-data under three tiers (see toygen.py docstring), and
#    check it against 3-sigma/5-sigma thresholds. This is the actual
#    "validate or invalidate the BSM claim" check.
# ---------------------------------------------------------------------------

def significance_hierarchy_plot(n_obs, event_topology, quoted_sigmas, energy_gev, outpath,
                                 n_trials=8):
    """Significance-vs-assumed-background scan, instead of a single bar per
    tier: with n_obs fixed at the (digitised) reported pseudo-data sum, the
    background yield b is not reliably known from the slides, so we scan it
    and show where the three significance tiers land relative to the quoted
    numbers. Where the Tier-2/Tier-3 curves cross a quoted horizontal line
    tells us what background level would make our recomputation consistent
    with that quoted number -- this is the actual validation: do the quoted
    numbers correspond to a *plausible* background yield, given n_obs?

    A 4th curve adds the look-elsewhere ("global") correction to Tier 3 --
    the first check any referee would make on a claimed discovery -- using a
    conservative Bonferroni trials factor (toygen.global_significance).
    n_trials=8 by default: 4 energy working points x ~2 independent
    kinematic observables searched for an excess at each (a mass-like
    variable and MET), which is how many places this analysis actually
    looked, per the talk -- not a rigorous trials count (that needs the
    Gross-Vitells treatment of the actual search windows/binning), but a
    defensible order-of-magnitude estimate.

    event_topology: dict(n_jets=, n_el=, n_mu=, n_bjets=) representative of
    the selection, used to combine the fce_studio systematics into sigma_b.
    """
    rel_unc = background_relative_uncertainty(
        sl.LUMI_UNC, sl.JEC_PER_JET, sl.LEP_PER_EL, sl.LEP_PER_MU, sl.BTAG_PER_BJET,
        **event_topology,
    )
    b_scan = np.linspace(0.3, n_obs * 0.97, 300)
    z1 = counting_significance(n_obs)  # independent of b
    z2 = np.array([poisson_excess_significance(n_obs, b) for b in b_scan])
    z3 = np.array([significance_with_bkg_uncertainty(n_obs, b, b * rel_unc) for b in b_scan])
    z4 = np.array([global_significance(z, n_trials) for z in z3])

    fig, ax = plt.subplots(figsize=(6, 4.5))
    ax.axhline(z1, color=style.PALETTE["X4"], lw=1.8,
               label=f"Tier 1: counting, $\\sqrt{{2n}}$ = {z1:.1f}$\\sigma$ (bkg-free)")
    ax.plot(b_scan, z2, color=style.PALETTE["X2"], lw=1.8, label="Tier 2: Poisson-Asimov, exact $b$")
    ax.plot(b_scan, z3, color=style.PALETTE["X1"], lw=1.8,
            label=rf"Tier 3: Asimov w/ bkg unc. ($\pm${rel_unc*100:.1f}% on $b$)")
    ax.plot(b_scan, z4, color=style.PALETTE["h1"], lw=1.8, ls="--",
            label=rf"Tier 3, global ($N_{{trials}}$={n_trials} look-elsewhere)")
    ax.axhline(5, color="black", ls="-", lw=1)
    ax.text(b_scan[-1], 5.1, "5$\\sigma$ discovery", fontsize=8, ha="right")
    ax.axhline(3, color="gray", ls="--", lw=1)
    ax.text(b_scan[-1], 3.1, "3$\\sigma$ evidence", fontsize=8, ha="right")
    single = len(quoted_sigmas) == 1
    for name, val in quoted_sigmas.items():
        if single:
            ax.axhline(val, color="red", ls="-", lw=1.8)
            ax.text(b_scan[-1], val + 0.15, f"{val}$\\sigma$", fontsize=11,
                    color="red", ha="right", fontweight="bold")
        else:
            ax.axhline(val, color=style.PALETTE["h1"], ls=":", lw=1.2, alpha=0.8)
            ax.text(b_scan[-1], val + 0.15, f"quoted: {name} = {val}$\\sigma$", fontsize=7.5,
                    color=style.PALETTE["h1"], ha="right")
    ax.set_xlim(b_scan[0], b_scan[-1])
    ax.set_ylim(0, max([z1, *quoted_sigmas.values()]) * 1.3)
    ax.set_xlabel(r"Assumed background yield $b$ [events]")
    ax.set_ylabel("Recomputed discovery significance")
    ax.legend(fontsize=7, loc="lower left")
    style.cld_atlasify(ax, energy_gev)
    style.annotate_note(ax, rf"observed $n$ = {n_obs:.0f} events")
    style.savefig(fig, outpath)
    plt.close(fig)
    return dict(z_counting=float(z1), rel_unc=rel_unc, n_obs=n_obs, n_trials=n_trials)


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main():
    # --- 91 GeV: HNL (m~40 GeV) vs. combinatorial mis-pairing alternative ---
    h0_91 = relativistic_bw_resonance(4000, 40, 0.5, 6, seed_offset=20)
    h1_91 = combinatorial_background(4000, sl.S91_MJ1L1_CENTERS[0] - 2.5,
                                      sl.S91_MJ1L1_CENTERS[-1] + 2.5, 25, seed_offset=21)
    chi2_h0_91, chi2_h1_91 = hypothesis_test_plot(
        h0_91, h1_91, sl.S91_MJ1L1_CENTERS, sl.S91_MJ1L1_DATA, "m(J1, l1) [GeV]",
        r"H0: HNL, $m$=40 GeV (toy)", "H1: combinatorial bkg (toy, wrong hyp.)",
        91, os.path.join(FIGDIR, "01_hnl_91GeV_hypothesis_test.png"),
    )

    # --- 91 GeV: dedicated HNL mass-reconstruction toy, analogous to the
    # 365 GeV W/HNL mass plots below. Per slide 15, at 91 GeV only ONE jet is
    # assumed reconstructed (the two quarks from the very off-shell W* in
    # N -> l' q qbar' are too collimated to resolve into two jets when
    # m_HNL=40 GeV << m_W=80.4 GeV), so there is no 365-GeV-style separate
    # "W mass" plot here -- m(J1, l1) already IS the full HNL mass estimator.
    # The combinatorial ambiguity at 91 GeV is instead which of the two
    # leptons in the "2 leptons + MET" final state (slide 15) is paired with
    # the jet; modelled the same way as the 365 GeV mis-pairing smear.
    correct_hnl_91 = relativistic_bw_resonance(4000, 40, 0.6, 6, seed_offset=22)
    hnl_toy_91 = wrong_pairing_smear(correct_hnl_91, mis_id_fraction=0.35, spread=12, seed_offset=23)
    single_histogram_plot(
        hnl_toy_91, (0, 60), "m(J1, l1) [GeV]", 91,
        os.path.join(FIGDIR, "02_HNL_mass_91GeV.png"), "X1",
        "toy: correct lepton pairing (65%) + mis-pairing (35%)", vline=40,
        vline_label=r"reported $m_{HNL} \sim$ 40 GeV",
    )

    # --- 91 GeV: independent cross-check on a SECOND observable (slide 16,
    # met.pt, headline "7 sigma") for the SAME excess/hypothesis studied
    # above in m(J1,l1). The HNL production+decay chain (slide 15:
    # e+e- -> Z -> N nu-bar, N -> l' W*, W* -> l'' nu'') carries away momentum
    # in TWO invisible neutrinos, so met.pt is modelled as the magnitude of
    # their vector-summed momentum (a chi-distribution "MET-like" toy, see
    # toygen.met_like) rather than reusing the mass-peak machinery -- a
    # genuinely different check of the same hypothesis, not a repeat of the
    # m(J1,l1) test.
    met_toy_91 = met_like(6000, scale=12, n_components=2, seed_offset=24)
    chi2_met91, ndof_met91, chi2ndof_met91 = toy_vs_data_histogram(
        met_toy_91, (0, 41), sl.S91_METPT_CENTERS, sl.S91_METPT_DATA, "met.pt [GeV]",
        91, os.path.join(FIGDIR, "03_HNL_metpt_91GeV.png"), "X1",
        "H0: HNL toy (2-neutrino MET model)",
    )

    # n_obs read directly off the slide-14 pseudo-data; as a side check, note
    # that n_obs - quoted_excess (31 - 29.6 ~= 1.4) already implies a small
    # background, consistent with this being a tight, high-purity selection.
    n_obs_91 = float(sl.S91_MJ1L1_DATA.sum())
    sig_stats_91 = significance_hierarchy_plot(
        n_obs_91, dict(n_jets=1, n_el=0.5, n_mu=0.5, n_bjets=0),
        {"slide-14 fit box": sl.S91_SIGMA_FITBOX, "slide-14 text": sl.S91_SIGMA_TEXT,
         "slide-16 headline": sl.S91_SIGMA_SLIDE16},
        91, os.path.join(FIGDIR, "04_significance_hierarchy_91GeV.png"),
    )

    # --- 365 GeV: W and HNL mass reconstruction, with an actual kinematic
    # pairing constraint instead of an arbitrary fixed correct/wrong split.
    # With (at least) 3 candidate jet pairings per event, "naive" always
    # reads off one fixed slot (~ no constraint applied, which is what the
    # flat, low-significance shapes on slides 19-20 look like); "constrained"
    # picks, per event, whichever candidate dijet mass is closest to m_W,
    # then reads the HNL mass off that SAME pairing (never off m_HNL itself
    # -- that would bias the measurement; m_W is known in advance, m_HNL
    # isn't). See toygen.three_way_pairing_toy.
    pairing = three_way_pairing_toy(
        6000, w_target=80.4, w_width=2.1, w_comb_scale=45, w_comb_range=(0, 200),
        hnl_mass=150, hnl_width=3.0, hnl_comb_scale=70, hnl_comb_range=(0, 300),
        resolution=8, seed_offset=30,
    )
    pairing_comparison_plot(
        pairing["naive_w"], pairing["constrained_w"], (0, 200), "m(j2, j3) [GeV]", 365,
        os.path.join(FIGDIR, "05_W_mass_365GeV.png"), target_mass=80.4, target_label=r"$m_W$ = 80.4 GeV",
    )
    pairing_comparison_plot(
        pairing["naive_hnl"], pairing["constrained_hnl"], (0, 300), "m(j2, j3, l2) [GeV]", 365,
        os.path.join(FIGDIR, "06_HNL_mass_365GeV.png"),
        target_mass=150, target_label=r"reported $m_{HNL} \sim$ 150 GeV",
    )

    # --- 365 GeV: localised resonance vs. mis-reconstructed SM ZZ/WW tail ---
    h0_365 = relativistic_bw_resonance(3000, 345, 5, 25, seed_offset=40)
    h1_365 = combinatorial_background(3000, sl.S365_MTOT_CENTERS[0] - 15,
                                       sl.S365_MTOT_CENTERS[-1] + 15, 90, seed_offset=41) \
        + sl.S365_MTOT_CENTERS[0] - 15
    chi2_h0_365, chi2_h1_365 = hypothesis_test_plot(
        h0_365, h1_365, sl.S365_MTOT_CENTERS, sl.S365_MTOT_DATA,
        "(j1+j2+j3+j4+l1+l2).mass [GeV]", "H0: localised resonance (toy)",
        "H1: mis-reco SM ZZ/WW tail (toy)", 365,
        os.path.join(FIGDIR, "07_hnl_365GeV_alternative_test.png"),
    )

    n_obs_365 = float(sl.S365_MTOT_DATA.sum())
    sig_stats_365 = significance_hierarchy_plot(
        n_obs_365, dict(n_jets=2, n_el=1, n_mu=1, n_bjets=0),
        {"slide-17 quoted": sl.S365_SIGMA_QUOTED},
        365, os.path.join(FIGDIR, "08_significance_hierarchy_365GeV.png"),
    )

    print("BSM interpretation figures written to", FIGDIR)
    print(f"91 GeV shape test: chi2(H0 HNL)={chi2_h0_91:.1f} vs chi2(H1 combinatorial)={chi2_h1_91:.1f}")
    print(f"91 GeV metpt cross-check: chi2/ndof={chi2ndof_met91:.2f}")
    print(f"91 GeV significance tiers: {sig_stats_91}")
    print(f"365 GeV pairing toy: naive correct fraction={pairing['naive_correct_frac']:.2f}, "
          f"constrained correct fraction={pairing['constrained_correct_frac']:.2f}")
    print(f"365 GeV shape test: chi2(H0 resonance)={chi2_h0_365:.1f} vs chi2(H1 SM mis-reco)={chi2_h1_365:.1f}")
    print(f"365 GeV significance tiers: {sig_stats_365}")
    print_x_identity_conclusion(chi2_h0_91, chi2_h1_91, chi2_h0_365, chi2_h1_365)
    print_mass_tension_conclusion()
    print_human_action_items()


def print_mass_tension_conclusion():
    print("=" * 72)
    print("ARE THE 91 GeV AND 365 GeV EXCESSES THE SAME PARTICLE?")
    print("-" * 72)
    print(
        "The talk interprets BOTH excesses as a Heavy Neutral Lepton, but\n"
        "quotes two very different masses: m_HNL ~ 40 GeV at 91 GeV (slide 14)\n"
        "vs. m_HNL ~ 150 GeV at 365 GeV (slide 20). Taken at face value these\n"
        "are two DIFFERENT particles, not one -- a single HNL has one mass. If\n"
        "that is genuinely the intended claim (two distinct HNL mass states,\n"
        "or two generations mixing with different flavours), it is a much\n"
        "stronger claim than the talk states and needs its own justification;\n"
        "the talk as written reads as though it's the same particle.\n"
    )
    print(
        "05_W_mass_365GeV.png / 06_HNL_mass_365GeV.png show why the 150 GeV\n"
        "number is the one to be more skeptical of: our 'naive' (unconstrained)\n"
        "toy reconstruction reproduces the same broad, weakly-peaked shape as\n"
        "slides 19-20, and only recovers the true pairing 1/3 of the time by\n"
        "construction. Applying a simple kinematic constraint (pick the jet\n"
        "pairing closest to m_W before reading off the HNL mass) narrows both\n"
        "peaks substantially in the toy. The 91 GeV m~40 GeV measurement has\n"
        "no such combinatorial ambiguity (only one jet is used, per slide 15),\n"
        "so it is the more trustworthy of the two numbers as reported. Before\n"
        "presenting m_HNL~150 GeV again, the real analysis should apply an\n"
        "equivalent pairing constraint (minimise |m(jj)-m_W| over all jet\n"
        "combinations in the event) and re-check whether the peak survives\n"
        "and where it sits.\n"
    )
    print("=" * 72)


def print_x_identity_conclusion(chi2_h0_91, chi2_h1_91, chi2_h0_365, chi2_h1_365):
    print("=" * 72)
    print("CAN THIS BSM STUDY TELL US WHAT X1..X5 REALLY ARE?")
    print("-" * 72)
    print(
        "Short answer: no, not individually -- this study never fits or\n"
        "identifies a specific X-labelled sample, at either energy. What it\n"
        "DOES show, quantitatively:\n"
    )
    print(
        f"  91 GeV:  chi2(HNL hypothesis)={chi2_h0_91:.1f}  vs.  "
        f"chi2(generic smooth SM-like background)={chi2_h1_91:.1f}\n"
        f" 365 GeV:  chi2(localised resonance)={chi2_h0_365:.1f}  vs.  "
        f"chi2(mis-reconstructed SM ZZ/WW tail)={chi2_h1_365:.1f}\n"
    )
    print(
        "In both cases the 'boring' alternative -- a smooth, generic\n"
        "background shape standing in for *any* combination of the ordinary\n"
        "Z-pole (91 GeV: Bhabha, Z->qqbar, Z->ll, gamma-gamma) or already-\n"
        "identified 365 GeV (ZZ, WW) processes -- fits far worse than the\n"
        "localised resonance hypothesis, by a wide margin. Since the H1\n"
        "alternative was deliberately built to be shape-agnostic (it does not\n"
        "assume which X is which, only that ordinary SM backgrounds produce\n"
        "smoothly falling / non-resonant shapes, which every physically\n"
        "plausible candidate at these energies does), this is evidence against\n"
        "'the excess is just an under-modelled tail of whichever X1..X5\n"
        "really are' -- regardless of the true X-label identities. It is not\n"
        "evidence FOR the HNL interpretation specifically (a different new-\n"
        "physics shape could fit comparably well); it only weighs against\n"
        "the null hypothesis that Task A, done correctly, would make the\n"
        "excess disappear.\n"
    )
    print("=" * 72)


def print_human_action_items():
    print("=" * 72)
    print("ITEMS THAT NEED HUMAN ACTION (cannot be resolved from the slides alone):")
    print("-" * 72)
    print(
        "1. 91 GeV significance is quoted 3 ways (5.79 / 7.8 / 7 sigma). Our\n"
        "   recomputation (04_significance_hierarchy_91GeV.png) reproduces the\n"
        "   same tiered pattern (bkg-free > Poisson-exact > with-systematics)\n"
        "   using the same 3-tier logic implemented in fce_studio/engine/\n"
        "   fitter.py, which strongly suggests the 3 numbers are 3 different\n"
        "   estimators of the same excess, not 3 independent results. Confirm\n"
        "   against the real fit log which estimator produced which number,\n"
        "   and quote only the most conservative (profile-likelihood / fit-box)\n"
        "   one going forward."
    )
    print(
        "2. No absolute cutflow numbers are in the deck -- only cut definitions\n"
        "   and two quoted percentages (20.9%, 1.8%). interpret_sm.py's cutflow\n"
        "   plots use ASSUMED per-cut efficiencies (marked '*'). Replace with\n"
        "   the real fce cutflow (aggregate yields only) when available."
    )
    print(
        "3. Task A (SM sample identification) is missing for 240 GeV and was\n"
        "   not shown for 91 GeV in the talk. This repo only provides an\n"
        "   expected-composition placeholder for both."
    )
    print(
        "4. sigma_b in the significance-hierarchy plots is built from generic\n"
        "   representative object multiplicities (n_jets, n_el, n_mu, n_bjets),\n"
        "   not the real per-event values. Replace with the real selection's\n"
        "   average multiplicities for a precise number.\n"
    )
    print("=" * 72)


if __name__ == "__main__":
    main()
