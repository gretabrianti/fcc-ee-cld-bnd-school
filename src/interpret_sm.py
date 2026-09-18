"""
Task A interpretation: Standard Model samples.

Every figure is written to its own file under figures/sm/, dpi=200, no plot
titles (CLD-branded badge + axis labels + legend only), styled with `puma`.
Toy MC is always compared to the pseudo-data points read off the
corresponding slide (see slide_readings.py) wherever the talk shows any.

See CODE_EXPLAINED.md for what each figure means and how to read it, and
notes/process_mapping.md for the physics reasoning behind each process ID.
"""
from __future__ import annotations

import logging
import os

import matplotlib.pyplot as plt
import numpy as np
import puma

logging.getLogger("puma").setLevel(logging.ERROR)  # silence benign "rejection is infinity" (bkg_rej unused here)

import slide_readings as sl
import style
from toygen import cutflow, relativistic_bw_resonance, rng, chi2_between

FIGDIR = os.path.join(os.path.dirname(__file__), "..", "figures", "sm")
os.makedirs(FIGDIR, exist_ok=True)


def edges_from_centers(centers):
    centers = np.asarray(centers, dtype=float)
    width = centers[1] - centers[0]
    return np.concatenate([centers - width / 2, [centers[-1] + width / 2]])


# ---------------------------------------------------------------------------
# 1) Cutflow EFFICIENCY plots (replaces the old tables): cumulative fraction
#    of events surviving each cut, one line per process, log-y. Per-cut
#    efficiencies are the same assumptions as before (marked '*' in the
#    legend note) since the talk gives no absolute cutflow numbers.
# ---------------------------------------------------------------------------

CUTFLOWS_160 = {
    r"Higgs ($\nu\nu H$, $H\rightarrow b\bar{b}$)": [
        ("presel.", 1.0), ("2j, b-tag>0.7*", 0.55), ("0 lep*", 0.85), ("MET cut*", 0.70),
    ],
    "WW (semileptonic)": [
        ("presel.", 1.0), ("2j*", 0.80), ("1 lep*", 0.60), ("MET>5*", 0.90),
    ],
}

CUTFLOWS_365 = {
    r"$t\bar{t}$": [
        ("presel.", 1.0), (">=2lep*", 0.35), (">=4j,b>0.7*", 0.45), ("lep pt>20*", 0.85), ("MET>20*", 0.80),
    ],
    r"$e^+e^- \rightarrow f\bar{f}$": [
        ("presel.", 1.0), (">=2lep*", 0.40), (">=4j,b<0.7*", 0.50), ("lep pt>20*", 0.85), ("m(ll) win*", 0.60),
    ],
    r"$ZZ \rightarrow \ell\ell q\bar{q}$ (X5)": [
        ("presel.", 1.0), (">=2lep*", 0.45), (">=2j,b<0.7*", 0.55), ("pt>20*", 0.85), ("Z-veto*", 0.55), ("MET<20*", 0.75),
    ],
    "ZH": [
        ("presel.", 1.0), (">=2lep*", 0.30), (">=2j,b>0.7*", 0.50), ("pt>20*", 0.85), ("m(ll) win*", 0.60), ("MET<10*", 0.70),
    ],
    "WW (365 sel.)": [
        ("presel.", 1.0), (">=0lep*", 1.0), (">=2j,b<0.7*", 0.65), ("pt>20*", 0.80),
    ],
}


def cutflow_efficiency_plot(cutflow_dict, energy_gev, outpath):
    """Cumulative selection efficiency vs. cut stage, one line per process.

    Different processes have different cuts at each stage (see
    CUTFLOWS_160/365 above), so the x-axis intentionally uses generic
    "Cut N" positions rather than literal cut text -- labelling every
    process's stage 2 as e.g. "2j, b-tag>0.7" would be wrong for the
    processes whose own stage 2 is a different cut. The per-process cut
    definitions are in the legend label and in CODE_EXPLAINED.md.
    """
    fig, ax = plt.subplots(figsize=(7, 5))
    colours = list(style.PALETTE.values())
    max_len = 0
    for i, (proc_name, cuts) in enumerate(cutflow_dict.items()):
        rows = cutflow(1.0, cuts)
        x = np.arange(len(rows) + 1)
        y = [1.0] + [r["cum_eff"] for r in rows]
        max_len = max(max_len, len(x))
        ax.plot(x, y, marker="o", lw=1.8, color=colours[i % len(colours)], label=proc_name)
    stage_labels = ["presel."] + [f"cut {i + 1}" for i in range(max_len - 1)]
    ax.set_xticks(np.arange(max_len))
    ax.set_xticklabels(stage_labels, fontsize=9)
    ax.set_yscale("log")
    ax.set_ylim(1e-3, 1.5)
    ax.set_ylabel("cumulative efficiency (toy, * = assumed per-cut eff.)")
    ax.legend(fontsize=8, loc="lower left")
    ax.grid(alpha=0.3, which="both")
    style.cld_atlasify(ax, energy_gev)
    style.savefig(fig, outpath)
    plt.close(fig)


