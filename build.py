#!/usr/bin/env python3
"""Assemble the static course site from content partials in content/.

Single source of truth:
  - prose for each page lives in  content/<slug>.html  (inner content only)
  - shared chrome + ALL SEO (meta, Open Graph, Twitter, JSON-LD, sitemap,
    robots, manifest) lives here, so regenerating never drifts from the source.
Run  `python3 build.py`  to regenerate the flat HTML pages + SEO files at the root.

>>> If you move the site, change SITE_URL (one line) and re-run. <<<
"""
import os, json, html

HERE = os.path.dirname(os.path.abspath(__file__))

# ------------------------------------------------------------------ site config
SITE_URL   = "https://sreenivas-sadhu-prabhakara.github.io/xslt-course"  # no trailing slash
SITE_NAME  = "The XSLT Course"
AUTHOR     = "Sreenivas Sadhu Prabhakara"
LOCALE     = "en_US"
BUILD_DATE = "2026-07-07"          # sitemap <lastmod>; bump when content changes
OG_IMAGE   = SITE_URL + "/assets/og-image.png"
LOGO       = SITE_URL + "/assets/icon-512.png"

ORG    = {"@type": "Organization", "name": SITE_NAME, "url": SITE_URL + "/",
          "logo": {"@type": "ImageObject", "url": LOGO}}
PERSON = {"@type": "Person", "name": AUTHOR}

# keywords the course legitimately targets (used in home meta + Course.about)
ABOUT = ["XSLT", "XSLT tutorial", "XML transformation", "XPath", "XSLT 3.0",
         "Saxon", "xsltproc", "XML Encryption", "encrypt XML", "Base64", "XOR cipher"]

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

A = lambda s: html.escape(s, quote=True)    # attribute-safe
T = lambda s: html.escape(s, quote=False)   # text-safe


def canonical_of(slug):
    return SITE_URL + "/" if slug == "index" else f"{SITE_URL}/{slug}.html"


def seo_title(slug, title):
    if slug == "index":
        return "The XSLT Course — Transformation & Encryption (1.0–3.0)"
    return f"{title} · {SITE_NAME}"


def head_seo(slug, title, desc):
    """All the per-page <head> SEO tags."""
    canon = canonical_of(slug)
    ogtype = "website" if slug == "index" else "article"
    desc_a = A(desc)
    kw = A(", ".join(ABOUT)) if slug == "index" else ""
    lines = [
        f'<title>{T(seo_title(slug, title))}</title>',
        f'<meta name="description" content="{desc_a}">',
        f'<link rel="canonical" href="{canon}">',
        '<meta name="robots" content="index, follow, max-image-preview:large">',
        f'<meta name="author" content="{A(AUTHOR)}">',
        '<meta name="theme-color" content="#16191f">',
        '<meta name="color-scheme" content="light">',
    ]
    if kw:
        lines.append(f'<meta name="keywords" content="{kw}">')
    lines += [
        '<link rel="icon" type="image/svg+xml" href="assets/favicon.svg">',
        '<link rel="icon" type="image/png" sizes="192x192" href="assets/icon-192.png">',
        '<link rel="apple-touch-icon" href="assets/icon-180.png">',
        '<link rel="manifest" href="site.webmanifest">',
        # Open Graph
        f'<meta property="og:type" content="{ogtype}">',
        f'<meta property="og:site_name" content="{A(SITE_NAME)}">',
        f'<meta property="og:title" content="{A(title)}">',
        f'<meta property="og:description" content="{desc_a}">',
        f'<meta property="og:url" content="{canon}">',
        f'<meta property="og:image" content="{OG_IMAGE}">',
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        f'<meta property="og:image:alt" content="{A(SITE_NAME)}">',
        f'<meta property="og:locale" content="{LOCALE}">',
        # Twitter
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{A(title)}">',
        f'<meta name="twitter:description" content="{desc_a}">',
        f'<meta name="twitter:image" content="{OG_IMAGE}">',
    ]
    return "\n".join(lines)


