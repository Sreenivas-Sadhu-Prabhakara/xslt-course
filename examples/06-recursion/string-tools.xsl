<?xml version="1.0" encoding="UTF-8"?>
<!-- Lesson 07 - Named templates, parameters and recursion.
     XSLT 1.0 has no loops that mutate a counter and no built-in reverse(),
     so we walk a string one character at a time by calling a template that
     calls itself. This is the SAME shape of code the Caesar cipher uses in
     lesson 10 - master it here first.
     Run:  xsltproc 06-recursion/string-tools.xsl data/catalog.xml
-->
<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

  <xsl:output method="text" encoding="UTF-8"/>

  <!-- Reverse a string by peeling off the last character and recursing. -->
  <xsl:template name="reverse-string">
    <xsl:param name="s"/>
    <xsl:if test="string-length($s) &gt; 0">
      <!-- emit the last character... -->
      <xsl:value-of select="substring($s, string-length($s), 1)"/>
      <!-- ...then reverse everything before it -->
      <xsl:call-template name="reverse-string">
        <xsl:with-param name="s" select="substring($s, 1, string-length($s) - 1)"/>
      </xsl:call-template>
    </xsl:if>
    <!-- when $s is empty the recursion stops (the base case) -->
  </xsl:template>

  <xsl:template match="/catalog">
    <xsl:for-each select="book">
      <xsl:value-of select="title"/><xsl:text>  ->  </xsl:text>
      <xsl:call-template name="reverse-string">
        <xsl:with-param name="s" select="title"/>
      </xsl:call-template>
      <xsl:text>&#10;</xsl:text>
    </xsl:for-each>
  </xsl:template>

</xsl:stylesheet>
