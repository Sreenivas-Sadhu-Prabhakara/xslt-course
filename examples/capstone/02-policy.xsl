<?xml version="1.0" encoding="UTF-8"?>
<!-- CAPSTONE stage 2 (POLICY). Identity transform that flags the sensitive fields
     of the invoice so the crypto step knows exactly what to encrypt. One reviewable
     place for "what counts as sensitive". (Same idea as Lesson 11.) -->
<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:sec="urn:course:sec">

  <xsl:output method="xml" indent="yes" encoding="UTF-8"/>

  <xsl:template match="@*|node()">
    <xsl:copy><xsl:apply-templates select="@*|node()"/></xsl:copy>
  </xsl:template>

  <!-- sensitive fields in an invoice: email, card number, card verification value -->
  <xsl:template match="email | pan | cvv">
    <xsl:copy>
      <xsl:attribute name="sec:protect">true</xsl:attribute>
      <xsl:apply-templates select="@*|node()"/>
    </xsl:copy>
  </xsl:template>

</xsl:stylesheet>
