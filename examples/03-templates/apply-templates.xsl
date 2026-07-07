<?xml version="1.0" encoding="UTF-8"?>
<!-- Lesson 04 - Template rules & the "push" style.
     Instead of one big template with loops, we write one small template
     per kind of node and let the processor walk the tree for us with
     <xsl:apply-templates/>. Compare this to the for-each "pull" style.
     Run:  xsltproc 03-templates/apply-templates.xsl data/catalog.xml
-->
<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

  <xsl:output method="text" encoding="UTF-8"/>

  <!-- Rule for the root: print a header, then process the books. -->
  <xsl:template match="/catalog">
    <xsl:text>CATALOGUE&#10;=========&#10;</xsl:text>
    <xsl:apply-templates select="book"/>
  </xsl:template>

  <!-- Rule for each book. It in turn asks for its children to be processed. -->
  <xsl:template match="book">
    <xsl:text>&#10;* </xsl:text>
    <xsl:apply-templates select="title"/>
    <xsl:apply-templates select="author"/>
    <xsl:apply-templates select="tags"/>
  </xsl:template>

  <xsl:template match="title">
    <xsl:value-of select="."/><xsl:text>&#10;</xsl:text>
  </xsl:template>

  <xsl:template match="author">
    <xsl:text>    by </xsl:text><xsl:value-of select="."/><xsl:text>&#10;</xsl:text>
  </xsl:template>

  <!-- 'mode' lets the same node be processed differently in different contexts. -->
  <xsl:template match="tags">
    <xsl:text>    tags: </xsl:text>
    <xsl:apply-templates select="tag" mode="inline"/>
    <xsl:text>&#10;</xsl:text>
  </xsl:template>

  <xsl:template match="tag" mode="inline">
    <xsl:if test="position() &gt; 1">, </xsl:if>
    <xsl:value-of select="."/>
  </xsl:template>

</xsl:stylesheet>