# ---------------------------------------------------------------------------
# 2) Toy mass spectra vs. reported pseudo-data, one puma HistogramPlot per
#    process, each saved to its own file.
# ---------------------------------------------------------------------------

def toy_vs_data_histogram(toy_values, xrange, data_centers, data_values, xlabel,
                           energy_gev, outpath, colour_key="X1", mc_label="toy MC (shape)"):
    edges = edges_from_centers(data_centers)
    mc_counts_raw, _ = np.histogram(toy_values, bins=edges)
    total_data = data_values.sum()
    total_mc = mc_counts_raw.sum()
    scale = (total_data / total_mc) if total_mc > 0 else 1.0
    mc_counts = mc_counts_raw * scale

    plot = puma.HistogramPlot(
        **style.puma_kwargs(
            energy_gev,
            n_ratio_panels=1,
            ylabel="Events / bin",
            ylabel_ratio=["Data / toy"],
            xlabel=xlabel,
            figsize=(6, 5),
            leg_loc="upper right",
            ymin_ratio=[0],
            ymax_ratio=[3],
        )
    )
    plot.add(
        puma.Histogram(values=mc_counts, bin_edges=edges, norm=False, histtype="stepfilled",
                        colour=style.PALETTE[colour_key], alpha=0.75, label=mc_label),
        key="mc", reference=True,
    )
    plot.add(
        puma.Histogram(values=data_values.astype(float), bin_edges=edges, norm=False, is_data=True,
                        colour=style.PALETTE["data"], label="pseudo-data"),
        key="data",
    )
    plot.draw()
    chi2, ndof, chi2_ndof = chi2_between(data_values, mc_counts)
    style.annotate_chi2(plot.axis_top, rf"$\chi^2$/ndof = {chi2:.1f}/{ndof} = {chi2_ndof:.2f}")
    plot.savefig(outpath)
    plt.close("all")
    return chi2, ndof, chi2_ndof


def make_all_mass_plots():
    results = {}
    results["higgs_160"] = toy_vs_data_histogram(
        relativistic_bw_resonance(6000, 125, 4.1, 8, 1), (60, 145),
        sl.S160_HIGGS_MJJ_CENTERS, sl.S160_HIGGS_MJJ_DATA,
        "m(J1, J2) [GeV]", 160, os.path.join(FIGDIR, "03_mass_higgs_160GeV.png"), "X1",
        r"Higgs (toy, $\nu\nu H$)",
    )
    results["ww_160"] = toy_vs_data_histogram(
        relativistic_bw_resonance(8000, 153, 2.0, 6, 2), (122, 168),
        sl.S160_WW_MLMETJJ_CENTERS, sl.S160_WW_MLMETJJ_DATA,
        "m(l1, MET, J1, J2) [GeV]", 160, os.path.join(FIGDIR, "04_mass_ww_160GeV.png"), "X2",
        "WW (toy, semileptonic)",
    )
    results["ttbar_365"] = toy_vs_data_histogram(
        relativistic_bw_resonance(6000, 178, 1.4, 20, 3), (110, 250),
        sl.S365_TTBAR_MASS_CENTERS, sl.S365_TTBAR_MASS_DATA,
        "(j1+met+l1).mass [GeV]", 365, os.path.join(FIGDIR, "05_mass_ttbar_365GeV.png"), "X1",
        r"$t\bar{t}$ (toy)",
    )
    results["zz_365"] = toy_vs_data_histogram(
        relativistic_bw_resonance(9000, 91, 2.5, 6, 5), (55, 125),
        sl.S365_ZZ_MASS_CENTERS, sl.S365_ZZ_MASS_DATA,
        "(j1+j2).mass [GeV]", 365, os.path.join(FIGDIR, "06_mass_zz_365GeV.png"), "X5",
        r"$ZZ \rightarrow \ell\ell q\bar{q}$ (toy)",
    )
    return results


# ---------------------------------------------------------------------------
# 3) Efficiency PLOTS (not tables): lepton-pt turn-on curve via puma
#    VarVsEffPlot, compared across 160 and 365 GeV, plus a b-tag efficiency
#    comparison bar chart using the real systematics.BTAG_PER_BJET constant
#    for the uncertainty.
# ---------------------------------------------------------------------------

