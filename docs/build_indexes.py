#!/usr/bin/env python3
"""Generate navigable index.html files under docs/."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# (relative css path depth helpers)
def css_href(depth: int) -> str:
    return "../" * depth + "style.css" if depth else "style.css"


def page(title: str, tag: str, crumb: list[tuple[str, str]], body: str, depth: int, lang="de") -> str:
    crumbs = ' <span aria-hidden="true">›</span> '.join(
        (f'<a href="{href}">{label}</a>' if href else label) for label, href in crumb
    )
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@500;700&family=Patrick+Hand&family=Caveat:wght@600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{css_href(depth)}">
</head>
<body>
<main class="sheet">
  <h1>{title}</h1>
  <p class="center"><span class="tag">{tag}</span></p>
  <p class="crumb">{crumbs}</p>
{body}
  <p class="footer">Kremstaler Digitalhilfe</p>
</main>
</body>
</html>
"""


def cards(items: list[tuple[str, str, str, str]]) -> str:
    """items: (href, title, desc, css color var like --c1)"""
    parts = ['  <section class="grid">']
    for href, title, desc, c in items:
        parts.append(
            f'    <a class="card" style="--c:var({c})" href="{href}">'
            f"<h2>{title}<span class=\"arrow\">→</span></h2>"
            f"<p>{desc}</p></a>"
        )
    parts.append("  </section>")
    return "\n".join(parts)


def file_list(items: list[tuple[str, str, str]], color="--c2") -> str:
    """items: (href, kind, label)"""
    lines = [f'  <ul class="list">']
    for href, kind, label in items:
        lines.append(
            f'    <li><a href="{href}"><span class="kind" style="--c:var({color});background:var({color})">{kind}</span>{label}</a></li>'
        )
    lines.append("  </ul>")
    return "\n".join(lines)


indexes = {}

# ── docs/ ──
indexes[ROOT / "index.html"] = page(
    "Courses",
    "Kremstaler Digitalhilfe",
    [("Home", None)],
    cards([
        ("deutsch/", "Deutsch", "Fiches & Übungen auf Deutsch", "--c1"),
        ("english/", "English", "Coming soon", "--c2"),
    ]),
    depth=0,
    lang="en",
)

# ── deutsch/ ──
indexes[ROOT / "deutsch" / "index.html"] = page(
    "Deutsch",
    "Artifacts · Fiches & Übungen",
    [("Home", "../"), ("Deutsch", None)],
    cards([
        ("WEB/", "WEB", "HTML · CSS · JavaScript · Übungen", "--c2"),
        ("PM/", "Product Management", "Agil · Boards · Tools · Übungen", "--c4"),
        ("technisches-objekt.html", "Technisches Objekt", "Beispiel-Fiche (Referenz)", "--c3"),
    ]),
    depth=1,
)

# ── deutsch/WEB/ ──
indexes[ROOT / "deutsch" / "WEB" / "index.html"] = page(
    "WEB",
    "Web Development",
    [("Home", "../../"), ("Deutsch", "../"), ("WEB", None)],
    cards([
        ("Exercises/", "Exercises", "In-presence & SOL Übungen", "--c3"),
        ("powerpoint/", "PowerPoint", "Flash-Theorie Sitzungen", "--c6"),
    ])
    + "\n  <hr>\n  <h3 style=\"font-family:var(--font-title);margin:0\">Fiches</h3>\n"
    + file_list([
        ("prerequisites-web.html", "Setup", "Prerequisites"),
        ("html-grundlagen.html", "Fiche", "HTML Grundlagen"),
        ("css-grundlagen.html", "Fiche", "CSS Grundlagen"),
        ("javascript-grundlagen.html", "Fiche", "JavaScript Grundlagen"),
        ("barrierefreiheit-a11y.html", "Fiche", "Barrierefreiheit (a11y)"),
        ("clean-code-prinzipien.html", "Fiche", "Clean Code Prinzipien"),
    ], "--c2"),
    depth=2,
)

# ── deutsch/WEB/Exercises/ ──
indexes[ROOT / "deutsch" / "WEB" / "Exercises" / "index.html"] = page(
    "WEB · Exercises",
    "Übungen",
    [("Home", "../../../"), ("Deutsch", "../../"), ("WEB", "../"), ("Exercises", None)],
    cards([
        ("in-presence/", "In-presence", "Übung 1 · 2 · 3", "--c1"),
        ("SOL/", "SOL", "Übung 4 · 5 (Self-learning)", "--c5"),
    ]),
    depth=3,
)

# ── deutsch/WEB/Exercises/in-presence/ ──
indexes[ROOT / "deutsch" / "WEB" / "Exercises" / "in-presence" / "index.html"] = page(
    "In-presence",
    "WEB · Präsenz",
    [
        ("Home", "../../../../"),
        ("Deutsch", "../../../"),
        ("WEB", "../../"),
        ("Exercises", "../"),
        ("In-presence", None),
    ],
    file_list([
        ("uebung-1-digitale-visitenkarte.html", "Übung 1", "Digitale Visitenkarte"),
        ("uebung-2-begruessungs-generator.html", "Übung 2", "Begrüßungs-Generator"),
        ("uebung-3-devtools-detektiv.html", "Übung 3", "DevTools Detektiv"),
    ], "--c1"),
    depth=4,
)

