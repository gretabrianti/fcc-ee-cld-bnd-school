"""
Builds pipeline.json for fce (fce_studio), covering exactly the tests the
team asked for:

  - 160 GeV Task A : Higgs (nu-nu H) and WW (semileptonic) identification
  - 365 GeV Task A : ttbar, e+e- -> ff, ZZ (X5), ZH, WW identification
  - 365 GeV Task B : the "New Physics" excess search (slide 17, sigma=6.46),
                      reproducing the team's own validated selection plus
                      the multi-pairing observable comparison they were
                      already exploring
  - 91 GeV  Task B : the HNL excess search ONLY (slide 14 + slide 16
                      met.pt cross-check) -- no 91 GeV Task A

Explicitly EXCLUDED, per instruction:
  - 91 GeV Task A (sample identification)
  - everything at 240 GeV (Task A was never attempted there either)

Schema reverse-engineered from fce_studio/ui/graph.py (save_pipeline /
_snapshot_node) and cross-checked against the team's own exported pipeline
files (Desktop/*.json) -- this is the analysis tool's config format, not
the downloaded data.
"""
import json

OUT = "/private/tmp/claude-501/-Users-gbrianti/5c921868-ec8f-4cc9-ab75-4abe09df28a3/scratchpad/pipeline.json"


class PB:
    def __init__(self):
        self.next_id = 0
        self.nodes = []
        self.links = []

    def nid(self):
        n = self.next_id
        self.next_id += 1
        return n

    def node(self, nid, node_type, name, values, pos, obs_row_count=None):
        self.nodes.append(dict(nid=nid, node_type=node_type, name=name,
                                values=values, pos=list(pos), obs_row_count=obs_row_count))

    def link(self, src, dst):
        self.links.append((src, dst))

    def render(self):
        touching = {n["nid"]: [] for n in self.nodes}
        for s, d in self.links:
            touching[s].append({"src_nid": s, "dst_nid": d})
            touching[d].append({"src_nid": s, "dst_nid": d})
        nodes_out = [
            {
                "type": "node", "nid": n["nid"], "node_type": n["node_type"],
                "pos": n["pos"], "name": n["name"], "values": n["values"],
                "links": touching[n["nid"]], "obs_row_count": n["obs_row_count"],
            }
            for n in self.nodes
        ]
        seen = []
        for s, d in self.links:
            if (s, d) not in seen:
                seen.append((s, d))
        links_out = [{"type": "link", "src_nid": s, "dst_nid": d} for s, d in seen]
        return {"version": 1, "next_id": self.next_id, "nodes": nodes_out, "links": links_out}


pb = PB()

# ---------------------------------------------------------------------------
# node-type factories
# ---------------------------------------------------------------------------

def datasource(x, y, energy, name=None):
    nid = pb.nid()
    pb.node(nid, "DataSource", name or f"CLD {energy} data",
             {f"cb_energy_{nid}": energy, f"cb_detector_{nid}": "CLD"}, (x, y))
    return nid


def multiplicity(x, y, name, ltype="Any", lep=0, lep_op=">=", jet=0, jet_op=">=",
                  phot=0, phot_op=">="):
    nid = pb.nid()
    pb.node(nid, "Multiplicity", name, {
        f"cb_ltype_{nid}": ltype,
        f"cb_op_lep_{nid}": lep_op, f"txt_leptons_{nid}": lep,
        f"cb_op_jet_{nid}": jet_op, f"txt_jets_{nid}": jet,
        f"cb_op_phot_{nid}": phot_op, f"txt_photons_{nid}": phot,
    }, (x, y))
    return nid


def selection(x, y, name, expr):
    nid = pb.nid()
    pb.node(nid, "Selection", name, {f"txt_sel_{nid}": expr}, (x, y))
    return nid


def obscustom(x, y, name, expr):
    nid = pb.nid()
    pb.node(nid, "ObsCustom", name, {f"txt_obs_{nid}": expr}, (x, y))
    return nid


def obsobject(x, y, name, pairs):
    nid = pb.nid()
    values = {}
    terms = []
    for i, (obj, var) in enumerate(pairs):
        values[f"obs_o_obj_{nid}_{i}"] = obj
        values[f"obs_o_var_{nid}_{i}"] = var
        terms.append(f"{obj}.{var}")
    values[f"obs_expr_{nid}"] = " + ".join(terms)
    pb.node(nid, "ObsObject", name, values, (x, y), obs_row_count=len(pairs))
    return nid


