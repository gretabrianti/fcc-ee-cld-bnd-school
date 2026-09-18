import base64, os
REPO = "/Users/gbrianti/Projects/fcc-ee-cld-bnd-school/figures"
OUT = "/Users/gbrianti/Projects/fcc-ee-cld-bnd-school/presentation/final_deck.html"

def b64(rel):
    with open(os.path.join(REPO, rel), "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode("ascii")

DETECTOR = b64("cld_detector.png")
FEYN_HNL91 = b64("feyn_hnl_91.png")
FEYN_HNL365 = b64("feyn_hnl_365.png")
FEYN_TTBAR = b64("feyn_ttbar.png")
IMG = {
    "higgs160": b64("sm/08_mass_higgs_160GeV.png"),
    "ww160": b64("sm/09_mass_ww_160GeV.png"),
    "ttbar365": b64("sm/10_mass_ttbar_365GeV.png"),
    "zz365": b64("sm/11_mass_zz_365GeV.png"),
    "comp91": b64("sm/16_completeness_91GeV.png"),
    "comp365": b64("sm/17_completeness_365GeV.png"),
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

def hl(txt):
    return f"<span class='hl'>{txt}</span>"

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
    f"<ul><li>FCC-ee: a 100&nbsp;km e&#8314;e&#8315; collider. Four energies: "
    f"{hl('91')} (Z pole), {hl('160')} (WW), {hl('240')} (ZH), {hl('365&nbsp;GeV')} (t&#772;t).</li>"
    "<li>CLD gives us tracking, calorimetry and a 2&nbsp;T field &mdash; enough to reconstruct "
    "jets, leptons and missing energy.</li>"
    "<li>Each energy hands us several <b>anonymised</b> samples. We don't know what they are yet.</li></ul>",
    imgs=[("plot", DETECTOR, "CLD detector &mdash; original FCC-ee CLD collaboration deck")])

content("Vincenzo Del Piano", "Introduction", "Method: four steps",
    "<div class='steps-big'>"
    "<div class='step'><span>1</span>Define the SM</div>"
    "<div class='arrow'>&rarr;</div>"
    "<div class='step'><span>2</span>Find an excess</div>"
    "<div class='arrow'>&rarr;</div>"
    "<div class='step'><span>3</span>Interpret it</div>"
    "<div class='arrow'>&rarr;</div>"
    "<div class='step'><span>4</span>Validate it</div>"
    "</div>"
    f"<p class='note-lg'>At {hl('91')} and {hl('365&nbsp;GeV')} we found an excess &mdash; all four "
    f"steps apply. At {hl('160')} and {hl('240&nbsp;GeV')}, no excess was found. "
    "We stop after step 1.</p>")

transition("Kobe Degeetere", "SM process identification at 160 GeV",
           "Reconstructing the known processes before studying the excess")

# ============================================================ SM 160 (Kobe)
eff_table_160 = """
<table class='eff-table'><thead><tr><th>Process</th><th>Key cuts</th><th>Efficiency</th></tr></thead><tbody>
<tr><td><b>Higgs</b> (&nu;&nu;H, H&rarr;bb&#772;)</td><td>2 jets b-tag&gt;0.7, 0 leptons, MET cut</td><td>32.7%*</td></tr>
<tr><td><b>WW</b> (semileptonic)</td><td>2 jets, 1 lepton, MET&nbsp;p<sub>T</sub>&gt;5&nbsp;GeV</td><td>43.2%*</td></tr>
</tbody></table>
<p class='table-note'>* assumed (toy), not measured &mdash; the talk gives cuts, not absolute yields.</p>
"""
content("Kobe Degeetere", "SM &middot; 160 GeV &middot; step 1 only", "Task A: identifying the samples",
    "<p>Task A: match each anonymous sample to a known process, using cuts on jets, leptons, "
    "b-tagging and MET. Two of four samples are identified this way. No excess is searched for "
    "at this energy &mdash; step 1 of the method is all we need here.</p>",
    table_html=eff_table_160)

content("Kobe Degeetere", "SM &middot; 160 GeV", "Higgs and WW mass peaks",
    f"<p>Higgs: the dijet mass peaks at {hl('~125&nbsp;GeV')}. WW: the effective mass recovers "
    f"close to {hl('&radic;s = 160&nbsp;GeV')}, as expected for a semileptonic decay. Both agree "
    "with the reported points at the peak.</p>",
    imgs=[("plot", IMG["higgs160"], ""), ("plot", IMG["ww160"], "")])

transition("Saurav Bania", "SM process identification at 365 GeV",
           "Five anonymous samples, five SM assignments")

# ============================================================ SM 365 (Saurav)
eff_table_365 = """
<table class='eff-table'><thead><tr><th>Process</th><th>Efficiency</th></tr></thead><tbody>
<tr><td>t&#772;t</td><td>10.7%*</td></tr>
<tr><td>e&#8314;e&#8315; &rarr; ff&#772;</td><td>10.2%*</td></tr>
<tr><td>ZZ &rarr; &#8467;&#8467;qq&#772; (X5)</td><td>8.7%*</td></tr>
<tr><td>ZH</td><td>5.4%*</td></tr>
<tr><td>WW</td><td>52.0%*</td></tr>
</tbody></table>
<p class='table-note'>* assumed (toy), not measured.</p>
"""
content("Saurav Bania", "SM &middot; 365 GeV &middot; step 1 only", "All five samples identified",
    "<p>365 GeV is the most complete working point: all five samples get an assignment "
    "&mdash; t&#772;t, e&#8314;e&#8315;&rarr;ff&#772;, ZZ, ZH, WW. More jets are available here "
    "than at 160&nbsp;GeV, so b-tagging separates these final states well.</p>",
    table_html=eff_table_365)

content("Saurav Bania", "SM &middot; 365 GeV", "Strongest evidence: t&#772;t and ZZ",
    f"<p>t&#772;t: reconstructed mass sits at the top scale, {hl('&chi;&sup2;/ndof = 0.81')} "
    "&mdash; the best agreement in this study. ZZ: dijet mass peaks cleanly at "
    f"{hl('m<sub>Z</sub> = 91&nbsp;GeV')}.</p>",
    imgs=[("diagram", FEYN_TTBAR, "t&#772;t production"),
          ("plot", IMG["ttbar365"], ""), ("plot", IMG["zz365"], "")])

transition("Andrea Maria", "From SM identification to the excess",
           "Once the samples are identified, can the SM explain the observed structure?")

# ============================================================ BRIDGE: excess vs SM
content("Andrea Maria", "Evidence &middot; both energies", "The SM alone doesn't explain it",
    f"<p>Sum every identified SM process and compare to the reported points. At both "
    f"{hl('91')} and {hl('365&nbsp;GeV')} the excess sits far above that sum. This is why an "
    "interpretation is needed &mdash; step 2 becomes step 3.</p>",
    imgs=[("plot", IMG["comp91"], "91 GeV"), ("plot", IMG["comp365"], "365 GeV")])

# ============================================================ BSM 91 (Andrea)
steps91 = ["Excess", "Reconstruction", "H1: flat bkg", "H0: HNL, m&asymp;40", "Test"]

content("Andrea Maria", "BSM &middot; 91 GeV", "An excess, not an SM sample",
    "<p>Tight selection: MET&nbsp;p<sub>T</sub>&gt;3&nbsp;GeV, &ge;1 lepton, small impact "
    f"parameter. A lepton+jet excess appears. Proposed: a {hl('Heavy Neutral Lepton')}, "
    f"mass {hl('&asymp;40&nbsp;GeV')}. The resonance hypothesis fits better than a flat "
    f"background: {hl('&chi;&sup2;/ndof 4.47 vs. 5.81')}.</p>",
    imgs=[("diagram", FEYN_HNL91, "HNL at a Z-factory"), ("plot", IMG["hyp91"], "")], steps=steps91)

content("Andrea Maria", "BSM &middot; 91 GeV", "An independent cross-check",
    f"<p>A second, independent variable &mdash; missing energy itself &mdash; agrees with the same "
    f"hypothesis: {hl('&chi;&sup2;/ndof = 1.14')}. This isn't the same test twice.</p>",
    imgs=[("plot", IMG["met91"], "")])

content("Andrea Maria", "BSM &middot; 91 GeV", "Significance: which definition?",
    f"<p>The source quotes {hl('~7&sigma;')} as its headline number. Our background-free "
    "recomputation gives 7.9&sigma; &mdash; close, but we can't confirm they're the same "
    "definition. The source also quotes 5.79&sigma; and 7.8&sigma; elsewhere; we don't know "
    "which tier those are (see audit). No look-elsewhere correction is applied: we don't have "
    "a real trials count.</p>",
    imgs=[("plot", IMG["sig91"], "")])

transition("Jurjan Bootsma", "The excess at 365 GeV",
           "Testing reconstruction and background hypotheses")

# ============================================================ BSM 365 (Jurjan)
content("Jurjan Bootsma", "BSM &middot; 365 GeV", "The excess, and the original method",
    f"<p>Tighter selection again: low MET, {hl('&ge;2 jets, &ge;2 leptons')}, Z-veto, b-veto. "
    "Original method: hadronic-W channel, one jet assumed, a fixed pairing "
    "m(j&#8322;,j&#8323;). The source itself flags this: <i>&ldquo;sub-optimal pairing might "
    "lead to large spread.&rdquo;</i></p>",
    imgs=[("diagram", FEYN_HNL365, "Production and decay, slide 18")])

content("Jurjan Bootsma", "BSM &middot; 365 GeV",
    "<span class='current-tag'>CURRENT ANALYSIS</span> Testing the pairing",
    f"<p>Four jets give three candidate pairings. The fixed original pairing is correct only "
    f"{hl('33%')} of the time by construction. Picking the pairing closest to m<sub>W</sub> "
    f"instead gets it right {hl('88%')} of the time, and both peaks narrow sharply. This is "
    "evidence the original pairing can mis-associate jets &mdash; it supports better "
    "reconstruction, not an HNL by itself.</p>",
    imgs=[("plot", IMG["wmass365"], "Naive = original &middot; Constrained = current analysis"),
          ("plot", IMG["hnlmass365"], "")])

content("Jurjan Bootsma", "BSM &middot; 365 GeV", "Resonance vs. SM-tail, and significance",
    f"<p>Resonance vs. a mis-measured ZZ/WW tail: {hl('&chi;&sup2;/ndof 4.12 vs. 215.55')} "
    f"&mdash; this specific SM-tail model is disfavoured. Quoted significance: "
    f"{hl('6.46&sigma;')}. The background behind that number isn't established in the source.</p>",
    imgs=[("plot", IMG["alt365"], ""), ("plot", IMG["sig365"], "")])

transition("Greta Brianti", "What has been established -- and what remains open?",
           "Consistency, caveats, and conclusions")

# ============================================================ CONSISTENCY (Greta)
content("Greta Brianti", "Consistency", "Open questions",
    f"<ul><li>{hl('40&nbsp;GeV vs. 150&nbsp;GeV')}: two HNL masses. One particle has one mass. "
    "This is open, not explained away.</li>"
    "<li>365&nbsp;GeV background normalisation: not established.</li>"
    "<li>No look-elsewhere trial count is available, so none is applied.</li>"
    "<li>Every cut efficiency shown is a toy assumption.</li>"
    "<li>Rejecting one background model is not proof of an HNL.</li></ul>")

chi2_table = """
<table class='eff-table'><thead><tr><th>Process (365 GeV)</th><th>&chi;&sup2;/ndof</th></tr></thead><tbody>
<tr><td>t&#772;t</td><td>0.81</td></tr>
<tr><td>ZZ &rarr; &#8467;&#8467;qq&#772;</td><td>8.40</td></tr>
<tr><td>e&#8314;e&#8315; &rarr; ff&#772;</td><td>5.17&dagger;</td></tr>
<tr><td>ZH</td><td>3.89&dagger;</td></tr>
<tr><td>WW</td><td>26.22&dagger;</td></tr>
</tbody></table>
<table class='eff-table' style='margin-top:8px'><thead><tr><th>Process (160 GeV)</th><th>&chi;&sup2;/ndof</th></tr></thead><tbody>
<tr><td>Higgs</td><td>37.77</td></tr>
<tr><td>WW</td><td>1.84</td></tr>
</tbody></table>
<p class='table-note'>&dagger; second-pass digitisation, lower precision than the other rows (see PROVENANCE_AUDIT.md).</p>
"""
content("Greta Brianti", "Conclusions", "&chi;&sup2; per SM process",
    "<p>All five 365&nbsp;GeV processes and both 160&nbsp;GeV processes now have a "
    "toy-vs-pseudo-data comparison &mdash; every value traceable to this repo's code.</p>",
    table_html=chi2_table)

flat_res_table = """
<table class='eff-table'><thead><tr><th></th><th>91 GeV</th><th>365 GeV</th></tr></thead><tbody>
<tr><td>Resonance (H0) &chi;&sup2;/ndof</td><td>4.47</td><td>4.12</td></tr>
<tr><td>Flat / SM-tail (H1) &chi;&sup2;/ndof</td><td>5.81</td><td>215.55</td></tr>
<tr><td>Reconstructed mass</td><td>&asymp;40 GeV</td><td>&asymp;150 GeV</td></tr>
<tr><td>Quoted significance</td><td>5.79 / 7 / 7.8&sigma;</td><td>6.46&sigma;</td></tr>
<tr><td>Jet mis-association (365 only)</td><td>&mdash;</td><td>33% &rarr; 88%</td></tr>
</tbody></table>
"""
content("Greta Brianti", "Conclusions", "Flat vs. resonant hypothesis",
    "<p>At both energies the resonance hypothesis fits better than the flat/SM-tail "
    "alternative tested. That supports the interpretation. It doesn't prove it.</p>",
    table_html=flat_res_table)

content("Greta Brianti", "Conclusions", "Where this leaves us",
    f"<p>Five SM processes at 365&nbsp;GeV, two at 160&nbsp;GeV, each traceable. Two excesses, "
    f"both {hl('consistent with')} a resonance hypothesis, both with open caveats. "
    "FCC-ee's precision lets small, careful excesses be taken seriously &mdash; if every "
    f"claim stays traceable. So: {hl('what do you think is really in there?')}</p>")

# ============================================================ POLL
SLIDES.append(dict(kind="poll"))

# ---------------------------------------------------------------------------
def render_media(imgs):
    if not imgs:
        return ""
    parts = []
    for kind, src, cap in imgs:
        cls = "diagram-img" if kind == "diagram" else "plot-img"
        capline = f"<div class='cap'>{cap}</div>" if cap else ""
        parts.append(f"<div class='mfig {cls}'><img src='{src}' alt=''>{capline}</div>")
    n = len(imgs)
    return f"<div class='media n{n}'>" + "".join(parts) + "</div>"

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

    media = render_media(s["imgs"])
    table = s.get("table") or ""
    steps_html = ""
    if s.get("steps"):
        steps_html = "<div class='mini-steps'>" + "<span class='sep'>&rarr;</span>".join(
            f"<span>{st}</span>" for st in s["steps"]) + "</div>"
    return f"""<section class="slide">
      <div class="slide-header"><h2>{s['title']}</h2><span class="section-tag">{s['section']}</span></div>
      <div class="slide-content">
        <div class="text-block">{steps_html}{s['body']}{table}</div>
        {media}
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
.slide{ width:100%; max-width:1120px; aspect-ratio:16/9; background:#FFFFFF; position:relative;
  box-shadow:0 10px 24px rgba(0,0,0,.35); display:flex; flex-direction:column; overflow:hidden; }
.title-slide{ justify-content:center; align-items:center; text-align:center;
  background:linear-gradient(135deg,#FFFFFF 60%,#F8F9FA 100%); border-top:14px solid #C8102E; padding:0 40px; }
.title-slide h1{ color:#003366; font-size:2.3rem; margin-bottom:12px; max-width:900px; line-height:1.15; }
.title-slide h2{ color:#4A5568; font-size:1.25rem; font-weight:300; margin-bottom:30px; }
.authors-container{ background:#F8F9FA; border-top:3px solid #C8102E; padding:14px 26px; width:82%; }
.authors-container p{ color:#003366; font-size:.9rem; line-height:1.5; }
.slide-header{ background:#003366; color:#FFF; padding:14px 32px; display:flex; justify-content:space-between;
  align-items:center; border-bottom:5px solid #C8102E; flex:none; }
.slide-header h2{ font-size:1.35rem; font-weight:600; }
.section-tag{ font-size:.68rem; letter-spacing:.05em; text-transform:uppercase; color:#B9C4D6; font-weight:600; }
/* consistent layout: text block ALWAYS on top, plot(s) ALWAYS centered below */
.slide-content{ padding:16px 32px 14px; flex:1; color:#222; display:flex; flex-direction:column;
  align-items:center; justify-content:center; min-height:0; }
.text-block{ width:100%; max-width:980px; font-size:.92rem; line-height:1.42; flex:none; }
.text-block p{ margin:2px 0; }
.text-block ul{ margin:2px 0 0 20px; }
.text-block li{ margin-bottom:4px; }
.text-block b{ color:#003366; }
.hl{ color:#C8102E; font-weight:700; }
.note-lg{ font-size:.92rem; color:#4A5568; margin-top:6px; }
.current-tag{ display:inline-block; background:#C8102E; color:#fff; font-size:.55em; font-weight:700;
  letter-spacing:.04em; padding:3px 8px; border-radius:3px; margin-right:7px; vertical-align:middle; }
/* media: centered row, NO boxes/frames/shadows on images */
.media{ display:flex; justify-content:center; align-items:center; gap:16px; flex:1; min-height:0;
  width:100%; margin-top:6px; }
.mfig{ display:flex; flex-direction:column; align-items:center; height:100%; min-width:0; }
.mfig img{ max-height:100%; max-width:100%; object-fit:contain; }
.media.n1 .mfig{ max-width:78%; }
.media.n2 .mfig{ max-width:46%; }
.media.n3 .mfig{ max-width:32%; }
.diagram-img img{ max-height:85%; }
.mfig .cap{ font-size:.6rem; color:#718096; text-align:center; margin-top:3px; }
.eff-table{ width:100%; border-collapse:collapse; font-size:1rem; margin-top:22px; }
.eff-table th{ text-align:left; color:#003366; border-bottom:2px solid #003366; padding:11px 8px; }
.eff-table td{ padding:11px 8px; border-bottom:1px solid #E2E8F0; color:#333; }
.table-note{ font-size:.68rem; color:#718096; margin-top:6px; }
.slide-footer{ position:relative; width:100%; padding:8px 32px; background:#FFF; border-top:1px solid #E2E8F0;
  display:flex; justify-content:space-between; align-items:center; font-size:.68rem; color:#718096; flex:none; }
.speaker-name{ font-weight:700; color:#C8102E; }
.steps-big{ display:flex; align-items:center; justify-content:center; gap:8px; flex-wrap:wrap; margin:18px 0 10px; }
.steps-big .step{ background:#F8F9FA; border-top:3px solid #C8102E; padding:12px 14px; width:160px; text-align:center; font-size:.85rem; font-weight:600; color:#003366; }
.steps-big .step span{ display:block; font-size:1.5rem; font-weight:800; color:#003366; }
.steps-big .arrow{ color:#C8102E; font-size:1.3rem; }
.mini-steps{ display:flex; gap:5px; flex-wrap:wrap; font-size:.62rem; color:#4A5568; margin-bottom:6px; }
.mini-steps .sep{ color:#C8102E; margin:0 3px; }
.transition-slide{ justify-content:center; align-items:center; text-align:center; background:#003366;
  color:#FFF; padding:0 60px; }
.t-msg{ font-size:1.9rem; font-weight:700; margin-bottom:12px; }
.t-sub{ font-size:1.05rem; color:#B9C4D6; font-weight:300; margin-bottom:24px; }
.t-speaker{ font-size:.95rem; color:#FFF; border-top:2px solid #C8102E; padding-top:10px; }
.poll-content{ align-items:center; text-align:center; justify-content:center; flex:1; }
.poll-content h3{ font-size:1.4rem; color:#003366; margin:10px 0 24px; }
.poll-grid{ display:flex; gap:40px; align-items:center; justify-content:center; width:100%; }
.poll-opts{ display:flex; flex-direction:column; gap:9px; text-align:left; width:320px; }
.opt{ display:flex; align-items:center; gap:11px; font-size:.95rem; font-weight:600; padding:9px 13px;
  border:1.5px solid #E2E8F0; border-radius:6px; color:#222; }
.opt span{ width:24px; height:24px; border-radius:999px; background:#003366; color:#fff; display:flex;
  align-items:center; justify-content:center; font-size:.8rem; flex:none; }
.qr{ display:flex; flex-direction:column; align-items:center; gap:9px; }
.qr-box{ width:150px; height:150px; border:2.5px dashed #C8102E; border-radius:8px; display:flex;
  align-items:center; justify-content:center; flex-direction:column; font-weight:800; color:#C8102E;
  letter-spacing:.05em; text-align:center; font-size:.8rem; }
.qr-box small{ font-weight:500; color:#718096; margin-top:5px; font-size:.58rem; }
.scan{ font-weight:700; color:#4A5568; }
@media (max-width:800px){ .media{flex-wrap:wrap;} .poll-grid{flex-direction:column;} }

@media print{
  @page{ size: 1280px 720px; margin:0; }
  body{ background:#fff; padding:0; gap:0; display:block; }
  .slide{ width:1280px; height:720px; max-width:none; aspect-ratio:auto; box-shadow:none;
    page-break-after:always; margin:0; }
  /* PDF renderer (weasyprint) doesn't reliably propagate flex percentage-heights,
     so cap image height with an explicit pixel value instead of relying on
     .mfig{height:100%}/.img{max-height:100%} alone -- otherwise single-image
     (n1) slides overflow the whole page. */
  .media{ max-height:430px; }
  .mfig{ height:auto; max-height:430px; }
  .mfig img{ max-height:430px; }
}
</style></head>
<body>
__SLIDES__
</body></html>
"""

out = TEMPLATE.replace("__SLIDES__", slides_html)
with open(OUT, "w") as f:
    f.write(out)
print("wrote", OUT, "bytes:", os.path.getsize(OUT), "slides:", len(SLIDES))
