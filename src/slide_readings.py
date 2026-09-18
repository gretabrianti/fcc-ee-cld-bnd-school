"""
Single source of truth for every number that was read directly off a plot or
a bullet point in `FCC-ee CLD collaboration.pdf`.

Nothing here comes from the real downloaded fce/CLD ntuples. These are either
values explicitly quoted in the talk (e.g. significances, the 29.6-event
excess, the 20.9%/1.8% selection efficiencies) or approximate digitisations
of histogram bin heights, read by eye off the slide images -- good enough to
check shape/order-of-magnitude consistency, not a substitute for the real
cutflow. Every array below says which slide it comes from.
"""
from __future__ import annotations

import numpy as np

# ---------------------------------------------------------------------------
# 91 GeV -- BSM search (slides 14, 16)
# ---------------------------------------------------------------------------

# slide 14: m(J1, l1), signal region of the lepton+jet excess
S91_MJ1L1_CENTERS = np.array([12.5, 17.5, 22.5, 27.5, 32.5, 37.5, 42.5, 47.5, 52.5, 57.5])
S91_MJ1L1_DATA = np.array([0, 1, 2, 5, 6, 2, 7, 2, 3, 3])

# slide 14 fit box: "Excess over all samples: 29.6 events, Significance: 5.79 sigma"
S91_EXCESS_QUOTED = 29.6
S91_SIGMA_FITBOX = 5.79        # slide 14, fit-result box (pyhf-style profile likelihood, most likely)
S91_SIGMA_TEXT = 7.8           # slide 14, bullet text ("Observed 7.8 sigma excess")
S91_SIGMA_SLIDE16 = 7.0        # slide 16 headline, different observable (met.pt)

# slide 16: met.pt, same excess region, different observable/binning
S91_METPT_CENTERS = np.array([2.0, 5.5, 9.0, 13.0, 16.5, 20.0, 23.5, 27.0, 31.0, 34.5, 38.0])
S91_METPT_DATA = np.array([1, 2, 4, 8, 4, 8, 0, 1, 0, 0, 0])

# ---------------------------------------------------------------------------
# 365 GeV -- BSM search (slide 17)
# ---------------------------------------------------------------------------

S365_MTOT_CENTERS = np.array([220.0, 250.0, 280.0, 310.0, 340.0, 370.0, 400.0, 430.0])
S365_MTOT_DATA = np.array([0, 3, 6, 8, 24, 4, 2, 1])
S365_SIGMA_QUOTED = 6.46       # slide 17, single quoted number

# ---------------------------------------------------------------------------
# 160 GeV -- Task A (slide 8)
# ---------------------------------------------------------------------------

# Higgs production, m(J1,J2), approximate pseudo-data points read off slide 8
S160_HIGGS_MJJ_CENTERS = np.array([65, 75, 85, 95, 105, 115, 125, 135])
S160_HIGGS_MJJ_DATA = np.array([4, 9, 18, 17, 26, 39, 40, 6])

# WW production, m(l1, MET, J1, J2), approximate pseudo-data
S160_WW_MLMETJJ_CENTERS = np.array([125, 130, 135, 140, 145, 150, 155, 160, 165])
S160_WW_MLMETJJ_DATA = np.array([2, 3, 5, 12, 20, 35, 38, 15, 4])

# quoted selection efficiencies (talk gives these two numbers explicitly)
S91_DILEPTON_EFF_QUOTED = 0.209   # slide 6, 91 GeV, "Dilepton" selection
S160_WWGAMMA_EFF_QUOTED = 0.018   # slide 9, 160 GeV, tight WWgamma-like selection

# ---------------------------------------------------------------------------
# 365 GeV -- Task A (slides 10-12)
# ---------------------------------------------------------------------------

S365_TTBAR_MASS_CENTERS = np.array([120, 140, 160, 180, 200, 220, 240])
S365_TTBAR_MASS_DATA = np.array([3, 15, 40, 48, 25, 8, 2])

S365_ZZ_MASS_CENTERS = np.array([60, 70, 80, 90, 100, 110, 120])
S365_ZZ_MASS_DATA = np.array([3, 10, 47, 107, 20, 6, 2])

S365_W_MASS_CENTERS = np.array([25, 45, 65, 75, 85, 95, 115, 135])
S365_W_MASS_DATA = np.array([1, 2, 5, 15, 6, 4, 5, 3])

# Digitised in a second pass (lower precision than the arrays above -- the
# source pseudo-data points are small and dense on these three panels).
# e+e- -> ffbar, (j1+j2).mass, slide 10 bottom-right.
S365_EEFF_MASS_CENTERS = np.array([10, 30, 50, 70, 90, 110, 130, 150, 170, 190, 210, 230])
S365_EEFF_MASS_DATA = np.array([1, 2, 6, 3, 2, 2, 2, 2, 1, 2, 1, 1])

# ZH, (j1+j2).mass, slide 12 left panel.
S365_ZH_MASS_CENTERS = np.array([65, 75, 85, 95, 105, 115, 130, 150])
S365_ZH_MASS_DATA = np.array([9, 16, 15, 24, 14, 11, 3, 1])

# WW (365 GeV selection), m(l1, MET), slide 12 middle panel -- dominated by
# an underflow-like spike near 0 with a flat low tail; approximate.
S365_WW_MASS_CENTERS = np.array([10, 40, 70, 100, 130, 160, 190])
S365_WW_MASS_DATA = np.array([180, 5, 5, 5, 3, 2, 2])

# ---------------------------------------------------------------------------
# Systematics constants, copied (not imported) from the installed fce_studio
# package: envs/bnd_school/lib/python3.11/site-packages/fce_studio/engine/
# systematics.py. This is analysis *code/config*, not the downloaded dataset
# -- reading it is consistent with the "look at fce's code, not the data"
# instruction under which this repo is built. Copied rather than imported so
# this repo stays runnable without the fce_studio package installed.
# ---------------------------------------------------------------------------

LUMI_UNC = 0.025        # 2.5% correlated luminosity uncertainty
JEC_PER_JET = 0.015     # 1.5% per jet (Jet Energy Correction)
LEP_PER_EL = 0.01       # 1.0% per electron
LEP_PER_MU = 0.005      # 0.5% per muon
BTAG_PER_BJET = 0.02    # 2.0% per b-tagged jet
BTAG_WP = 0.7           # b-tagging working point -- matches every b-tag>0.7 cut in the talk
