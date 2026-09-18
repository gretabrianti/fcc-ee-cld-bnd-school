# What this code does, why, and how to read it

This file explains the two analysis scripts (`src/interpret_sm.py`,
`src/interpret_bsm.py`), the reasoning behind them, and how to read every
figure they produce. It assumes you've read the talk
(`FCC-ee CLD collaboration.pdf`) but not necessarily any of the code.

## 0. The constraint this code was built under

Nobody looked at the real downloaded FCC-ee/CLD ntuples to write this code.
That's a deliberate choice, not a limitation we're apologising for: Task A of
the project is *"figure out what each anonymised sample X1..X5 actually is"*,
and peeking at the data (or at anything that reveals the answer, like a
label-to-process lookup table) would defeat that exercise. So everywhere
this code needs a number it doesn't have, it either:

- takes it verbatim from the talk (a quoted percentage, a quoted
  significance, a cut definition), or
- reads it approximately off a histogram image in the talk (documented in
  `src/slide_readings.py`, with the slide number for every array), or
- takes it from **the analysis *code*** (`fce_studio`, installed in the
  `bnd_school` conda env) rather than from any dataset -- specifically the
  systematic-uncertainty constants and the discovery-significance formulas
  in `fce_studio/engine/systematics.py` and `fce_studio/engine/fitter.py`.
  This is config/methodology, not an answer key: it does not say what any
  X-labelled sample is, it says how the tool computes uncertainties and
  significances, and using it doesn't compromise Task A, or
- makes an explicit, labelled assumption (marked with a trailing `*` in
  cutflow plots, or spelled out in this file).

Nowhere does the code claim to have identified a sample that the talk itself
didn't identify. Where the talk leaves a gap (91 GeV and 240 GeV Task A),
the code says so and stops, rather than inventing an answer.

## 1. `interpret_sm.py` -- Task A (Standard Model interpretation)

### Why it exists

The talk identifies several SM processes (Higgs and WW at 160 GeV; ttbar,
`e+e- -> ff`, ZZ, ZH, WW at 365 GeV) from cut definitions and histogram
shapes, but never checks whether that interpretation is *internally
consistent* -- e.g. whether a detector-level quantity like a b-tagging
efficiency comes out the same at two different collision energies, which it
should if it's really measuring detector performance and not something
energy-dependent. It also never touches 91 GeV or 240 GeV Task A at all.
This script builds that consistency layer.

### What each figure means

