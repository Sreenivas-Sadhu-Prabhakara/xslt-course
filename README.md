# The XSLT Course

A hands-on, beginner-friendly course on **XSLT** — first for *transformation*
(reshaping XML into HTML, text, JSON, or other XML), then for an honestly-scoped look
at *encryption and decryption* with XSLT.

Two deliverables in one folder:

1. **A static course website** — 15 pages, read it in any browser, host it anywhere.
2. **A runnable examples repo** — every example is actually executed and verified, not
   just printed on a page.

It covers **XSLT 1.0 → 2.0 → 3.0** as a progression, and the crypto track covers all
three honest paths: pure-XSLT teaching ciphers, the **W3C XML Encryption** standard, and
calling **real crypto** from a transform via extension functions. It ends with a
**capstone** that combines transformation and selective encryption end to end.

---

## Read the course

Open **`index.html`** in a browser. That's it — the site is plain static HTML/CSS/JS with
no build step required to view it, and no external network dependencies (system fonts,
inline assets).

Syllabus:

| Track | Lessons |
|-------|---------|
| **Transformation** | what XSLT is · first stylesheet · XPath · template rules · shaping data · keys & grouping · recursion · 1.0→3.0 |
| **Encryption** | the honest framing (+ security) · teaching ciphers · W3C XML Encryption · extension functions |
| **Practice** | capstone: Secure Invoice Exchange · reference & cheat-sheet |

## Run the examples

```bash
cd examples
./fetch-saxon.sh     # once — downloads Saxon-HE for the 2.0/3.0 examples (needs Java)
./run.sh all         # run every example, printing each command
./run.sh 08          # run one lesson's example
./run.sh capstone    # run the full end-to-end capstone pipeline
```

Requirements:

- **`xsltproc`** (ships with macOS/Linux `libxslt`) — for all XSLT 1.0 examples
- **Java 8+** — to run Saxon-HE 10.9 (fetched by `fetch-saxon.sh`) for 2.0/3.0
- **`python3`** with **`lxml`** and **`cryptography`** — for the two real-crypto lessons
  and the capstone (`pip install lxml cryptography`)

See [`examples/README.md`](examples/README.md) for the per-lesson breakdown.

## Project layout

```
xslt-course/
├── index.html, l01-*.html … reference.html   generated site pages (flat, hostable)
├── 404.html                                   friendly not-found page
├── sitemap.xml, robots.txt, site.webmanifest  generated SEO files
├── assets/style.css, assets/app.js           design system + progressive-enhancement JS
├── assets/favicon.svg, og-image.png, icon-*.png   favicon, social card, PWA icons
├── content/                                   editable prose partials (one per page)
├── build.py                                   assembles content/ + chrome + SEO → the pages
├── examples/                                  runnable, verified examples
│   ├── data/catalog.xml                       shared sample data
│   ├── 01-first-transform … 12-extension-crypto
│   ├── capstone/                              the end-to-end pipeline
│   ├── run.sh, fetch-saxon.sh
│   └── README.md
└── README.md
```

## Editing the site

Prose lives in **`content/<page>.html`** (inner content only). Shared chrome (head,
sidebar nav, footer) lives in **`build.py`**. After editing, regenerate the pages:

```bash
python3 build.py       # rebuilds all 15 flat .html files
```

The generated `.html` files are committed so the site hosts as pure static content with
no build step at deploy time. `content/` + `build.py` are the source of truth — edit
there, not the generated files.

## SEO

The site ships a full SEO layer, all generated from `build.py` (so it never drifts):

- Unique `<title>` + meta description, `<link rel="canonical">`, and
  `robots: index, follow` on every page.
- **Open Graph** + **Twitter** `summary_large_image` cards, backed by a branded
  1200×630 `assets/og-image.png`.
- **JSON-LD structured data**: `WebSite` + `Course` (with syllabus, free `offers`,
  and a `CourseInstance`) on the home page; `LearningResource` + `BreadcrumbList` on
  every lesson.
- `sitemap.xml`, `robots.txt` (points at the sitemap), `site.webmanifest`, an SVG
  favicon, Apple-touch and PWA icons, and a `404.html`.

**One knob:** the canonical/OG/sitemap URLs are built from `SITE_URL` at the top of
`build.py`. It is set to
`https://sreenivas-sadhu-prabhakara.github.io/xslt-course`. If you host it elsewhere,
change that one line and re-run `python3 build.py`.

> GitHub Pages note: a project-site `robots.txt` lives under `/xslt-course/` and isn't
> read from the domain root, so after publishing, submit `sitemap.xml` directly in
> Google Search Console. (With a custom domain at the root, `robots.txt` works normally.)

## An important note on the crypto track

XSLT is a **transformation** language, not a cryptography engine. This course is explicit
about that line:

- The pure-XSLT ciphers (Caesar, Base64, XOR) are **teaching tools** — great for learning
  recursion and byte math, and **not safe** for protecting real data.
- Real protection (Lessons 11–12 and the capstone) keeps the cryptography in a **vetted
  library** (AES-256-GCM). XSLT's honest job is to decide *what* to protect and *where* it
  goes; the library does the *how*.

The demo key handling (`SHA-256(passphrase)`) is deliberately simple so the examples are
self-contained. Production systems must use a proper KDF/KMS, per-recipient key wrapping,
authenticated encryption, key rotation, and XXE-safe parsing.

---

*Built for learning. Every command and output shown in the course was executed against
the code in `examples/`.*
