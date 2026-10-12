#!/usr/bin/env python3
"""Copy reviewed static app assets into Android's offline asset directory.
No Gradle invocation, APK packaging, network requests or GitHub Actions.
"""
from pathlib import Path
import shutil
ROOT=Path(__file__).resolve().parents[1]
TARGET=ROOT/"android"/"app"/"src"/"main"/"assets"
FILES=["index.html","foods.html","meal-builder.html","profile.html","barcode.html","history.html","food-catalog.js","packaged-foods.js","food-quality.js","journal-data.js","manifest.webmanifest","service-worker.js"]
TARGET.mkdir(parents=True,exist_ok=True)
for filename in FILES:
    origin=ROOT/filename
    if not origin.is_file():raise SystemExit("Missing "+filename)
    shutil.copy2(origin,TARGET/filename)
    print("Copied",filename)
print("Asset staging done; APK NOT built.")