**`01_cutflow_efficiency_160GeV.png`, `02_cutflow_efficiency_365GeV.png`**
Cumulative selection efficiency after each cut, one line per identified
process, log-y. This replaces the table-of-numbers approach (numbers alone
don't show you *where* a selection is expensive) with something you can
read a shape off: a steep drop at a given stage tells you which cut is
doing the heavy lifting for that process. The x-axis is deliberately generic
(`cut 1`, `cut 2`, ...) because different processes have *different* cuts at
each stage (see `CUTFLOWS_160`/`CUTFLOWS_365` in the script for exactly
which); labelling the axis with one process's cut text would misdescribe
every other process's line. Every per-cut efficiency is an assumption
(marked `*`) -- the talk gives no absolute cutflow numbers, only cut
definitions and two overall percentages (20.9% at 91 GeV, 1.8% at 160 GeV),
which the toy generators are calibrated against where relevant.

**`03_mass_higgs_160GeV.png` ... `06_mass_zz_365GeV.png`**
For each confidently-identified process, a toy Monte Carlo mass distribution
(built as a Breit-Wigner resonance at the process's known mass, smeared by a
Gaussian detector resolution -- see `toygen.relativistic_bw_resonance`)
overlaid against the approximate pseudo-data points read off the
corresponding slide. The toy is normalised in shape only (scaled so its
total matches the data's total, since we have no absolute cross-section to
anchor an absolute prediction) -- **how to read the ratio panel**: near the
peak, data/toy should sit close to 1 if the process ID and mass are right;
in the tails it often won't, because our toy is a pure single-resonance
model and doesn't include whatever continuum/combinatorial background is
really sitting under the peak in the real analysis. A tail disagreement is
not a red flag; a peak-region disagreement would be.

**`07_lepton_pt_efficiency_turnon.png`**
The efficiency of a `lepton pt > 20 GeV` cut as a function of the *true*
lepton pt, built from a toy detector model (true pt smeared by a resolution)
at 160 GeV and 365 GeV. This is the efficiency-as-a-plot the cutflow tables
couldn't give you: a turn-on curve. The two energies' curves overlap almost
exactly by construction, because a lepton-pt reconstruction efficiency is a
detector property and *should not* depend on the collision energy -- this is
the actual cross-energy consistency check, done properly (a physical
quantity's behaviour vs. a kinematic variable), rather than a bar chart of
two single numbers.

**`08_btag_efficiency_comparison.png`**
b-tagging efficiency at the WP=0.7 working point (the threshold used in
every `b-tag>0.7`/`b-tag<0.7` cut in the talk), compared at 160 and 365 GeV,
with error bars from the **real** `BTAG_PER_BJET` systematic constant
(2%/b-jet) read out of `fce_studio/engine/systematics.py`. Same logic as the
lepton-pt plot: a detector working point shouldn't move with `sqrt(s)`.

**`09_gap_91GeV.png`, `10_gap_240GeV.png`**
Not a result -- a flagged gap. The talk never performs Task A at 91 GeV
(only the BSM search is shown) and never performs it at all at 240 GeV (3
samples, zero slides). These figures show a *hypothesised* (91 GeV, argued
from the slide-6 pie chart + generic Z-pole cross-section hierarchy) or
*expected* (240 GeV, generic ZH-run physics) composition, explicitly
labelled as not extracted from any data. See `notes/process_mapping.md` for
the reasoning. Use these as a checklist, not an answer.

**`11_completeness_91GeV.png`, `12_completeness_365GeV.png`**
The point of these two: show that the BSM excesses claimed in Task B
(slides 14 and 17) sit *above* a fully-summed SM prediction, not in place of
one. The stacked (tiny, at this scale) SM toy prediction plus the reported
pseudo-data, with a Data/Pred. ratio panel -- exactly the plot style used in
the talk's own FCE screenshots. If the ratio panel showed values near 1
throughout, that would undermine the BSM claim (SM alone would explain the
data); instead it climbs to several-to-dozens in the excess region, which is
consistent with (though does not on its own prove) a real excess.

## 2. `interpret_bsm.py` -- Task B (BSM validation)

### Why it exists

The talk *asserts* two BSM discoveries (91 GeV, 365 GeV, both interpreted as
a Heavy Neutral Lepton) but never checks them against an alternative
explanation, and quotes the 91 GeV significance as three different numbers
in two slides (5.79 / 7.8 / 7 σ) without saying why. This script does two
things: a shape-level hypothesis test (does the claimed particle's mass
hypothesis actually describe the reported data shape better than a mundane
alternative?), and a numbers-level validation (does the significance survive
a realistic, systematics-aware recomputation, and can the three quoted
numbers be reconciled?).

### What each figure means

**`01_hnl_91GeV_hypothesis_test.png`**
Three things on one plot: the reported pseudo-data (slide 14), a toy HNL
signal at the reported mass (H0, solid), and a toy non-resonant
combinatorial background (H1, dashed -- representing "the excess is just
random jet+lepton mis-pairings, not a new particle"). The chi2 printed by
the script (H0=40.2 vs H1=52.3) favours H0, and visually H0 tracks the
30-50 GeV peak in the data much better than the flat-ish H1. This doesn't
*prove* the HNL interpretation, but it does show the data shape is not
naturally explained by a boring alternative either.

**`02_significance_hierarchy_91GeV.png`, `06_significance_hierarchy_365GeV.png`**
The most important validation plot in this repo. `fce_studio/engine/
fitter.py` (the real analysis tool, not the dataset) implements three
different significance estimators:

1. **counting** (`sqrt(2n)`): ignores background entirely, always the most
   optimistic number;
2. **Poisson-Asimov** (`n` observed vs. an exact `b`): accounts for
   background but not its uncertainty;
3. **Asimov with background uncertainty** (Cowan, Cranmer, Gross, Vitells,
   *"Asymptotic formulae for likelihood-based tests of new physics"*,
   Eur.Phys.J.C71:1554 (2011), eq. 25): the most conservative, and the
   closest public-formula stand-in for what a full profile-likelihood fit
   (which is what tier 3 in `fitter.py` actually runs, via `pyhf`) would
   give once the luminosity/JEC/lepton/b-tag nuisance parameters are
   profiled.

This is almost certainly why the talk quotes three different 91 GeV
numbers: they're plausibly three different tiers applied to the same excess,
not three separate measurements. The plot fixes `n` at the digitised
pseudo-data sum and scans the assumed background `b` (which the talk
doesn't give a number for), plotting all three tiers against it, with the
three quoted numbers as horizontal reference lines. **Read it as**: where a
tier's curve crosses a quoted line tells you what background yield would
make that quoted number consistent with that tier. At 91 GeV, tier 1 sits
at 7.9σ -- strikingly close to the quoted "7.8σ" text on slide 14, which is
a genuine, notable finding (not tuned to match; tier 1 doesn't depend on
`b` at all). Tiers 2/3 cross the 5.79σ fit-box number around `b`≈9-10 events
and the 7.0σ slide-16 number around `b`≈4, both very plausible background
levels for a tight Z-pole selection. This is the actual validation: the
quoted numbers are mutually consistent with being different statistical
treatments of one excess, evaluated at a plausible (if unconfirmed)
background level -- not evidence of an error, but also not something that
should be presented as three independent confirmations.

At 365 GeV, the single quoted number (6.46σ, slide 17) crosses the tier 2/3
curves around `b`≈15 events, noticeably higher than the small illustrative
background (`b`≈2.4) assumed for the `12_completeness_365GeV.png` plot in
the SM script -- flagged as an open inconsistency worth checking against the
real background prediction, not silently reconciled.

**`03_W_mass_365GeV.png`, `04_HNL_mass_365GeV.png`**
Toy reconstruction of the W boson (from `j2+j3`) and the HNL (from
`j2+j3+l2`) in the HNL decay chain (slide 18). Both toys mix a
correctly-paired resonance with a "wrong jet combination" smear (see
`toygen.wrong_pairing_smear`) at roughly 50/50, which reproduces the same
qualitative broad-bump shape the talk shows and flags as a caveat ("sub-optimal
pairing might lead to large spread", slide 20). Reading these together: the
broad spread in the HNL mass plot is consistent with being a 3-body
combinatorics/resolution effect, not evidence that the mass hypothesis
itself is wrong.

**`05_hnl_365GeV_alternative_test.png`**
Same H0-vs-H1-vs-data logic as the 91 GeV plot, applied to the 365 GeV
excess (slide 17): H0 is a localised new-physics resonance near `sqrt(s)`,
H1 is a mis-reconstructed SM ZZ/WW tail (since ZZ and WW are *already*
identified processes at 365 GeV with a similar final state -- see
`notes/process_mapping.md`). H1 badly overshoots at high mass where the data
does not, and undershoots the actual peak region; H0 tracks the data shape
much more closely (chi2 28.9 vs. 1508.8). This is a meaningful check because
it rules out the most obvious "boring" explanation (mundane SM background
mismeasurement) using processes the team has *already* identified in the
same dataset, rather than an arbitrary alternative.

## 3. Statistics reference (`toygen.py`)

- `relativistic_bw_resonance`: Breit-Wigner lineshape (via a Cauchy draw, the
  standard trick since a BW has the same functional form) convolved with
  Gaussian detector resolution. Used for every genuine resonance (Higgs, W,
  Z, HNL).
- `combinatorial_background`: smoothly falling non-resonant toy, used for
  "wrong hypothesis" alternatives.
- `wrong_pairing_smear`: mixes a correctly-reconstructed value with an
  extra-wide smear on a configurable fraction of events, modelling a
  combinatorial mis-pairing tail.
- `counting_significance`, `poisson_excess_significance`,
  `significance_with_bkg_uncertainty`: the three significance tiers
  described above; see the docstring in `toygen.py` for the exact formulas
  and references.
- `background_relative_uncertainty`: combines the `fce_studio` systematics
  constants in quadrature for a representative event topology.

## 4. Honesty notes / where this could be wrong

- Every digitised pseudo-data array in `slide_readings.py` is read by eye
  off a rendered PDF page, not extracted from a plotting library's data
  file. Treat it as good to ~10-20% and to correct order of magnitude, not
  pixel-exact.
- The `*`-marked per-cut efficiencies in the cutflow plots are illustrative
  assumptions, not measurements. Replace them with the real `fce` cutflow
  (aggregate yields only) as soon as the team has it.
- The "expected composition" panels for 91 and 240 GeV are physics-motivated
  guesses, explicitly not fits to anything. They exist to give the team a
  sanity-check target once they do the real Task A work, not to pre-empt it.
