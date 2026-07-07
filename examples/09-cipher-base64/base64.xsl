<?xml version="1.0" encoding="UTF-8"?>
<!-- Lesson 10 : Base64 in XSLT 3.0 (Saxon).
     Base64 is ENCODING, not encryption - it hides nothing, it just makes
     bytes safe to put in text. We build it by hand to see how 3 bytes map to
     4 characters, and to show why byte work needs 2.0+ (string-to-codepoints).

     Encode:  java -jar lib/Saxon-HE-10.9.jar -xsl:09-cipher-base64/base64.xsl -s:09-cipher-base64/message.xml
     Decode:  add  decode=yes  (put the Base64 text inside <message>)
     NOTE: assumes ASCII input; real UTF-8 bytes need a codepoint->bytes step.
-->
<xsl:stylesheet version="3.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:xs="http://www.w3.org/2001/XMLSchema"
                xmlns:c="urn:course:fn"
                exclude-result-prefixes="xs c">

  <xsl:output method="text" encoding="UTF-8"/>
  <xsl:param name="decode" select="'no'"/>

  <xsl:variable name="ALPHA"
    select="'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'"/>

  <!-- ENCODE: recurse over the byte sequence three bytes at a time. -->
  <xsl:function name="c:encode" as="xs:string">
    <xsl:param name="bytes" as="xs:integer*"/>
    <xsl:choose>
      <xsl:when test="empty($bytes)"><xsl:sequence select="''"/></xsl:when>
      <xsl:otherwise>
        <xsl:variable name="n"  select="count($bytes[position() le 3])"/>
        <xsl:variable name="b0" select="$bytes[1]"/>
        <xsl:variable name="b1" select="if ($n ge 2) then $bytes[2] else 0"/>
        <xsl:variable name="b2" select="if ($n ge 3) then $bytes[3] else 0"/>
        <xsl:variable name="i0" select="$b0 idiv 4"/>
        <xsl:variable name="i1" select="($b0 mod 4)*16 + $b1 idiv 16"/>
        <xsl:variable name="i2" select="($b1 mod 16)*4 + $b2 idiv 64"/>
        <xsl:variable name="i3" select="$b2 mod 64"/>
        <xsl:sequence select="concat(
            substring($ALPHA, $i0 + 1, 1),
            substring($ALPHA, $i1 + 1, 1),
            (if ($n ge 2) then substring($ALPHA, $i2 + 1, 1) else '='),
            (if ($n ge 3) then substring($ALPHA, $i3 + 1, 1) else '='),
            c:encode(subsequence($bytes, 4)))"/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:function>

  <!-- value (0-63) of one Base64 character -->
  <xsl:function name="c:val" as="xs:integer">
    <xsl:param name="ch" as="xs:string"/>
    <xsl:sequence select="string-length(substring-before($ALPHA, $ch))"/>
  </xsl:function>

  <!-- DECODE: 4 characters back into 3 bytes; trim bytes for '=' padding. -->
  <xsl:function name="c:decode" as="xs:integer*">
    <xsl:param name="text" as="xs:string"/>
    <xsl:variable name="pad"   select="string-length(replace($text, '[^=]', ''))"/>
    <xsl:variable name="clean" select="translate($text, '=', 'A')"/>
    <xsl:variable name="vals"  select="for $i in 1 to string-length($clean)
                                       return c:val(substring($clean, $i, 1))"/>
    <xsl:variable name="bytes" as="xs:integer*">
      <xsl:for-each select="1 to (count($vals) idiv 4)">
        <xsl:variable name="g" select="(. - 1) * 4"/>
        <xsl:variable name="v0" select="$vals[$g + 1]"/>
        <xsl:variable name="v1" select="$vals[$g + 2]"/>
        <xsl:variable name="v2" select="$vals[$g + 3]"/>
        <xsl:variable name="v3" select="$vals[$g + 4]"/>
        <xsl:sequence select="$v0 * 4 + $v1 idiv 16"/>
        <xsl:sequence select="($v1 mod 16) * 16 + $v2 idiv 4"/>
        <xsl:sequence select="($v2 mod 4) * 64 + $v3"/>
      </xsl:for-each>
    </xsl:variable>
    <xsl:sequence select="$bytes[position() le (count($bytes) - $pad)]"/>
  </xsl:function>

  <xsl:template match="/message">
    <xsl:choose>
      <xsl:when test="$decode = 'yes'">
        <xsl:value-of select="codepoints-to-string(c:decode(normalize-space(string(.))))"/>
      </xsl:when>
      <xsl:otherwise>
        <xsl:value-of select="c:encode(string-to-codepoints(string(.)))"/>
      </xsl:otherwise>
    </xsl:choose>
    <xsl:text>&#10;</xsl:text>
  </xsl:template>

</xsl:stylesheet>
