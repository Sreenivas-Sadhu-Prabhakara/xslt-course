<?xml version="1.0" encoding="UTF-8"?>
<!-- Lesson 11 : the XSLT half of XML Encryption.
     XSLT does NOT do the crypto. Its job here is POLICY: an identity transform
     that copies the whole document unchanged, except that it flags the elements
     which must be encrypted with  sec:protect="true".  The policy is declarative,
     auditable, and lives in one place. The crypto engine (xmlenc.py) then acts
     only on the flagged elements.
     Run:  xsltproc 11-xml-encryption/protect-policy.xsl 11-xml-encryption/secret-order.xml
-->
<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:sec="urn:course:sec">

  <xsl:output method="xml" indent="yes" encoding="UTF-8"/>

  <!-- Identity rule: copy every node and attribute as-is. -->
  <xsl:template match="@*|node()">
    <xsl:copy><xsl:apply-templates select="@*|node()"/></xsl:copy>
  </xsl:template>

  <!-- Policy: these element types carry sensitive data -> flag them. -->
  <xsl:template match="pan | cvv | email">
    <xsl:copy>
      <xsl:attribute name="sec:protect">true</xsl:attribute>
      <xsl:apply-templates select="@*|node()"/>
    </xsl:copy>
  </xsl:template>

</xsl:stylesheet>
