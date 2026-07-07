#!/usr/bin/env python3
"""Assemble the XSLT course, themed to match the Apigee Courses family.

Published as a sub-course of the Apigee Courses hub:
  https://sreenivas-sadhu-prabhakara.github.io/apigee-courses/xslt-course/

Emits the same page anatomy as the other courses (fapi-30-day etc.): a dark-navy
sidebar with progress, a light content column with crumbs/h1/pager, a right
"On this page" TOC rail, and a reading-progress bar. The hub's tools/seo_inject.py
owns SEO, so the <head> here stays minimal. Output -> docs/ (pulled by sync.sh).
Source of truth = content/ + this file. Run: python3 build.py
"""
import os, re, html

HERE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(HERE, "docs")

# slug, track, per-track number, nav title, page title, lede, kind
PAGES = [
    ("index", None, None, "Home", "The XSLT Course",
     "Learn to transform XML with confidence — then see, honestly, what XSLT can and cannot do for encryption.", "home"),
    ("l01-what-is-xslt", "Transformation", 1, "What XSLT is", "What XSLT is & how it runs",
     "A stylesheet is a program that turns one tree into another. Meet the processor, the source tree, and the result tree.", "lesson"),
    ("l02-first-stylesheet", "Transformation", 2, "Your first stylesheet", "Your first stylesheet",
     "Write, run, and understand a complete transform from XML to HTML in a dozen lines.", "lesson"),
    ("l03-xpath", "Transformation", 3, "XPath essentials", "XPath — the addressing language",
     "Before you can transform a node you must point at it. XPath is how.", "lesson"),
    ("l04-templates", "Transformation", 4, "Template rules", "Template rules & apply-templates",
     "The heart of XSLT: describe what to do with each kind of node and let the processor walk the tree.", "lesson"),
    ("l05-shape-data", "Transformation", 5, "Shaping data", "Shaping data: sort, choose, attributes",
     "Reorder, branch, compute values, and build attributes at run time.", "lesson"),
    ("l06-keys-grouping", "Transformation", 6, "Keys & grouping", "Keys & grouping",
     "Fast lookups with keys, and turning a flat list into groups — the 1.0 way and the 2.0 way.", "lesson"),
    ("l07-recursion", "Transformation", 7, "Recursion", "Named templates, parameters & recursion",
     "Reusable subroutines and the recursion pattern you'll reuse to build ciphers.", "lesson"),
    ("l08-versions", "Transformation", 8, "1.0 → 2.0 → 3.0", "1.0 → 2.0 → 3.0: what each version adds",
     "Sequences, real functions, regex, maps, and JSON — and when the jump is worth it.", "lesson"),
    ("l09-honest-framing", "Encryption", 1, "The honest framing", "Encryption with XSLT — the honest framing",
     "XSLT is a transformer, not a cipher engine. Here are the three real paths, and the rules that keep you safe.", "lesson"),
    ("l10-teaching-ciphers", "Encryption", 2, "Teaching ciphers", "Teaching ciphers in pure XSLT",
     "Caesar, Base64, and XOR — built by hand to learn recursion and byte math. Great teachers, terrible security.", "lesson"),
    ("l11-xml-encryption", "Encryption", 3, "W3C XML Encryption", "W3C XML Encryption — and XSLT's real role",
     "Encrypt only the sensitive elements of a document. XSLT decides what and where; a vetted library does the how.", "lesson"),
    ("l12-extension-crypto", "Encryption", 4, "Extension functions", "Real crypto via extension functions",
     "Call AES, HMAC, and hashing from inside the transform — the pattern used in Java, .NET, and Python stacks.", "lesson"),
    ("capstone", "Practice", 1, "Capstone project", "Capstone — the Secure Invoice Exchange",
     "Assemble everything: transform an order feed to a partner invoice, protect the sensitive fields, and reverse it on the far side.", "page"),
    ("reference", "Practice", 2, "Reference & cheat-sheet", "Reference & cheat-sheet",
     "The instructions, XPath functions, and commands you'll reach for most, on one page.", "page"),
]

SEQUENCE = [p for p in PAGES if p[0] != "index"]           # ordered lessons
IDX = {p[0]: i + 1 for i, p in enumerate(SEQUENCE)}        # global 1..N per slug
TOTAL = len(SEQUENCE)
TRACKS = ["Transformation", "Encryption", "Practice"]


def title_tag(slug, title):
    if slug == "index":
        return "The XSLT Course — Transformation & Encryption (1.0–3.0)"
    return f"{title} · The XSLT Course"


def slugify(text, used):
    s = re.sub(r"<[^>]+>", "", text)          # strip tags
    s = html.unescape(s).lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-") or "section"
    base, n = s, 2
    while s in used:
        s = f"{base}-{n}"; n += 1
    used.add(s)
    return s


def process_headings(body):
    """Inject ids into h2/h3 (if missing) and return (body, toc_items)."""
    used, toc = set(), []

    def repl(m):
        tag, level, attrs, inner = m.group(0), m.group(1), m.group(2), m.group(3)
        idm = re.search(r'id="([^"]+)"', attrs)
        hid = idm.group(1) if idm else slugify(inner, used)
        if idm:
            used.add(hid)
        else:
            tag = f"<h{level}{attrs} id=\"{hid}\">{inner}</h{level}>"
        label = re.sub(r"<[^>]+>", "", inner).strip()
        toc.append((int(level), hid, label))
        return tag

    body = re.sub(r'<h([23])((?:\s[^>]*)?)>(.*?)</h\1>', repl, body, flags=re.DOTALL)
    return body, toc


