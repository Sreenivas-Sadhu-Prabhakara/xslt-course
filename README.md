# The XSLT Course

A hands-on, beginner-friendly course on **XSLT** — first for *transformation*
(reshaping XML into HTML, text, JSON, or other XML), then for an honestly-scoped look
at *encryption and decryption* with XSLT. Covers **XSLT 1.0 → 2.0 → 3.0** and ends with a
capstone that combines transformation and selective encryption.

**▶ Live:** https://sreenivas-sadhu-prabhakara.github.io/apigee-courses/xslt-course/
(published as a sub-course of the Apigee Courses hub.)

Two things live in this repo:

1. **The course site source** — prose partials in `content/`, assembled by `build.py`
   into the static site in `docs/`.
2. **A runnable examples repo** — every example is actually executed and verified.

## Run the examples

```bash
cd examples
./fetch-saxon.sh     # once — downloads Saxon-HE for the 2.0/3.0 examples (needs Java)
./run.sh all         # run every example, printing each command
./run.sh 08          # run one lesson's example
./run.sh capstone    # run the full end-to-end capstone pipeline
```

Requirements: `xsltproc` (1.0), Java for Saxon-HE 10.9 (`fetch-saxon.sh`), and `python3`
with `lxml` + `cryptography` (real-crypto lessons + capstone). See
[`examples/README.md`](examples/README.md).

## Project layout

```
xslt-course/
├── content/                 editable prose partials (one per page) — source of truth
├── build.py                 assembles content/ → docs/ (minimal-head static pages)
├── docs/                    the built site (pages + assets) — what the hub publishes
│   ├── index.html, l01-*.html … reference.html
│   └── assets/style.css, assets/app.js
├── examples/                runnable, verified examples (+ capstone/)
└── README.md
```

## Editing the site

Prose lives in `content/<slug>.html`; shared chrome (nav, footer) lives in `build.py`.
After editing, regenerate:

```bash
python3 build.py             # rebuilds docs/
```

## How it's published (and where SEO lives)

This course is hosted as a sub-course of the **Apigee Courses hub**
(`../apigee-courses`). The hub pulls this repo's `docs/` folder via its `tools/sync.sh`
and then runs `tools/seo_inject.py`, which **owns all SEO** — canonical, Open Graph,
Twitter, JSON-LD (Course + LearningResource + BreadcrumbList), plus the aggregated
`sitemap.xml`. That's why the pages here ship a deliberately minimal `<head>`: adding SEO
tags in `build.py` would duplicate the hub's managed block. To change what the hub emits
for this course, edit its `tools/seo_inject.py` (`COURSES`) and `tools/seo_descriptions.json`.

## An important note on the crypto track

XSLT is a **transformation** language, not a cryptography engine. The pure-XSLT ciphers
(Caesar, Base64, XOR) are **teaching tools** — not safe for real data. Real protection
(Lessons 11–12 and the capstone) keeps the cryptography in a **vetted library**
(AES-256-GCM); XSLT only decides *what* to protect and *where*. The demo key handling is
deliberately simple — production needs a proper KDF/KMS, key rotation, and XXE-safe parsing.

---

*Every command and output shown in the course was executed against the code in `examples/`.*
