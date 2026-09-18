import os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from PIL import Image

REPO = "/Users/gbrianti/Projects/fcc-ee-cld-bnd-school/figures"
OUT = "/Users/gbrianti/Projects/fcc-ee-cld-bnd-school/presentation/final_deck.pptx"

NAVY = RGBColor(0x00, 0x33, 0x66)
RED = RGBColor(0xC8, 0x10, 0x2E)
DARKTXT = RGBColor(0x22, 0x22, 0x22)
GREY = RGBColor(0x71, 0x80, 0x96)
LGREY = RGBColor(0xB9, 0xC4, 0xD6)
LBG = RGBColor(0xF8, 0xF9, 0xFA)
LINE = RGBColor(0xE2, 0xE8, 0xF0)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)

SW, SH = Inches(13.333), Inches(7.5)
MARGIN = Inches(0.5)
CONTENT_W = SW - 2 * MARGIN
HEADER_H = Inches(0.72)
RED_BAR_H = Inches(0.045)
FOOTER_Y = Inches(7.05)

FIG = lambda rel: os.path.join(REPO, rel)

prs = Presentation()
prs.slide_width = SW
prs.slide_height = SH
BLANK = prs.slide_layouts[6]

# --------------------------------------------------------------------------- helpers

def add_rect(slide, x, y, w, h, color, line=False):
    sh = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h)
    sh.fill.solid()
    sh.fill.fore_color.rgb = color
    if line:
        sh.line.color.rgb = color
    else:
        sh.line.fill.background()
    sh.shadow.inherit = False
    return sh

def add_header(slide, title_runs, section_tag):
    add_rect(slide, 0, 0, SW, HEADER_H, NAVY)
    add_rect(slide, 0, HEADER_H, SW, RED_BAR_H, RED)
    tb = slide.shapes.add_textbox(MARGIN, Inches(0.10), CONTENT_W - Inches(2.2), Inches(0.55))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    set_runs(p, title_runs, base_size=20, base_color=WHITE, bold=True)
    if section_tag:
        tb2 = slide.shapes.add_textbox(SW - Inches(4.2) - MARGIN, Inches(0.10), Inches(4.2), Inches(0.55))
        tf2 = tb2.text_frame
        tf2.word_wrap = True
        tf2.vertical_anchor = MSO_ANCHOR.MIDDLE
        p2 = tf2.paragraphs[0]
        p2.alignment = PP_ALIGN.RIGHT
        r = p2.add_run()
        r.text = section_tag.upper()
        r.font.size = Pt(10)
        r.font.bold = True
        r.font.color.rgb = LGREY
        r.font.name = "Helvetica Neue"

def add_footer(slide, speaker, slide_no_text):
    ln = slide.shapes.add_connector(1, 0, FOOTER_Y, SW, FOOTER_Y)
    ln.line.color.rgb = LINE
    ln.line.width = Pt(0.75)
    tb = slide.shapes.add_textbox(MARGIN, FOOTER_Y + Inches(0.04), Inches(3.5), Inches(0.35))
    tf = tb.text_frame
    tf.word_wrap = False
    p = tf.paragraphs[0]
    r = p.add_run(); r.text = "FCC-ee CLD Collaboration"
    r.font.size = Pt(9); r.font.color.rgb = GREY; r.font.name = "Helvetica Neue"

    tb2 = slide.shapes.add_textbox(SW / 2 - Inches(2), FOOTER_Y + Inches(0.04), Inches(4), Inches(0.35))
    tf2 = tb2.text_frame
    tf2.word_wrap = False
    p2 = tf2.paragraphs[0]
    p2.alignment = PP_ALIGN.CENTER
    r2 = p2.add_run(); r2.text = speaker or ""
    r2.font.size = Pt(9); r2.font.bold = True; r2.font.color.rgb = RED; r2.font.name = "Helvetica Neue"

    tb3 = slide.shapes.add_textbox(SW - Inches(2) - MARGIN, FOOTER_Y + Inches(0.04), Inches(2), Inches(0.35))
    tf3 = tb3.text_frame
    tf3.word_wrap = False
    p3 = tf3.paragraphs[0]
    p3.alignment = PP_ALIGN.RIGHT
    r3 = p3.add_run(); r3.text = slide_no_text
    r3.font.size = Pt(9); r3.font.color.rgb = GREY; r3.font.name = "Helvetica Neue"

def set_runs(paragraph, runs, base_size=15, base_color=DARKTXT, bold=False):
    """runs: list of (text, style[, url]) where style in {'n','b','r','i','link'}"""
    for item in runs:
        text, style = item[0], item[1]
        url = item[2] if len(item) > 2 else None
        r = paragraph.add_run()
        r.text = text
        r.font.size = Pt(base_size)
        r.font.name = "Helvetica Neue"
        if style == "r":
            r.font.color.rgb = RED
            r.font.bold = True
        elif style == "b":
            r.font.color.rgb = NAVY
            r.font.bold = True
        elif style == "i":
            r.font.color.rgb = base_color
            r.font.italic = True
            r.font.bold = bold
        elif style == "link":
            r.font.color.rgb = RGBColor(0x1A, 0x5A, 0xA6)
            r.font.underline = True
        else:
            r.font.color.rgb = base_color
            r.font.bold = bold
        if url:
            r.hyperlink.address = url

