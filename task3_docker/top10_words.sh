#!/bin/bash

set -euo pipefail

file="$1"; outdir="$2"; mkdir -p "$outdir"

i=1

head -n 10 "$file" | awk '{print $2}' | while read w; do
    touch "${outdir}/${w}_${i}.txt"
    echo "Создан файл: ${outdir}/${w}_${i}.txt"
    ((i++))
done
