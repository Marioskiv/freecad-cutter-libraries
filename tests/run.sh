#!/bin/sh
# Cutter Libraries — run the test in a real FreeCAD, with a throw-away user folder.
#
#   FREECAD=/path/to/bin/freecad sh tests/run.sh
#
# Copyright (c) 2026 Marioskiv
# https://github.com/Marioskiv/freecad-cutter-libraries
# SPDX-License-Identifier: MIT
set -u
FREECAD=${FREECAD:-freecad}
REPO=$(cd "$(dirname "$0")/.." && pwd)
OUT=${OUT:-/tmp/cutterlibs-test}
rm -rf "$OUT"
mkdir -p "$OUT/home/.local/share/FreeCAD/v26-3/Mod"
ln -s "$REPO" "$OUT/home/.local/share/FreeCAD/v26-3/Mod/CutterLibraries"
HOME="$OUT/home" CL_OUT="$OUT/run" xvfb-run -a -s "-screen 0 1600x1000x24" \
    "$FREECAD" "$REPO/tests/freecad_install_test.py" > "$OUT/freecad.log" 2>&1
cat "$OUT/run/log.txt" 2>/dev/null
r=$(cat "$OUT/run/result.txt" 2>/dev/null || echo "RESULT: no result (see $OUT/freecad.log)")
echo "$r"
[ "$r" = "RESULT: PASS" ]
