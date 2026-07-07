<?xml version="1.0" encoding="UTF-8"?>
<!-- Lesson 10 : A repeating-key XOR cipher in XSLT 3.0 (Saxon).
     XOR is the atom every real stream cipher is built from - but a *fixed
     repeating key* like this is trivially broken (frequency / crib dragging).
     Treat it as a way to SEE how encrypt and decrypt are the very same op.

     XPath has no bitwise operators, so we compute XOR one bit at a time.
     Output is hex so the (non-printable) cipher bytes are visible.

     Encrypt: java -jar lib/Saxon-HE-10.9.jar -xsl:10-cipher-xor/xor.xsl -s:10-cipher-xor/message.xml key=SECRET
     Decrypt: feed the hex back inside <message> and add  decrypt=yes
-->
<xsl:stylesheet version="3.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:xs="http://www.w3.org/2001/XMLSchema"
                xmlns:c="urn:course:fn"
                exclude-result-prefixes="xs c">

  <xsl:output method="text" encoding="UTF-8"/>
  <xsl:param name="key" select="'SECRET'"/>
  <xsl:param name="decrypt" select="'no'"/>

  <xsl:variable name="POW" as="xs:integer*" select="(1,2,4,8,16,32,64,128)"/>
  <xsl:variable name="HEX" select="'0123456789abcdef'"/>

  <!-- XOR of two bytes, computed bit by bit: for each of 8 bit positions the
       result bit is 1 exactly when the two input bits differ. -->
  <xsl:function name="c:xor" as="xs:integer">
    <xsl:param name="a" as="xs:integer"/>
    <xsl:param name="b" as="xs:integer"/>
    <xsl:sequence select="sum(
        for $i in 1 to 8 return
          if ((($a idiv $POW[$i]) mod 2) ne (($b idiv $POW[$i]) mod 2))
          then $POW[$i] else 0)"/>
  </xsl:function>

  <xsl:function name="c:hex2" as="xs:string">           <!-- byte -> two hex digits -->
    <xsl:param name="n" as="xs:integer"/>
    <xsl:sequence select="concat(substring($HEX, $n idiv 16 + 1, 1),
                                 substring($HEX, $n mod 16 + 1, 1))"/>
  </xsl:function>

  <xsl:function name="c:unhex" as="xs:integer">         <!-- two hex digits -> byte -->
    <xsl:param name="h" as="xs:string"/>
    <xsl:sequence select="string-length(substring-before($HEX, substring($h,1,1))) * 16
                        + string-length(substring-before($HEX, substring($h,2,1)))"/>
  </xsl:function>

  <xsl:template match="/message">
    <xsl:variable name="keyb" select="string-to-codepoints($key)"/>
    <xsl:variable name="klen" select="count($keyb)"/>
    <xsl:choose>

      <!-- DECRYPT: hex string -> bytes -> XOR with key -> text -->
      <xsl:when test="$decrypt = 'yes'">
        <xsl:variable name="hex" select="normalize-space(string(.))"/>
        <xsl:variable name="plain" select="
            for $i in 1 to (string-length($hex) idiv 2) return
              c:xor(c:unhex(substring($hex, ($i - 1) * 2 + 1, 2)),
                    $keyb[($i - 1) mod $klen + 1])"/>
        <xsl:value-of select="codepoints-to-string($plain)"/>
      </xsl:when>

      <!-- ENCRYPT: text -> XOR with key -> hex string -->
      <xsl:otherwise>
        <xsl:variable name="cp" select="string-to-codepoints(string(.))"/>
        <xsl:value-of separator="" select="
            for $i in 1 to count($cp) return
              c:hex2(c:xor($cp[$i], $keyb[($i - 1) mod $klen + 1]))"/>
      </xsl:otherwise>
    </xsl:choose>
    <xsl:text>&#10;</xsl:text>
  </xsl:template>

</xsl:stylesheet>
