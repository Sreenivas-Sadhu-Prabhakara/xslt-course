<?xml version="1.0" encoding="UTF-8"?>
<!-- Lesson 10 : A Caesar cipher in PURE XSLT 1.0.
     This is a TEACHING cipher: it demonstrates recursion over characters.
     It is NOT security : a Caesar shift is broken by a child with a pencil.

     Encrypt (shift 3):  xsltproc -stringparam shift 3 caesar.xsl message.xml
     Decrypt: pass the ciphertext back in and set decrypt=yes.
     (Use two dashes before "stringparam" on the real command line.)
-->
<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

  <xsl:output method="text" encoding="UTF-8"/>

  <xsl:param name="shift" select="3"/>       <!-- how far to rotate (0-25)   -->
  <xsl:param name="decrypt" select="'no'"/>   <!-- 'yes' to reverse the shift -->

  <!-- Doubled alphabets so that pos+shift never runs off the end (wrap-around). -->
  <xsl:variable name="UP">ABCDEFGHIJKLMNOPQRSTUVWXYZ</xsl:variable>
  <xsl:variable name="LO">abcdefghijklmnopqrstuvwxyz</xsl:variable>
  <xsl:variable name="UP2">ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ</xsl:variable>
  <xsl:variable name="LO2">abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz</xsl:variable>

  <!-- Shift ONE character by $n places (0-25). -->
  <xsl:template name="shift-char">
    <xsl:param name="ch"/>
    <xsl:param name="n"/>
    <xsl:choose>
      <xsl:when test="contains($UP, $ch)">
        <xsl:value-of select="substring($UP2, string-length(substring-before($UP, $ch)) + 1 + $n, 1)"/>
      </xsl:when>
      <xsl:when test="contains($LO, $ch)">
        <xsl:value-of select="substring($LO2, string-length(substring-before($LO, $ch)) + 1 + $n, 1)"/>
      </xsl:when>
      <xsl:otherwise>
        <xsl:value-of select="$ch"/>   <!-- digits, spaces, punctuation pass through -->
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <!-- Walk the whole string, shifting the first character and recursing on the rest. -->
  <xsl:template name="caesar">
    <xsl:param name="text"/>
    <xsl:param name="n"/>
    <xsl:if test="string-length($text) &gt; 0">
      <xsl:call-template name="shift-char">
        <xsl:with-param name="ch" select="substring($text, 1, 1)"/>
        <xsl:with-param name="n" select="$n"/>
      </xsl:call-template>
      <xsl:call-template name="caesar">
        <xsl:with-param name="text" select="substring($text, 2)"/>
        <xsl:with-param name="n" select="$n"/>
      </xsl:call-template>
    </xsl:if>
  </xsl:template>

  <xsl:template match="/message">
    <!-- Encrypting shifts forward; decrypting shifts by (26 - shift). -->
    <xsl:variable name="norm" select="$shift mod 26"/>
    <xsl:variable name="effective">
      <xsl:choose>
        <xsl:when test="$decrypt = 'yes'"><xsl:value-of select="(26 - $norm) mod 26"/></xsl:when>
        <xsl:otherwise><xsl:value-of select="$norm"/></xsl:otherwise>
      </xsl:choose>
    </xsl:variable>
    <xsl:call-template name="caesar">
      <xsl:with-param name="text" select="string(.)"/>
      <xsl:with-param name="n" select="number($effective)"/>
    </xsl:call-template>
    <xsl:text>&#10;</xsl:text>
  </xsl:template>

</xsl:stylesheet>
