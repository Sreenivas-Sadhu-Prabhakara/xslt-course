#!/usr/bin/env python3
"""Lesson 11 : the CRYPTO half of XML Encryption.

XSLT (protect-policy.xsl) marks sensitive elements with sec:protect="true".
This script does what XSLT deliberately cannot: real AES-256-GCM. Each flagged
element is replaced, in place, by a W3C-standard <xenc:EncryptedData> element.
decrypt reverses it. The non-sensitive parts of the document are untouched, so
middleware can still read the order id, totals, SKUs, etc.

    python3 xmlenc.py encrypt secret-order.xml  > order.enc.xml   # (via the marker)
    python3 xmlenc.py decrypt order.enc.xml      > order.dec.xml

Key handling here (SHA-256 of a passphrase) is deliberately simple so the demo
is self-contained. REAL systems must use a proper KDF (HKDF/PBKDF2) or a KMS,
and must manage key rotation - never hard-code keys.
"""
import sys, os, hashlib, base64
from lxml import etree
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

SEC  = "urn:course:sec"
XENC = "http://www.w3.org/2001/04/xmlenc#"
ALGO = "http://www.w3.org/2009/xmlenc11#aes256-gcm"
PASSPHRASE = os.environ.get("XMLENC_PASS", "correct horse battery staple")

def key() -> bytes:
    return hashlib.sha256(PASSPHRASE.encode()).digest()   # 32 bytes = AES-256

def run_policy(doc_path: str) -> etree._ElementTree:
    """Apply the XSLT policy so sensitive elements get sec:protect='true'."""
    here = os.path.dirname(os.path.abspath(__file__))
    xslt = etree.XSLT(etree.parse(os.path.join(here, "protect-policy.xsl")))
    return xslt(etree.parse(doc_path))

def encrypt(doc_path: str) -> bytes:
    tree = run_policy(doc_path)
    aes = AESGCM(key())
    for el in tree.iter():
        if el.get("{%s}protect" % SEC) != "true":
            continue
        el.attrib.pop("{%s}protect" % SEC)          # strip the marker...
        etree.cleanup_namespaces(el)
        plaintext = etree.tostring(el)              # ...encrypt the whole element
        nonce = os.urandom(12)
        blob  = nonce + aes.encrypt(nonce, plaintext, None)   # nonce||ciphertext||tag

        enc = etree.SubElement(el.getparent(), "{%s}EncryptedData" % XENC,
                               nsmap={"xenc": XENC})
        enc.set("Type", XENC + "Element")
        etree.SubElement(enc, "{%s}EncryptionMethod" % XENC, Algorithm=ALGO)
        cd = etree.SubElement(enc, "{%s}CipherData" % XENC)
        etree.SubElement(cd, "{%s}CipherValue" % XENC).text = base64.b64encode(blob).decode()
        enc.tail = el.tail
        el.getparent().replace(el, enc)             # swap plaintext -> ciphertext
    return etree.tostring(tree, pretty_print=True, xml_declaration=True, encoding="UTF-8")

def decrypt(doc_path: str) -> bytes:
    tree = etree.parse(doc_path)
    aes = AESGCM(key())
    for enc in tree.findall(".//{%s}EncryptedData" % XENC):
        blob = base64.b64decode(enc.findtext(".//{%s}CipherValue" % XENC))
        nonce, ct = blob[:12], blob[12:]
        plaintext = aes.decrypt(nonce, ct, None)
        restored = etree.fromstring(plaintext)      # back to the original element
        restored.tail = enc.tail
        enc.getparent().replace(enc, restored)
    return etree.tostring(tree, pretty_print=True, xml_declaration=True, encoding="UTF-8")

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] not in ("encrypt", "decrypt"):
        sys.exit("usage: xmlenc.py [encrypt|decrypt] <file.xml>")
    out = encrypt(sys.argv[2]) if sys.argv[1] == "encrypt" else decrypt(sys.argv[2])
    sys.stdout.buffer.write(out)
