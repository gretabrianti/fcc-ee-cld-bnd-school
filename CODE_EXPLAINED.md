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

## Style conventions (both scripts)

- One PNG per figure, dpi=300, no plot titles -- CLD badge (top-left, via
  `puma`/`atlasify`) + axis labels + legend only, following ATLAS
  plot-style conventions as closely as `puma` lets us.
- The CLD badge is pinned to the same 10pt size `puma` itself uses
  (`style.BADGE_FONTSIZE`) on every figure, puma-generated or not, so the
  badge doesn't look oversized on the plain-matplotlib figures (bar/line
  charts) relative to the puma histogram plots.
- Every `chi2/ndof` or short numeric note is drawn as a plain third line
  directly under the badge (`style.annotate_note`, no box), never floating
  elsewhere on the figure.
- Cutflow efficiencies are drawn as bar charts on a linear 0-1.2+ scale
  (ATLAS cutflow-plot convention), one figure per process, with cuts spelled
  out in LaTeX -- not a shared log-scale line plot, which would force a
  misleading generic x-axis across processes with different cuts.

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

**`01_cutflow_higgs_160GeV.png` ... `07_cutflow_ww_365GeV.png`**
One bar chart per identified SM process: cumulative selection efficiency
after each cut, linear y-axis, cuts spelled out in LaTeX
(`CUTFLOWS_160`/`CUTFLOWS_365` in the script). Every per-cut efficiency is
an assumption (the talk gives no absolute cutflow numbers, only cut
definitions and two overall percentages -- 20.9% at 91 GeV, 1.8% at 160
GeV -- which the toy mass-plot generators are calibrated against
separately). One file per process rather than one shared plot, because
different processes have different cuts at each stage; overlaying them on
one shared axis would force a generic "cut 1, cut 2, ..." x-axis that
misdescribes every process but one.

**`08_mass_higgs_160GeV.png` ... `11_mass_zz_365GeV.png`**
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

Every one of these plots also carries a **chi2/ndof** note under the badge
(Pearson chi2 between the pseudo-data and the shape-scaled toy, computed by
`toygen.chi2_between`, `ndof = n_bins - 1` for the one normalisation degree
of freedom used in the shape-scaling). Read chi2/ndof close to 1 as "the toy
shape is statistically compatible with the reported points"; chi2/ndof >> 1
(e.g. the Higgs plot, ~38) means the toy shape and the data disagree
somewhere significantly -- check the ratio panel to see where (for the
Higgs plot it's the rising low-mass tail below the peak, which our
single-resonance toy was never meant to capture; the peak region itself
agrees well). A large chi2/ndof here is a comment on the *toy's*
simplifications, not on the talk's process identification.

**`12_lepton_pt_efficiency_turnon.png`**
The efficiency of a `lepton pt > 20 GeV` cut as a function of the *true*
lepton pt, built from a toy detector model (true pt smeared by a resolution)
at 160 GeV and 365 GeV, via a genuine `puma.VarVsEffPlot` turn-on curve. The
two energies' curves overlap almost exactly by construction, because a
lepton-pt reconstruction efficiency is a detector property and *should not*
depend on the collision energy -- this is the cross-energy consistency
check, done as an efficiency-vs-variable plot rather than a bar chart of two
single numbers.

**`13_btag_efficiency_comparison.png`**
b-tagging efficiency at the WP=0.7 working point (the threshold used in
every `b-tag>0.7`/`b-tag<0.7` cut in the talk), compared at 160 and 365 GeV,
with error bars from the **real** `BTAG_PER_BJET` systematic constant
(2%/b-jet) read out of `fce_studio/engine/systematics.py`. Same logic as the
lepton-pt plot: a detector working point shouldn't move with `sqrt(s)`.

**`14_gap_91GeV.png`, `15_gap_240GeV.png`**
Not a result -- a flagged gap. The talk never performs Task A at 91 GeV
(only the BSM search is shown) and never performs it at all at 240 GeV (3
samples, zero slides). These figures show a *hypothesised* (91 GeV, argued
from the slide-6 pie chart + generic Z-pole cross-section hierarchy) or
*expected* (240 GeV, generic ZH-run physics) composition. See
`notes/process_mapping.md` for the reasoning behind every bar. Use these as
a checklist, not an answer.

