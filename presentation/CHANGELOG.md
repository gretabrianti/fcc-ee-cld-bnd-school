# Changelog -- presentation revision

## Scientific fixes

- **Removed the `N_trials=8` look-elsewhere assumption** entirely from
  `interpret_bsm.py`'s `significance_hierarchy_plot` (both 91 and 365 GeV
  figures) and from the toy-generator import list. No trials factor is
  substituted; the deck and script instead state explicitly: *"a
  look-elsewhere correction requires the actual number of independent
  search trials and is not fixed here."*
- **91 GeV significance**: kept only the recomputation that is actually
  traceable -- Tier 1 (background-free counting, `sqrt(2n)`) = 7.9σ,
  consistent with the quoted 7.8σ text. We do **not** claim to know which
  tier produced the other two quoted numbers (7.0σ, 5.79σ); the deck says
  so explicitly rather than inventing a correspondence.
- **365 GeV background**: added an explicit statement (deck + printed human
  action items) that the small illustrative background level used in the
  SM-completeness plot is *not* the background behind the quoted 6.46σ --
  neither number is presented as "the" validated background estimate.
- **Jet-pairing framing checked against the original source**: confirmed
  the deck already correctly describes the *original* 365 GeV method
  (hadronic-W channel, one jet assumed reconstructed on the production
  side, fixed `m(j2,j3)`/`m(j2,j3,l2)` pairing) as originally described,
  and labels the m_W-constrained pairing as a **current-analysis addition**
  (`[CURRENT ANALYSIS]` tag on slide 12), never as something the original
  plots already used. No plot or text was found to misattribute this.
- Added the explicit **jet mis-association value**: naive (fixed) pairing
  is correct 33% of the time by construction; the m_W-constrained pairing
  recovers the correct pairing 88% of the time (both numbers already
  computed and printed by `interpret_bsm.py`, reused as-is).

## New scientific-honesty language

- 40 GeV vs. 150 GeV HNL masses presented as an **explicit, unresolved
  consistency question** on its own slide, not folded into a caveat bullet.
- Conclusion language restricted to "consistent with", "supports",
  "disfavours this specific hypothesis" -- never "proves", "discovery" or
  "confirmed".

## Visual / design changes

- New deck built in the **BOOST2026 style** (navy `#003366` header bars,
  red `#C8102E` accent, white body, footer with collaboration / speaker
  name / slide number), following `Reading_the_Excess_BOOST_style.html` as
  the concrete implementation reference.
- **Cutflow plots removed entirely** from the deck; cut efficiencies now
  appear only as compact tables (marked `*` = assumed/toy, never presented
  as measured) on the two SM identification slides.
- **Detector figure** added to the introduction, cropped directly from
  page 3 of the original `FCC-ee CDL collaboration.pdf` (not redrawn).
- **New 4-step method slide** (Define SM &rarr; Evidence &rarr; Interpret
  &rarr; Validate) added to the introduction.
- **5 transition slides** added between every speaker/topic change, styled
  as minimal navy full-bleed cards (large message, one-line subtitle, next
  speaker's name).
- Every content slide carries a **speaker name** in the footer.
- Significance-hierarchy plots kept at both energies but simplified (see
  Scientific fixes above); a small text breadcrumb ("Observed excess →
  Reconstruction → H1 → H0 → Statistical test") added above each to keep
  the validate/reject logic visible without turning it into a flowchart.

## New slides added

Detector figure + method slide (intro), 5 transition slides, SM
efficiency-table slides (160 and 365 GeV), consistency/open-questions
slide, 3 conclusion-table slides (χ² per process, flat-vs-resonant, jet
mis-association), poll slide.

## Speaker assignments (per instruction)

| Section | Speaker |
|---|---|
| Introduction | Vincenzo Del Piano |
| SM @ 160 GeV | Kobe Degeetere |
| SM @ 365 GeV | Saurav Bania |
| BSM @ 91 GeV | Andrea Maria |
| BSM @ 365 GeV | Jurjan Bootsma |
| Consistency / Conclusions / Poll | Greta Brianti |

## Outstanding item

The poll slide QR code is a **visual placeholder only** -- no real QR code
or URL was generated. Insert the actual poll link (e.g. Slido/Mentimeter)
and regenerate a real QR code image before presenting; see
`presentation/OPEN_QUESTIONS.md`.
