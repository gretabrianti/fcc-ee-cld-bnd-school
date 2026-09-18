# fce pipeline

`pipeline.json` is a ready-to-load node graph for `fce` (the `fce_studio`
GUI installed in the `bnd_school` conda env, File &rarr; Load Pipeline)
covering exactly the tests this project still needs to run for real, and
nothing else:

| Energy | Task A (sample ID) | Task B (BSM search) |
|---|---|---|
| 91 GeV  | **not included** (by request) | HNL search: `m(J1,l1)` + `met.pt` cross-check (slides 14, 16) |
| 160 GeV | Higgs (&nu;&nu;H) + WW (semileptonic) | &mdash; |
| 240 GeV | **not included** (never attempted in the talk either) | &mdash; |
| 365 GeV | ttbar, e&#8314;e&#8315;&rarr;ff&#772;, ZZ (X5), ZH, WW | "New Physics" excess (slide 17, &sigma;=6.46) |

## Loading it

```
conda activate bnd_school
fce
```
Then **File &rarr; Load Pipeline** and pick `fce_pipeline/pipeline.json`.
63 nodes across 9 branches, one `DataSource` per energy (91/160/365 GeV)
fanning out into each branch's own `Multiplicity` &rarr; `Selection`
chain &rarr; observable &rarr; `Histogram`.

## What each branch actually does

- **Task A histograms** (`cb_target = "None"`): plain identification plots
  &mdash; every sample's shape stacked, no fit. This is deliberately the
  *only* mode used for the Task A branches: it lets you compare the shapes
  yourself rather than pre-selecting a "signal", which would defeat the
  point of a blind identification exercise.
- **Task B histograms** (`cb_target = "New Physics"`): triggers `fce`'s own
  data-driven excess fit (`fce_studio/engine/fitter.py`) &mdash; the same
  mechanism behind the quoted 91 GeV and 365 GeV significances in the talk.
- **365 GeV "New Physics" branch** reproduces the team's own validated
  selection (`met.pt<5`, Z-veto on `m(l1,l2)`, `njets>2`, b-veto on all 4
  jets) exactly as found in a previously-exported pipeline on this machine
  (`~/Desktop/pipeline_646sigma_clean_selection_new_physics_365.json`),
  with two corrections/additions:
  - the **primary** observable is set to the actual slide-17 variable,
    `(j1+j2+j3+j4+l1+l2).mass` (the exported file's own primary observable
    only summed 2 of the 4 jets);
  - the team's own multi-pairing exploration (`(j1+j2+l1).mass`,
    `(j1+j2+l2).mass`, `(j1+j3+l1).mass`, `(j1+j3+l2).mass`) is kept as
    secondary observables on the same histogram, so you can compare them
    side by side &mdash; this is exactly the kind of by-hand pairing
    exploration the toy-MC validation (`interpret_bsm.py`,
    `toygen.three_way_pairing_toy`) argued should replace an unconstrained
    default jet ordering. Running this branch for real is the natural next
    step after that toy result.
- **91 GeV branch**: reconstructs `m(J1,l1)` (slide 14) and, separately,
  `met.pt` (slide 16) from the *same* upstream selection (`nlep>=1`,
  `met.pt>3`, `|d0(l1)|<500`), each with its own `New Physics` fit &mdash;
  running both gives two independently-fit significances for the same
  excess, which is the real-data version of the cross-check
  `03_HNL_metpt_91GeV.png` already does with a toy.

## One placeholder that needs a human

`Higgs: MET cut -- SET THRESHOLD` (160 GeV branch) is left as `met.pt > 0`
(a no-op). The talk states a "MET pt cut" is applied but never quotes the
threshold (slide 8) &mdash; pick a real value before trusting that branch's
output, everything else in this pipeline uses a cut value taken directly
from a slide.

## Schema note

This schema was reverse-engineered from `fce_studio/ui/graph.py`
(`save_pipeline`/`_snapshot_node`) and cross-checked against the team's own
previously-exported pipeline files on this machine &mdash; i.e. from the
analysis tool's own config format and prior *exported configs*, never from
the downloaded ntuples. `build_pipeline.py` regenerates `pipeline.json`
from a small Python DSL (`PB`/`datasource`/`multiplicity`/`selection`/
`obscustom`/`histogram`) if you need to add or tweak a branch; a schema
self-check (valid `Fit Signal` target per energy, valid operators, valid
object/variable names, no dangling links) can be re-run by loading the
JSON and checking it against `_FIT_CHOICES`/`_OPS`/`_OBJ_VARS` in
`fce_studio/ui/graph.py` if the tool's schema ever changes.
