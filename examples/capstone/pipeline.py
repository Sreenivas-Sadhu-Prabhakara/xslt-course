#!/usr/bin/env python3
"""CAPSTONE — the Secure Invoice Exchange, end to end.

    SENDER                                   RECEIVER
    orders.xml
      │ 1  transform (01-to-invoice.xsl)
      ▼
    invoices  ── 2 policy (02-policy.xsl) ── 3 encrypt (AES-256-GCM)
                                                     │  the wire document
                                                     ▼
                                              4 decrypt ── 5 render (03-render.xsl) ── report.html

Every stage is real: XSLT does the transforming and policy; the `cryptography`
library does the AES-GCM. Run:  python3 pipeline.py       (writes out/ and prints a log)
"""
import os, hashlib, base64
from lxml import etree
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
SEC, XENC = "urn:course:sec", "http://www.w3.org/2001/04/xmlenc#"
ALGO = "http://www.w3.org/2009/xmlenc11#aes256-gcm"
KEY = hashlib.sha256(os.environ.get("CAPSTONE_PASS", "shared-demo-key").encode()).digest()


def xslt(name):
    return etree.XSLT(etree.parse(os.path.join(HERE, name)))


def encrypt_marked(tree):
    aes = AESGCM(KEY)
    for el in list(tree.iter()):
        if el.get("{%s}protect" % SEC) != "true":
            continue
        el.attrib.pop("{%s}protect" % SEC)
        etree.cleanup_namespaces(el)
        nonce = os.urandom(12)
        blob = nonce + aes.encrypt(nonce, etree.tostring(el), None)
        enc = etree.Element("{%s}EncryptedData" % XENC, nsmap={"xenc": XENC})
        enc.set("Type", XENC + "Element")
        etree.SubElement(enc, "{%s}EncryptionMethod" % XENC, Algorithm=ALGO)
        cd = etree.SubElement(enc, "{%s}CipherData" % XENC)
        etree.SubElement(cd, "{%s}CipherValue" % XENC).text = base64.b64encode(blob).decode()
        enc.tail = el.tail
        el.getparent().replace(el, enc)
    return tree


def decrypt_wire(tree):
    aes = AESGCM(KEY)
    for enc in tree.findall(".//{%s}EncryptedData" % XENC):
        blob = base64.b64decode(enc.findtext(".//{%s}CipherValue" % XENC))
        restored = etree.fromstring(aes.decrypt(blob[:12], blob[12:], None))
        restored.tail = enc.tail
        enc.getparent().replace(enc, restored)
    return tree


def save(tree_or_bytes, name):
    os.makedirs(OUT, exist_ok=True)
    data = tree_or_bytes if isinstance(tree_or_bytes, bytes) else etree.tostring(
        tree_or_bytes, pretty_print=True, xml_declaration=True, encoding="UTF-8")
    with open(os.path.join(OUT, name), "wb") as f:
        f.write(data)
    return data


def main():
    orders = etree.parse(os.path.join(HERE, "orders.xml"))

    # 1 — transform orders -> partner invoice batch
    invoices = xslt("01-to-invoice.xsl")(orders)
    save(invoices, "1-invoices.xml")
    grand = sum(float(t.text) for t in invoices.iter("total"))
    print("1 TRANSFORM  -> %d invoices, batch total USD %.2f" % (len(invoices.findall("//invoice")), grand))

    # 2 — policy marks sensitive fields
    marked = xslt("02-policy.xsl")(invoices)
    n_marked = len(marked.xpath("//*[@*[local-name()='protect']]"))
    print("2 POLICY     -> flagged %d sensitive fields (email/pan/cvv)" % n_marked)

    # 3 — encrypt marked fields (real AES-256-GCM) -> the wire document
    wire = encrypt_marked(etree.ElementTree(marked.getroot()))
    wire_bytes = save(wire, "3-wire.xml")
    n_enc = wire_bytes.count(b"EncryptedData") // 2
    readable = b"<total" in wire_bytes and b"INV-SO-1001" in wire_bytes
    print("3 ENCRYPT    -> %d EncryptedData blocks; ids/totals still readable: %s" % (n_enc, readable))

    # 4 — receiver decrypts
    back = decrypt_wire(etree.parse(os.path.join(OUT, "3-wire.xml")))
    save(back, "4-decrypted.xml")
    ok = back.findtext("//pan") == "4111111111111111"
    print("4 DECRYPT    -> fields recovered on the far side: %s" % ok)

    # 5 — render to an HTML report
    report = xslt("03-render.xsl")(back)
    save(bytes(report), "5-report.html")
    print("5 RENDER     -> out/5-report.html written")
    print("\nAll stages complete. See the out/ folder for every intermediate document.")


if __name__ == "__main__":
    main()
