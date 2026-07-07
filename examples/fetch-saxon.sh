#!/usr/bin/env bash
# Downloads Saxon-HE 10.9 (a self-contained XSLT 3.0 processor) into lib/.
# Only needed for the 2.0 / 3.0 examples (05b, 07, 09, 10). The 1.0 examples
# use xsltproc, which ships with macOS/Linux.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p lib
JAR="lib/Saxon-HE-10.9.jar"
URL="https://repo1.maven.org/maven2/net/sf/saxon/Saxon-HE/10.9/Saxon-HE-10.9.jar"
if [[ -f "$JAR" ]]; then echo "Already present: $JAR"; exit 0; fi
echo "Downloading Saxon-HE 10.9 ..."
curl -fsSL -o "$JAR" "$URL"
echo "Done: $JAR"
java -jar "$JAR" -? >/dev/null 2>&1 || true
echo "Test: java -jar $JAR -xsl:... -s:..."
