# Open questions / unresolved issues

These are surfaced, not hidden, in the deck itself (Slide 14, "Consistency
/ Open questions") -- repeated here for a written record.

1. **40 GeV vs. 150 GeV HNL mass.** The 91 GeV and 365 GeV excesses are
   both interpreted as a Heavy Neutral Lepton but reconstruct to different
   masses. A single particle has one mass. Either these are two distinct
   states (a stronger claim, unsupported by anything in the source
   material) or one of the two mass measurements is unreliable -- the
   365 GeV one is the more suspect of the two, given the jet-pairing
   ambiguity demonstrated in this study, but that is not a proof.
2. **365 GeV background normalisation** behind the quoted 6.46σ is not
   established from the source material or the analysis code available to
   us. The small background level used in the SM-completeness check
   elsewhere in this project is an unrelated illustrative assumption.
3. **Look-elsewhere / trials factor.** No global-significance correction is
   applied anywhere in this repo. Getting one requires the real number of
   independent search trials from the actual analysis, which is not
   available.
4. **All cutflow efficiencies are toy/assumed values (`*`)**, calibrated
   only against the two overall percentages the talk quotes (20.9% at
   91 GeV, 1.8% at 160 GeV) plus cut definitions -- never measured yields.
5. **91 GeV significance tiering** is only partially reconstructed: Tier 1
   (background-free counting) matches the quoted 7.8σ text. We could not
   trace the other two quoted numbers (7.0σ, 5.79σ) to a specific
   definition from the source material alone.
6. **e+e-→ff, ZH and WW at 365 GeV have no χ²** in the conclusion table --
   that comparison was never computed for those three processes and is
   marked `N/A` rather than estimated.
7. **Rejecting a specific SM-tail/flat hypothesis is not proof of an HNL.**
   Both BSM sections disfavour the *specific* alternative tested; neither
   establishes the resonance interpretation as the only possible
   explanation.
8. **Poll QR code** on the closing slide is a visual placeholder; no real
   URL or QR image has been generated (see CHANGELOG for what to insert).
