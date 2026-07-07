# Runnable examples

Every example here is **actually executed** in the course — no hand-waving. Files
are numbered to match the lessons on the site.

## One-time setup

| Tool | Used for | Install |
|------|----------|---------|
| `xsltproc` | all XSLT **1.0** examples | ships with macOS & most Linux (`libxslt`) |
| **Saxon-HE 10.9** | XSLT **2.0 / 3.0** examples | `./fetch-saxon.sh` (needs Java 8+ and internet) |
| `python3` + `lxml` + `cryptography` | the two real-crypto examples (11, 12) | `pip install lxml cryptography` |

```bash
./fetch-saxon.sh          # pulls Saxon-HE into lib/ (skip if you only do 1.0)
./run.sh all              # run every example, printing the command for each
./run.sh 08               # run just one
```

## What each example teaches

| # | Folder | Processor | Point |
|---|--------|-----------|-------|
| 01 | `01-first-transform` | xsltproc | the smallest useful stylesheet: XML → HTML |
| 02 | `02-xpath` | xsltproc | XPath: paths, predicates, `count`/`sum`/`last()` |
| 03 | `03-templates` | xsltproc | template rules, `apply-templates`, modes (push style) |
| 04 | `04-shape-data` | xsltproc | `sort`, `choose`, computed attributes (AVTs) |
| 05 | `05-keys-grouping` | both | grouping: 1.0 Muenchian **vs** 2.0 `for-each-group` |
| 06 | `06-recursion` | xsltproc | named templates + recursion (the cipher pattern) |
| 07 | `07-versions` | Saxon | 3.0 power: functions, regex, maps, JSON output |
| 08 | `08-cipher-caesar` | xsltproc | **teaching cipher** — Caesar/ROT13 in pure 1.0 |
| 09 | `09-cipher-base64` | Saxon | **encoding, not crypto** — Base64 by hand |
| 10 | `10-cipher-xor` | Saxon | XOR: encrypt == decrypt; bitwise math without bit ops |
| 11 | `11-xml-encryption` | xsltproc + Python | **W3C XML Encryption**: XSLT marks, AES-GCM protects |
| 12 | `12-extension-crypto` | Python/lxml | **real crypto** called from inside the transform |
| ★ | `capstone` | Python/lxml | **Secure Invoice Exchange** — transform + selective encryption, end to end (`./run.sh capstone`) |

## The honesty rule (read this before the crypto examples)

XSLT is a **transformation** language, not a cipher engine.

- 08–10 are **teaching ciphers**. They are great for learning recursion and byte
  math, and they are **not secure**. Never protect real data with them.
- 11–12 use a vetted library (`cryptography`, AES-256-GCM) for the actual crypto.
  XSLT's job is to decide **what** and **where** — the library does the **how**.
- The demo key is `SHA-256(passphrase)`. Real systems use a proper KDF (HKDF/
  PBKDF2) or a KMS, authenticate ciphertext (GCM/HMAC), and rotate keys.

See the site's *Lesson 09 — the honest framing* for the full decision guide.
