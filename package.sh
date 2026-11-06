#!/usr/bin/env bash
# SPDX-FileCopyrightText: 2026 GeometrIA Lab, CBG
# SPDX-License-Identifier: MIT
# Build zip archives of the skills in dist/:
#   dist/<skill>.zip               one archive per skill (the skill folder at the archive root)
#   dist/math-research-skills.zip  the whole pack (README, licences, templates, skills)
set -euo pipefail
cd "$(dirname "$0")"
command -v zip >/dev/null || { echo "zip not found" >&2; exit 1; }
rm -rf dist
mkdir -p dist
EXCLUDES=(-x '*.DS_Store' -x '*__pycache__*' -x '*.pyc')
for dir in skills/*/; do
  name=$(basename "$dir")
  [ -f "skills/$name/SKILL.md" ] || continue
  (cd skills && zip -qr "../dist/$name.zip" "$name" "${EXCLUDES[@]}")
  echo "dist/$name.zip"
done
zip -qr dist/math-research-skills.zip README.md LICENSE.md LICENSES package.sh templates skills "${EXCLUDES[@]}"
echo "dist/math-research-skills.zip"
