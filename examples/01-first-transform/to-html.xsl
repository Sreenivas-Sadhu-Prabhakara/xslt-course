<?xml version="1.0" encoding="UTF-8"?>
<!-- Lesson 02 - Your first stylesheet.
     Turns catalog.xml into a small HTML page.
     Run:  xsltproc 01-first-transform/to-html.xsl data/catalog.xml
-->
<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

  <!-- Ask for tidy, indented HTML output -->
  <xsl:output method="html" indent="yes" encoding="UTF-8"/>

  <!-- The processor starts at the document root "/".
       This single template describes the whole output document. -->
  <xsl:template match="/">
    <html>
      <head>
        <title>Bookshop catalogue</title>
      </head>
      <body>
        <h1>Bookshop catalogue</h1>
        <p>We have <xsl:value-of select="count(catalog/book)"/> titles.</p>
        <ul>
          <!-- Loop over every <book> and emit one list item -->
          <xsl:for-each select="catalog/book">
            <li>
              <xsl:value-of select="title"/>
              <xsl:text> — </xsl:text>
              <xsl:value-of select="author"/>
            </li>
          </xsl:for-each>
        </ul>
      </body>
    </html>
  </xsl:template>

</xsl:stylesheet>
