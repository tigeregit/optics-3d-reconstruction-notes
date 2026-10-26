#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
TECTONIC="${TECTONIC:-/workspace/bin/tectonic}"
if [[ ! -x "$TECTONIC" ]]; then
  TECTONIC="$(command -v tectonic || true)"
fi
if [[ -z "${TECTONIC}" ]]; then
  echo "tectonic not found" >&2
  exit 1
fi
# Two passes help ToC / refs with tectonic's bibtex integration
"$TECTONIC" -X compile book.tex
echo "Built: $ROOT/book.pdf"