def histogram(x, y, name, target="None", bins=40, rmin=0.0, rmax=150.0):
    nid = pb.nid()
    pb.node(nid, "Histogram", name, {
        f"cb_target_{nid}": target, f"txt_bins_{nid}": bins,
        f"txt_range_min_{nid}": rmin, f"txt_range_max_{nid}": rmax,
    }, (x, y))
    return nid


def chain(*nids):
    for a, b in zip(nids, nids[1:]):
        pb.link(a, b)


STAGE = 150  # vertical spacing between pipeline stages on the canvas

# ===========================================================================
# 160 GeV -- Task A (slide 8)
# ===========================================================================

ds160 = datasource(-1600, -60, "160 GeV")

# --- Higgs: nu-nu H, H -> bb ---
x = -1750
m = multiplicity(x, -60 + STAGE, "Higgs: presel.", ltype="Any", jet=2, jet_op=">=")
s1 = selection(x, -60 + 2 * STAGE, "Higgs: b-tag>0.7 on j1,j2",
               "j1.btag > 0.7 and j2.btag > 0.7")
s2 = selection(x, -60 + 3 * STAGE, "Higgs: 0 leptons", "nlep == 0")
s3 = selection(x, -60 + 4 * STAGE,
               "Higgs: MET cut -- SET THRESHOLD (talk gives no number)", "met.pt > 0")
o1 = obscustom(x, -60 + 5 * STAGE, "m(J1,J2)", "(j1.p4 + j2.p4).mass")
h1 = histogram(x, -60 + 6 * STAGE, "Higgs mass", target="None", bins=40, rmin=60, rmax=160)
pb.link(ds160, m)
chain(m, s1, s2, s3, o1, h1)

# --- WW: semileptonic ---
x = -1450
m = multiplicity(x, -60 + STAGE, "WW: presel.", ltype="Any", lep=1, lep_op="==", jet=2, jet_op=">=")
s1 = selection(x, -60 + 2 * STAGE, "WW: MET pt > 5 GeV", "met.pt > 5")
o1 = obscustom(x, -60 + 3 * STAGE, "m(l1,MET,J1,J2)", "(l1.p4 + met.p4 + j1.p4 + j2.p4).mass")
h1 = histogram(x, -60 + 4 * STAGE, "WW mass", target="None", bins=40, rmin=120, rmax=185)
pb.link(ds160, m)
chain(m, s1, o1, h1)

# ===========================================================================
# 365 GeV -- Task A (slides 10-12) + Task B (slide 17)
# ===========================================================================

ds365 = datasource(-900, -60, "365 GeV")

# --- ttbar (slide 10) ---
x = -1150
m = multiplicity(x, -60 + STAGE, "ttbar: presel.", lep=2, lep_op=">=", jet=4, jet_op=">=")
s1 = selection(x, -60 + 2 * STAGE, "ttbar: b-tag>0.7 on j1..j4",
               "j1.btag > 0.7 and j2.btag > 0.7 and j3.btag > 0.7 and j4.btag > 0.7")
s2 = selection(x, -60 + 3 * STAGE, "ttbar: lepton pt>20", "l1.pt > 20 and l2.pt > 20")
s3 = selection(x, -60 + 4 * STAGE, "ttbar: MET pt>20", "met.pt > 20")
o1 = obscustom(x, -60 + 5 * STAGE, "(j1+met+l1).mass", "(j1.p4 + met.p4 + l1.p4).mass")
h1 = histogram(x, -60 + 6 * STAGE, "ttbar mass", target="None", bins=50, rmin=0, rmax=400)
pb.link(ds365, m)
chain(m, s1, s2, s3, o1, h1)

# --- e+e- -> ff (slide 10) ---
x = -850
m = multiplicity(x, -60 + STAGE, "e+e->ff: presel.", lep=2, lep_op=">=", jet=4, jet_op=">=")
s1 = selection(x, -60 + 2 * STAGE, "e+e->ff: b-tag<0.7 on j1,j2 (leading two)",
               "j1.btag < 0.7 and j2.btag < 0.7")
s2 = selection(x, -60 + 3 * STAGE, "e+e->ff: lepton pt>20", "l1.pt > 20 and l2.pt > 20")
s3 = selection(x, -60 + 4 * STAGE, "e+e->ff: 80<m(l1,l2)<100",
               "(l1.p4 + l2.p4).mass > 80 and (l1.p4 + l2.p4).mass < 100")
