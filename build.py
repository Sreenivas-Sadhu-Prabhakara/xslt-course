#!/usr/bin/env python3
"""Assemble the XSLT course site from content partials in content/.

This course is published as a sub-course of the Apigee Courses hub, at
  https://sreenivas-sadhu-prabhakara.github.io/apigee-courses/xslt-course/

The hub owns SEO: its tools/seo_inject.py injects canonical / Open Graph /
Twitter / JSON-LD and regenerates the sitemap for every page after each sync.
So build.py emits a deliberately MINIMAL <head> (title + stylesheet); do not add
SEO tags here or they will duplicate the hub's managed block.

Output goes to docs/ (pages + assets) — the folder the hub's tools/sync.sh pulls.
Run  `python3 build.py`  to regenerate. Source of truth = content/ + this file.
"""
import os, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(HERE, "docs")

# slug, track, number-in-track, nav title, page title, subtitle/lede, kind
PAGES = [
    ("index", None, None, "Home", "The XSLT Course",
     "Learn to transform XML with confidence — then see, honestly, what XSLT can and cannot do for encryption.", "home"),

    ("l01-what-is-xslt", "Transformation", 1, "What XSLT is",
     "What XSLT is & how it runs",
     "A stylesheet is a program that turns one tree into another. Meet the processor, the source tree, and the result tree.", "lesson"),
    ("l02-first-stylesheet", "Transformation", 2, "Your first stylesheet",
     "Your first stylesheet",
     "Write, run, and understand a complete transform from XML to HTML in a dozen lines.", "lesson"),
    ("l03-xpath", "Transformation", 3, "XPath essentials",
     "XPath — the addressing language",
     "Before you can transform a node you must point at it. XPath is how.", "lesson"),
    ("l04-templates", "Transformation", 4, "Template rules",
     "Template rules & apply-templates",
     "The heart of XSLT: describe what to do with each kind of node and let the processor walk the tree.", "lesson"),
    ("l05-shape-data", "Transformation", 5, "Shaping data",
     "Shaping data: sort, choose, attributes",
     "Reorder, branch, compute values, and build attributes at run time.", "lesson"),
    ("l06-keys-grouping", "Transformation", 6, "Keys & grouping",
     "Keys & grouping",
     "Fast lookups with keys, and turning a flat list into groups — the 1.0 way and the 2.0 way.", "lesson"),
    ("l07-recursion", "Transformation", 7, "Recursion",
     "Named templates, parameters & recursion",
     "Reusable subroutines and the recursion pattern you'll reuse to build ciphers.", "lesson"),
    ("l08-versions", "Transformation", 8, "1.0 → 2.0 → 3.0",
     "1.0 → 2.0 → 3.0: what each version adds",
     "Sequences, real functions, regex, maps, and JSON — and when the jump is worth it.", "lesson"),

    ("l09-honest-framing", "Encryption", 1, "The honest framing",
     "Encryption with XSLT — the honest framing",
     "XSLT is a transformer, not a cipher engine. Here are the three real paths, and the rules that keep you safe.", "lesson"),
    ("l10-teaching-ciphers", "Encryption", 2, "Teaching ciphers",
     "Teaching ciphers in pure XSLT",
     "Caesar, Base64, and XOR — built by hand to learn recursion and byte math. Great teachers, terrible security.", "lesson"),
    ("l11-xml-encryption", "Encryption", 3, "W3C XML Encryption",
     "W3C XML Encryption — and XSLT's real role",
     "Encrypt only the sensitive elements of a document. XSLT decides what and where; a vetted library does the how.", "lesson"),
    ("l12-extension-crypto", "Encryption", 4, "Extension functions",
     "Real crypto via extension functions",
     "Call AES, HMAC, and hashing from inside the transform — the pattern used in Java, .NET, and Python stacks.", "lesson"),

    ("capstone", "Practice", 1, "Capstone project",
     "Capstone — the Secure Invoice Exchange",
     "Assemble everything: transform an order feed to a partner invoice, protect the sensitive fields, and reverse it on the far side.", "page"),
    ("reference", "Practice", 2, "Reference & cheat-sheet",
     "Reference & cheat-sheet",
     "The instructions, XPath functions, and commands you'll reach for most, on one page.", "page"),
]

