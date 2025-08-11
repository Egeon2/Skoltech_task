#!/bin/bash
set -euo pipefail

file="$1"; outdir="$2"; mkdir -p "$outdir"; export LC_ALL=C

tr '[:upper:]' '[:lower:]' < "$file" \
| grep -oE "[[:alpha:]]+(?:'[[:alpha:]]+|-?[[:alpha:]]+)*" \
| sed -E "s/'s$//; s/'s[[:punct:]]$//" \
| sort | uniq -c | sort -nr \
| tee "$outdir/word_count.txt"