o1 = obscustom(x, -60 + 5 * STAGE, "(j1+j2).mass", "(j1.p4 + j2.p4).mass")
h1 = histogram(x, -60 + 6 * STAGE, "e+e->ff mass", target="None", bins=40, rmin=0, rmax=400)
pb.link(ds365, m)
chain(m, s1, s2, s3, o1, h1)

# --- ZZ -> llqq (X5) (slide 11) ---
x = -550
m = multiplicity(x, -60 + STAGE, "ZZ: presel.", lep=2, lep_op=">=", jet=2, jet_op=">=")
s1 = selection(x, -60 + 2 * STAGE, "ZZ: b-tag<0.7 on j1,j2", "j1.btag < 0.7 and j2.btag < 0.7")
s2 = selection(x, -60 + 3 * STAGE, "ZZ: lepton/jet pt>20",
               "l1.pt > 20 and l2.pt > 20 and j1.pt > 20 and j2.pt > 20")
s3 = selection(x, -60 + 4 * STAGE, "ZZ: Z-veto on m(l1,l2)",
               "(l1.p4 + l2.p4).mass < 80 or (l1.p4 + l2.p4).mass > 100")
s4 = selection(x, -60 + 5 * STAGE, "ZZ: MET pt<20", "met.pt < 20")
o1 = obscustom(x, -60 + 6 * STAGE, "(j1+j2).mass", "(j1.p4 + j2.p4).mass")
h1 = histogram(x, -60 + 7 * STAGE, "ZZ mass (X5)", target="None", bins=40, rmin=0, rmax=400)
pb.link(ds365, m)
chain(m, s1, s2, s3, s4, o1, h1)

# --- ZH (slide 12) ---
x = -250
m = multiplicity(x, -60 + STAGE, "ZH: presel.", lep=2, lep_op=">=", jet=2, jet_op=">=")
s1 = selection(x, -60 + 2 * STAGE, "ZH: b-tag>0.7 on j1,j2", "j1.btag > 0.7 and j2.btag > 0.7")
s2 = selection(x, -60 + 3 * STAGE, "ZH: lepton/jet pt>20",
               "l1.pt > 20 and l2.pt > 20 and j1.pt > 20 and j2.pt > 20")
s3 = selection(x, -60 + 4 * STAGE, "ZH: 80<m(l1,l2)<100",
               "(l1.p4 + l2.p4).mass > 80 and (l1.p4 + l2.p4).mass < 100")
s4 = selection(x, -60 + 5 * STAGE, "ZH: MET pt<10", "met.pt < 10")
o1 = obscustom(x, -60 + 6 * STAGE, "(j1+j2).mass", "(j1.p4 + j2.p4).mass")
h1 = histogram(x, -60 + 7 * STAGE, "ZH mass", target="None", bins=40, rmin=0, rmax=400)
pb.link(ds365, m)
chain(m, s1, s2, s3, s4, o1, h1)

# --- WW, 365 GeV selection (slide 12) ---
x = 50
m = multiplicity(x, -60 + STAGE, "WW(365): presel.", lep=0, lep_op=">=", jet=2, jet_op=">=")
s1 = selection(x, -60 + 2 * STAGE, "WW(365): b-tag<0.7 on j1,j2", "j1.btag < 0.7 and j2.btag < 0.7")
s2 = selection(x, -60 + 3 * STAGE,
               "WW(365): lepton/jet pt>20 (talk also says >=0 leptons -- kept as-is)",
               "l1.pt > 20 and j1.pt > 20 and j2.pt > 20")
o1 = obscustom(x, -60 + 4 * STAGE, "m(l1,MET)", "(l1.p4 + met.p4).mass")
h1 = histogram(x, -60 + 5 * STAGE, "WW(365) mass", target="None", bins=40, rmin=0, rmax=220)
pb.link(ds365, m)
chain(m, s1, s2, o1, h1)

# --- 365 GeV Task B: "New Physics" excess (slide 17, sigma=6.46) ---
# Selection reproduces the team's own validated pipeline
# (Desktop/pipeline_646sigma_clean_selection_new_physics_365.json) exactly;
# the primary observable is corrected to the actual slide-17 variable
# (all 4 jets + 2 leptons), with the team's own multi-pairing exploration
# kept as secondary observables on the same histogram -- directly useful
# for testing the m(jj)=m_W pairing-constraint fix flagged in the toy-MC
# validation (see notes/process_mapping.md).
x = 400
m = multiplicity(x, -60 + STAGE, "New Physics: presel.", ltype="Electron",
                  lep=2, lep_op=">=", jet=4, jet_op=">=")
