<?xml version="1.0" encoding="UTF-8"?>
<!-- Lesson 06 - The same grouping in XSLT 2.0/3.0.
     xsl:for-each-group replaces the whole Muenchian dance with one instruction.
     Run:  java -jar lib/Saxon-HE-10.9.jar -xsl:05-keys-grouping/grouping-2.0.xsl -s:data/catalog.xml
-->
<xsl:stylesheet version="2.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

  <xsl:output method="text" encoding="UTF-8"/>

  <xsl:template match="/catalog">
    <xsl:text>Books grouped by category&#10;</xsl:text>
    <xsl:for-each-group select="book" group-by="@category">
      <xsl:sort select="current-grouping-key()"/>
      <xsl:value-of select="current-grouping-key()"/>
      <xsl:text> (</xsl:text><xsl:value-of select="count(current-group())"/><xsl:text>):&#10;</xsl:text>
      <xsl:for-each select="current-group()">
        <xsl:sort select="title"/>
        <xsl:text>  - </xsl:text><xsl:value-of select="title"/><xsl:text>&#10;</xsl:text>
      </xsl:for-each>
    </xsl:for-each-group>
  </xsl:template>

</xsl:stylesheet>