def lepton_pt_turnon_plot(outpath):
    """Efficiency of a lepton-pt > 20 GeV cut as a function of the true lepton
    pt, at 160 and 365 GeV. Built from the same underlying resolution model
    at both energies (only the kinematic spectrum differs) -- this is a
    detector-performance quantity, so the two curves should overlap, which is
    exactly the cross-energy consistency check the team asked for, done as a
    plot instead of a table.
    """
    sigma_pt = 3.0  # GeV, illustrative lepton-pt resolution (wide enough to show a turn-on)

    g160 = rng(50)
    true_pt_160 = g160.uniform(0, 80, size=20000)
    reco_pt_160 = true_pt_160 + g160.normal(0, sigma_pt, size=20000)

    g365 = rng(51)
    true_pt_365 = g365.uniform(0, 80, size=20000)
    reco_pt_365 = true_pt_365 + g365.normal(0, sigma_pt, size=20000)

    var160 = puma.VarVsEff(
        x_var_sig=true_pt_160, disc_sig=reco_pt_160, disc_cut=20,
        bins=np.linspace(0, 80, 33), colour=style.PALETTE["X1"], label="160 GeV toy",
    )
    var365 = puma.VarVsEff(
        x_var_sig=true_pt_365, disc_sig=reco_pt_365, disc_cut=20,
        bins=np.linspace(0, 80, 33), colour=style.PALETTE["X3"], label="365 GeV toy",
    )

    plot = puma.VarVsEffPlot(
        mode="sig_eff",
        **style.puma_kwargs(
            "160 & 365", xlabel="true lepton $p_T$ [GeV]", ylabel="efficiency of $p_T$ > 20 GeV cut",
            figsize=(6, 5), grid=True, logy=False, ymin=0, ymax=1.15,
        ),
    )
    plot.add(var160, key="e160")
    plot.add(var365, key="e365")
    plot.draw()
    plot.savefig(outpath)
    plt.close("all")


def btag_efficiency_comparison_plot(outpath):
    from toygen import background_relative_uncertainty

    nominal_eff = 0.80  # illustrative CLD-like b-tag efficiency at BTAG_WP=0.7
    rel_unc_1b = background_relative_uncertainty(
        sl.LUMI_UNC, sl.JEC_PER_JET, sl.LEP_PER_EL, sl.LEP_PER_MU, sl.BTAG_PER_BJET,
        n_jets=2, n_el=0, n_mu=0, n_bjets=1,
    )
    abs_unc = nominal_eff * sl.BTAG_PER_BJET  # per-b-jet systematic only, for the bar error bar

    g = rng(60)
    eff_160 = np.clip(g.normal(nominal_eff, abs_unc, 400), 0, 1).mean()
    eff_365 = np.clip(g.normal(nominal_eff, abs_unc, 400), 0, 1).mean()

    fig, ax = plt.subplots(figsize=(5.5, 5))
    ax.bar(["160 GeV", "365 GeV"], [eff_160, eff_365], yerr=[abs_unc, abs_unc],
           color=[style.PALETTE["X1"], style.PALETTE["X3"]], capsize=6, width=0.5)
    ax.axhline(nominal_eff, color="gray", ls=":", lw=1)
    ax.set_ylim(0, 1.05)
    ax.set_ylabel(rf"b-tag efficiency at WP={sl.BTAG_WP} (toy, $\pm${sl.BTAG_PER_BJET*100:.0f}% syst./b-jet)")
    style.cld_atlasify(ax, "160 & 365")
    style.savefig(fig, outpath)
    plt.close(fig)
    return dict(eff_160=eff_160, eff_365=eff_365, rel_unc_1b=rel_unc_1b)


# ---------------------------------------------------------------------------
# 4) Gap panels for 91 and 240 GeV (Task A missing/never done in the talk).
# ---------------------------------------------------------------------------

def gap_panel(labels, fractions, energy_gev, outpath, note):
    fig, ax = plt.subplots(figsize=(8, 5))
    colours = list(style.PALETTE.values())[: len(labels)]
    ax.barh(labels, fractions, color=colours)
    ax.set_xlabel(f"hypothesised / expected fraction [%]  --  {note}")
    style.cld_atlasify(ax, energy_gev)
    style.savefig(fig, outpath)
    plt.close(fig)


# ---------------------------------------------------------------------------
# 5) SM-completeness check: stacked toy SM prediction vs. the reported
#    BSM-search pseudo-data, with a proper Data/Pred. ratio panel (puma).
# ---------------------------------------------------------------------------

