"""
Shared toy-Monte-Carlo utilities.

None of this touches the real FCC-ee/CLD samples produced with `fce`. Every
distribution here is a *parametric toy* built only from information that is
explicitly stated or visually readable in the BND-school presentation
(FCC-ee CLD collaboration.pdf): quoted cut definitions, quoted selection
efficiencies (e.g. "20.9%", "1.8%"), approximate peak positions/widths read
off the histograms, and the quoted significances/masses in the BSM slides.

The goal is not to reproduce the real analysis bin-by-bin (impossible without
looking at the data, which was explicitly ruled out) but to check whether the
*interpretation* given in the slides is internally consistent, and to give a
reusable, labelled reference the team can compare their real `fce` cutflow
output against once they extract it.
"""
from __future__ import annotations

import numpy as np

RNG_SEED = 20260918  # date of the talk, kept fixed for reproducibility


def rng(seed_offset: int = 0) -> np.random.Generator:
    return np.random.default_rng(RNG_SEED + seed_offset)


def gaussian_resonance(n, mass, sigma, seed_offset=0):
    """Toy reconstructed-mass peak: Gaussian resolution around a resonance."""
    g = rng(seed_offset)
    return g.normal(mass, sigma, size=n)


def relativistic_bw_resonance(n, mass, width, sigma_reco, seed_offset=0):
    """Breit-Wigner lineshape convolved with a Gaussian detector resolution.

    Used for genuine resonances (W, Z, Higgs, HNL) reconstructed from
    calorimeter/tracker objects, where both the natural width and the
    detector resolution matter.
    """
    g = rng(seed_offset)
    # Sample from a Breit-Wigner via inverse-CDF-like rejection is overkill
    # for a toy; a Cauchy draw is the standard trick (BW has the same shape).
    bw = g.standard_cauchy(size=n) * (width / 2.0) + mass
    smear = g.normal(0.0, sigma_reco, size=n)
    return bw + smear


def combinatorial_background(n, low, high, falling_scale, seed_offset=0):
    """Smoothly falling, non-resonant toy background over [low, high]."""
    g = rng(seed_offset)
    x = g.exponential(falling_scale, size=n) + low
    return np.clip(x, low, high)


def wrong_pairing_smear(correct_values, mis_id_fraction, spread, seed_offset=0):
    """Model the effect of picking the wrong jet/lepton combination.

    A fraction `mis_id_fraction` of events get an extra wide smearing applied
    on top of the correctly-reconstructed value, mimicking a combinatorial
    mis-pairing tail (e.g. picking the wrong two jets out of four).
    """
    g = rng(seed_offset)
    values = np.array(correct_values, dtype=float).copy()
    n = len(values)
    mis_mask = g.random(n) < mis_id_fraction
    values[mis_mask] += g.normal(0.0, spread, size=mis_mask.sum())
    return values


def poisson_pseudodata(expected_counts, seed_offset=0):
    g = rng(seed_offset)
    return g.poisson(np.clip(expected_counts, 0, None))


def cutflow(n_start, cuts):
    """Apply a sequence of named efficiencies to an initial yield.

    Parameters
    ----------
    n_start : float
        Yield before any selection.
    cuts : list[tuple[str, float]]
        (cut_name, efficiency_of_this_cut_relative_to_previous_step)

    Returns
    -------
    list[dict] with keys: cut, n_pass, rel_eff, cum_eff
    """
    rows = []
    n_prev = n_start
    n0 = n_start
    for name, eff in cuts:
        n_pass = n_prev * eff
        rows.append(
            {
                "cut": name,
                "n_pass": n_pass,
                "rel_eff": eff,
                "cum_eff": n_pass / n0 if n0 > 0 else 0.0,
            }
        )
        n_prev = n_pass
    return rows


def compatibility_pull(a, a_err, b, b_err):
    """Simple Gaussian pull between two measurements, for a consistency check."""
    denom = np.sqrt(a_err**2 + b_err**2)
    if denom == 0:
        return 0.0
    return (a - b) / denom
