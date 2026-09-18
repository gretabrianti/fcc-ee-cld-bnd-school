# Internal scientific consistency audit / provenance table

Every important number used in the revised deck, its source, and its
status. This is the internal check used to prevent mixing source-derived
quantities with assumptions -- not itself presented as a deck slide.

| Quantity | Value | Source | Status |
|---|---:|---|---|
| 91 GeV quoted significance (fit box) | 5.79σ | original deck, slide 14 | quoted (definition not traceable) |
| 91 GeV quoted significance (text) | 7.8σ | original deck, slide 14 | quoted |
| 91 GeV quoted significance (headline) | 7.0σ | original deck, slide 16 | quoted |
| 91 GeV recomputed Tier-1 significance | 7.9σ | `toygen.counting_significance`, this repo | calculated (matches 7.8σ quoted) |
| 91 GeV reconstructed n (excess region) | 31 events | digitised from slide 14 pseudo-data | measured (digitised, ~10-20% precision) |
| 91 GeV quoted excess | 29.6 events | original deck, slide 14 fit box | quoted |
| 91 GeV HNL mass | &asymp;40 GeV | original deck, slide 14 | quoted |
| 365 GeV quoted significance | 6.46σ | original deck, slide 17 | quoted |
| 365 GeV background behind 6.46σ | unknown | not in source material or code | **unresolved -- not available** |
| 365 GeV illustrative background (completeness plot) | &asymp;2.4 events | `interpret_sm.py`, `completeness_plot` | assumed (toy), unrelated to 6.46σ |
| 365 GeV HNL mass | &asymp;150 GeV | original deck, slide 20 | quoted |
| Jet mis-association: naive correct-pairing fraction | 33% | `toygen.three_way_pairing_toy` (1/3 by construction), this repo | calculated |
| Jet mis-association: m_W-constrained correct-pairing fraction | 88% | `toygen.three_way_pairing_toy`, this repo | calculated |
| 91 GeV resonance (H0) χ²/ndof | 40.2/9 = 4.47 | `interpret_bsm.py`, `hypothesis_test_plot` | calculated |
| 91 GeV flat/combinatorial (H1) χ²/ndof | 52.3/9 = 5.81 | `interpret_bsm.py`, `hypothesis_test_plot` | calculated |
| 365 GeV resonance (H0) χ²/ndof | 28.9/7 = 4.12 | `interpret_bsm.py`, `hypothesis_test_plot` | calculated |
| 365 GeV SM-tail (H1) χ²/ndof | 1508.8/7 = 215.55 | `interpret_bsm.py`, `hypothesis_test_plot` | calculated |
| 160 GeV Higgs mass-shape χ²/ndof | 264.4/7 = 37.77 | `interpret_sm.py`, `toy_vs_data_histogram` | calculated |
| 160 GeV WW mass-shape χ²/ndof | 14.8/8 = 1.84 | `interpret_sm.py`, `toy_vs_data_histogram` | calculated |
| 365 GeV ttbar mass-shape χ²/ndof | 4.9/6 = 0.81 | `interpret_sm.py`, `toy_vs_data_histogram` | calculated |
| 365 GeV ZZ mass-shape χ²/ndof | 50.4/6 = 8.40 | `interpret_sm.py`, `toy_vs_data_histogram` | calculated |
| 365 GeV e+e-&rarr;ff&#772;, ZH, WW mass-shape χ² | -- | not computed | **N/A -- not evaluated, not estimated** |
| 160/365 GeV cut efficiencies (all processes) | 5.4%-52.0% | `interpret_sm.py`, `CUTFLOWS_160`/`CUTFLOWS_365` | **assumed/toy (`*`), not measured** -- talk gives cut definitions, not yields |
| 91 GeV quoted overall selection efficiency | 20.9% | original deck, slide 6 | quoted |
| 160 GeV quoted overall selection efficiency | 1.8% | original deck, slide 9 | quoted |
| Look-elsewhere trials factor | none applied | -- | **deliberately not fixed** -- real trials count unavailable |
| b-tag systematic (2%/b-jet), luminosity (2.5%), JEC (1.5%/jet), lepton (1.0%/0.5%) | -- | `fce_studio/engine/systematics.py` (installed analysis code) | measured/configured in the real tool, reused as-is |
| Original 365 GeV pairing method | fixed `m(j2,j3)`, one jet assumed reconstructed | original deck, slides 15/19/20 | quoted/verified against source |
| Current-analysis pairing method | m_W-closest of 3 candidates | `toygen.three_way_pairing_toy`, this repo | new, clearly labelled as current-analysis |

## Audit checklist (section N of the request)

1. Every value above has a traceable source column. ✅
2. No assumed value is labelled as measured (cutflow efficiencies carry `*`
   / "assumed" explicitly, both in the deck and this table). ✅
3. No look-elsewhere trials factor is invented -- none is applied. ✅
4. Original 365 GeV method (hadronic-W, one-jet, fixed j2+j3) and the
   current constrained pairing are visually and textually distinguished
   (`[CURRENT ANALYSIS]` tag, slide 12); the original is never redrawn to
   look like it already used the improved method. ✅
5. 365 GeV significance's background is explicitly labelled unresolved,
   not silently assigned a value. ✅
6. 40 vs. 150 GeV HNL mass tension is a dedicated, visible slide. ✅
7. 365 GeV SM process assignments (Task A) are kept separate from the BSM
   shape tests (Task B) throughout. ✅
8. No claim that rejecting the SM-tail model proves an HNL. ✅
9. Conclusion tables (χ² per process, flat-vs-resonant, jet
   mis-association) are each sourced to code/talk above, with `N/A` used
   rather than an estimate where nothing was computed. ✅
10. No cutflow plots in the deck; efficiencies appear only as the two
    tables (slides 4 and 6). ✅
11. Transition slides present between every speaker/topic change,
    visually minimal. ✅
12. Intro contains both the detector figure and the four-step method
    slide. ✅
13. 91 GeV significance section states the one tier match it could verify
    (Tier 1 ≈ 7.8σ text) and does not claim the other two. ✅
