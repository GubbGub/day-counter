#!/bin/bash
# Builds "Day Counter Plan.app" into dist/ and copies it to /Applications.
set -e
cd "$(dirname "$0")"

source .venv/bin/activate

pyinstaller app.py \
  --name "Day Counter Plan" \
  --windowed \
  --icon assets/AppIcon.icns \
  --add-data "ui:ui" \
  --osx-bundle-identifier com.jaredbridgewater.daycounterplan \
  --noconfirm \
  --clean

rm -rf "/Applications/Day Counter Plan.app"
cp -R "dist/Day Counter Plan.app" /Applications/
echo "Installed to /Applications/Day Counter Plan.app"