def jsonld(slug, track, num, title, desc):
    """Structured data. Home: WebSite + Course. Lessons: LearningResource + Breadcrumb."""
    canon = canonical_of(slug)
    if slug == "index":
        course = {
            "@type": "Course", "name": SITE_NAME, "description": desc,
            "url": SITE_URL + "/", "inLanguage": "en", "provider": ORG,
            "author": PERSON, "isAccessibleForFree": True,
            "educationalLevel": "Beginner", "about": ABOUT,
            "teaches": ["XSLT transformation", "XPath", "grouping and recursion",
                        "XSLT 1.0 to 3.0", "XML Encryption", "calling crypto from XSLT"],
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD",
                       "availability": "https://schema.org/InStock"},
            "hasCourseInstance": {"@type": "CourseInstance", "courseMode": "online",
                                  "courseWorkload": "PT8H",
                                  "instructor": PERSON},
            "hasPart": [{"@type": "LearningResource", "name": p[4],
                         "url": canonical_of(p[0])}
                        for p in SEQUENCE],
        }
        website = {"@type": "WebSite", "name": SITE_NAME, "url": SITE_URL + "/",
                   "inLanguage": "en", "description": desc, "publisher": ORG}
        graph = [website, course]
    else:
        crumbs = [{"@type": "ListItem", "position": 1, "name": "Home", "item": SITE_URL + "/"}]
        if track:
            crumbs.append({"@type": "ListItem", "position": 2, "name": track,
                           "item": SITE_URL + "/#syllabus"})
        crumbs.append({"@type": "ListItem", "position": len(crumbs) + 1,
                       "name": title, "item": canon})
        breadcrumb = {"@type": "BreadcrumbList", "itemListElement": crumbs}
        resource = {
            "@type": "LearningResource", "name": title, "description": desc,
            "url": canon, "inLanguage": "en",
            "learningResourceType": "lesson", "educationalLevel": "Beginner",
            "isPartOf": {"@type": "Course", "name": SITE_NAME, "url": SITE_URL + "/"},
            "author": PERSON, "publisher": ORG, "isAccessibleForFree": True,
        }
        if num:
            resource["position"] = num
        graph = [breadcrumb, resource]
    payload = {"@context": "https://schema.org", "@graph": graph}
    blob = json.dumps(payload, ensure_ascii=False, indent=2).replace("</", "<\\/")
    return f'<script type="application/ld+json">\n{blob}\n</script>'


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


SHELL = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{seo}
<link rel="sitemap" type="application/xml" href="sitemap.xml">
<link rel="stylesheet" href="assets/style.css">
{jsonld}
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
course is executed, not imagined. Built for learning; ciphers marked “teaching” are
not for protecting real data.
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


def write_sitemap():
    prio = {"index": "1.0"}
    urls = []
    for slug, track, num, navtitle, title, lede, kind in PAGES:
        p = prio.get(slug, "0.8" if kind == "lesson" else "0.7")
        urls.append(
            f"  <url>\n    <loc>{canonical_of(slug)}</loc>\n"
            f"    <lastmod>{BUILD_DATE}</lastmod>\n"
            f"    <changefreq>monthly</changefreq>\n    <priority>{p}</priority>\n  </url>")
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           + "\n".join(urls) + "\n</urlset>\n")
    with open(os.path.join(HERE, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(xml)


def write_robots():
    txt = ("# The XSLT Course\n"
           "User-agent: *\n"
           "Allow: /\n"
           f"Sitemap: {SITE_URL}/sitemap.xml\n")
    with open(os.path.join(HERE, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(txt)


def write_manifest():
    m = {"name": SITE_NAME, "short_name": "XSLT Course", "start_url": "./index.html",
         "scope": "./", "display": "standalone",
         "background_color": "#f6f7f4", "theme_color": "#16191f",
         "description": "A hands-on course on XSLT transformation and honestly-scoped encryption.",
         "icons": [
             {"src": "assets/icon-192.png", "sizes": "192x192", "type": "image/png"},
             {"src": "assets/icon-512.png", "sizes": "512x512", "type": "image/png",
              "purpose": "any maskable"}]}
    with open(os.path.join(HERE, "site.webmanifest"), "w", encoding="utf-8") as f:
        json.dump(m, f, indent=2)


def write_404():
    body = ('<section class="hero">'
            '<p class="eyebrow">Error 404</p>'
            '<h1>This page didn\'t transform.</h1>'
            '<p class="lede">The URL you followed isn\'t part of the course. '
            'Head back to the start or jump to the syllabus.</p>'
            '<div class="cta"><a class="btn btn--primary" href="index.html">Go to the home page &#8594;</a> '
            '<a class="btn btn--ghost" href="reference.html">Open the reference</a></div></section>')
    html_out = SHELL.format(
        seo=('<title>Page not found — The XSLT Course</title>'
             '<meta name="robots" content="noindex, follow">'
             '<link rel="icon" type="image/svg+xml" href="assets/favicon.svg">'),
        jsonld="", sidebar=sidebar(""), body=body, lessonnav="")
    with open(os.path.join(HERE, "404.html"), "w", encoding="utf-8") as f:
        f.write(html_out)


def build():
    n = 0
    for slug, track, num, navtitle, title, lede, kind in PAGES:
        with open(os.path.join(HERE, "content", f"{slug}.html"), encoding="utf-8") as f:
            partial = f.read()
        if kind == "home":
            body = partial
        else:
            body = pagehead(track, num, title, lede) + '\n<div class="prose">\n' + partial + '\n</div>'
        html_out = SHELL.format(
            seo=head_seo(slug, title, lede),
            jsonld=jsonld(slug, track, num, title, lede),
            sidebar=sidebar(slug),
            body=body,
            lessonnav="" if kind == "home" else lessonnav(slug),
        )
        with open(os.path.join(HERE, f"{slug}.html"), "w", encoding="utf-8") as f:
            f.write(html_out)
        n += 1
    write_sitemap()
    write_robots()
    write_manifest()
    write_404()
    print(f"built {n} pages + sitemap.xml, robots.txt, site.webmanifest, 404.html")


if __name__ == "__main__":
    build()
