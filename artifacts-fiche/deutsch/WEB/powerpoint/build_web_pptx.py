#!/usr/bin/env python3
"""WEB Flash-Theorie deck — same visual language as PM / artifacts fiches."""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from lxml import etree

PAPER = RGBColor(0xFF, 0xFD, 0xFA)
INK = RGBColor(0x2B, 0x2B, 0x3A)
ACCENT = RGBColor(0xE8, 0x63, 0x9A)
ACCENT_SOFT = RGBColor(0xFB, 0xD3, 0xE4)
HIGHLIGHT = RGBColor(0xFF, 0xF1, 0x76)
C1 = RGBColor(0x7B, 0xC4, 0x7F)
C2 = RGBColor(0x6F, 0xA8, 0xE8)
C3 = RGBColor(0xF2, 0xA6, 0x5A)
C4 = RGBColor(0xB5, 0x8B, 0xE0)
C5 = RGBColor(0x4C, 0xC0, 0xB5)
C6 = RGBColor(0xF2, 0x8A, 0xA5)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)

F1 = RGBColor(0xF2, 0xF9, 0xF2)
F2 = RGBColor(0xF0, 0xF6, 0xFC)
F3 = RGBColor(0xFD, 0xF6, 0xEE)
F4 = RGBColor(0xF7, 0xF2, 0xFB)
F5 = RGBColor(0xED, 0xF9, 0xF7)
F6 = RGBColor(0xFD, 0xF2, 0xF5)
W1 = RGBColor(0xB8, 0xE0, 0xBA)
W2 = RGBColor(0xB0, 0xD0, 0xF2)
W3 = RGBColor(0xF8, 0xD0, 0xA4)
W4 = RGBColor(0xD6, 0xC0, 0xEE)
W5 = RGBColor(0x9C, 0xDC, 0xD6)
W6 = RGBColor(0xF8, 0xC0, 0xCE)

FONT_TITLE = "Fredoka"
FONT_BODY = "Patrick Hand"
FONT_HAND = "Caveat"

OUT = "/Users/lisa/artifacts/artifacts-fiche/deutsch/WEB/powerpoint/web-seance-flash-theorie.pptx"
LOGO = "/Users/lisa/artifacts/logo.png"
GRID_BG = "/Users/lisa/artifacts/artifacts-fiche/deutsch/WEB/powerpoint/grid-bg.png"
FOOTER = "Kremstaler Digitalhilfe – Lisa Scelli / WEB 13.11.2026"
MUTED = RGBColor(0x8A, 0x84, 0x90)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]
SW, SH = prs.slide_width, prs.slide_height


def set_run(run, size=22, bold=False, color=INK, font=FONT_BODY):
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    run.font.name = font
    rPr = run._r.get_or_add_rPr()
    for tag in ("latin", "ea", "cs"):
        el = rPr.find(qn(f"a:{tag}"))
        if el is None:
            el = etree.SubElement(rPr, qn(f"a:{tag}"))
        el.set("typeface", font)


def add_run(p, text, size=22, bold=False, color=INK, font=FONT_BODY, highlight=False):
    run = p.add_run()
    run.text = text
    set_run(run, size=size, bold=bold, color=color, font=font)
    if highlight:
        rPr = run._r.get_or_add_rPr()
        hl = etree.SubElement(rPr, qn("a:highlight"))
        srgb = etree.SubElement(hl, qn("a:srgbClr"))
        srgb.set("val", "FFF176")
    return run


def send_to_back(slide, shape):
    spTree = slide.shapes._spTree
    el = shape._element
    spTree.remove(el)
    spTree.insert(2, el)


def add_bg(slide):
    pic = slide.shapes.add_picture(GRID_BG, 0, 0, SW, SH)
    send_to_back(slide, pic)


def rounded(slide, l, t, w, h, fill, border=None, border_pt=2.25, adj=0.12):
    sh = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(l), Inches(t), Inches(w), Inches(h)
    )
    sh.fill.solid()
    sh.fill.fore_color.rgb = fill
    if border:
        sh.line.color.rgb = border
        sh.line.width = Pt(border_pt)
    else:
        sh.line.fill.background()
    try:
        sh.adjustments[0] = adj
    except Exception:
        pass
    return sh