def completeness_plot(components, data_centers, data_values, xlabel, energy_gev, outpath):
    """components: list of (label, colour_key, fraction_of_small_bkg) tuples;
    the combined background is deliberately small and flat (order of
    magnitude read off the slides), since these are control-region toys, not
    a fit to the excess itself.
    """
    edges = edges_from_centers(data_centers)
    n_bins = len(data_centers)
    bkg_level = 0.3 * data_values.max() / 10  # small, flat, illustrative

    plot = puma.HistogramPlot(
        **style.puma_kwargs(
            energy_gev, n_ratio_panels=1, stacked=True,
            ylabel="Events / bin", ylabel_ratio=["Data / Pred."], xlabel=xlabel,
            figsize=(6.5, 5.5), leg_loc="upper right",
            ymin_ratio=[0], ymax_ratio=[10],
        )
    )
    for label, colour_key, frac in components:
        counts = np.full(n_bins, bkg_level * frac)
        plot.add(
            puma.Histogram(values=counts, bin_edges=edges, norm=False,
                            colour=style.PALETTE[colour_key], label=label),
            key=colour_key,
        )
    plot.add(
        puma.Histogram(values=data_values.astype(float), bin_edges=edges, norm=False, is_data=True,
                        colour=style.PALETTE["data"], label="pseudo-data"),
        key="data",
    )
    plot.draw()
    bkg_total = np.full(n_bins, bkg_level * sum(f for _, _, f in components))
    chi2, ndof, chi2_ndof = chi2_between(data_values, bkg_total, n_fit_params=0)
    style.annotate_chi2(
        plot.axis_top, rf"$\chi^2$/ndof (data vs. SM sum) = {chi2:.0f}/{ndof} = {chi2_ndof:.0f}"
    )
    plot.savefig(outpath)
    plt.close("all")
    return chi2, ndof, chi2_ndof


def main():
    cutflow_efficiency_plot(CUTFLOWS_160, 160, os.path.join(FIGDIR, "01_cutflow_efficiency_160GeV.png"))
    cutflow_efficiency_plot(CUTFLOWS_365, 365, os.path.join(FIGDIR, "02_cutflow_efficiency_365GeV.png"))

    mass_chi2 = make_all_mass_plots()

    lepton_pt_turnon_plot(os.path.join(FIGDIR, "07_lepton_pt_efficiency_turnon.png"))
    btag_stats = btag_efficiency_comparison_plot(os.path.join(FIGDIR, "08_btag_efficiency_comparison.png"))

    gap_panel(
        [r"X1: Bhabha $e^+e^-(\gamma)$", r"X2: $Z\rightarrow q\bar{q}$",
         r"X3: $Z\rightarrow \mu\mu/\tau\tau$", r"X4: $\gamma\gamma\rightarrow$ hadrons",
         "X5: rare/other"],
        [45, 30, 15, 8, 2], 91, os.path.join(FIGDIR, "09_gap_91GeV.png"),
        "Task A not carried out in the talk -- hypothesis only",
    )
    gap_panel(
        ["ZH signal", "WW background", r"$e^+e^- \rightarrow f\bar{f}$ / ZZ background"],
        [15, 55, 30], 240, os.path.join(FIGDIR, "10_gap_240GeV.png"),
        "Task A entirely missing from the talk -- expected mix only",
    )

    comp_chi2_91 = completeness_plot(
        [("toy SM sum (Task A not done at 91 GeV)", "X2", 1.0)],
        sl.S91_MJ1L1_CENTERS, sl.S91_MJ1L1_DATA,
        "m(J1, l1) [GeV]", 91, os.path.join(FIGDIR, "11_completeness_91GeV.png"),
    )
    comp_chi2_365 = completeness_plot(
        [(r"$t\bar{t}$", "X1", 0.30), (r"$e^+e^- \rightarrow f\bar{f}$", "X2", 0.25),
         ("ZZ", "X5", 0.20), ("ZH", "X3", 0.15), ("WW", "X4", 0.10)],
        sl.S365_MTOT_CENTERS, sl.S365_MTOT_DATA,
        "(j1+j2+j3+j4+l1+l2).mass [GeV]", 365, os.path.join(FIGDIR, "12_completeness_365GeV.png"),
    )

    print("SM interpretation figures written to", FIGDIR)
    print("b-tag toy stats:", btag_stats)
    print("mass-plot chi2/ndof (toy vs pseudo-data):")
    for name, (chi2, ndof, chi2_ndof) in mass_chi2.items():
        print(f"  {name}: chi2={chi2:.1f}, ndof={ndof}, chi2/ndof={chi2_ndof:.2f}")
    print(f"completeness 91 GeV (data vs SM sum): chi2/ndof = {comp_chi2_91[0]:.0f}/{comp_chi2_91[1]} = {comp_chi2_91[2]:.0f}")
    print(f"completeness 365 GeV (data vs SM sum): chi2/ndof = {comp_chi2_365[0]:.0f}/{comp_chi2_365[1]} = {comp_chi2_365[2]:.0f}")


if __name__ == "__main__":
    main()
