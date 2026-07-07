<?xml version="1.0" encoding="UTF-8"?>
<!-- Lesson 12 : calling REAL crypto from inside a transform.
     The c:* functions are NOT part of XSLT. They are host-language functions
     (see run.py) registered into the processor and invoked from XPath. This is
     the production pattern: XSLT stays declarative and orchestrates; a vetted
     crypto library does the actual AES / HMAC / hashing.

     Encrypt:  python3 run.py encrypt note.xml
     Decrypt:  python3 run.py decrypt envelope.xml
-->
<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:c="urn:course:crypto"
                exclude-result-prefixes="c">

  <xsl:output method="xml" indent="yes" encoding="UTF-8"/>
  <xsl:param name="mode" select="'encrypt'"/>

  <xsl:template match="/">
    <xsl:choose>

      <!-- Verify the HMAC, then decrypt, all via extension functions. -->
      <xsl:when test="$mode = 'decrypt'">
        <note>
          <verified><xsl:value-of
              select="c:hmac(string(/envelope/ciphertext)) = string(/envelope/hmac)"/></verified>
          <body><xsl:value-of select="c:aesDecrypt(string(/envelope/ciphertext))"/></body>
        </note>
      </xsl:when>

      <!-- Encrypt the body, and attach a SHA-256 digest + an HMAC tag. -->
      <xsl:otherwise>
        <xsl:variable name="ct" select="c:aesEncrypt(string(/note/body))"/>
        <envelope alg="AES-256-GCM">
          <ciphertext><xsl:value-of select="$ct"/></ciphertext>
          <sha256 note="digest of plaintext"><xsl:value-of select="c:sha256(string(/note/body))"/></sha256>
          <hmac note="integrity tag over ciphertext"><xsl:value-of select="c:hmac($ct)"/></hmac>
        </envelope>
      </xsl:otherwise>

    </xsl:choose>
  </xsl:template>

</xsl:stylesheet>