def textbox(slide, l, t, w, h):
    box = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    return box, tf


def p_clear(tf):
    p = tf.paragraphs[0]
    p.clear()
    return p


def title_block(slide, title, tag):
    box, tf = textbox(slide, 0.9, 0.28, 11.5, 0.72)
    p = p_clear(tf)
    p.alignment = PP_ALIGN.CENTER
    add_run(p, title, size=36, bold=True, font=FONT_TITLE)
    rounded(slide, 4.6, 1.02, 4.1, 0.07, ACCENT, adj=0.5)
    rounded(slide, 4.55, 1.22, 4.2, 0.40, ACCENT_SOFT, ACCENT, border_pt=1.75, adj=0.2)
    box, tf = textbox(slide, 4.55, 1.24, 4.2, 0.38)
    p = p_clear(tf)
    p.alignment = PP_ALIGN.CENTER
    add_run(p, tag, size=15, bold=True, font=FONT_TITLE)


def washi(slide, l, t, w, h, fill, rot=4):
    tape = rounded(slide, l, t, w, h, fill, adj=0.05)
    tape.rotation = rot
    return tape


def num_badge(slide, l, t, color, n, size=0.34):
    c = slide.shapes.add_shape(
        MSO_SHAPE.OVAL, Inches(l), Inches(t), Inches(size), Inches(size)
    )
    c.fill.solid()
    c.fill.fore_color.rgb = color
    c.line.fill.background()
    box, tf = textbox(slide, l, t + 0.02, size, size)
    p = p_clear(tf)
    p.alignment = PP_ALIGN.CENTER
    add_run(p, str(n), size=14, bold=True, color=WHITE, font=FONT_TITLE)


def card(slide, l, t, w, h, fill, border, washi_c, title, bullets,
         body_size=20, num=None, title_size=18):
    rounded(slide, l, t, w, h, fill, border, border_pt=2.4, adj=0.1)
    washi(slide, l + w - 1.05, t - 0.11, 0.78, 0.20, washi_c, rot=5)

    title_x = l + 0.28
    if num is not None:
        num_badge(slide, l + 0.22, t + 0.22, border, num)
        title_x = l + 0.62

    box, tf = textbox(slide, title_x, t + 0.18, w - (title_x - l) - 0.25, 0.42)
    p = p_clear(tf)
    add_run(p, title.upper(), size=title_size, bold=True, font=FONT_TITLE)

    box, tf = textbox(slide, l + 0.28, t + 0.68, w - 0.55, h - 0.9)
    first = True
    for b in bullets:
        p = p_clear(tf) if first else tf.add_paragraph()
        first = False
        p.space_after = Pt(6)
        if b == "":
            add_run(p, " ", size=body_size, font=FONT_BODY)
            continue
        if isinstance(b, tuple):
            add_run(p, "✓  ", size=body_size, bold=True, color=border, font=FONT_BODY)
            for text, hl in b:
                add_run(p, text, size=body_size, color=INK, font=FONT_BODY, highlight=hl)
        else:
            add_run(p, "✓  ", size=body_size, bold=True, color=border, font=FONT_BODY)
            add_run(p, b, size=body_size, color=INK, font=FONT_BODY)


def star(slide, l, t, s, fill=HIGHLIGHT):
    sh = slide.shapes.add_shape(
        MSO_SHAPE.STAR_5_POINT, Inches(l), Inches(t), Inches(s), Inches(s)
    )
    sh.fill.solid()
    sh.fill.fore_color.rgb = fill
    sh.line.color.rgb = INK
    sh.line.width = Pt(1.25)
    return sh


def heart(slide, l, t, s, fill=ACCENT):
    sh = slide.shapes.add_shape(
        MSO_SHAPE.HEART, Inches(l), Inches(t), Inches(s), Inches(s)
    )
    sh.fill.solid()
    sh.fill.fore_color.rgb = fill
    sh.line.color.rgb = INK
    sh.line.width = Pt(1.25)
    return sh


