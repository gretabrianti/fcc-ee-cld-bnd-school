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

**No real FCC-ee/CLD data or `fce` output was read to build this repo.**
Everything here is a parametric *toy* Monte Carlo, anchored only to what is
explicitly stated or visually readable in the presentation (cut
definitions, quoted percentages, approximate peak positions/widths, quoted
significances). This is intentional -- see the request that led to this
repo. Do not extend these scripts to load real ntuples without first
checking that this is still the intent.

## Layout

```
src/
  toygen.py          shared toy-MC building blocks (resonances, combinatorial
                      backgrounds, cutflow helper, pull/compatibility helper)
  style.py            shared plot style ("FCE (toy, synthetic)" header)
  interpret_sm.py      Task A: SM cutflow tables, mass-spectrum toys,
                       cross-energy consistency check, 91/240 GeV gap panels,
                       SM-completeness check behind the Task B excesses
  interpret_bsm.py     Task B: HNL hypothesis tests at 91 and 365 GeV,
                       W/HNL mass reconstruction toys, alternative-hypothesis
                       tests, and a printed list of human action items
figures/
  sm/                  PNGs produced by interpret_sm.py
  bsm/                 PNGs produced by interpret_bsm.py
notes/
  process_mapping.md   full reasoning behind the X1..X5 -> process mapping
                       used in this repo, energy point by energy point, with
                       the inconsistencies found in the deck itself
data/
  (synthetic toy samples, if/when exported -- see interpret_sm.py / interpret_bsm.py)
```

## Running it

```bash
conda activate bnd_school   # numpy, matplotlib already available there
cd src
python interpret_sm.py
python interpret_bsm.py
```

Each script is self-contained, writes its PNGs under `figures/`, and prints
a short summary (including, for `interpret_bsm.py`, the list of things that
need a human to resolve -- see below).

## What still needs a human

`interpret_bsm.py` prints these at the end of every run; repeated here for
visibility:

1. **91 GeV significance is inconsistent across the deck**: the slide-14 fit
   box quotes 5.79 sigma, the slide-14 body text quotes 7.8 sigma, and the
   slide-16 headline quotes 7 sigma. These can't be reconciled from the
   slides alone -- re-run/inspect the original fit log and fix the deck.
2. **No absolute cutflow numbers are given** in the talk, only cut
   definitions and two quoted percentages (20.9% at 91 GeV, 1.8% at 160
   GeV). The cutflow tables in `interpret_sm.py` use assumed per-cut
   efficiencies (marked `*`). If/when the team extracts the real cutflow
   from `fce` (aggregate yields only, not the underlying events -- this is
   a summary statistic, not "the data"), replace the `*` numbers with the
   real ones for a genuine cross-energy consistency check instead of a toy
   one.
3. **Task A was never carried out for 91 GeV** (only Task B was shown) **and
   is entirely missing for 240 GeV** (3 samples, no slide at all). This repo
   only provides an expected-composition placeholder for both -- the actual
   identification needs to be done by the team from the real distributions.
4. Any luminosity/cross-section values used elsewhere in the real analysis
   should be confirmed against the actual generator config; this repo
   deliberately does not use or infer absolute physical cross-sections.

## Data policy

Per the constraint under which this repo was built: nobody on this project
looked at the downloaded FCC-ee/CLD samples to write this code. If synthetic
toy samples are exported to `data/` they are small (npz/csv, generated by a
fixed-seed parametric model) and safe to version -- they are not, and must
never become, a stand-in for the real analysis output.
