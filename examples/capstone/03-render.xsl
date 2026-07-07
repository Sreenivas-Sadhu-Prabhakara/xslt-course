<?xml version="1.0" encoding="UTF-8"?>
<!-- CAPSTONE stage 5 (RENDER). The receiver, having DECRYPTED the batch, turns it
     into a human-readable HTML report. Masks the card number for display - decrypted
     does not mean "show in full". Pure XSLT 1.0. -->
<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

  <xsl:output method="html" indent="yes" encoding="UTF-8"/>

  <xsl:template match="/invoiceBatch">
    <html>
      <head><title>Invoice batch <xsl:value-of select="@date"/></title></head>
      <body style="font-family:sans-serif">
        <h1>Invoice batch — <xsl:value-of select="@date"/></h1>
        <xsl:apply-templates select="invoice"/>
      </body>
    </html>
  </xsl:template>

  <xsl:template match="invoice">
    <section>
      <h2><xsl:value-of select="@no"/></h2>
      <p>
        <strong><xsl:value-of select="billTo/name"/></strong>
        &lt;<xsl:value-of select="billTo/email"/>&gt;<br/>
        <!-- show only the last 4 digits of the (decrypted) card number -->
        Card: ****-<xsl:value-of select="substring(payment/pan, string-length(payment/pan) - 3)"/>
      </p>
      <table border="1" cellpadding="4">
        <tr><th>SKU</th><th>Item</th><th>Qty</th><th>Amount</th></tr>
        <xsl:for-each select="lines/line">
          <tr>
            <td><xsl:value-of select="@sku"/></td>
            <td><xsl:value-of select="."/></td>
            <td><xsl:value-of select="@qty"/></td>
            <td>USD <xsl:value-of select="@amount"/></td>
          </tr>
        </xsl:for-each>
        <tr>
          <td colspan="3" align="right"><strong>Total</strong></td>
          <td><strong><xsl:value-of select="total/@currency"/><xsl:text> </xsl:text>
              <xsl:value-of select="total"/></strong></td>
        </tr>
      </table>
    </section>
  </xsl:template>

</xsl:stylesheet>
