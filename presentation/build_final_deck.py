import base64, os
REPO = "/Users/gbrianti/Projects/fcc-ee-cld-bnd-school/figures"
OUT = "/private/tmp/claude-501/-Users-gbrianti/5c921868-ec8f-4cc9-ab75-4abe09df28a3/scratchpad/final_deck.html"

def b64(path_abs_or_rel, rel=True):
    p = os.path.join(REPO, path_abs_or_rel) if rel else path_abs_or_rel
    with open(p, "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode("ascii")

DETECTOR = b64("cld_detector.png")
IMG = {
    "higgs160": b64("sm/08_mass_higgs_160GeV.png"),
    "ww160": b64("sm/09_mass_ww_160GeV.png"),
    "ttbar365": b64("sm/10_mass_ttbar_365GeV.png"),
    "zz365": b64("sm/11_mass_zz_365GeV.png"),
    "hyp91": b64("bsm/01_hnl_91GeV_hypothesis_test.png"),
    "met91": b64("bsm/03_HNL_metpt_91GeV.png"),
    "sig91": b64("bsm/04_significance_hierarchy_91GeV.png"),
    "wmass365": b64("bsm/05_W_mass_365GeV.png"),
    "hnlmass365": b64("bsm/06_HNL_mass_365GeV.png"),
    "alt365": b64("bsm/07_hnl_365GeV_alternative_test.png"),
    "sig365": b64("bsm/08_significance_hierarchy_365GeV.png"),
}

AUTHORS = ("Saurav Bania, Greta Brianti, Jurjan Bootsma, Vincenzo Del Piano, "
           "Kobe Degeetere, Andrea Maria, Sergei Solokhin")

SLIDES = []
def content(speaker, section, title, body, imgs=None, table_html=None, steps=None):
    SLIDES.append(dict(kind="content", speaker=speaker, section=section, title=title,
                        body=body, imgs=imgs or [], table=table_html, steps=steps))
def transition(speaker, msg, sub):
    SLIDES.append(dict(kind="transition", speaker=speaker, msg=msg, sub=sub))

# ============================================================ TITLE
SLIDES.append(dict(kind="title"))

# ============================================================ INTRO (Vincenzo)
content("Vincenzo Del Piano", "Introduction", "FCC-ee and the CLD detector",
    "<ul><li><b>FCC-ee</b>: 100&nbsp;km e&#8314;e&#8315; collider, four working points -- "
    "<b>91</b> (Z pole), <b>160</b> (WW threshold), <b>240</b> (ZH), <b>365&nbsp;GeV</b> (t&#772;t threshold).</li>"
    "<li><b>CLD</b>: silicon vertex/tracker, Si-W ECAL, scintillator-steel HCAL, 2&nbsp;T solenoid "
    "-- precision tracking and calorimetry for jets, leptons and missing energy.</li>"
    "<li>Each working point delivers several <b>anonymised</b> Monte Carlo samples "
    "(X1&#8230;X5) to be identified before any search for new physics.</li></ul>",
    imgs=[("img", DETECTOR, "CLD detector, ~11&times;11&times;2.1&nbsp;m &mdash; original FCC-ee CLD collaboration deck")])

content("Vincenzo Del Piano", "Introduction", "Method: four steps",
    "<div class='steps-big'>"
    "<div class='step'><span>1</span>Define the SM<br><small>what processes are expected at this energy</small></div>"
    "<div class='arrow'>&rarr;</div>"
    "<div class='step'><span>2</span>Find the evidence<br><small>identify an excess over that expectation</small></div>"
    "<div class='arrow'>&rarr;</div>"
    "<div class='step'><span>3</span>Interpret it<br><small>propose a resonance hypothesis (HNL)</small></div>"
    "<div class='arrow'>&rarr;</div>"
    "<div class='step'><span>4</span>Validate it<br><small>test resonant vs. flat/SM-tail hypothesis</small></div>"
    "</div><p class='note-lg'>This talk follows exactly this logic, twice: once at 91&nbsp;GeV, once at 365&nbsp;GeV.</p>")

transition("Kobe Degeetere", "SM process identification at 160 GeV",
           "Reconstructing the known processes before studying the excess")

# ============================================================ SM 160 (Kobe)
eff_table_160 = """
<table class='eff-table'><thead><tr><th>Process</th><th>Key cuts</th><th>Cumulative efficiency</th></tr></thead><tbody>
<tr><td><b>Higgs</b> (&nu;&nu;H, H&rarr;bb&#772;)</td><td>2 jets b-tag&gt;0.7, 0 leptons, MET cut</td><td>32.7%*</td></tr>
<tr><td><b>WW</b> (semileptonic)</td><td>2 jets, 1 lepton, MET&nbsp;p<sub>T</sub>&gt;5&nbsp;GeV</td><td>43.2%*</td></tr>
</tbody></table>
<p class='table-note'>* per-cut efficiencies are assumed (toy), not measured -- the talk gives cut definitions but no absolute cutflow yields.</p>
"""
content("Kobe Degeetere", "SM &middot; 160 GeV", "Task A: identifying the samples",
    "<ul><li><b>Task A</b> = match each anonymous sample to a known SM process using "
    "cuts on jet/lepton multiplicity, b-tagging and MET, then checking the resulting mass peak.</li>"
    "<li>At 160&nbsp;GeV, two of the four samples are confidently identified this way.</li></ul>",
    table_html=eff_table_160)

content("Kobe Degeetere", "SM &middot; 160 GeV", "Higgs and WW mass peaks",
    "<ul><li><b>Higgs</b>: m(J&#8321;,J&#8322;) peaks at ~125&nbsp;GeV, the Higgs mass.</li>"
    "<li><b>WW</b>: the effective mass recovers close to &radic;s&nbsp;=&nbsp;160&nbsp;GeV, as "
    "expected for a semileptonic decay.</li>"
    "<li>Toy MC vs. reported pseudo-data agree at the peak in both cases.</li></ul>",
    imgs=[("img", IMG["higgs160"], ""), ("img", IMG["ww160"], "")])

transition("Saurav Bania", "SM process identification at 365 GeV",
           "Five anonymous samples, five SM assignments")

# ============================================================ SM 365 (Saurav)
eff_table_365 = """
<table class='eff-table'><thead><tr><th>Process</th><th>Cumulative efficiency</th></tr></thead><tbody>
<tr><td><b>t&#772;t</b></td><td>10.7%*</td></tr>
<tr><td><b>e&#8314;e&#8315; &rarr; ff&#772;</b></td><td>10.2%*</td></tr>
<tr><td><b>ZZ &rarr; &#8467;&#8467;qq&#772;</b> (X5)</td><td>8.7%*</td></tr>
<tr><td><b>ZH</b></td><td>5.4%*</td></tr>
<tr><td><b>WW</b></td><td>52.0%*</td></tr>
</tbody></table>
<p class='table-note'>* assumed per-cut efficiencies (toy) -- same caveat as 160&nbsp;GeV; no absolute cutflow yields in the source material.</p>
"""
content("Saurav Bania", "SM &middot; 365 GeV", "All five samples identified",
    "<ul><li>The most complete Task&nbsp;A working point: <b>t&#772;t, e&#8314;e&#8315;&rarr;ff&#772;, "
    "ZZ, ZH, WW</b> all assigned from cuts + mass-peak shape.</li>"
    "<li>More jets available (up to 4) than at 160&nbsp;GeV, enabling b-tag-based separation "
    "of top and Higgs final states from continuum.</li></ul>",
    table_html=eff_table_365)

content("Saurav Bania", "SM &middot; 365 GeV", "Strongest evidence: t&#772;t and ZZ",
    "<ul><li><b>t&#772;t</b>: m(j&#8321;,MET,l&#8321;) peaks at the top-mass scale "
    "-- best toy/data agreement of any process studied (&chi;&sup2;/ndof&nbsp;=&nbsp;0.81).</li>"
    "<li><b>ZZ&rarr;&#8467;&#8467;qq&#772;</b> (X5): dijet mass peaks cleanly at "
    "m<sub>Z</sub>&nbsp;=&nbsp;91&nbsp;GeV (&chi;&sup2;/ndof&nbsp;=&nbsp;8.4, peak region only).</li></ul>",
    imgs=[("img", IMG["ttbar365"], ""), ("img", IMG["zz365"], "")])

transition("Andrea Maria", "From SM identification to the excess",
           "Once the samples are identified, can the SM explain the observed structure?")

# ============================================================ BSM 91 (Andrea)
steps91 = ["Observed excess", "Reconstruction: m(J&#8321;,l&#8321;)", "H1: flat background",
           "H0: HNL resonance, m&asymp;40&nbsp;GeV", "Statistical test"]

content("Andrea Maria", "BSM &middot; 91 GeV", "An excess, not an SM sample",
    "<ul><li>Selection: MET&nbsp;p<sub>T</sub>&gt;3&nbsp;GeV, &ge;1 lepton, |d&#8320;|&lt;500 "
    "-- a lepton+jet final state not explained by the identified SM processes.</li>"
    "<li>Proposed interpretation: a long-lived <b>Heavy Neutral Lepton</b>, reconstructed "
    "mass &asymp;40&nbsp;GeV.</li>"
    "<li>H0 (resonance) tracks the reported peak better than H1 (flat combinatorial): "
    "&chi;&sup2;/ndof 4.47 vs. 5.81.</li></ul>",
    imgs=[("img", IMG["hyp91"], "")])

content("Andrea Maria", "BSM &middot; 91 GeV", "Independent cross-check",
    "<ul><li>A second, independent observable (met.pt) is consistent with the same "
    "hypothesis (&chi;&sup2;/ndof&nbsp;=&nbsp;1.14) -- not a repeat of the mass-peak test.</li></ul>",
    imgs=[("img", IMG["met91"], "")])

content("Andrea Maria", "BSM &middot; 91 GeV", "Significance: which definition?",
    "<ul><li>The source quotes three numbers: 5.79 / 7.0 / 7.8&sigma;. Our recomputation "
    "shows <b>Tier&nbsp;1</b> (background-free counting, &radic;2n) lands at 7.9&sigma; "
    "-- consistent with the quoted 7.8&sigma;.</li>"
    "<li>The original source does not label which tier produced the other two numbers; "
    "we do not invent that correspondence beyond this one match.</li>"
    "<li>No look-elsewhere correction is applied: that requires the real number of "
    "independent search trials, not available here.</li></ul>",
    imgs=[("img", IMG["sig91"], "")], steps=steps91)

transition("Jurjan Bootsma", "The excess at 365 GeV",
           "Testing reconstruction and background hypotheses")

# ============================================================ BSM 365 (Jurjan)
content("Jurjan Bootsma", "BSM &middot; 365 GeV", "The excess and the original method",
    "<ul><li>Signal region: p<sub>T</sub>(MET)&lt;5, N<sub>jets</sub>&ge;2, N<sub>lep</sub>&ge;2, "
    "Z-veto, b-veto -- interpreted, again, as an HNL.</li>"
    "<li><b>Original method</b> (as described in the source): hadronic-W channel, "
    "<u>one jet assumed reconstructed</u>, W mass from a <u>fixed</u> m(j&#8322;,j&#8323;) pairing, "
    "HNL mass from m(j&#8322;,j&#8323;,l&#8322;).</li>"
    "<li>The source itself flags this: <i>&ldquo;sub-optimal pairing might lead to large spread&rdquo;, "
    "&ldquo;other possible candidates&rdquo;</i> -- a caveat on that same original method.</li></ul>")

content("Jurjan Bootsma", "BSM &middot; 365 GeV",
    "<span class='current-tag'>CURRENT ANALYSIS</span> A kinematic-pairing test",
    "<ul><li>With 4 jets there are 3 candidate pairings. We test: does picking the pairing "
    "closest to m<sub>W</sub>=80.4&nbsp;GeV (rather than the fixed j&#8322;+j&#8323;) change the result?</li>"
    "<li><b>Naive</b> (fixed pairing, as original): correct only 33% of the time by construction "
    "-- reproduces the flat, weak shape in the source plots.</li>"
    "<li><b>Constrained</b> (m<sub>W</sub>-closest, new step): correct 88% of the time, "
    "narrows both the W and HNL peaks substantially.</li>"
    "<li>This is quantitative evidence that the original fixed pairing <b>can mis-associate jets</b> "
    "-- it does not by itself establish an HNL.</li></ul>",
    imgs=[("img", IMG["wmass365"], "Naive = original method &middot; Constrained = current-analysis step"),
          ("img", IMG["hnlmass365"], "Same pairing choice, propagated to the HNL mass")])

steps365 = ["Observed excess", "Reconstruction: m(jj,&#8467;&#8467;)", "H1: SM ZZ/WW tail",
            "H0: HNL resonance, m&asymp;150&nbsp;GeV", "Statistical test"]
content("Jurjan Bootsma", "BSM &middot; 365 GeV", "Resonance vs. SM-tail, and significance",
    "<ul><li>H0 (localised resonance) vs. H1 (mis-measured SM ZZ/WW tail, using the "
    "<i>already-identified</i> 365&nbsp;GeV processes): &chi;&sup2;/ndof 4.12 vs. 215.55 "
    "-- disfavours this specific SM-tail hypothesis.</li>"
    "<li>Quoted significance: <b>6.46&sigma;</b>. The background level behind that number "
    "is not established in the source; the small flat level used elsewhere in this study "
    "is an illustrative assumption only, not a validated background estimate.</li></ul>",
    imgs=[("img", IMG["alt365"], ""), ("img", IMG["sig365"], "")], steps=steps365)

transition("Greta Brianti", "What has been established -- and what remains open?",
           "Consistency, caveats, and conclusions")

# ============================================================ CONSISTENCY (Greta)
content("Greta Brianti", "Consistency", "Open questions",
    "<ul><li><b>40&nbsp;GeV vs. 150&nbsp;GeV</b>: two reconstructed HNL masses at two energies. "
    "A single particle has one mass -- this is an unresolved consistency question, not "
    "explained away by the analysis to date.</li>"
    "<li><b>Background normalisation</b> at 365&nbsp;GeV is not established from source.</li>"
    "<li><b>Look-elsewhere trials</b>: not fixed here; needs the real search-trial count.</li>"
    "<li><b>Toy vs. real cutflows</b>: all cut efficiencies shown are assumed (*), not measured.</li>"
    "<li>Rejecting one SM-tail hypothesis is <b>not</b> proof of an HNL.</li></ul>")

# ---- Conclusion tables ----
chi2_table = """
<table class='eff-table'><thead><tr><th>Process (365 GeV)</th><th>&chi;&sup2;/ndof (toy vs. pseudo-data)</th></tr></thead><tbody>
<tr><td>t&#772;t</td><td>0.81</td></tr>
<tr><td>ZZ &rarr; &#8467;&#8467;qq&#772;</td><td>8.40</td></tr>
<tr><td>e&#8314;e&#8315; &rarr; ff&#772;</td><td>N/A -- not evaluated</td></tr>
<tr><td>ZH</td><td>N/A -- not evaluated</td></tr>
<tr><td>WW</td><td>N/A -- not evaluated</td></tr>
</tbody></table>
<table class='eff-table' style='margin-top:10px'><thead><tr><th>Process (160 GeV)</th><th>&chi;&sup2;/ndof</th></tr></thead><tbody>
<tr><td>Higgs</td><td>37.77</td></tr>
<tr><td>WW</td><td>1.84</td></tr>
</tbody></table>
"""
content("Greta Brianti", "Conclusions", "&chi;&sup2; per SM process",
    "<p class='note-lg'>Only processes where a toy-vs-pseudo-data comparison was actually "
    "computed are shown with a value; the rest are marked N/A rather than estimated.</p>",
    table_html=chi2_table)

flat_res_table = """
<table class='eff-table'><thead><tr><th></th><th>91 GeV</th><th>365 GeV</th></tr></thead><tbody>
<tr><td>Resonance (H0) &chi;&sup2;/ndof</td><td>4.47</td><td>4.12</td></tr>
<tr><td>Flat / SM-tail (H1) &chi;&sup2;/ndof</td><td>5.81</td><td>215.55</td></tr>
<tr><td>Reconstructed mass</td><td>&asymp;40 GeV</td><td>&asymp;150 GeV</td></tr>
<tr><td>Quoted significance</td><td>5.79 / 7.0 / 7.8&sigma;</td><td>6.46&sigma;</td></tr>
<tr><td>Jet mis-association (365 only)</td><td>&mdash;</td><td>33% &rarr; 88% correct pairing</td></tr>
</tbody></table>
"""
content("Greta Brianti", "Conclusions", "Flat vs. resonant hypothesis",
    "<p class='note-lg'>At both energies the resonance hypothesis fits better than the "
    "tested flat/SM-tail alternative. This supports, but does not prove, the resonance "
    "interpretation -- it rejects the <i>specific</i> background models tested here.</p>",
    table_html=flat_res_table)

content("Greta Brianti", "Conclusions", "Where this leaves us",
    "<ul><li>Five SM processes identified at 365&nbsp;GeV, two at 160&nbsp;GeV, each with "
    "traceable (not invented) validation numbers.</li>"
    "<li>Two excesses, at 91 and 365&nbsp;GeV, both <b>consistent with</b> a resonance "
    "hypothesis under the tests performed -- and both with open caveats (mass tension, "
    "background normalisation, look-elsewhere).</li>"
    "<li>FCC-ee/CLD's precision lets even small, carefully-validated excesses be taken "
    "seriously -- provided every claim stays traceable to source or code.</li></ul>"
    "<p class='note-lg'><b>So: what do you think is really in there?</b></p>")

# ============================================================ POLL
SLIDES.append(dict(kind="poll"))

# ---------------------------------------------------------------------------
def render(i, s):
    if s["kind"] == "title":
        return f"""<section class="slide title-slide">
          <h1>Task A &amp; Task B: SM Identification and BSM Validation</h1>
          <h2>FCC-ee with the CLD Detector</h2>
          <div class="authors-container"><strong>FCC-ee CLD Collaboration</strong><br><br>
          <p>{AUTHORS}</p></div>
        </section>"""
    if s["kind"] == "transition":
        return f"""<section class="slide transition-slide">
          <div class="t-msg">{s['msg']}</div>
          <div class="t-sub">{s['sub']}</div>
          <div class="t-speaker">Next: <b>{s['speaker']}</b></div>
        </section>"""
    if s["kind"] == "poll":
        return """<section class="slide poll-slide">
          <div class="slide-header"><h2>Audience poll</h2></div>
          <div class="slide-content poll-content">
            <h3>Which process do you think could be among the BSM processes studied?</h3>
            <div class="poll-grid">
              <div class="poll-opts">
                <div class="opt"><span>A</span>Heavy Neutral Lepton (HNL)</div>
                <div class="opt"><span>B</span>Leptoquark</div>
                <div class="opt"><span>C</span>Dark photon / Z&prime;</div>
                <div class="opt"><span>D</span>Supersymmetric slepton</div>
              </div>
              <div class="qr"><div class="qr-box">QR CODE<br><small>placeholder -- insert poll URL</small></div>
              <div class="scan">Scan and vote</div></div>
            </div>
          </div>
          <div class="slide-footer"><span>FCC-ee CLD Collaboration</span>
          <span class="speaker-name">Greta Brianti</span><span>Poll</span></div>
        </section>"""

    imgs_html = "".join(f"<figure><img src='{src}' alt=''>" + (f"<figcaption>{cap}</figcaption>" if cap else "") + "</figure>"
                         for _, src, cap in s["imgs"])
    media = f"<div class='media n{len(s['imgs'])}'>{imgs_html}</div>" if imgs_html else ""
    table = s.get("table") or ""
    steps_html = ""
    if s.get("steps"):
        steps_html = "<div class='mini-steps'>" + "<span class='sep'>&rarr;</span>".join(
            f"<span>{st}</span>" for st in s["steps"]) + "</div>"
    return f"""<section class="slide">
      <div class="slide-header"><h2>{s['title']}</h2><span class="section-tag">{s['section']}</span></div>
      <div class="slide-content">
        {steps_html}
        <div class="body-cols">
          <div class="text-col">{s['body']}{table}</div>
          {media}
        </div>
      </div>
      <div class="slide-footer"><span>FCC-ee CLD Collaboration</span>
      <span class="speaker-name">{s['speaker']}</span><span>Slide {i+1}</span></div>
    </section>"""

slides_html = "\n".join(render(i, s) for i, s in enumerate(SLIDES))

TEMPLATE = r"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>FCC-ee CLD: Task A/B Results</title>
<style>
:root{ color-scheme: light; }
* { box-sizing:border-box; margin:0; padding:0; font-family:'Helvetica Neue',Helvetica,Arial,sans-serif; }
body{ background:#333; display:flex; flex-direction:column; align-items:center; padding:24px 16px; gap:26px; }
.slide{ width:100%; max-width:1100px; aspect-ratio:16/9; background:#FFFFFF; position:relative;
  box-shadow:0 10px 24px rgba(0,0,0,.35); display:flex; flex-direction:column; overflow:hidden; }
.title-slide{ justify-content:center; align-items:center; text-align:center;
  background:linear-gradient(135deg,#FFFFFF 60%,#F8F9FA 100%); border-top:14px solid #C8102E; padding:0 40px; }
.title-slide h1{ color:#003366; font-size:2.4rem; margin-bottom:12px; max-width:900px; line-height:1.15; }
.title-slide h2{ color:#4A5568; font-size:1.3rem; font-weight:300; margin-bottom:32px; }
.authors-container{ background:#F8F9FA; border-top:3px solid #C8102E; padding:14px 26px; width:82%; }
.authors-container p{ color:#003366; font-size:.92rem; line-height:1.5; }
.slide-header{ background:#003366; color:#FFF; padding:16px 34px; display:flex; justify-content:space-between;
  align-items:center; border-bottom:5px solid #C8102E; }
.slide-header h2{ font-size:1.5rem; font-weight:600; }
.section-tag{ font-size:.72rem; letter-spacing:.06em; text-transform:uppercase; color:#B9C4D6; font-weight:600; }
.slide-content{ padding:22px 34px; flex-grow:1; color:#222; overflow:hidden; display:flex; flex-direction:column; }
.slide-content ul{ margin-left:20px; font-size:1.02rem; line-height:1.55; }
.slide-content li{ margin-bottom:9px; }
.slide-content b{ color:#003366; }
.note-lg{ font-size:1.02rem; color:#4A5568; margin-top:8px; }
.body-cols{ display:flex; gap:26px; flex:1; align-items:flex-start; }
.text-col{ flex:1; min-width:0; }
.media{ display:flex; flex-direction:column; gap:8px; flex:1.15; min-width:0; }
.media.n2{ flex-direction:row; }
.media figure{ margin:0; background:#F8F9FA; border:1px solid #E2E8F0; border-radius:6px; padding:6px; flex:1; min-width:0; }
.media img{ width:100%; display:block; border-radius:3px; }
.media figcaption{ font-size:.65rem; color:#718096; text-align:center; margin-top:4px; }
.eff-table{ width:100%; border-collapse:collapse; font-size:.85rem; margin-top:10px; }
.eff-table th{ text-align:left; color:#003366; border-bottom:2px solid #003366; padding:5px 8px; }
.eff-table td{ padding:5px 8px; border-bottom:1px solid #E2E8F0; color:#333; }
.table-note{ font-size:.72rem; color:#718096; margin-top:8px; }
.current-tag{ display:inline-block; background:#C8102E; color:#fff; font-size:.6em; font-weight:700;
  letter-spacing:.05em; padding:3px 9px; border-radius:3px; margin-right:8px; vertical-align:middle; }
.slide-footer{ position:relative; width:100%; padding:10px 34px; background:#FFF; border-top:1px solid #E2E8F0;
  display:flex; justify-content:space-between; align-items:center; font-size:.72rem; color:#718096; }
.speaker-name{ font-weight:700; color:#C8102E; }
.steps-big{ display:flex; align-items:center; justify-content:center; gap:10px; flex-wrap:wrap; margin:24px 0; }
.steps-big .step{ background:#F8F9FA; border-top:3px solid #C8102E; padding:14px 16px; width:180px; text-align:center; }
.steps-big .step span{ display:block; font-size:1.6rem; font-weight:800; color:#003366; }
.steps-big .step small{ color:#718096; font-size:.72rem; }
.steps-big .arrow{ color:#C8102E; font-size:1.4rem; }
.mini-steps{ display:flex; gap:6px; flex-wrap:wrap; font-size:.68rem; color:#4A5568; margin-bottom:10px;
  background:#F8F9FA; padding:6px 10px; border-radius:4px; }
.mini-steps .sep{ color:#C8102E; margin:0 4px; }
.transition-slide{ justify-content:center; align-items:center; text-align:center; background:#003366;
  color:#FFF; padding:0 60px; }
.t-msg{ font-size:2rem; font-weight:700; margin-bottom:14px; }
.t-sub{ font-size:1.1rem; color:#B9C4D6; font-weight:300; margin-bottom:26px; }
.t-speaker{ font-size:1rem; color:#FFF; border-top:2px solid #C8102E; padding-top:12px; }
.poll-content{ align-items:center; text-align:center; }
.poll-content h3{ font-size:1.5rem; color:#003366; margin:10px 0 26px; }
.poll-grid{ display:flex; gap:40px; align-items:center; justify-content:center; width:100%; }
.poll-opts{ display:flex; flex-direction:column; gap:10px; text-align:left; width:340px; }
.opt{ display:flex; align-items:center; gap:12px; font-size:1rem; font-weight:600; padding:10px 14px;
  border:1.5px solid #E2E8F0; border-radius:6px; color:#222; }
.opt span{ width:26px; height:26px; border-radius:999px; background:#003366; color:#fff; display:flex;
  align-items:center; justify-content:center; font-size:.85rem; flex:none; }
.qr{ display:flex; flex-direction:column; align-items:center; gap:10px; }
.qr-box{ width:160px; height:160px; border:2.5px dashed #C8102E; border-radius:8px; display:flex;
  align-items:center; justify-content:center; flex-direction:column; font-weight:800; color:#C8102E;
  letter-spacing:.05em; text-align:center; font-size:.85rem; }
.qr-box small{ font-weight:500; color:#718096; margin-top:5px; font-size:.6rem; }
.scan{ font-weight:700; color:#4A5568; }
@media (max-width:800px){ .body-cols{flex-direction:column;} .media.n2{flex-direction:column;} .poll-grid{flex-direction:column;} }
</style></head>
<body>
__SLIDES__
</body></html>
"""

out = TEMPLATE.replace("__SLIDES__", slides_html)
with open(OUT, "w") as f:
    f.write(out)
print("wrote", OUT, "bytes:", os.path.getsize(OUT), "slides:", len(SLIDES))
