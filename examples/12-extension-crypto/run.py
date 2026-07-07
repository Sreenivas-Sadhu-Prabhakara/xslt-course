#!/usr/bin/env python3
"""Lesson 12 : register host-language crypto as XSLT extension functions.

We hang four functions under the namespace urn:course:crypto (prefix c:) and
then run ext-crypto.xsl, which calls them from XPath. The exact same idea exists
in every serious XSLT stack:
  - Java / Saxon-PE|EE : integrated ExtensionFunction classes, or reflexive java:
  - .NET               : XsltArgumentList.AddExtensionObject(...)
  - Python / lxml      : etree.FunctionNamespace (this file)

    python3 run.py encrypt note.xml       > envelope.xml
    python3 run.py decrypt envelope.xml   > round-trip.xml

Demo key = SHA-256 of a passphrase. Real systems: use a KDF/KMS, not this.
"""
import sys, os, base64, hashlib, hmac as hmaclib
from lxml import etree
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

KEY = hashlib.sha256(os.environ.get("EXT_PASS", "correct horse battery staple").encode()).digest()

def _s(v):
    """lxml hands string args straight through, node-sets as a list - normalise."""
    return v[0] if isinstance(v, list) else v

def aes_encrypt(ctx, s):
    nonce = os.urandom(12)
    return base64.b64encode(nonce + AESGCM(KEY).encrypt(nonce, str(_s(s)).encode(), None)).decode()

def aes_decrypt(ctx, s):
    blob = base64.b64decode(str(_s(s)))
    return AESGCM(KEY).decrypt(blob[:12], blob[12:], None).decode()

def sha256(ctx, s):
    return hashlib.sha256(str(_s(s)).encode()).hexdigest()

def hmac(ctx, s):
    return hmaclib.new(KEY, str(_s(s)).encode(), hashlib.sha256).hexdigest()

ns = etree.FunctionNamespace("urn:course:crypto")
ns.prefix = "c"
ns.update({"aesEncrypt": aes_encrypt, "aesDecrypt": aes_decrypt,
           "sha256": sha256, "hmac": hmac})

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] not in ("encrypt", "decrypt"):
        sys.exit("usage: run.py [encrypt|decrypt] <file.xml>")
    here = os.path.dirname(os.path.abspath(__file__))
    transform = etree.XSLT(etree.parse(os.path.join(here, "ext-crypto.xsl")))
    result = transform(etree.parse(sys.argv[2]), mode="'%s'" % sys.argv[1])
    sys.stdout.buffer.write(etree.tostring(result, pretty_print=True, xml_declaration=True, encoding="UTF-8"))