s1 = selection(x, -60 + 2 * STAGE, "New Physics: nlep>=2", "nlep >= 2")
s2 = selection(x, -60 + 3 * STAGE, "New Physics: njets>2", "njets > 2")
s3 = selection(x, -60 + 4 * STAGE, "New Physics: MET<5, Z-veto on m(l1,l2)",
               "met.pt < 5 and ((l1.p4 + l2.p4).mass < 80 or (l1.p4 + l2.p4).mass > 100)")
s4 = selection(x, -60 + 5 * STAGE, "New Physics: b-veto on j1..j4",
               "j1.btag < 0.7 and j2.btag < 0.7 and j3.btag < 0.7 and j4.btag < 0.7")
pb.link(ds365, m)
chain(m, s1, s2, s3, s4)

obs_x = 650
o_main = obscustom(obs_x, -60 + 5 * STAGE - 40,
                    "PRIMARY: (j1+j2+j3+j4+l1+l2).mass -- slide 17 observable",
                    "(j1.p4 + j2.p4 + j3.p4 + j4.p4 + l1.p4 + l2.p4).mass")
o_lpt = obsobject(obs_x, -60 + 5 * STAGE + 60, "l1.pt+l2.pt", [("l1", "pt"), ("l2", "pt")])
o_p1 = obscustom(obs_x, -60 + 5 * STAGE + 160, "pairing: (j1+j2+l1).mass",
                  "(j1.p4 + j2.p4 + l1.p4).mass")
o_p2 = obscustom(obs_x, -60 + 5 * STAGE + 260, "pairing: (j1+j2+l2).mass",
                  "(j1.p4 + j2.p4 + l2.p4).mass")
o_p3 = obscustom(obs_x, -60 + 5 * STAGE + 360, "pairing: (j1+j3+l1).mass",
                  "(j1.p4 + j3.p4 + l1.p4).mass")
o_p4 = obscustom(obs_x, -60 + 5 * STAGE + 460, "pairing: (j1+j3+l2).mass",
                  "(j1.p4 + j3.p4 + l2.p4).mass")
h_np = histogram(obs_x + 300, -60 + 5 * STAGE + 210, "New Physics fit",
                  target="New Physics", bins=40, rmin=0.0, rmax=400.0)
for o in (o_main, o_lpt, o_p1, o_p2, o_p3, o_p4):
    pb.link(s4, o)
    pb.link(o, h_np)

# ===========================================================================
# 91 GeV -- Task B ONLY (slide 14 + slide 16). No 91 GeV Task A by request.
# ===========================================================================

ds91 = datasource(1100, -60, "91 GeV")
x = 1100
m = multiplicity(x, -60 + STAGE, "HNL search: presel.", ltype="Any",
                  lep=1, lep_op=">=", jet=1, jet_op=">=")
s1 = selection(x, -60 + 2 * STAGE, "HNL search: MET pt>3 GeV", "met.pt > 3")
s2 = selection(x, -60 + 3 * STAGE, "HNL search: |d0(l1)|<500", "abs(l1.d0) < 500")
pb.link(ds91, m)
chain(m, s1, s2)

o_mass = obscustom(x - 150, -60 + 4 * STAGE, "m(J1,l1) -- slide 14", "(j1.p4 + l1.p4).mass")
h_mass = histogram(x - 150, -60 + 5 * STAGE, "HNL mass fit", target="New Physics",
                    bins=12, rmin=8.0, rmax=62.0)
pb.link(s2, o_mass)
pb.link(o_mass, h_mass)

o_met = obscustom(x + 150, -60 + 4 * STAGE, "met.pt -- slide 16 cross-check", "met.pt")
h_met = histogram(x + 150, -60 + 5 * STAGE, "HNL met.pt fit", target="New Physics",
                   bins=11, rmin=0.0, rmax=41.0)
pb.link(s2, o_met)
pb.link(o_met, h_met)

# ===========================================================================
with open(OUT, "w") as f:
    json.dump(pb.render(), f, indent=2)

n = pb.render()
print("wrote", OUT)
print("nodes:", len(n["nodes"]), " links:", len(n["links"]))
