<?xml version="1.0" encoding="UTF-8"?>
<!-- Lesson 06 - Grouping in XSLT 1.0 (the "Muenchian" method).
     XSLT 1.0 has no group-by, so we use xsl:key + generate-id() to pick one
     representative node per group. It works, but it is famously fiddly - which
     is exactly why 2.0 added xsl:for-each-group (see grouping-2.0.xsl).
     Run:  xsltproc 05-keys-grouping/muenchian-1.0.xsl data/catalog.xml
-->
<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

  <xsl:output method="text" encoding="UTF-8"/>

  <!-- Index every book by its category -->
  <xsl:key name="byCategory" match="book" use="@category"/>

  <xsl:template match="/catalog">
    <xsl:text>Books grouped by category&#10;</xsl:text>
    <!-- Select only the FIRST book of each category: a book is "first" if it is
         identical to the first node returned by key() for its category. -->
    <xsl:for-each select="book[generate-id() =
                               generate-id(key('byCategory', @category)[1])]">
      <xsl:sort select="@category"/>
      <xsl:value-of select="@category"/><xsl:text> (</xsl:text>
      <xsl:value-of select="count(key('byCategory', @category))"/>
      <xsl:text>):&#10;</xsl:text>
      <xsl:for-each select="key('byCategory', @category)">
        <xsl:sort select="title"/>
        <xsl:text>  - </xsl:text><xsl:value-of select="title"/><xsl:text>&#10;</xsl:text>
      </xsl:for-each>
    </xsl:for-each>
  </xsl:template>

</xsl:stylesheet>
