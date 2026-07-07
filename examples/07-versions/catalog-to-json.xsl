<?xml version="1.0" encoding="UTF-8"?>
<!-- Lesson 08 - What 2.0/3.0 add. A single stylesheet that would be painful
     in 1.0: user-defined functions, regex tokenize, maps/arrays, and direct
     JSON output. Turns the XML catalogue into a JSON document.
     Run:  java -jar lib/Saxon-HE-10.9.jar -xsl:07-versions/catalog-to-json.xsl -s:data/catalog.xml
-->
<xsl:stylesheet version="3.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:xs="http://www.w3.org/2001/XMLSchema"
                xmlns:c="urn:course:fn"
                exclude-result-prefixes="xs c">

  <!-- method="json" serialises a map/array as JSON - built in to XSLT 3.0 -->
  <xsl:output method="json" indent="yes"/>

  <!-- A typed, reusable user-defined function (new in 2.0). -->
  <xsl:function name="c:slug" as="xs:string">
    <xsl:param name="s" as="xs:string"/>
    <xsl:sequence select="lower-case(replace(normalize-space($s), '\s+', '-'))"/>
  </xsl:function>

  <xsl:template match="/catalog">
    <!-- Build an array of maps, then let xsl:output serialise it to JSON. -->
    <xsl:sequence select="array {
        for $b in book return map {
          'id'       : string($b/@id),
          'slug'     : c:slug($b/title),
          'title'    : string($b/title),
          'author'   : string($b/author),
          'year'     : xs:integer($b/year),
          'price'    : xs:decimal($b/price),
          'inStock'  : xs:boolean($b/@inStock),
          'tags'     : array { $b/tags/tag ! string(.) }
        }
      }"/>
  </xsl:template>

</xsl:stylesheet>