def cloud(slide, l, t, w, h, text, size=22):
    rounded(slide, l, t, w, h, WHITE, ACCENT, border_pt=2.0, adj=0.5)
    box, tf = textbox(slide, l + 0.15, t + 0.12, w - 0.3, h - 0.2)
    p = p_clear(tf)
    p.alignment = PP_ALIGN.CENTER
    add_run(p, text, size=size, font=FONT_HAND)


def add_footer(slide):
    logo_size = 0.28
    logo_l = 0.45
    logo_t = 7.08
    slide.shapes.add_picture(LOGO, Inches(logo_l), Inches(logo_t), Inches(logo_size), Inches(logo_size))
    box, tf = textbox(slide, logo_l + logo_size + 0.12, 7.10, 11.5, 0.28)
    p = p_clear(tf)
    p.alignment = PP_ALIGN.LEFT
    add_run(p, FOOTER, size=11, color=MUTED, font=FONT_BODY)


# ───────────────── SLIDES ─────────────────

# 1 Title
s = prs.slides.add_slide(BLANK)
add_bg(s)
star(s, 1.1, 1.1, 0.45)
star(s, 11.7, 1.3, 0.35, ACCENT_SOFT)
heart(s, 11.9, 5.9, 0.38)
star(s, 0.9, 5.8, 0.32, C5)
rounded(s, 1.8, 1.7, 9.7, 4.0, WHITE, ACCENT, border_pt=2.8, adj=0.1)
washi(s, 9.9, 1.55, 1.1, 0.24, W6, rot=6)
box, tf = textbox(s, 1.8, 2.15, 9.7, 0.9)
p = p_clear(tf)
p.alignment = PP_ALIGN.CENTER
add_run(p, "Web Development", size=44, bold=True, font=FONT_TITLE)
rounded(s, 5.0, 3.1, 3.3, 0.09, ACCENT, adj=0.5)
box, tf = textbox(s, 1.8, 3.4, 9.7, 0.5)
p = p_clear(tf)
p.alignment = PP_ALIGN.CENTER
add_run(p, "Flash Theorie  ·  Übungen  ·  Self-learning", size=24, font=FONT_BODY)
rounded(s, 5.15, 4.15, 3.0, 0.42, ACCENT_SOFT, ACCENT, border_pt=1.75, adj=0.2)
box, tf = textbox(s, 5.15, 4.18, 3.0, 0.4)
p = p_clear(tf)
p.alignment = PP_ALIGN.CENTER
add_run(p, "3 UE · 2 Sitzungen", size=16, bold=True, font=FONT_TITLE)
cloud(s, 3.6, 5.1, 6.1, 0.55, "Details stehen in euren Artifacts", size=20)

# 2 Agenda
s = prs.slides.add_slide(BLANK)
add_bg(s)
title_block(s, "Agenda heute", "2 × 75 Min  ·  mit Pause")
card(s, 0.7, 2.0, 5.7, 4.4, F2, C2, W2, "Sitzung 1 · 75 Min", [
    "Flash Theorie Web-Grundlagen  (30)",
    "Übung 3 · DevTools  (15)",
    "Übung 1 · Visitenkarte  (20)",
    (("→ Pause  (10)", True),),
], body_size=18, num=1)
card(s, 6.9, 2.0, 5.7, 4.4, F4, C4, W4, "Sitzung 2 · 75 Min", [
    "Flash Theorie JS & DOM  (15)",
    "Tools & Workflow  (15)",
    "Übung 2 · Begrüßung  (25)",
    "Bilan & Self-learning  (20)",
], body_size=18, num=2)

# 3 Sitzung 1
s = prs.slides.add_slide(BLANK)
add_bg(s)
star(s, 1.2, 1.5, 0.4)
star(s, 11.6, 5.5, 0.35, C3)
rounded(s, 2.4, 2.0, 8.5, 3.5, ACCENT_SOFT, ACCENT, border_pt=2.8, adj=0.1)
washi(s, 9.4, 1.85, 1.0, 0.22, W6, rot=5)
box, tf = textbox(s, 2.4, 2.5, 8.5, 0.9)
p = p_clear(tf)
p.alignment = PP_ALIGN.CENTER
add_run(p, "Sitzung 1", size=48, bold=True, font=FONT_TITLE)
box, tf = textbox(s, 2.4, 3.5, 8.5, 0.5)
p = p_clear(tf)
p.alignment = PP_ALIGN.CENTER
add_run(p, "Web-Grundlagen · HTML/CSS · DevTools", size=24, font=FONT_BODY)
cloud(s, 3.5, 4.4, 6.3, 0.55, "75 Minuten  ·  danach Pause", size=20)