def toc_rail(toc):
    if not toc:
        return ""
    items = []
    for level, hid, label in toc:
        cls = ' class="lvl3"' if level == 3 else ""
        items.append(f'    <li{cls}><a href="#{hid}">{label}</a></li>')
    return ('<aside class="toc-rail" aria-label="On this page">\n'
            '  <div class="toc-title">On this page</div>\n'
            '  <nav class="toc"><ul>\n' + "\n".join(items) + '\n  </ul></nav>\n</aside>')


def sidebar(active_slug):
    out = ['<a class="brand" href="index.html">'
           '<span class="mark">&lt;<span class="in">x</span>&#8202;&#8594;&#8202;<span class="out">/</span>&gt;</span>'
           'The&nbsp;XSLT&nbsp;Course</a>',
           '<div class="nav-progress"><div class="nav-progress-bar"><span id="navProgressFill"></span></div>'
           '<span class="nav-progress-text" id="navProgressText">0 / %d complete</span></div>' % TOTAL]
    for track in TRACKS:
        out.append(f'<div class="nav-week">{track}</div>')
        out.append('<ul>')
        for slug, tr, num, navtitle, *_ in PAGES:
            if tr != track:
                continue
            gi = IDX[slug]
            active = ' class="active"' if slug == active_slug else ''
            out.append(
                f'  <li data-idx="{gi}"{active}><a href="{slug}.html">'
                f'<span class="daynum">{gi:02d}</span><span>{navtitle}</span>'
                f'<span class="done-check">&#10003;</span></a></li>')
        out.append('</ul>')
    return "\n".join(out)


def crumbs(track, num, kind):
    if not track:
        return ""
    tail = f' <span class="tick">·</span> LESSON {num:02d}' if kind == "lesson" else ""
    return f'<div class="crumbs">{track.upper()}{tail}</div>'


def pager(slug):
    i = IDX.get(slug)
    if not i:
        return ""
    prev_p = SEQUENCE[i - 2] if i > 1 else None
    next_p = SEQUENCE[i] if i < TOTAL else None
    parts = ['<nav class="lessonnav" aria-label="Lesson navigation">']
    if prev_p:
        parts.append(f'<a href="{prev_p[0]}.html" rel="prev"><span class="dir">&#8592; Previous</span>'
                     f'<span class="ttl">{prev_p[4]}</span></a>')
    if next_p:
        parts.append(f'<a class="next" href="{next_p[0]}.html" rel="next"><span class="dir">Next &#8594;</span>'
                     f'<span class="ttl">{next_p[4]}</span></a>')
    parts.append('</nav>')
    return "\n".join(parts)


def mark_complete(slug):
    i = IDX.get(slug)
    if not i:
        return ""
    return ('<div class="day-complete"><button class="mark-btn" id="markComplete" type="button">'
            '<span class="mark-box">&#10003;</span> Mark lesson complete</button>'
            '<span class="mark-hint">Saved in your browser</span></div>')


SHELL = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title_tag}</title>
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<div id="readingBar"></div>
<button class="nav-toggle" id="navToggle" aria-label="Toggle navigation">&#9776; Menu</button>
<a class="skip" href="#main">Skip to content</a>
<div class="layout">
<nav class="sidebar" aria-label="Course syllabus">
{sidebar}
</nav>
<main class="content{index_cls}" id="main"{data_idx}>
{crumbs}
{h1}
{body}
{mark}
{pager}
<footer class="foot">
The XSLT Course · every example is executed, not imagined. Ciphers marked
“teaching” are not for protecting real data.
<br><a href="../">↩ Back to the Apigee Courses hub</a>
</footer>
</main>
{toc}
</div>
<script src="assets/app.js"></script>
</body>
</html>
"""


def build():
    os.makedirs(DOCS, exist_ok=True)
    n = 0
    for slug, track, num, navtitle, title, lede, kind in PAGES:
        with open(os.path.join(HERE, "content", f"{slug}.html"), encoding="utf-8") as f:
            partial = f.read()

        if kind == "home":
            body, toc = partial, []
            h1 = ""       # index partial supplies its own hero/h1
            index_cls, data_idx = " index", ""
            crumb = mark = pgr = tocr = ""
        else:
            body, toc = process_headings(partial)
            h1 = f'<h1>{title}</h1>\n<p class="lead">{lede}</p>'
            index_cls = ""
            data_idx = f' data-idx="{IDX[slug]}"'
            crumb = crumbs(track, num, kind)
            mark = mark_complete(slug)
            pgr = pager(slug)
            tocr = toc_rail(toc)

        page = SHELL.format(
            title_tag=title_tag(slug, title),
            sidebar=sidebar(slug),
            index_cls=index_cls,
            data_idx=data_idx,
            crumbs=crumb,
            h1=h1,
            body=body,
            mark=mark,
            pager=pgr,
            toc=tocr,
        )
        with open(os.path.join(DOCS, f"{slug}.html"), "w", encoding="utf-8") as f:
            f.write(page)
        n += 1
    print(f"built {n} pages into docs/")


if __name__ == "__main__":
    build()
