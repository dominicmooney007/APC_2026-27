#!/usr/bin/env bash
# Regenerate the Schoology offline HTML + whole-course zip in one command.
# Run from anywhere:  ./rebuild-offline.sh
set -e
cd "$(dirname "$0")"        # repo root (apc-2026-27/)

# One-time setup (safe to re-run): pip install markdown pymdown-extensions pygments
python3 build_offline.py docs schoology-offline

echo
echo "Done. Upload the schoology-offline/ folder to Schoology."