# 4 Flash overview
s = prs.slides.add_slide(BLANK)
add_bg(s)
title_block(s, "Flash Theorie · Web-Grundlagen", "30 Minuten · Überblick")
card(s, 1.4, 2.05, 10.5, 4.5, WHITE, C5, W5, "Heute in 5 Blöcken", [
    "Webentwicklung · Körper-Analogie",
    "Client / Server · DNS · HTTP",
    "Design & UX",
    "Frameworks (React · Vue · Angular)",
    "SEO & Barrierefreiheit (BFSG 2025)",
], body_size=20)

# 5 Körper-Analogie
s = prs.slides.add_slide(BLANK)
add_bg(s)
title_block(s, "Webentwicklung", "Die Körper-Analogie")
card(s, 0.45, 2.0, 4.0, 4.4, F3, C3, W3, "HTML", [
    (("Knochen", True),),
    "Struktur & Inhalt",
], body_size=22, num=1)
card(s, 4.65, 2.0, 4.0, 4.4, F2, C2, W2, "CSS", [
    (("Haut / Style", True),),
    "Aussehen & Layout",
], body_size=22, num=2)
card(s, 8.85, 2.0, 4.0, 4.4, F1, C1, W1, "JavaScript", [
    (("Muskeln", True),),
    "Verhalten & Interaktion",
], body_size=20, num=3)

# 6 Client / Server
s = prs.slides.add_slide(BLANK)
add_bg(s)
title_block(s, "So funktionierts Web", "Client · Server · DNS · HTTP")
card(s, 0.7, 2.0, 5.7, 4.4, F2, C2, W2, "Client & Server", [
    (("Client = Browser", True),),
    (("Server = Antwortet", True),),
    "DNS findet die Adresse",
], body_size=22, num=1)
card(s, 6.9, 2.0, 5.7, 4.4, F5, C5, W5, "HTTP", [
    "Anfrage → Antwort",
    "Seiten · Bilder · Daten",
    (("Artifacts = Details", True),),
], body_size=22, num=2)

# 7 Design & UX
s = prs.slides.add_slide(BLANK)
add_bg(s)
title_block(s, "Design & UX", "Schön und nutzbar")
card(s, 0.7, 2.0, 5.7, 4.4, F6, ACCENT, W6, "CSS / UI", [
    "Farben · Abstände · Typo",
    (("UI = was man sieht", True),),
], body_size=22, num=1)
card(s, 6.9, 2.0, 5.7, 4.4, F3, C3, W3, "UX", [
    (("UX = wie es sich anfühlt", True),),
    "Klar · einfach · hilfreich",
], body_size=22, num=2)

# 8 Frameworks
s = prs.slides.add_slide(BLANK)
add_bg(s)
title_block(s, "Frameworks", "Werkzeugkästen für große Apps")
card(s, 0.45, 2.0, 4.0, 4.4, F2, C2, W2, "React", [
    "Sehr verbreitet",
    "Komponenten",
], body_size=20, num=1)
card(s, 4.65, 2.0, 4.0, 4.4, F1, C1, W1, "Vue.js", [
    "Einstieg oft leichter",
    "Flexibel",
], body_size=20, num=2)
card(s, 8.85, 2.0, 4.0, 4.4, F4, C4, W4, "Angular", [
    "Großes Framework",
    "Viele eingebaute Tools",
], body_size=18, num=3)

