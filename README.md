# FCC-ee CLD -- BND School interpretation toolkit

Support material for the *FCC-ee CLD collaboration* project (BND school,
18/09/2026): reads the presentation
(`FCC-ee CLD collaboration.pdf`) as the only source of truth and turns it
into a small, reproducible interpretation layer for the Standard Model
(Task A) and BSM (Task B) results shown there.

## Why this exists

The talk covers four center-of-mass energy points (91, 160, 240, 365 GeV),
each with several anonymised MC samples (`X1`, `X2`, ...) that have to be
identified from their kinematics, plus two claimed BSM excesses (91 GeV and
365 GeV) interpreted as a Heavy Neutral Lepton (HNL). The interpretation in
the deck is uneven across energy points (see
[`notes/process_mapping.md`](notes/process_mapping.md) for the full
breakdown) and a couple of numbers are inconsistent between slides. This
repo:

1. reconstructs cut-flow efficiencies for the SM processes that *are*
   identified in the talk, and checks whether object-level efficiencies
   (lepton-pt and b-tag selections) are consistent between energy points, as
   they should be if they reflect detector performance rather than the
   underlying physics process;
2. stress-tests the two BSM (HNL) interpretations by simulating the claimed
   hypothesis and at least one plausible wrong hypothesis, and comparing
   both to the shapes reported in the slides;
3. explicitly flags the two working points (91 and 240 GeV) where Task A
   was not actually carried out in the talk, with an expected-composition
   placeholder instead of a fabricated identification.

**No real FCC-ee/CLD data was read to build this repo.** Everything here is
a parametric *toy* Monte Carlo, anchored only to what is explicitly stated
or visually readable in the presentation (cut definitions, quoted
percentages, approximate peak positions/widths, quoted significances) plus
a handful of legitimate constants pulled from the **code** (not the data) of
the `fce_studio` package installed in the `bnd_school` conda env --
systematic-uncertainty magnitudes and the discovery-significance formulas it
implements (see [`CODE_EXPLAINED.md`](CODE_EXPLAINED.md) section 0 for the
exact boundary). Do not extend these scripts to load real ntuples without
first checking that this is still the intent.

Figures are styled with [`puma`](https://github.com/umami-hep/puma) (the
FTAG-group plotting library built on `atlasify`), with the ATLAS badge
re-pointed at "CLD Collaboration"; every figure is its own PNG at dpi=300
with no plot titles (axis labels + legend + CLD badge only).

## Layout

```
src/
  slide_readings.py    single source of truth for every number read off the
                        talk (pseudo-data points, quoted significances/
                        percentages) plus the fce_studio systematics constants
  toygen.py             shared toy-MC building blocks (resonances, combinatorial
                        backgrounds, 3-way kinematic-pairing toy, MET-like toy,
                        significance formulas incl. look-elsewhere correction)
  style.py              shared CLD/puma plot style (dpi=300, no titles,
                        badge size matched between puma and plain-matplotlib
                        figures)
  interpret_sm.py       Task A: per-process cutflow EFFICIENCY bar charts
                        (ATLAS-style, linear scale, LaTeX cuts), mass spectra
                        vs. reported pseudo-data with chi2/ndof, lepton-pt
                        turn-on efficiency (puma VarVsEffPlot) and b-tag
                        efficiency cross-energy checks, 91/240 GeV gap
                        panels, SM-completeness checks behind the Task B
                        excesses
  interpret_bsm.py      Task B: HNL hypothesis-vs-alternative tests (91 and
                        365 GeV) with chi2/ndof, a second independent 91 GeV
                        observable (met.pt, slide 16), a proper kinematic
                        jet-pairing treatment of the 365 GeV W/HNL mass
                        plots, a significance-tier validation with a
                        look-elsewhere (global) correction, and an explicit
                        discussion of the 40 GeV vs. 150 GeV HNL mass tension
figures/
  sm/                   PNGs produced by interpret_sm.py (17 figures)
  bsm/                  PNGs produced by interpret_bsm.py (8 figures)
notes/
  process_mapping.md    full reasoning behind the X1..X5 -> process mapping
                        used in this repo, energy point by energy point, with
                        the inconsistencies found in the deck itself
CODE_EXPLAINED.md       what every script/figure does, why, and how to read it
data/
  (synthetic toy samples, if/when exported -- see interpret_sm.py / interpret_bsm.py)
```