def add_paragraphs(slide, x, y, w, h, paragraphs, bullets=False, size=15, anchor_top=True):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.TOP if anchor_top else MSO_ANCHOR.MIDDLE
    first = True
    for runs in paragraphs:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.space_after = Pt(8)
        p.line_spacing = 1.18
        if bullets:
            _set_bullet(p)
            p.level = 0
        set_runs(p, runs, base_size=size)
    return tb

def _set_bullet(paragraph):
    pPr = paragraph._pPr
    if pPr is None:
        pPr = paragraph._p.get_or_add_pPr()
    buChar = pPr.makeelement(qn('a:buChar'), {'char': '•'})
    buFont = pPr.makeelement(qn('a:buFont'), {'typeface': 'Arial'})
    pPr.append(buFont)
    pPr.append(buChar)
    pPr.set('indent', str(Emu(Inches(-0.22))))
    pPr.set('marL', str(Emu(Inches(0.22))))

def add_note(slide, text):
    slide.notes_slide.notes_text_frame.text = text

def estimate_text_height(paragraphs, width_in, size=15, bullets=False):
    """Rough but conservative line-wrap estimate so text boxes are sized to
    actually fit their content (python-pptx textboxes don't auto-fit; an
    undersized box lets text visually overflow past its shape)."""
    chars_per_in = 1.0 / 0.098  # ~10.2 chars/in at 15pt Helvetica, conservative
    usable_w = width_in - (0.22 if bullets else 0.0)
    chars_per_line = max(20, usable_w * chars_per_in)
    line_h = size * 1.18 / 72.0  # inches
    space_after = 8 / 72.0
    total = 0.0
    for runs in paragraphs:
        text = "".join(item[0] for item in runs)
        n_lines = max(1, -(-len(text) // int(chars_per_line)))  # ceil div
        total += n_lines * line_h + space_after
    return Inches(total)

def fit_images(imgs, box_x, box_y, box_w, box_h, gap=Inches(0.22)):
    """imgs: list of (path, caption). Returns list of placements."""
    n = len(imgs)
    sizes = []
    for path, cap in imgs:
        with Image.open(path) as im:
            iw, ih = im.size
        sizes.append((iw / ih))
    cap_h = Inches(0.25) if any(c for _, c in imgs) else 0
    avail_h = box_h - cap_h
    slot_w = (box_w - gap * (n - 1)) / n
    placements = []
    widths = []
    for ar in sizes:
        w = slot_w
        h = w / ar
        if h > avail_h:
            h = avail_h
            w = h * ar
        widths.append((w, h))
    total_w = sum(w for w, h in widths) + gap * (n - 1)
    start_x = box_x + (box_w - total_w) / 2
    cx = start_x
    for (path, cap), (w, h) in zip(imgs, widths):
        px = cx
        py = box_y + (avail_h - h) / 2
        placements.append((path, cap, px, py, w, h))
        cx += w + gap
    return placements

def add_images_row(slide, imgs, box_x, box_y, box_w, box_h):
    placements = fit_images(imgs, box_x, box_y, box_w, box_h)
    for path, cap, px, py, w, h in placements:
        slide.shapes.add_picture(path, px, py, width=w, height=h)
        if cap:
            tb = slide.shapes.add_textbox(px, py + h + Inches(0.02), w, Inches(0.22))
            tf = tb.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER
            r = p.add_run(); r.text = cap
            r.font.size = Pt(9); r.font.color.rgb = GREY; r.font.name = "Helvetica Neue"

def add_table(slide, x, y, w, rows, col_widths, header=True, header_span=None):
    nrows = len(rows)
    ncols = len(rows[0])
    row_h = Inches(0.42)
    gshape = slide.shapes.add_table(nrows, ncols, x, y, w, row_h * nrows)
    table = gshape.table
    for j, cw in enumerate(col_widths):
        table.columns[j].width = cw
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            cell = table.cell(i, j)
            cell.text = ""
            tf = cell.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            r = p.add_run(); r.text = val
            r.font.name = "Helvetica Neue"
            cell.margin_top = Inches(0.03)
            cell.margin_bottom = Inches(0.03)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            if header and i == 0:
                r.font.bold = True
                r.font.size = Pt(13)
                r.font.color.rgb = NAVY
                cell.fill.solid(); cell.fill.fore_color.rgb = WHITE
            else:
                r.font.size = Pt(13)
                r.font.color.rgb = DARKTXT
                cell.fill.solid(); cell.fill.fore_color.rgb = WHITE
    # strip default style borders look by using a plain table style
    tbl_el = table._tbl
    tblPr = tbl_el.find(qn('a:tblPr'))
    if tblPr is not None:
        tblPr.set('firstRow', '0')
        tblPr.set('bandRow', '0')
    return table, row_h * nrows

# --------------------------------------------------------------------------- content data

AUTHORS = ("Saurav Bania, Greta Brianti, Jurjan Bootsma, Vincenzo Del Piano, "
           "Kobe Degeetere, Andrea Maria, Sergei Solokhin")

def R(text, style="n"):
    return (text, style)

SLIDES = []  # populated below

# 0 ---------------------------------------------------------------- TITLE
def build_title():
    slide = prs.slides.add_slide(BLANK)
    add_rect(slide, 0, 0, SW, Inches(0.14), RED)
    tb = slide.shapes.add_textbox(Inches(1.0), Inches(2.5), SW - Inches(2.0), Inches(1.6))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = "Team Project: FCC-ee, the CLD detector"
    r.font.size = Pt(34); r.font.bold = True; r.font.color.rgb = NAVY; r.font.name = "Helvetica Neue"

    tb2 = slide.shapes.add_textbox(Inches(1.0), Inches(3.75), SW - Inches(2.0), Inches(0.6))
    tf2 = tb2.text_frame; tf2.word_wrap = True
    p2 = tf2.paragraphs[0]; p2.alignment = PP_ALIGN.CENTER
    r2 = p2.add_run(); r2.text = "FCC-ee with the CLD Detector"
    r2.font.size = Pt(18); r2.font.color.rgb = RGBColor(0x4A, 0x55, 0x68); r2.font.name = "Helvetica Neue"

    box = add_rect(slide, Inches(1.9), Inches(4.7), SW - Inches(3.8), Inches(1.15), LBG)
    box.line.color.rgb = RED; box.line.width = Pt(2.2)
    tf3 = box.text_frame; tf3.word_wrap = True; tf3.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf3.margin_left = Inches(0.25); tf3.margin_right = Inches(0.25)
    p3 = tf3.paragraphs[0]; p3.alignment = PP_ALIGN.CENTER
    r3 = p3.add_run(); r3.text = "FCC-ee CLD Collaboration"
    r3.font.size = Pt(14); r3.font.bold = True; r3.font.color.rgb = NAVY; r3.font.name = "Helvetica Neue"
    p4 = tf3.add_paragraph(); p4.alignment = PP_ALIGN.CENTER; p4.space_before = Pt(6)
    r4 = p4.add_run(); r4.text = AUTHORS
    r4.font.size = Pt(12); r4.font.color.rgb = NAVY; r4.font.name = "Helvetica Neue"
    add_note(slide, "Whole team: welcome the audience, introduce the two-task structure "
                     "(Task A = SM identification, Task B = BSM validation) and the speaker line-up.")
    return slide

# generic content slide builder
def build_content(speaker, section, title_runs, paragraphs, imgs=None, table_rows=None,
                   table_rows2=None, table_note=None, bullets=False, steps=None, notes=""):
    slide = prs.slides.add_slide(BLANK)
    add_header(slide, title_runs, section)
    add_footer(slide, speaker, "")
    y = Inches(0.98)
    if steps:
        tb = slide.shapes.add_textbox(MARGIN, y, CONTENT_W, Inches(0.3))
        tf = tb.text_frame; tf.word_wrap = True
        p = tf.paragraphs[0]
        for i, st in enumerate(steps):
            if i:
                r = p.add_run(); r.text = "   →   "
                r.font.size = Pt(11); r.font.color.rgb = RED; r.font.name = "Helvetica Neue"
            r = p.add_run(); r.text = st
            r.font.size = Pt(11); r.font.color.rgb = RGBColor(0x4A, 0x55, 0x68); r.font.name = "Helvetica Neue"
        y += Inches(0.32)
    width_in = CONTENT_W / 914400.0
    text_h = estimate_text_height(paragraphs, width_in, size=15, bullets=bullets)
    text_h = min(text_h, Inches(4.5))
    if not table_rows and not imgs:
        # no media below -- center the text block in the whole content area instead
        # of leaving it stranded at the top with empty space below (same fix as
        # the earlier HTML/PDF deck's sparse-slide issue).
        content_bottom = FOOTER_Y - Inches(0.15)
        y = y + (content_bottom - y - text_h) / 2
    add_paragraphs(slide, MARGIN, y, CONTENT_W, text_h, paragraphs, bullets=bullets, size=15)
    y2 = y + text_h + Inches(0.08)
    if table_rows:
        col_widths = table_rows[1]
        rows = table_rows[0]
        table, th = add_table(slide, MARGIN + Inches(0.3), y2, sum(col_widths, Emu(0)), rows, col_widths)
        y2 = y2 + th + Inches(0.18)
        if table_rows2:
            col_widths2 = table_rows2[1]
            rows2 = table_rows2[0]
            table2, th2 = add_table(slide, MARGIN + Inches(0.3), y2, sum(col_widths2, Emu(0)), rows2, col_widths2)
            y2 = y2 + th2
        if table_note:
            tb = slide.shapes.add_textbox(MARGIN + Inches(0.3), y2 + Inches(0.05), CONTENT_W, Inches(0.3))
            tf = tb.text_frame; tf.word_wrap = True
            p = tf.paragraphs[0]
            r = p.add_run(); r.text = table_note
            r.font.size = Pt(9.5); r.font.italic = False; r.font.color.rgb = GREY; r.font.name = "Helvetica Neue"
    elif imgs:
        box_h = FOOTER_Y - Inches(0.15) - y2
        add_images_row(slide, imgs, MARGIN, y2, CONTENT_W, box_h)
    if notes:
        add_note(slide, notes)
    return slide

def build_transition(speaker_next, msg, sub, notes=""):
    slide = prs.slides.add_slide(BLANK)
    bg = add_rect(slide, 0, 0, SW, SH, NAVY)
    tb = slide.shapes.add_textbox(Inches(1.0), Inches(3.0), SW - Inches(2.0), Inches(0.9))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = msg
    r.font.size = Pt(28); r.font.bold = True; r.font.color.rgb = WHITE; r.font.name = "Helvetica Neue"

    tb2 = slide.shapes.add_textbox(Inches(1.0), Inches(3.75), SW - Inches(2.0), Inches(0.5))
    tf2 = tb2.text_frame; tf2.word_wrap = True
    p2 = tf2.paragraphs[0]; p2.alignment = PP_ALIGN.CENTER
    r2 = p2.add_run(); r2.text = sub
    r2.font.size = Pt(15); r2.font.color.rgb = LGREY; r2.font.name = "Helvetica Neue"

    ln = slide.shapes.add_connector(1, Inches(5.6), Inches(4.35), Inches(7.7), Inches(4.35))
    ln.line.color.rgb = RED; ln.line.width = Pt(1.5)

    tb3 = slide.shapes.add_textbox(Inches(1.0), Inches(4.42), SW - Inches(2.0), Inches(0.4))
    tf3 = tb3.text_frame; tf3.word_wrap = True
    p3 = tf3.paragraphs[0]; p3.alignment = PP_ALIGN.CENTER
    r3 = p3.add_run(); r3.text = "Next: "
    r3.font.size = Pt(13); r3.font.color.rgb = WHITE; r3.font.name = "Helvetica Neue"
    r4 = p3.add_run(); r4.text = speaker_next
    r4.font.size = Pt(13); r4.font.bold = True; r4.font.color.rgb = WHITE; r4.font.name = "Helvetica Neue"
    if notes:
        add_note(slide, notes)
    return slide

print("helpers ready")

# --------------------------------------------------------------------------- build deck

slide_registry = []  # (slide_obj, speaker) in order, for footer numbering at the end

def reg(slide, speaker):
    slide_registry.append((slide, speaker))
    return slide

s = build_title()
slide_registry.append((s, None))

# 1 -- Vincenzo: FCC-ee and the CLD detector
s = build_content("Vincenzo Del Piano", "Introduction",
    [R("FCC-ee and the CLD detector")],
    [
        [R("FCC-ee: a 100 km e"), R("+", "n"), R("e"), R("−", "n"),
         R(" collider. Four energies: "), R("91", "r"), R(" (Z pole), "), R("160", "r"),
         R(" (WW), "), R("240", "r"), R(" (ZH), "), R("365 GeV", "r"), R(" (t̅t)."), ],
        [R("CLD gives us tracking, calorimetry and a 2 T field — enough to reconstruct "
           "jets, leptons and missing energy.")],
        [R("Each energy hands us several "), R("anonymised", "b"),
         R(" samples. We don't know what they are yet.")],
        [R("Code and analysis pipeline: "),
         ("github.com/gretabrianti/fcc-ee-cld-bnd-school", "link",
          "https://github.com/gretabrianti/fcc-ee-cld-bnd-school")],
    ],
    imgs=[(FIG("cld_detector.png"), "CLD detector — original FCC-ee CLD collaboration deck")],
    bullets=True,
    notes=("State FCC-ee basics: 100 km ring, four run energies.\n"
           "Emphasize what CLD gives us: tracking, calorimetry, 2T field.\n"
           "Set up the framing for the whole talk: every sample is anonymised -- "
           "the audience (and we) don't know what they are yet.\n"
           "Point out the GitHub repo link for anyone who wants to follow along with the code."))
reg(s, "Vincenzo Del Piano")

# 2 -- Vincenzo: Method & Task Split (UPDATED per user request)
def build_method_slide():
    slide = prs.slides.add_slide(BLANK)
    add_header(slide, [R("Method & Task Split")], "Introduction")
    add_footer(slide, "Vincenzo Del Piano", "")
    # whole content block (statement + steps + note) is ~2.8in tall; center it in
    # the content area instead of leaving it stranded under the header.
    block_h = Inches(2.8)
    content_bottom = FOOTER_Y - Inches(0.15)
    y = Inches(0.98) + (content_bottom - Inches(0.98) - block_h) / 2
    add_paragraphs(slide, MARGIN, y, CONTENT_W, Inches(0.85),
        [[R("Agreed with the IDEA collaboration: "), R("Task A", "b"),
          R(" — the CLD detector studies center-of-mass energies of "),
          R("160 GeV", "r"), R(" and "), R("365 GeV", "r"), R(". "), R("Task B", "b"),
          R(" — both collaborations present the found excesses.")]], size=15)
    y2 = y + Inches(0.95)
    box_w = Inches(1.9); gap = Inches(0.35)
    total_w = 4 * box_w + 3 * gap
    x0 = MARGIN + (CONTENT_W - total_w) / 2
    labels = ["Define the SM", "Find an excess", "Interpret it", "Validate it"]
    for i, lab in enumerate(labels):
        bx = x0 + i * (box_w + gap)
        box = add_rect(slide, bx, y2, box_w, Inches(1.0), LBG)
        red = add_rect(slide, bx, y2, box_w, Inches(0.05), RED)
        tf = box.text_frame; tf.word_wrap = True; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
        r = p.add_run(); r.text = str(i + 1)
        r.font.size = Pt(22); r.font.bold = True; r.font.color.rgb = NAVY; r.font.name = "Helvetica Neue"
        p2 = tf.add_paragraph(); p2.alignment = PP_ALIGN.CENTER
        r2 = p2.add_run(); r2.text = lab
        r2.font.size = Pt(12); r2.font.bold = True; r2.font.color.rgb = NAVY; r2.font.name = "Helvetica Neue"
        if i < 3:
            ln = slide.shapes.add_textbox(bx + box_w, y2 + Inches(0.32), gap, Inches(0.4))
            tfa = ln.text_frame
            pa = tfa.paragraphs[0]; pa.alignment = PP_ALIGN.CENTER
            ra = pa.add_run(); ra.text = "→"
            ra.font.size = Pt(18); ra.font.color.rgb = RED; ra.font.name = "Helvetica Neue"
    y3 = y2 + Inches(1.15)
    add_paragraphs(slide, MARGIN, y3, CONTENT_W, Inches(0.7),
        [[R("At "), R("91", "r"), R(" and "), R("365 GeV", "r"),
          R(" we found an excess — all four steps apply. At "), R("160", "r"), R(" and "),
          R("240 GeV", "r"), R(", no excess was found. We stop after step 1.")]], size=14)
    add_note(slide, ("Explain the IDEA-collaboration agreement up front: Task A is the CLD "
                      "detector's own analysis at 160 and 365 GeV; Task B is both collaborations "
                      "independently presenting whatever excesses they found.\n"
                      "Walk through the four-step method.\n"
                      "Flag immediately: at 160/240 GeV we stop after step 1 -- no excess there, "
                      "so don't over-promise for that part of the talk."))
    return slide
s = build_method_slide()
reg(s, "Vincenzo Del Piano")

# 3 -- transition to Kobe
s = build_transition("Kobe Degeetere", "SM process identification at 160 GeV",
    "Reconstructing the known processes before studying the excess",
    notes="Quick hand-off: Kobe covers the 160 GeV SM identification (Task A, step 1 only).")
reg(s, None)

# 4 -- Kobe: Task A: identifying the samples
s = build_content("Kobe Degeetere", "SM · 160 GeV · step 1 only",
    [R("Task A: identifying the samples")],
    [[R("Task A: match each anonymous sample to a known process, using cuts on jets, leptons, "
        "b-tagging and MET. Two of four samples are identified this way. No excess is searched "
        "for at this energy — step 1 of the method is all we need here.")]],
    table_rows=([
        ["Process", "Key cuts", "Efficiency"],
        ["Higgs (ννH, H→bb̅)", "2 jets b-tag>0.7, 0 leptons, MET cut", "32.7%*"],
        ["WW (semileptonic)", "2 jets, 1 lepton, MET pT>5 GeV", "43.2%*"],
    ], [Inches(3.2), Inches(6.0), Inches(2.0)]),
    table_note="* assumed (toy), not measured — the talk gives cuts, not absolute yields.",
    notes=("Explain the cut-based matching: jets, leptons, b-tagging, MET.\n"
           "Stress the efficiencies are toy assumptions (*), not measured.\n"
           "Reiterate: no excess search happens at 160 GeV."))
reg(s, "Kobe Degeetere")

# 5 -- Kobe: Higgs and WW mass peaks
s = build_content("Kobe Degeetere", "SM · 160 GeV",
    [R("Higgs and WW mass peaks")],
    [[R("Higgs: the dijet mass peaks at "), R("~125 GeV", "r"), R(". WW: the effective mass "
       "recovers close to "), R("√s = 160 GeV", "r"), R(", as expected for a semileptonic "
       "decay. Both agree with the reported points at the peak.")]],
    imgs=[(FIG("sm/08_mass_higgs_160GeV.png"), ""), (FIG("sm/09_mass_ww_160GeV.png"), "")],
    notes=("Walk through both mass plots side by side.\n"
           "Point out where each peak lands vs. expectation (125 GeV Higgs, sqrt(s)=160 GeV WW).\n"
           "Note both agree with the reported points -- nothing unusual here yet."))
reg(s, "Kobe Degeetere")

# 6 -- transition to Saurav
s = build_transition("Saurav Bania", "SM process identification at 365 GeV",
    "Five anonymous samples, five SM assignments",
    notes="Hand off to Saurav for the 365 GeV SM identification (all five samples).")
reg(s, None)

# 7 -- Saurav: All five samples identified
s = build_content("Saurav Bania", "SM · 365 GeV · step 1 only",
    [R("All five samples identified")],
    [[R("365 GeV is the most complete working point: all five samples get an assignment — "
        "t̅t, e⁺e⁻→ff̅, ZZ, ZH, WW. More jets are available here than at "
        "160 GeV, so b-tagging separates these final states well.")]],
    table_rows=([
        ["Process", "Efficiency"],
        ["t̅t", "10.7%*"],
        ["e⁺e⁻ → ff̅", "10.2%*"],
        ["ZZ → ℓℓqq̅ (X5)", "8.7%*"],
        ["ZH", "5.4%*"],
        ["WW", "52.0%*"],
    ], [Inches(6.0), Inches(3.2)]),
    table_note="* assumed (toy), not measured.",
    notes=("365 GeV is the richest working point -- all five processes get assigned.\n"
           "Briefly mention more jets + b-tagging separates the final states well.\n"
           "Keep it quick, this sets up the two 365 GeV highlight plots next."))
reg(s, "Saurav Bania")

# 8 -- Saurav: Strongest evidence: ttbar and ZZ
s = build_content("Saurav Bania", "SM · 365 GeV",
    [R("Strongest evidence: t̅t and ZZ")],
    [[R("t̅t: reconstructed mass sits at the top scale, "), R("χ²/ndof = 0.81", "r"),
       R(" — the best agreement in this study. ZZ: dijet mass peaks cleanly at "),
       R("mZ = 91 GeV", "r"), R(".")]],
    imgs=[(FIG("feyn_ttbar.png"), "t̅t production"),
          (FIG("sm/10_mass_ttbar_365GeV.png"), ""),
          (FIG("sm/11_mass_zz_365GeV.png"), "")],
    notes=("Point at the ttbar Feynman diagram briefly to orient the audience.\n"
           "Highlight this is the best chi2/ndof in the whole study (0.81).\n"
           "ZZ peaks cleanly at mZ -- another clean SM identification."))
reg(s, "Saurav Bania")

# 9 -- transition to Andrea (BSM 91 GeV)
s = build_transition("Andrea Maria", "From SM identification to the excess",
    "Once the samples are identified, can the SM explain the observed structure?",
    notes="Hand off to Andrea -- pivot from SM identification into the excess/BSM section.")
reg(s, None)

# 10 -- Andrea: bridge slide
s = build_content("Andrea Maria", "Evidence · both energies",
    [R("The SM alone doesn't explain it")],
    [[R("Sum every identified SM process and compare to the reported points. At both "),
       R("91", "r"), R(" and "), R("365 GeV", "r"), R(" the excess sits far above that sum. "
       "This is why an interpretation is needed — step 2 becomes step 3.")]],
    imgs=[(FIG("sm/16_completeness_91GeV.png"), "91 GeV"),
          (FIG("sm/17_completeness_365GeV.png"), "365 GeV")],
    notes=("This is the pivot slide of the whole talk.\n"
           "Show clearly: summed SM does not cover the excess at either energy.\n"
           "Say explicitly: this is why we move from evidence to interpretation "
           "(method step 2 to step 3)."))
reg(s, "Andrea Maria")

# 11 -- Andrea: An excess, not an SM sample
s = build_content("Andrea Maria", "BSM · 91 GeV",
    [R("An excess, not an SM sample")],
    [[R("Tight selection: MET pT>3 GeV, ≥1 lepton, small impact parameter. A lepton+jet "
       "excess appears. Proposed: a "), R("Heavy Neutral Lepton", "r"), R(", mass "),
       R("≈40 GeV", "r"), R(". The resonance hypothesis fits better than a flat "
       "background: "), R("χ²/ndof 4.47 vs. 5.81", "r"), R(".")]],
    imgs=[(FIG("feyn_hnl_91.png"), "HNL at a Z-factory"),
          (FIG("bsm/01_hnl_91GeV_hypothesis_test.png"), "")],
    steps=["Excess", "Reconstruction", "H1: flat bkg", "H0: HNL, m≈40", "Test"],
    notes=("Describe the tight selection that isolates the excess.\n"
           "Introduce the HNL hypothesis, mass ~40 GeV.\n"
           "Resonance fit beats flat background (4.47 vs 5.81) -- but this alone doesn't "
           "prove HNL, just that a bump fits better than no bump."))
reg(s, "Andrea Maria")

# 12 -- Andrea: independent cross-check
s = build_content("Andrea Maria", "BSM · 91 GeV",
    [R("An independent cross-check")],
    [[R("A second, independent variable — missing energy itself — agrees with the same "
       "hypothesis: "), R("χ²/ndof = 1.14", "r"), R(". This isn't the same test twice.")]],
    imgs=[(FIG("bsm/03_HNL_metpt_91GeV.png"), "")],
    notes=("Stress independence: MET is a different observable, not a re-test of the same "
           "variable.\n"
           "chi2/ndof = 1.14 is a strong agreement -- use this to build confidence before "
           "the significance slide."))
reg(s, "Andrea Maria")

# 13 -- Andrea: Significance (TRIMMED to 7 sigma only)
s = build_content("Andrea Maria", "BSM · 91 GeV",
    [R("Significance of the excess")],
    [[R("The source quotes "), R("7σ", "r"), R(" as the headline significance for the "
       "91 GeV excess. Our recomputation, shown below, converges toward the same value. "
       "No look-elsewhere correction is applied — we don't have a real trials count.")]],
    imgs=[(FIG("bsm/04_significance_hierarchy_91GeV.png"), "")],
    notes=("State only the 7 sigma headline number -- don't cite the other tiers from the "
           "source, we're not confident they're the same definition.\n"
           "Caveat clearly: no look-elsewhere correction. Don't over-claim discovery."))
reg(s, "Andrea Maria")

# 14 -- transition to Jurjan
s = build_transition("Jurjan Bootsma", "The excess at 365 GeV",
    "Testing reconstruction and background hypotheses",
    notes="Hand off to Jurjan for the 365 GeV excess and pairing/reconstruction study.")
reg(s, None)

# 15 -- Jurjan: original method
s = build_content("Jurjan Bootsma", "BSM · 365 GeV",
    [R("The excess, and the original method")],
    [[R("Tighter selection again: low MET, "), R("≥2 jets, ≥2 leptons", "r"),
       R(", Z-veto, b-veto. Original method: hadronic-W channel, one jet assumed, a fixed "
       "pairing m(j₂,j₃). The source itself flags this: "),
       R("“sub-optimal pairing might lead to large spread.”", "i")]],
    imgs=[(FIG("feyn_hnl_365.png"), "Production and decay, slide 18")],
    notes=("Describe the tighter 365 GeV selection.\n"
           "Explain the original method's fixed jet pairing and its acknowledged weakness "
           "(quote the source's own caveat)."))
reg(s, "Jurjan Bootsma")

# 16 -- Jurjan: testing the pairing
s = build_content("Jurjan Bootsma", "BSM · 365 GeV",
    [R("[CURRENT ANALYSIS] ", "r"), R("Testing the pairing")],
    [[R("Four jets give three candidate pairings. The fixed original pairing is correct only "),
       R("33%", "r"), R(" of the time by construction. Picking the pairing closest to mW "
       "instead gets it right "), R("88%", "r"), R(" of the time, and both peaks narrow "
       "sharply. This is evidence the original pairing can mis-associate jets — it "
       "supports better reconstruction, not an HNL by itself.")]],
    imgs=[(FIG("bsm/05_W_mass_365GeV.png"), "Naive = original · Constrained = current analysis"),
          (FIG("bsm/06_HNL_mass_365GeV.png"), "")],
    notes=("Explain why the original pairing is only right 1/3 of the time, by construction.\n"
           "Constrained (closest to mW) pairing: 88%, peaks narrow sharply.\n"
           "Be careful with the conclusion: this supports better reconstruction, it is not by "
           "itself evidence for an HNL."))
reg(s, "Jurjan Bootsma")

# 17 -- Jurjan: resonance vs SM-tail
s = build_content("Jurjan Bootsma", "BSM · 365 GeV",
    [R("Resonance vs. SM-tail, and significance")],
    [[R("Resonance vs. a mis-measured ZZ/WW tail: "), R("χ²/ndof 4.12 vs. 215.55", "r"),
       R(" — this specific SM-tail model is disfavoured. Quoted significance: "),
       R("6.46σ", "r"), R(". The background behind that number isn't established in the "
       "source.")]],
    imgs=[(FIG("bsm/07_hnl_365GeV_alternative_test.png"), ""),
          (FIG("bsm/08_significance_hierarchy_365GeV.png"), "")],
    notes=("Chi2 comparison strongly disfavors the SM-tail alternative (4.12 vs 215.55).\n"
           "Cite 6.46 sigma but flag clearly: the background behind that number is not "
           "established in the source -- treat it as quoted, not verified."))
reg(s, "Jurjan Bootsma")

# 18 -- transition (REASSIGNED Greta -> Jurjan)
s = build_transition("Jurjan Bootsma", "What has been established -- and what remains open?",
    "Consistency, caveats, and conclusions",
    notes="Jurjan bridges into the closing section: consistency recap, then open questions.")
reg(s, None)

# 19 -- Open questions (REASSIGNED Greta -> Jurjan)
s = build_content("Jurjan Bootsma", "Consistency",
    [R("Open questions")],
    [
        [R("40 GeV vs. 150 GeV", "r"), R(": two HNL masses. One particle has one mass. "
           "This is open, not explained away.")],
        [R("365 GeV background normalisation: not established.")],
        [R("No look-elsewhere trial count is available, so none is applied.")],
        [R("Every cut efficiency shown is a toy assumption.")],
        [R("Rejecting one background model is not proof of an HNL.")],
    ],
    bullets=True,
    notes=("Walk through each open question in turn:\n"
           "- 40 vs 150 GeV mass tension -- flag it, don't explain it away.\n"
           "- 365 GeV background normalisation not established.\n"
           "- No real trials count, so no look-elsewhere correction applied.\n"
           "- All cut efficiencies are toy assumptions.\n"
           "Land on: rejecting one background model is not proof of an HNL."))
reg(s, "Jurjan Bootsma")

# 20 -- chi2 per SM process (REASSIGNED Greta -> Andrea)
s = build_content("Andrea Maria", "Conclusions",
    [R("χ² per SM process")],
    [[R("All five 365 GeV processes and both 160 GeV processes now have a toy-vs-pseudo-data "
        "comparison — every value traceable to this repo's code.")]],
    table_rows=([
        ["Process (365 GeV)", "χ²/ndof"],
        ["t̅t", "0.81"],
        ["ZZ → ℓℓqq̅", "8.40"],
        ["e⁺e⁻ → ff̅", "5.17†"],
        ["ZH", "3.89†"],
        ["WW", "26.22†"],
    ], [Inches(6.0), Inches(3.2)]),
    table_rows2=([
        ["Process (160 GeV)", "χ²/ndof"],
        ["Higgs", "37.77"],
        ["WW", "1.84"],
    ], [Inches(6.0), Inches(3.2)]),
    table_note="† second-pass digitisation, lower precision than the other rows (see PROVENANCE_AUDIT.md).",
    notes=("Point to the full table -- every SM process now has a chi2 comparison.\n"
           "Flag the dagger-marked rows explicitly as lower-precision, second-pass "
           "digitisation -- don't present them with the same confidence as the rest."))
reg(s, "Andrea Maria")

# 21 -- flat vs resonant (REASSIGNED Greta -> Andrea, significance row TRIMMED to 7 sigma)
s = build_content("Andrea Maria", "Conclusions",
    [R("Flat vs. resonant hypothesis")],
    [[R("At both energies the resonance hypothesis fits better than the flat/SM-tail "
        "alternative tested. That supports the interpretation. It doesn't prove it.")]],
    table_rows=([
        ["", "91 GeV", "365 GeV"],
        ["Resonance (H0) χ²/ndof", "4.47", "4.12"],
        ["Flat / SM-tail (H1) χ²/ndof", "5.81", "215.55"],
        ["Reconstructed mass", "≈40 GeV", "≈150 GeV"],
        ["Quoted significance", "7σ", "6.46σ"],
        ["Jet mis-association (365 only)", "—", "33% → 88%"],
    ], [Inches(4.2), Inches(2.5), Inches(2.5)]),
    notes=("Recap the table: resonance wins at both energies.\n"
           "Significance: 7 sigma at 91 GeV, 6.46 sigma at 365 GeV -- quoted numbers only.\n"
           "Reiterate the caveat: this supports the interpretation, it does not prove it."))
reg(s, "Andrea Maria")

# 22 -- Where this leaves us (REASSIGNED Greta -> Jurjan)
s = build_content("Jurjan Bootsma", "Conclusions",
    [R("Where this leaves us")],
    [[R("Five SM processes at 365 GeV, two at 160 GeV, each traceable. Two excesses, both "),
       R("consistent with", "r"), R(" a resonance hypothesis, both with open caveats. FCC-ee's "
       "precision lets small, careful excesses be taken seriously — if every claim stays "
       "traceable. So: "), R("what do you think is really in there?", "r")]],
    notes=("Closing summary: seven SM processes traced, two excesses found, both open.\n"
           "End on the open question to the audience: \"what do you think is really in "
           "there?\" -- invite discussion."))
reg(s, "Jurjan Bootsma")

# renumber footers now that the deck is final (poll slide already excluded)
n_total = len(slide_registry)
for i, (slide, speaker) in enumerate(slide_registry):
    if speaker is None:
        continue
    for shp in slide.shapes:
        if shp.has_text_frame:
            for p in shp.text_frame.paragraphs:
                for r in p.runs:
                    pass
# set slide-number text directly by finding the 3rd footer textbox we added (right-aligned)
# simplest: redo footer numbering by locating textboxes at FOOTER_Y with grey right-aligned text
from pptx.util import Emu as _Emu
for i, (slide, speaker) in enumerate(slide_registry):
    if speaker is None:
        continue
    for shp in slide.shapes:
        if not shp.has_text_frame:
            continue
        if abs(shp.top - (FOOTER_Y + Inches(0.04))) < Emu(Inches(0.02)) and shp.left > SW - Inches(2.5) - MARGIN - Inches(0.1):
            shp.text_frame.paragraphs[0].runs[0].text = f"Slide {i + 1}"

prs.save(OUT)
print("wrote", OUT, "slides:", len(prs.slides.__iter__.__self__._sldIdLst))
