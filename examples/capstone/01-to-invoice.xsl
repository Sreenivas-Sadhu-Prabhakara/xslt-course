<?xml version="1.0" encoding="UTF-8"?>
<!-- CAPSTONE stage 1 (TRANSFORM). orders  ->  partner invoice batch.
     Uses: template rules, computed attributes, and a RECURSIVE named template to
     total each invoice (Lesson 7). Pure XSLT 1.0 so it runs in xsltproc or lxml. -->
<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

  <xsl:output method="xml" indent="yes" encoding="UTF-8"/>

  <!-- Recursively sum qty * unitPrice across a set of <item> nodes. -->
  <xsl:template name="sum-items">
    <xsl:param name="items"/>
    <xsl:param name="acc" select="0"/>
    <xsl:choose>
      <xsl:when test="$items">
        <xsl:call-template name="sum-items">
          <xsl:with-param name="items" select="$items[position() &gt; 1]"/>
          <xsl:with-param name="acc" select="$acc + $items[1]/@qty * $items[1]/@unitPrice"/>
        </xsl:call-template>
      </xsl:when>
      <xsl:otherwise><xsl:value-of select="format-number($acc, '0.00')"/></xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template match="/orders">
    <invoiceBatch date="{@batch}">
      <xsl:apply-templates select="order"/>
    </invoiceBatch>
  </xsl:template>

  <xsl:template match="order">
    <invoice no="INV-{@id}">
      <billTo>
        <name><xsl:value-of select="customer/name"/></name>
        <email><xsl:value-of select="customer/email"/></email>
      </billTo>
      <!-- carry payment through; it will be encrypted in stage 2/3 -->
      <payment>
        <pan><xsl:value-of select="payment/pan"/></pan>
        <cvv><xsl:value-of select="payment/cvv"/></cvv>
      </payment>
      <lines>
        <xsl:for-each select="items/item">
          <line sku="{@sku}" qty="{@qty}" unitPrice="{@unitPrice}"
                amount="{format-number(@qty * @unitPrice, '0.00')}">
            <xsl:value-of select="."/>
          </line>
        </xsl:for-each>
      </lines>
      <total currency="USD">
        <xsl:call-template name="sum-items">
          <xsl:with-param name="items" select="items/item"/>
        </xsl:call-template>
      </total>
    </invoice>
  </xsl:template>

</xsl:stylesheet>