**`16_completeness_91GeV.png`, `17_completeness_365GeV.png`**
The point of these two: show that the BSM excesses claimed in Task B
(slides 14 and 17) sit *above* a fully-summed SM prediction, not in place of
one. The stacked (tiny, at this scale) SM toy prediction plus the reported
pseudo-data, with a Data/Pred. ratio panel -- exactly the plot style used in
the talk's own FCE screenshots. If the ratio panel showed values near 1
throughout, that would undermine the BSM claim (SM alone would explain the
data); instead it climbs to several-to-dozens in the excess region, which is
consistent with (though does not on its own prove) a real excess. The
chi2/ndof note quantifies the same thing as a single number (27/10=3 at
91 GeV, 40/8=5 at 365 GeV, both computed against the flat toy SM sum) --
values well above 1 confirm the SM-alone hypothesis is a poor description
of the reported data, by construction of these plots.

## 2. `interpret_bsm.py` -- Task B (BSM validation)

### Why it exists

The talk *asserts* two BSM discoveries (91 GeV, 365 GeV, both interpreted as
a Heavy Neutral Lepton) but never checks them against an alternative
explanation, quotes the 91 GeV significance as three different numbers in
two slides (5.79 / 7.8 / 7 σ) without saying why, and quotes two *different*
HNL masses (~40 GeV and ~150 GeV) without addressing that a single particle
can't have two masses. This script builds four layers of validation: a
shape-level hypothesis test at each energy, a second independent observable
at 91 GeV, a proper kinematic-pairing treatment of the 365 GeV mass
reconstruction, and a numbers-level significance validation (including a
look-elsewhere check -- the first thing any referee would ask for).

### What each figure means

