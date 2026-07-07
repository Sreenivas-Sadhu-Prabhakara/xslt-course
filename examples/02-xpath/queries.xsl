<?xml version="1.0" encoding="UTF-8"?>
<!-- Lesson 03 - XPath essentials.
     XPath is the little query language XSLT uses to *address* nodes.
     This stylesheet prints the result of several XPath expressions as text.
     Run:  xsltproc 02-xpath/queries.xsl data/catalog.xml
-->
<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

  <xsl:output method="text" encoding="UTF-8"/>

  <xsl:template match="/">
    <xsl:text>All titles (child axis):&#10;</xsl:text>
    <xsl:for-each select="catalog/book/title">
      <xsl:text>  - </xsl:text><xsl:value-of select="."/><xsl:text>&#10;</xsl:text>
    </xsl:for-each>

    <xsl:text>&#10;Books that are in stock (predicate [@inStock='true']):&#10;</xsl:text>
    <xsl:for-each select="catalog/book[@inStock='true']">
      <xsl:text>  - </xsl:text><xsl:value-of select="title"/><xsl:text>&#10;</xsl:text>
    </xsl:for-each>

    <xsl:text>&#10;Security books under $55 (compound predicate):&#10;</xsl:text>
    <xsl:for-each select="catalog/book[@category='security'][price &lt; 55]">
      <xsl:text>  - </xsl:text><xsl:value-of select="title"/>
      <xsl:text> ($</xsl:text><xsl:value-of select="price"/><xsl:text>)&#10;</xsl:text>
    </xsl:for-each>

    <xsl:text>&#10;Aggregations:&#10;</xsl:text>
    <xsl:text>  total books   = </xsl:text><xsl:value-of select="count(catalog/book)"/><xsl:text>&#10;</xsl:text>
    <xsl:text>  sum of prices = </xsl:text><xsl:value-of select="sum(catalog/book/price)"/><xsl:text>&#10;</xsl:text>
    <xsl:text>  first author  = </xsl:text><xsl:value-of select="catalog/book[1]/author"/><xsl:text>&#10;</xsl:text>
    <xsl:text>  last title    = </xsl:text><xsl:value-of select="catalog/book[last()]/title"/><xsl:text>&#10;</xsl:text>
  </xsl:template>

</xsl:stylesheet>
