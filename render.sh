#!/bin/bash

INPUT="$1"
OUTDIR="/tmp/wiki_render"
FILENAME=$(basename "$INPUT")
OUTFILE="$OUTDIR/${FILENAME}.html"

mkdir -p "$OUTDIR"

if [ ! -f "$INPUT" ]; then
    echo "[ERROR] Input file does not exist: $INPUT"
    exit 1
fi

CONTENT=$(cat "$INPUT")

CONTENT=$(echo "$CONTENT" | sed -E '
    s/\*\*(.+?)\*\*/<b>\1<\/b>/g;                    # grassetto
    s/__(.+?)__/<i>\1<\/i>/g;                        # corsivo
    s/~~(.+?)~~/<del>\1<\/del>/g;                    # barrato
    s/^# (.+)/<h1>\1<\/h1>/g;                        # h1 header
    s/\[(.+?)\]\((.+?)\)/<a href="\2">\1<\/a>/g;     # link markdown
    s/FLAG/\[FL4G\]/g;
    s/\{/\(/g;                                       # graffa aperta → parentesi
    s/\}/\)/g;                                       # graffa chiusa → parentesi
    s/_/-/g;                                         # underscore → trattino
    s/O/Ø/g;                                         # O maiuscola → Ø
    s/o/ø/g;                                         # o minuscola → ø
    s/a/@/g;
    s/e/3/g;
    s/i/1/g;
    s/s/5/g;
    s/S/\$/g;
    s/0/O/g;
    s/l/|/g;
    s/I/!/g;
    s/g/9/g;
    s/z/2/g;
')

echo "$CONTENT" > "$OUTFILE"
echo "[OK] Rendered to: $OUTFILE"