# 9 Qualitätsstandards
s = prs.slides.add_slide(BLANK)
add_bg(s)
title_block(s, "Qualitätsstandards", "SEO · Barrierefreiheit")
card(s, 0.7, 2.0, 5.7, 4.4, F1, C1, W1, "SEO", [
    (("Auffindbar für Suchmaschinen", True),),
    "Gute Struktur · klare Texte",
], body_size=20, num=1)
card(s, 6.9, 2.0, 5.7, 4.4, F4, C4, W4, "Barrierefreiheit", [
    (("Für alle nutzbar", True),),
    "BFSG 2025",
    "Artifact: a11y",
], body_size=20, num=2)

# 10 Übung 3 DevTools
s = prs.slides.add_slide(BLANK)
add_bg(s)
title_block(s, "Übung 3 · DevTools", "15 Minuten · Detektiv-Mission")
card(s, 1.4, 2.05, 10.5, 4.5, F3, C3, W3, "Drei Missionen", [
    (("Überschrift im HTML ändern", True),),
    "Farbe im CSS ändern",
    "In der Console: alert()",
    "",
    "Artifact: uebung-3-devtools-detektiv",
], body_size=22)

# 11 Übung 1 Visitenkarte
s = prs.slides.add_slide(BLANK)
add_bg(s)
title_block(s, "Übung 1 · Visitenkarte", "20 Minuten · HTML + CSS")
card(s, 0.7, 2.0, 5.7, 4.4, F2, C2, W2, "HTML", [
    (("Digitale Visitenkarte bauen", True),),
    "Name · Rolle · Kontakt",
], body_size=22, num=1)
card(s, 6.9, 2.0, 5.7, 4.4, F6, ACCENT, W6, "CSS", [
    (("Design personalisieren", True),),
    "Farben · Layout · Stil",
], body_size=22, num=2)

# 12 Pause
s = prs.slides.add_slide(BLANK)
add_bg(s)
heart(s, 2.2, 2.5, 0.4)
heart(s, 10.6, 2.5, 0.4, C6)
rounded(s, 3.0, 2.3, 7.3, 3.0, ACCENT_SOFT, ACCENT, border_pt=2.8, adj=0.12)
box, tf = textbox(s, 3.0, 2.8, 7.3, 0.9)
p = p_clear(tf)
p.alignment = PP_ALIGN.CENTER
add_run(p, "Pause", size=52, bold=True, font=FONT_TITLE)
cloud(s, 4.2, 4.0, 4.9, 0.55, "10 Minuten – Sitzung 2 folgt", size=20)

# 13 Sitzung 2
s = prs.slides.add_slide(BLANK)
add_bg(s)
star(s, 1.2, 1.5, 0.4, C4)
rounded(s, 2.4, 2.0, 8.5, 3.5, F4, C4, border_pt=2.8, adj=0.1)
washi(s, 9.4, 1.85, 1.0, 0.22, W4, rot=5)
box, tf = textbox(s, 2.4, 2.5, 8.5, 0.9)
p = p_clear(tf)
p.alignment = PP_ALIGN.CENTER
add_run(p, "Sitzung 2", size=48, bold=True, font=FONT_TITLE)
box, tf = textbox(s, 2.4, 3.5, 8.5, 0.5)
p = p_clear(tf)
p.alignment = PP_ALIGN.CENTER
add_run(p, "JavaScript · Tools · Self-learning", size=24, font=FONT_BODY)
cloud(s, 4.0, 4.4, 5.3, 0.55, "75 Minuten", size=22)

# 14 JS & DOM
s = prs.slides.add_slide(BLANK)
add_bg(s)
title_block(s, "Flash Theorie · JS & DOM", "15 Minuten")
card(s, 0.7, 2.0, 5.7, 4.4, F1, C1, W1, "JavaScript Basics", [
    (("Variablen · Funktionen", True),),
    "Bedingungen (if)",
    "Debugging: Fehler lesen",
], body_size=20, num=1)
card(s, 6.9, 2.0, 5.7, 4.4, F2, C2, W2, "DOM", [
    (("JS spricht mit HTML", True),),
    "Elemente finden & ändern",
    "Artifact: javascript-grundlagen",
], body_size=20, num=2)