SEQUENCE = [p for p in PAGES if p[0] != "index"]   # for prev/next
TRACKS = ["Transformation", "Encryption", "Practice"]


def title_tag(slug, title):
    if slug == "index":
        return "The XSLT Course — Transformation & Encryption (1.0–3.0)"
    return f"{title} · The XSLT Course"


def sidebar(active_slug):
    out = ['<div class="brand">',
           '  <a href="index.html" aria-label="The XSLT Course home"><span class="mark">&lt;<span class="in">x</span>&#8202;&#8594;&#8202;<span class="out">/</span>&gt;</span></a>',
           '  <a href="index.html" class="name">The&nbsp;XSLT&nbsp;Course</a>',
           '</div>',
           '<button class="menu-btn" aria-expanded="false" aria-controls="nav">Menu</button>',
           '<nav class="nav-wrap" id="nav" aria-label="Course syllabus">']
    for track in TRACKS:
        out.append(f'  <p class="nav-track">{track}</p>')
        out.append('  <ul class="nav-list">')
        for slug, tr, num, navtitle, *_ in PAGES:
            if tr != track:
                continue
            cls = ' class="active" aria-current="page"' if slug == active_slug else ''
            nn = f'{num:02d}' if num else '&#8226;'
            out.append(f'    <li><a href="{slug}.html"{cls}><span class="n">{nn}</span><span>{navtitle}</span></a></li>')
        out.append('  </ul>')
    out.append('</nav>')
    return "\n".join(out)


def lessonnav(slug):
    idx = next((i for i, p in enumerate(SEQUENCE) if p[0] == slug), None)
    if idx is None:
        return ""
    prev_p = SEQUENCE[idx - 1] if idx > 0 else None
    next_p = SEQUENCE[idx + 1] if idx < len(SEQUENCE) - 1 else None
    parts = ['<nav class="lessonnav" aria-label="Lesson navigation">']
    if prev_p:
        parts.append(f'<a href="{prev_p[0]}.html" rel="prev"><span class="dir">&#8592; Previous</span>'
                     f'<span class="ttl">{prev_p[4]}</span></a>')
    if next_p:
        parts.append(f'<a class="next" href="{next_p[0]}.html" rel="next"><span class="dir">Next &#8594;</span>'
                     f'<span class="ttl">{next_p[4]}</span></a>')
    parts.append('</nav>')
    return "\n".join(parts)


# Minimal head — the hub's seo_inject.py adds the managed SEO block before </head>.
SHELL = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title_tag}</title>
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="shell">
<aside class="sidebar">
{sidebar}
</aside>
<main class="main" id="main">
<div class="wrap">
{body}
{lessonnav}
<footer class="foot">
The XSLT Course · a hands-on, honestly-scoped introduction. Every example in this
course is executed, not imagined. Ciphers marked “teaching” are not for protecting real data.
<br><a href="../">↩ Back to the Apigee Courses hub</a>
</footer>
</div>
</main>
</div>
<script src="assets/app.js"></script>
</body>
</html>
"""


def pagehead(track, num, title, lede):
    eyebrow = ""
    if track:
        label = f'{track.upper()}'
        if num:
            label += f' <span class="tick">·</span> LESSON {num:02d}'
        eyebrow = f'<p class="eyebrow">{label}</p>'
    return (f'<header class="pagehead">{eyebrow}'
            f'<h1>{title}</h1><p class="lede">{lede}</p></header>')


def build():
    os.makedirs(DOCS, exist_ok=True)
    n = 0
    for slug, track, num, navtitle, title, lede, kind in PAGES:
        with open(os.path.join(HERE, "content", f"{slug}.html"), encoding="utf-8") as f:
            partial = f.read()
        if kind == "home":
            body = partial
        else:
            body = pagehead(track, num, title, lede) + '\n<div class="prose">\n' + partial + '\n</div>'
        html_out = SHELL.format(
            title_tag=title_tag(slug, title),
            sidebar=sidebar(slug),
            body=body,
            lessonnav="" if kind == "home" else lessonnav(slug),
        )
        with open(os.path.join(DOCS, f"{slug}.html"), "w", encoding="utf-8") as f:
            f.write(html_out)
        n += 1
    print(f"built {n} pages into docs/")


if __name__ == "__main__":
    build()
