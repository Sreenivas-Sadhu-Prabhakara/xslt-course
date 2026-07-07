#!/usr/bin/env bash
# Tiny dispatcher so you can run any lesson's example without memorising flags.
#   ./run.sh 01        run one example      ./run.sh all     run them all
# Each case prints the exact command first, so you learn the real invocation.
set -euo pipefail
cd "$(dirname "$0")"
SELF="$PWD/run.sh"   # absolute path, so `all` can re-invoke after the cd above

SAXON_JAR="lib/Saxon-HE-10.9.jar"
saxon() {
  if [[ ! -f "$SAXON_JAR" ]]; then
    echo "Saxon not found. Run ./fetch-saxon.sh first (needs Java + internet)." >&2
    exit 1
  fi
  java -jar "$SAXON_JAR" "$@"
}
run() { echo "\$ $*" >&2; "$@"; echo >&2; }

case "${1:-help}" in
  01) run xsltproc 01-first-transform/to-html.xsl data/catalog.xml ;;
  02) run xsltproc 02-xpath/queries.xsl data/catalog.xml ;;
  03) run xsltproc 03-templates/apply-templates.xsl data/catalog.xml ;;
  04) run xsltproc 04-shape-data/report.xsl data/catalog.xml ;;
  05) run xsltproc 05-keys-grouping/muenchian-1.0.xsl data/catalog.xml
      echo "----- same result with XSLT 2.0 xsl:for-each-group -----" >&2
      run saxon -xsl:05-keys-grouping/grouping-2.0.xsl -s:data/catalog.xml ;;
  06) run xsltproc 06-recursion/string-tools.xsl data/catalog.xml ;;
  07) run saxon -xsl:07-versions/catalog-to-json.xsl -s:data/catalog.xml ;;
  08) echo "# encrypt (Caesar shift 3):" >&2
      run xsltproc --stringparam shift 3 08-cipher-caesar/caesar.xsl 08-cipher-caesar/message.xml ;;
  09) echo "# Base64 encode:" >&2
      run saxon -xsl:09-cipher-base64/base64.xsl -s:09-cipher-base64/message.xml ;;
  10) echo "# XOR encrypt (key=SECRET) -> hex:" >&2
      run saxon -xsl:10-cipher-xor/xor.xsl -s:10-cipher-xor/message.xml key=SECRET ;;
  11) echo "# 1) XSLT policy marks sensitive elements, 2) AES-256-GCM encrypts, 3) decrypt round-trips" >&2
      run python3 11-xml-encryption/xmlenc.py encrypt 11-xml-encryption/secret-order.xml > /tmp/order.enc.xml
      cat /tmp/order.enc.xml
      echo "----- decrypted again -----" >&2
      run python3 11-xml-encryption/xmlenc.py decrypt /tmp/order.enc.xml ;;
  12) ( cd 12-extension-crypto
        echo "# XSLT calls AES/SHA/HMAC as extension functions:" >&2
        python3 run.py encrypt note.xml > /tmp/envelope.xml
        cat /tmp/envelope.xml
        echo "----- decrypt + HMAC verify -----" >&2
        python3 run.py decrypt /tmp/envelope.xml ) ;;
  capstone) echo "# full Secure Invoice Exchange pipeline (transform → protect → encrypt → decrypt → render)" >&2
      run python3 capstone/pipeline.py ;;
  all) for i in 01 02 03 04 05 06 07 08 09 10 11 12; do
         echo "========================================= EXAMPLE $i"
         "$SELF" "$i"
       done ;;
  *) echo "usage: ./run.sh [01..12|capstone|all]"; exit 1 ;;
esac