# 15 Tools & Workflow
s = prs.slides.add_slide(BLANK)
add_bg(s)
title_block(s, "Tools & Workflow", "15 Minuten · professionell arbeiten")
card(s, 0.45, 2.0, 4.0, 4.4, F2, C2, W2, "VS Code", [
    (("Live Server", True),),
    "Prettier",
], body_size=20, num=1, title_size=16)
card(s, 4.65, 2.0, 4.0, 4.4, F3, C3, W3, "Projektstruktur", [
    "index.html",
    "style.css",
    "script.js",
], body_size=20, num=2, title_size=15)
card(s, 8.85, 2.0, 4.0, 4.4, F5, C5, W5, "DevTools", [
    (("Console", True),),
    "Network-Tab",
], body_size=20, num=3, title_size=16)

# 16 Übung 2
s = prs.slides.add_slide(BLANK)
add_bg(s)
title_block(s, "Übung 2 · Begrüßungs-Generator", "25 Minuten · HTML + CSS + JS")
card(s, 1.4, 2.05, 10.5, 4.5, F6, ACCENT, W6, "Ablauf", [
    "Interface in HTML/CSS bauen",
    (("JS-Funktion + Validierung", True),),
    "Dynamische Begrüßung",
    "Testen & debuggen",
], body_size=22)

# 17 Bilan & Self-learning
s = prs.slides.add_slide(BLANK)
add_bg(s)
title_block(s, "Bilan & Self-learning", "20 Minuten")
card(s, 0.7, 2.0, 5.7, 4.4, F4, C4, W4, "Übung 4 & 5", [
    (("Selbstständig üben", True),),
    "Übung 4 · JS Code Katas",
    "Übung 5 · Ordner & Live Server",
], body_size=20, num=1)
card(s, 6.9, 2.0, 5.7, 4.4, ACCENT_SOFT, ACCENT, W6, "Abschluss", [
    "Kurz zusammenfassen",
    (("Offenes Q&A", True),),
    "Nächste Schritte",
], body_size=20, num=2)

# 18 Zum Mitnehmen
s = prs.slides.add_slide(BLANK)
add_bg(s)
title_block(s, "Zum Mitnehmen", "Artifacts = eure Nachschlagekarte")
card(s, 0.45, 2.0, 4.0, 4.4, F3, C3, W3, "Sitzung 1", [
    "HTML · CSS · Web",
    "DevTools",
    "Visitenkarte",
], body_size=18, num=1)
card(s, 4.65, 2.0, 4.0, 4.4, F2, C2, W2, "Sitzung 2", [
    "JS · DOM",
    "VS Code · Struktur",
    "Begrüßungs-Generator",
], body_size=18, num=2)
card(s, 8.85, 2.0, 4.0, 4.4, F1, C1, W1, "SOL", [
    "Übung 4 · Katas",
    "Übung 5 · Live Server",
    "a11y · Clean Code",
], body_size=18, num=3)

# 19 Danke
s = prs.slides.add_slide(BLANK)
add_bg(s)
star(s, 1.3, 1.8, 0.45)
heart(s, 11.5, 1.9, 0.4)
star(s, 11.7, 5.6, 0.35, C5)
heart(s, 1.2, 5.7, 0.38, C6)
rounded(s, 2.5, 1.9, 8.3, 3.8, WHITE, ACCENT, border_pt=2.8, adj=0.1)
washi(s, 9.3, 1.75, 1.05, 0.22, W6, rot=6)
box, tf = textbox(s, 2.5, 2.4, 8.3, 0.9)
p = p_clear(tf)
p.alignment = PP_ALIGN.CENTER
add_run(p, "Danke!", size=52, bold=True, font=FONT_TITLE)
rounded(s, 5.3, 3.4, 2.7, 0.08, ACCENT, adj=0.5)
box, tf = textbox(s, 2.5, 3.7, 8.3, 0.5)
p = p_clear(tf)
p.alignment = PP_ALIGN.CENTER
add_run(p, "Fragen?  →  jetzt oder später", size=24, font=FONT_BODY)
cloud(s, 4.2, 4.5, 4.9, 0.55, "Artifacts offen lassen", size=22)

for slide in prs.slides:
    add_footer(slide)

prs.save(OUT)
print(f"saved {OUT} ({len(prs.slides)} slides)")
