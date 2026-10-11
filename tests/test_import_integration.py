#!/usr/bin/env python3
"""End-to-end OFF import and audit checks using synthetic rows. Never makes network calls."""
import json,subprocess,sys,tempfile,unittest,gzip
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
IMPORT=ROOT/"tools"/"import_openfoodfacts.py"
AUDIT=ROOT/"tools"/"audit_packaged.py"
FIXTURE=ROOT/"tests"/"fixtures"/"off_small.tsv"
PREFIX="globalThis.KaloriPackagedFoods="

class ImportIntegrationTests(unittest.TestCase):
    def test_import_and_audit(self):
        with tempfile.TemporaryDirectory() as tmp:
            output=Path(tmp)/"packaged-foods.js"
            command=[sys.executable,str(IMPORT),"--input",str(FIXTURE),"--output",str(output),"--limit","100"]
            proc=subprocess.run(command,capture_output=True,text=True,check=False)
            self.assertEqual(proc.returncode,0,proc.stderr)
            content=output.read_text(encoding="utf-8")
            self.assertIn(PREFIX,content)
            products=json.loads(content.split(PREFIX,1)[1].strip().removesuffix(";"))
            self.assertEqual(len(products),2)
            self.assertEqual({p["barcode"] for p in products},{"8691234567890","8691234567892"})
            self.assertEqual(next(p for p in products if p["name"]=="Örnek Gofret")["brand"],"Örnek Marka")
            audit=subprocess.run([sys.executable,str(AUDIT),"--input",str(output)],capture_output=True,text=True)
            self.assertEqual(audit.returncode,0,audit.stdout+"\n"+audit.stderr)
    def test_release_gate_rejects_empty_catalog(self):
        with tempfile.TemporaryDirectory() as tmp:
            output=Path(tmp)/"packaged-foods.js"
            output.write_text(PREFIX+"[];",encoding="utf-8")
            proc=subprocess.run([sys.executable,str(AUDIT),"--input",str(output),"--min-products","1"],capture_output=True,text=True)
            self.assertNotEqual(proc.returncode,0)
            self.assertIn("at least 1 required",proc.stdout)
    def test_release_gate_accepts_valid_fixture(self):
        with tempfile.TemporaryDirectory() as tmp:
            output=Path(tmp)/"packaged-foods.js"
            subprocess.run([sys.executable,str(IMPORT),"--input",str(FIXTURE),"--output",str(output)],check=True,capture_output=True)
            proc=subprocess.run([sys.executable,str(AUDIT),"--input",str(output),"--min-products","1"],capture_output=True,text=True)
            self.assertEqual(proc.returncode,0,proc.stdout+proc.stderr)
    def test_gzip_dump_import(self):
        with tempfile.TemporaryDirectory() as tmp:
            source=Path(tmp)/"foods.tsv.gz"
            output=Path(tmp)/"packaged-foods.js"
            with gzip.open(source,"wb") as handle:
                handle.write(FIXTURE.read_bytes())
            proc=subprocess.run([sys.executable,str(IMPORT),"--input",str(source),"--output",str(output)],capture_output=True,text=True)
            self.assertEqual(proc.returncode,0,proc.stderr)
            rows=json.loads(output.read_text(encoding="utf-8").split(PREFIX,1)[1].strip().removesuffix(";"))
            self.assertEqual(len(rows),2)
    def test_size_limit_rejects_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            output=Path(tmp)/"packaged-foods.js"
            proc=subprocess.run([sys.executable,str(IMPORT),"--input",str(FIXTURE),"--output",str(output),"--max-bytes","1024"],capture_output=True,text=True)
            # Either the small fixture fits the limit or the importer refuses it.
            if proc.returncode!=0:
                self.assertFalse(output.exists())
                self.assertIn("size budget",proc.stderr)
            else:
                self.assertLessEqual(output.stat().st_size,1024)

if __name__=="__main__":unittest.main()
