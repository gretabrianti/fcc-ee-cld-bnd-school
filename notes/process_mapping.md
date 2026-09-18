# Process mapping and consistency notes

Reasoning behind every process identification used in `src/interpret_sm.py`
and `src/interpret_bsm.py`, traced back to specific slides in
`FCC-ee CLD collaboration.pdf`. Confidence is stated explicitly for each
item; nothing here was checked against real data.

## 91 GeV (Z pole) -- 5 samples

**Task A was not carried out in the talk.** Slide 7 ("Task A: Discover the
sample") only lists bullets for 160 GeV and 365 GeV; 91 GeV is absent. Slide
6 shows a composition pie for `Total` vs `Dilepton` at 91 GeV
(X1=45%, X2=30%, X3=15%, X4=8%, X5=2% of `Total`; X1=82%, X3=18% of
`Dilepton`) but never states what X1..X5 physically are.

Hypothesis used in `interpret_sm.py::gap_panel_91` (**not a claim**):

| sample | hypothesis | reasoning |
|---|---|---|
| X1 (45%, 82% of dilepton) | Bhabha e+e- -> e+e-(gamma) | t-channel photon exchange cross-section at the Z pole is typically far larger than the Z resonance itself before angular cuts; dominates any "has >=2 leptons" selection almost by construction |
| X2 (30%, absent from dilepton) | Z -> qqbar | hadronic Z decays (BR~70%) are the natural candidate for a large sample that contributes essentially nothing to a dilepton-tagged selection |
| X3 (15%, 18% of dilepton) | Z -> mumu or Z -> tautau | genuine leptonic Z decay; smaller than Bhabha because it's resonance-only, not t-channel-enhanced |
| X4 (8%, absent from dilepton) | gamma-gamma -> hadrons | two-photon background, mostly forward, low visible activity, unlikely to satisfy a clean dilepton tag |
| X5 (2%) | remaining rare leptonic Z flavour / other EW background | smallest of the five, no strong constraint available |

Confidence: **low**. This is a plausibility ordering based on well-known
cross-section hierarchies at the Z pole, not a fit to any observable. Needs
real Task A work.

## 160 GeV (WW threshold) -- 4 samples

Slide 8 gives explicit cut definitions and labels for two processes:

- **Higgs production** (`e+e- -> nu nu H`, `H -> bb`): 2 jets (b-tag>0.7), 0
  leptons, MET pt cut. `m(J1,J2)` peaks around 120-130 GeV in the shown
  histogram, consistent with a Higgs mass peak (confidence: **high**, this
  is stated in the talk, not inferred here).
- **WW production** (semileptonic): 2 jets, 1 lepton, MET pt>5 GeV.
  `m(l1, MET, j1, j2)` peaks around 150-160 GeV, i.e. close to
  `sqrt(s)=160 GeV` as expected for a semileptonic WW decay where the
  reconstructed system approximately recovers the full center-of-mass
  energy (confidence: **high**, stated in the talk).

Slide 9 describes the remaining two samples only qualitatively: high
`deltaR(l1,l2)+deltaR(j1,j2)`, low statistics, "probably WW-gamma", 2
jets+photon channel. X4 dominates the inclusive sample and drops to being
subdominant after a tighter "Event selection" cut where X3 takes over
(1.8% of the total, quoted). This repo does **not** attempt to name X3/X4
individually -- the talk itself only offers "probably WWgamma" as a
hypothesis, and there isn't enough shape information in two histograms to
add anything beyond what's already stated. `interpret_sm.py` builds cutflow
toys only for the two confidently-labelled processes (Higgs, WW) at 160 GeV.

## 240 GeV (ZH run) -- 3 samples

**Task A is entirely missing.** Slide 6 lists "ZH production: 240 GeV - 3
samples" as a working point, but no other slide in the deck shows cuts,
histograms, or a composition chart for it. `interpret_sm.py::gap_panel_240`
provides only an illustrative expected hierarchy (ZH signal, WW background,
e+e- -> ff / ZZ background) based on standard FCC-ee ZH-run physics
expectations -- **not extracted from any data, and not a claim about what
X1/X2/X3 at 240 GeV actually are.**

## 365 GeV (ttbar threshold) -- 5 samples

The most complete Task A section in the talk (slides 10-12):

| sample | process | evidence in the talk |
|---|---|---|
| X1 | ttbar production | slide 10: >=2 lep, >=4 jets (b-tag>0.7), lepton pt>20, MET pt>20; `(j1+met+l1).mass` peaks ~170-190 GeV, consistent with a top-quark-mass-scale reconstruction |
| X2 | e+e- -> ff (Z/gamma\* continuum) | slide 10: >=2 lep, >=4 jets (b-tag<0.7 on leading two), lepton pt>20, jet pt>20, 80<m(l1,l2)<100; `(j1+j2).mass` falls smoothly, consistent with initial-state-radiation-dominated continuum production rather than a resonance |
| X5 | ZZ -> ll qq (t/u-channel e+-) | slide 11: explicit Feynman diagram given in the talk (`e+e- -t/u-channel e+- -> ZZ`), `(j1+j2).mass` peaks sharply at ~90 GeV (one Z decaying hadronically); reported as a "10 sigma observation" for the selection itself (i.e. as a measurement of a known SM process, not a BSM claim) |
| X3 | ZH production | slide 12: >=2 lep, >=2 jets (b-tag>0.7), 80<m(l1,l2)<100, MET pt<10; X3+X5 combination peaks near the Higgs/Z mass region in `(j1+j2).mass` |
| X4 | WW production | slide 12: >=0 lep, >=2 jets (b-tag<0.7), jet/lepton pt>20; X4 dominates `m(l1, MET)` with a peak near 80 GeV, i.e. the W mass |

Confidence: **medium-high** for X1, X2, X5 (explicit cuts + shapes shown and
discussed in the talk); **medium** for X3/X4 (correctly matched to the right
plot panel on slide 12, but the talk does not walk through the identification
logic as explicitly as for X1/X2/X5).

## BSM claims

### 91 GeV: 7.8-sigma / 5.79-sigma / 7-sigma excess -> HNL, m~40 GeV

Selection (slide 14): `MET pt>3 GeV`, `n_lep>=1`, `|d0|<500`. Reconstructed
in `m(J1, l1)`, peaking around 30-50 GeV. Interpreted as a long-lived Heavy
Neutral Lepton.

**Inconsistency found in the deck**: the significance of this excess is
quoted as three different numbers:
- slide 14, fit-result box: **5.79 sigma**
- slide 14, bullet text: **7.8 sigma**
- slide 16, headline number (different observable, `met.pt`): **7 sigma**

These are not necessarily all wrong -- they could correspond to different
observables/fit configurations -- but the deck does not say which is which,
and presenting three different numbers for what reads as "the same
discovery" will draw immediate questions. This needs to be resolved from
the original fit outputs before the next presentation of this material.

### 365 GeV: 6.46-sigma excess -> HNL, m~150 GeV

Selection (slide 17): `pT(MET)<5`, `N_jets>=2`, `N_lep>=2`,
`m(l1,l2)` outside [80,100] GeV, b-veto. Significance quoted as a single,
consistent number this time: **sigma=6.46**.

Production/decay hypothesis (slide 18): `e+e- -> l- N (qqbar)`,
`N -> l'+ q' qbar'`. W-boson reconstructed from the hadronic side (`j2+j3`,
slide 19, broad peak around 80 GeV as expected for a 2-jet W with
combinatorial mis-pairing). HNL mass reconstructed from `j2+j3+l2`
(slide 20): `m_HNL ~ 150 GeV`, with the talk itself noting "sub-optimal
pairing might lead to large spread" -- i.e. acknowledging the reconstruction
is not clean, not claiming a narrow resonance.

`interpret_bsm.py` treats this caveat as a testable claim: a toy mixing a
correctly-paired resonance with a mis-paired combinatorial smear reproduces
the qualitative broad-bump shape seen on slide 19/20, supporting (but not
proving, without the real data) that the observed spread is a
reconstruction/combinatorics effect rather than evidence against the HNL
mass value itself.
