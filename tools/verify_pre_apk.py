#!/usr/bin/env python3
"""Run the Kalori pre-APK checks locally. Never invokes GitHub Actions or builds an APK."""
from pathlib import Path
import subprocess,sys,json,shutil,argparse

ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description="Local pre-APK checks; never builds APK")
parser.add_argument("--release",action="store_true",help="Block if real packaged catalog is empty")
args=parser.parse_args()
required=["index.html","foods.html","meal-builder.html","profile.html","barcode.html","history.html",
          "food-catalog.js","packaged-foods.js","food-quality.js","manifest.webmanifest","service-worker.js",
          "tools/import_openfoodfacts.py","tools/import_usda.py","tools/audit_packaged.py"]
failures=[]
android_files=[
 "android/settings.gradle.kts", "android/build.gradle.kts",
 "android/app/build.gradle.kts", "android/app/src/main/AndroidManifest.xml",
 "android/app/src/main/java/com/kalori/journal/MainActivity.java"
]
for name in android_files:
    if not (ROOT/name).is_file():failures.append("Missing Android source "+name)
try:
    gradle=(ROOT/"android/app/build.gradle.kts").read_text(encoding="utf-8")
    if "syncKaloriWebAssets" not in gradle or 'assets.srcDir(syncKaloriWebAssets)' not in gradle:
        failures.append("Android HTML assets not wired to Gradle")
except OSError:pass

for path in required:
    if not (ROOT/path).is_file():failures.append("Missing "+path)
try:
    manifest=json.loads((ROOT/"manifest.webmanifest").read_text(encoding="utf-8"))
    if manifest.get("start_url")!="./index.html":failures.append("Unexpected start_url")
except (ValueError,OSError) as exc:failures.append("Manifest invalid: "+str(exc))
pages=["index.html","foods.html","meal-builder.html","profile.html","barcode.html","history.html"]
for name in pages:
    try:
        html=(ROOT/name).read_text(encoding="utf-8")
        if 'href="manifest.webmanifest"' not in html:failures.append(name+" missing PWA manifest")
        if "serviceWorker.register" not in html:failures.append(name+" missing SW registration")
    except OSError:pass
command=[sys.executable,"-m","unittest","discover","-s","tests","-p","test_*.py","-v"]
proc=subprocess.run(command,cwd=ROOT)
if proc.returncode:failures.append("Python unittest failed")
if shutil.which("node"):
    for file in ["food-catalog.js","packaged-foods.js","food-quality.js","service-worker.js","tests/catalog.test.cjs","tests/food-quality.test.cjs","tests/service-worker.test.cjs"]:
        if file.endswith(".test.cjs"):
            cmd=["node",file]
        else:
            cmd=["node","--check",file]
        result=subprocess.run(cmd,cwd=ROOT)
        if result.returncode:failures.append("Node check failed: "+file)
else:
    print("NOT RUN: Node.js JS syntax/catalog tests (Node.js unavailable)")
result=subprocess.run([sys.executable,"tools/audit_packaged.py","--input","packaged-foods.js"]+(["--min-products","1"] if args.release else []),cwd=ROOT)
if result.returncode:failures.append("Packaged-food data audit failed")
if failures:
    print("PRE-APK BLOCKED:",json.dumps(failures,ensure_ascii=False,indent=2))
    sys.exit(1)
print("AVAILABLE PRE-APK CHECKS PASSED; this does not certify data accuracy, browser QA or APK readiness.")