# ── deutsch/WEB/Exercises/SOL/ ──
indexes[ROOT / "deutsch" / "WEB" / "Exercises" / "SOL" / "index.html"] = page(
    "SOL",
    "WEB · Self-learning",
    [
        ("Home", "../../../../"),
        ("Deutsch", "../../../"),
        ("WEB", "../../"),
        ("Exercises", "../"),
        ("SOL", None),
    ],
    file_list([
        ("uebung-4-js-code-katas.html", "Übung 4", "JS Code Katas"),
        ("uebung-5-lokaler-ordner-live-server.html", "Übung 5", "Ordner & Live Server"),
    ], "--c5"),
    depth=4,
)

# ── deutsch/WEB/powerpoint/ ──
indexes[ROOT / "deutsch" / "WEB" / "powerpoint" / "index.html"] = page(
    "WEB · PowerPoint",
    "Flash Theorie",
    [
        ("Home", "../../../"),
        ("Deutsch", "../../"),
        ("WEB", "../"),
        ("PowerPoint", None),
    ],
    file_list([
        ("web-seance-flash-theorie.pptx", "PPTX", "Séance Flash Theorie (WEB)"),
    ], "--c6"),
    depth=3,
)

# ── deutsch/PM/ ──
indexes[ROOT / "deutsch" / "PM" / "index.html"] = page(
    "Product Management",
    "PM · Agile",
    [("Home", "../../"), ("Deutsch", "../"), ("PM", None)],
    cards([
        ("Exercises/", "Exercises", "In-presence & SOL Übungen", "--c3"),
        ("powerpoint/", "PowerPoint", "Flash-Theorie Sitzungen", "--c6"),
    ])
    + "\n  <hr>\n  <h3 style=\"font-family:var(--font-title);margin:0\">Module</h3>\n"
    + file_list([
        ("prerequisites-pm.html", "Setup", "Prerequisites"),
        ("modul1-agiles-setup.html", "Modul 1", "Agiles Setup"),
        ("modul2-boards-und-stories.html", "Modul 2", "Boards & Stories"),
        ("modul3-tools.html", "Modul 3", "Tools"),
    ], "--c4"),
    depth=2,
)

# ── deutsch/PM/Exercises/ ──
indexes[ROOT / "deutsch" / "PM" / "Exercises" / "index.html"] = page(
    "PM · Exercises",
    "Übungen",
    [("Home", "../../../"), ("Deutsch", "../../"), ("PM", "../"), ("Exercises", None)],
    cards([
        ("in-presence/", "In-presence", "Module 1 · 2 · 3", "--c1"),
        ("SOL/", "SOL", "Mini-Projekt & Epic", "--c5"),
    ]),
    depth=3,
)

# ── deutsch/PM/Exercises/in-presence/ ──
indexes[ROOT / "deutsch" / "PM" / "Exercises" / "in-presence" / "index.html"] = page(
    "In-presence",
    "PM · Präsenz",
    [
        ("Home", "../../../../"),
        ("Deutsch", "../../../"),
        ("PM", "../../"),
        ("Exercises", "../"),
        ("In-presence", None),
    ],
    file_list([
        ("uebung-modul-1.html", "Modul 1", "Übung Modul 1"),
        ("uebung-modul-2.html", "Modul 2", "Übung Modul 2"),
        ("uebung-modul-3.html", "Modul 3", "Übung Modul 3"),
    ], "--c1"),
    depth=4,
)

# ── deutsch/PM/Exercises/SOL/ ──
indexes[ROOT / "deutsch" / "PM" / "Exercises" / "SOL" / "index.html"] = page(
    "SOL",
    "PM · Self-learning",
    [
        ("Home", "../../../../"),
        ("Deutsch", "../../../"),
        ("PM", "../../"),
        ("Exercises", "../"),
        ("SOL", None),
    ],
    file_list([
        ("mini-projekt-fitnessstudio-app.html", "SOL", "Mini-Projekt Fitnessstudio-App"),
        ("uebung-epic-in-user-stories.html", "SOL", "Epic → User Stories"),
    ], "--c5"),
    depth=4,
)

# ── deutsch/PM/powerpoint/ ──
indexes[ROOT / "deutsch" / "PM" / "powerpoint" / "index.html"] = page(
    "PM · PowerPoint",
    "Flash Theorie",
    [
        ("Home", "../../../"),
        ("Deutsch", "../../"),
        ("PM", "../"),
        ("PowerPoint", None),
    ],
    file_list([
        ("pm-seance-flash-theorie.pptx", "PPTX", "Séance Flash Theorie (PM)"),
    ], "--c6"),
    depth=3,
)

# ── english/ ──
indexes[ROOT / "english" / "index.html"] = page(
    "English",
    "Coming soon",
    [("Home", "../"), ("English", None)],
    '  <div class="note"><p style="margin:0">English artifacts will appear here.</p></div>',
    depth=1,
    lang="en",
)

for path, html in indexes.items():
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")
    print("wrote", path.relative_to(ROOT))

print(f"done · {len(indexes)} indexes")
