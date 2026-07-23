#!/usr/bin/env bash
set -euo pipefail

pdf="${1:?usage: booklet_pdf_smoke.sh BOOKLET_PDF}"

if [[ ! -s "$pdf" ]]; then
    echo "booklet PDF is missing or empty: $pdf" >&2
    exit 1
fi

if [[ "$(LC_ALL=C head -c 5 "$pdf")" != "%PDF-" ]]; then
    echo "booklet output does not start with the PDF magic header: $pdf" >&2
    exit 1
fi
