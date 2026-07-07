<?xml version="1.0" encoding="UTF-8"?>
<!-- Lesson 05 - Shaping data: sorting, computed attributes and AVTs.
     Produces an HTML table sorted by price (descending), with a CSS class
     chosen at run time via an Attribute Value Template ({...}).
     Run:  xsltproc 04-shape-data/report.xsl data/catalog.xml
-->
<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

  <xsl:output method="html" indent="yes" encoding="UTF-8"/>

  <xsl:template match="/catalog">
    <table border="1">
      <tr><th>Title</th><th>Author</th><th>Price</th><th>Status</th></tr>
      <!-- xsl:sort re-orders the selected nodes before we process them -->
      <xsl:for-each select="book">
        <xsl:sort select="price" data-type="number" order="descending"/>
        <!-- The {...} is an Attribute Value Template: the expression inside
             is evaluated and its result becomes the attribute's value. -->
        <tr class="{@category}">
          <td><xsl:value-of select="title"/></td>
          <td><xsl:value-of select="author"/></td>
          <td><xsl:value-of select="concat(price/@currency, ' ', price)"/></td>
          <td>
            <xsl:choose>
              <xsl:when test="@inStock='true'">in stock</xsl:when>
              <xsl:otherwise>backorder</xsl:otherwise>
            </xsl:choose>
          </td>
        </tr>
      </xsl:for-each>
    </table>
  </xsl:template>

</xsl:stylesheet>