## Running it

```bash
conda activate bnd_school
pip install -r requirements.txt   # puma-hep, atlasify (numpy/matplotlib already present)
cd src
python interpret_sm.py
python interpret_bsm.py
```

Each script is self-contained, writes its PNGs under `figures/`, and prints
a short summary (including, for `interpret_bsm.py`, the list of things that
need a human to resolve -- see below). **See [`CODE_EXPLAINED.md`](CODE_EXPLAINED.md)
for what every figure means and how to read it.**

## What still needs a human

`interpret_bsm.py` prints these at the end of every run; repeated here for
visibility:

1. **91 GeV significance is quoted 3 ways across the deck** (5.79 / 7.8 / 7
   sigma). `interpret_bsm.py`'s `04_significance_hierarchy_91GeV.png`
   reproduces the same 3-tier pattern using the same significance-estimator
   logic implemented in `fce_studio/engine/fitter.py`, and finds the
   bkg-free tier lands at 7.9σ -- close to the quoted 7.8σ -- which is
   evidence (not proof) that the 3 numbers are 3 different estimators of one
   excess. Confirm against the real fit log which estimator produced which
   number, and quote only the most conservative one going forward.
2. **Neither quoted significance has a look-elsewhere (global) correction.**
   The same figures add a 4th curve applying a conservative Bonferroni
   trials factor (`n_trials=8`, order-of-magnitude only); it sits well below
   the local significance. Any discovery claim needs a real trials estimate
   from the actual search procedure before it goes back in the talk.
3. **The two HNL mass claims (~40 GeV at 91 GeV, ~150 GeV at 365 GeV) are in
   tension** -- a single particle has one mass. `interpret_bsm.py` prints
   this explicitly and shows (05/06 figures) that the 365 GeV measurement is
   the one to be skeptical of: it has an unresolved 3-way jet-pairing
   ambiguity (only 33% correct with the naive/no-constraint approach the
   slides appear to use) that a simple kinematic constraint
   (`|m(jj)-m_W|` minimisation) resolves to ~88% in the toy, meaningfully
   narrowing the peak. Apply the equivalent constraint in the real analysis
   before quoting m_HNL~150 GeV again.
4. **No absolute cutflow numbers are given** in the talk, only cut
   definitions and two quoted percentages (20.9% at 91 GeV, 1.8% at 160
   GeV). The cutflow plots in `interpret_sm.py` use assumed per-cut
   efficiencies (marked `*`). If/when the team extracts the real cutflow
   from `fce` (aggregate yields only, not the underlying events -- this is
   a summary statistic, not "the data"), replace the `*` numbers with the
   real ones for a genuine cross-energy consistency check instead of a toy
   one.
5. **Task A was never carried out for 91 GeV** (only Task B was shown) **and
   is entirely missing for 240 GeV** (3 samples, no slide at all). This repo
   only provides an expected-composition placeholder for both -- the actual
   identification needs to be done by the team from the real distributions.
6. **HNL mixing-angle cross-check with LEP/L3/DELPHI limits is not
   attempted** in this repo (would need the real observed rate and an
   accurate citation of the published exclusion contours, not a
   from-memory guess) -- a concrete next step for whoever picks this up.
7. Any luminosity/cross-section values used elsewhere in the real analysis
   should be confirmed against the actual generator config; this repo
   deliberately does not use or infer absolute physical cross-sections.

## Data policy

Per the constraint under which this repo was built: nobody on this project
looked at the downloaded FCC-ee/CLD samples to write this code. If synthetic
toy samples are exported to `data/` they are small (npz/csv, generated by a
fixed-seed parametric model) and safe to version -- they are not, and must
never become, a stand-in for the real analysis output.