**`01_hnl_91GeV_hypothesis_test.png`**
Three things on one plot: the reported pseudo-data (slide 14), a toy HNL
signal at the reported mass (H0, solid), and a toy non-resonant
combinatorial background (H1, dashed -- representing "the excess is just
random jet+lepton mis-pairings, not a new particle"). The chi2/ndof note on
the plot (H0=40.2/9=4.47 vs H1=52.3/9=5.81) favours H0, and visually H0
tracks the 30-50 GeV peak in the data much better than the flat-ish H1.
This doesn't *prove* the HNL interpretation, but it does show the data
shape is not naturally explained by a boring alternative either.

**`02_HNL_mass_91GeV.png`**
A dedicated mass-reconstruction toy at the reported 40 GeV value. There is
no separate "W mass" plot at 91 GeV like the 365 GeV pair below: per
slide 15, only **one** jet is assumed reconstructed for the whole HNL decay
chain, because at m_HNL~40 GeV the virtual W* in `N -> l' q qbar'` is so far
off-shell (m_HNL << m_W = 80.4 GeV) that its two quarks are too collimated
to resolve into two separate jets -- so `m(J1,l1)` *is* the full HNL mass
estimator here, not an intermediate step. The combinatorial ambiguity at
this energy is instead which of the (up to two) leptons in the
"2 leptons + MET" final state (slide 15) gets paired with the jet; the toy
mixes a correctly-paired resonance at 40 GeV with a wrong-lepton-pairing
smear.

**`03_HNL_metpt_91GeV.png`**
An independent cross-check on a *second* observable for the *same* 91 GeV
excess: slide 16 shows the identical excess in `met.pt` (headline "7σ"),
which the earlier version of this repo never used even though the data for
it was sitting in `slide_readings.py`. The HNL production+decay chain
(slide 15: `e+e- -> Z -> N nu-bar`, `N -> l' W*`, `W* -> l'' nu''`) carries
away momentum in **two** invisible neutrinos, so the toy models `met.pt` as
the magnitude of their vector-summed momentum (a chi-distribution, see
`toygen.met_like`) -- a genuinely different kinematic check of the same
hypothesis, not a repeat of the mass-peak test. It agrees well
(chi2/ndof = 1.14), which strengthens the case that the 91 GeV excess is a
real, kinematically consistent feature rather than a fluctuation isolated
to one variable.

**`04_significance_hierarchy_91GeV.png`, `08_significance_hierarchy_365GeV.png`**
The most important validation plot in this repo. `fce_studio/engine/
fitter.py` (the real analysis tool, not the dataset) implements three
different significance estimators:

1. **counting** (`sqrt(2n)`): ignores background entirely, always the most
   optimistic number;
2. **Poisson-Asimov** (`n` observed vs. an exact `b`): accounts for
   background but not its uncertainty;
3. **Asimov with background uncertainty** (Cowan, Cranmer, Gross, Vitells,
   *"Asymptotic formulae for likelihood-based tests of new physics"*,
   Eur.Phys.J.C71:1554 (2011), eq. 25): the most conservative of the three,
   and the closest public-formula stand-in for what a full
   profile-likelihood fit (which is what tier 3 in `fitter.py` actually
   runs, via `pyhf`) would give once the luminosity/JEC/lepton/b-tag
   nuisance parameters are profiled.

A **4th curve** goes one step further and asks the first question any
referee would: *how much of this survives a look-elsewhere correction?*
`toygen.global_significance` applies a conservative Bonferroni trials
factor (`n_trials=8`, i.e. 4 energy points x ~2 independent observables
searched for an excess at each -- a defensible order-of-magnitude estimate,
not a rigorous Gross-Vitells trials count) to Tier 3. The global curve sits
visibly below Tier 3 and crosses the 5σ discovery line at a noticeably
lower background value -- a concrete, quantitative version of "the local
significance overstates the case," which the talk does not address at all.

This is almost certainly also why the talk quotes three different 91 GeV
*local* numbers: they're plausibly three different tiers applied to the
same excess, not three separate measurements. The plot fixes `n` at the
digitised pseudo-data sum and scans the assumed background `b` (which the
talk doesn't give a number for), plotting all tiers against it, with the
quoted numbers as horizontal reference lines. **Read it as**: where a
tier's curve crosses a quoted line tells you what background yield would
make that quoted number consistent with that tier. At 91 GeV, tier 1 sits
at 7.9σ -- strikingly close to the quoted "7.8σ" text on slide 14, which is
a genuine, notable finding (not tuned to match; tier 1 doesn't depend on
`b` at all). Tiers 2/3 cross the 5.79σ fit-box number around `b`≈9-10 events
and the 7.0σ slide-16 number around `b`≈4, both plausible background levels
for a tight Z-pole selection.

At 365 GeV, the single quoted number (6.46σ, slide 17) crosses the tier 2/3
curves around `b`≈15 events, noticeably higher than the small illustrative
background (`b`≈2.4) assumed for the `17_completeness_365GeV.png` plot in
the SM script -- flagged as an open inconsistency worth checking against the
real background prediction, not silently reconciled.

**`05_W_mass_365GeV.png`, `06_HNL_mass_365GeV.png`**
These replace a naive fixed-fraction "correct vs. wrong pairing" toy with an
actual kinematic-pairing treatment (`toygen.three_way_pairing_toy`): each
toy event has 3 candidate jet-pairings, only one of which is truly the
`N -> ... W*` pair. The **naive** curve (red) always reads off one fixed
slot -- equivalent to using whatever jet ordering happens to come out of the
reconstruction with no constraint applied, which is what the flat,
barely-peaked shapes on slides 19-20 look like -- and is correct only 1/3 of
the time by construction. The **constrained** curve (blue) instead picks,
per event, whichever candidate dijet mass is closest to `m_W = 80.4 GeV`
(known in advance) and reads *both* the W mass and the HNL mass off that
same pairing -- never off `m_HNL` itself, which would bias the measurement.
In the toy, this recovers the true pairing ~88% of the time (vs. 33% naive,
printed by the script) and turns both broad, weak bumps into clean, narrow
peaks. **Takeaway**: slides 19-20's unconvincing shapes are consistent with
simply not having applied this constraint yet, not with the mass hypothesis
being wrong -- but until the real analysis applies an equivalent
constraint, `m_HNL~150 GeV` should be treated as provisional.

**`07_hnl_365GeV_alternative_test.png`**
Same H0-vs-H1-vs-data logic as the 91 GeV plot, applied to the 365 GeV
excess (slide 17): H0 is a localised new-physics resonance near `sqrt(s)`,
H1 is a mis-reconstructed SM ZZ/WW tail (since ZZ and WW are *already*
identified processes at 365 GeV with a similar final state -- see
`notes/process_mapping.md`). H1 badly overshoots at high mass where the data
does not, and undershoots the actual peak region; H0 tracks the data shape
much more closely (chi2/ndof: 28.9/7=4.12 vs. 1508.8/7=215.55, shown on the
plot). This rules out the most obvious "boring" explanation (mundane SM
background mismeasurement) using processes the team has *already*
identified in the same dataset, rather than an arbitrary alternative.

### Are the 91 GeV and 365 GeV excesses the same particle?

Printed explicitly at the end of every `interpret_bsm.py` run, because it's
the single biggest internal tension in the talk: a Heavy Neutral Lepton has
one mass, and the talk reports two (~40 GeV and ~150 GeV) for what it
presents as the same interpretation. Either this is meant to be two
distinct HNL states (a much stronger claim, needing its own justification
the talk doesn't give), or one of the two mass measurements is unreliable.
The pairing-constraint result above (05/06) points at *which* one to be
skeptical of: the 91 GeV measurement has no combinatorial ambiguity (one
jet only), while the 365 GeV one visibly suffers from it and only firms up
once a kinematic constraint is applied in the toy. This doesn't resolve the
tension -- only the real analysis, with a real pairing constraint, can do
that -- but it tells you where to look first.

### Does any of this tell us what X1..X5 really are?

Short answer: **no, not individually.** Neither hypothesis test fits or
names a specific X-labelled sample at either energy. What the two H0-vs-H1
tests *do* show, quantitatively, is that a deliberately shape-agnostic
"boring SM" alternative (H1 -- a smooth non-resonant shape at 91 GeV, a
mis-measured ZZ/WW tail at 365 GeV, standing in for *any* combination of the
plausible candidates) fits far worse than a localised-resonance hypothesis
at both energies. Since H1 doesn't assume which X is which -- only that
ordinary SM processes produce smoothly-falling or already-understood
shapes, which is true of every physically plausible candidate at these
energies -- a bad H1 fit is evidence against *"the excess is just an
under-modelled tail of whichever X1..X5 really are"*, regardless of their
true identities. It is not evidence *for* the HNL interpretation
specifically (a different new-physics shape could fit comparably well); it
only weighs against the null hypothesis that correctly finishing Task A
would make the excess disappear on its own.

## 3. Statistics reference (`toygen.py`)

- `relativistic_bw_resonance`: Breit-Wigner lineshape (via a Cauchy draw, the
  standard trick since a BW has the same functional form) convolved with
  Gaussian detector resolution. Used for every genuine resonance (Higgs, W,
  Z, HNL).
- `combinatorial_background`: smoothly falling non-resonant toy, used for
  "wrong hypothesis" alternatives.
- `wrong_pairing_smear`: mixes a correctly-reconstructed value with an
  extra-wide smear on a configurable fraction of events -- a simple
  illustrative model, superseded for the 365 GeV W/HNL plots by
  `three_way_pairing_toy` below, but still used for the 91 GeV lepton
  pairing ambiguity.
- `three_way_pairing_toy`: proper 3-candidate combinatorial-pairing toy with
  a "naive" (fixed slot) and "constrained" (closest to `m_W`) reconstruction
  strategy, used for the 365 GeV W/HNL mass plots -- see above.
- `met_like`: chi-distribution ("vector sum of N invisible momenta")
  MET-shape toy, used for the 91 GeV met.pt cross-check.
- `counting_significance`, `poisson_excess_significance`,
  `significance_with_bkg_uncertainty`: the three significance tiers
  described above; see the docstring in `toygen.py` for the exact formulas
  and references.
- `global_significance`: Bonferroni look-elsewhere correction from a local
  significance and a trials count.
- `background_relative_uncertainty`: combines the `fce_studio` systematics
  constants in quadrature for a representative event topology.
- `chi2_between(observed, expected, n_fit_params)`: Pearson chi2 using the
  observed counts for the variance (`sum((obs-exp)^2 / max(obs,1))`),
  `ndof = n_bins - n_fit_params`. Used on every distribution-comparison plot
  in both scripts and drawn directly on the figure as a `chi2/ndof` note.

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
- The `n_trials=8` look-elsewhere estimate is an order-of-magnitude
  placeholder, not a rigorous trials count. A real Gross-Vitells treatment
  needs the actual scan range and binning used in the real fit, which we
  don't have.
- The MET-based selections (91 GeV: `MET pT > 3 GeV`, a very low threshold)
  are exactly where MET resolution/modelling is hardest to get right in any
  MC -- this repo doesn't attempt to model that mismodelling risk
  quantitatively, it's flagged here as a caveat the real analysis should
  address (e.g. with a dedicated MET-response systematic), not something a
  toy without the real detector simulation could usefully estimate.
- **Not attempted**: comparing an implied HNL-mixing-angle (`|V_eN|^2`) from
  the observed rates against existing LEP/L3/DELPHI exclusion limits. This
  needs (a) the real observed cross-section/rate, not just a bin count, and
  (b) an accurate citation of the actual published exclusion contours at
  these masses -- both should come from the team looking up the real papers
  rather than this code guessing remembered numbers. Flagged as a concrete
  next step, not done here.
