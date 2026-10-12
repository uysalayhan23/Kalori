"""SDK-free javac regression: exit failures and missing class output must block."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("kalori_stub_check",ROOT/"tools/check_android_java_stubs.py")
tool=importlib.util.module_from_spec(spec)
spec.loader.exec_module(tool)

class JavaStubToolTests(unittest.TestCase):
    def test_javac_missing_blocks(self):
        with patch.object(tool.shutil,"which",return_value=None):
            with self.assertRaises(SystemExit) as ctx:tool.main()
        self.assertIn("javac unavailable",str(ctx.exception))

    def test_nonzero_compiler_blocks(self):
        class Result: returncode=1;stderr="deliberate compile failure"
        with patch.object(tool.shutil,"which",return_value="/fake/javac"),patch.object(tool.subprocess,"run",return_value=Result()):
            with self.assertRaises(SystemExit) as ctx:tool.main()
        self.assertEqual(ctx.exception.code,1)

    def test_success_without_class_blocks(self):
        class Result: returncode=0;stderr=""
        with patch.object(tool.shutil,"which",return_value="/fake/javac"),patch.object(tool.subprocess,"run",return_value=Result()):
            with self.assertRaises(SystemExit) as ctx:tool.main()
        self.assertIn("MainActivity.class was not generated",str(ctx.exception))

    def test_real_javac_if_available(self):
        if not tool.shutil.which("javac"):self.skipTest("javac not installed")
        tool.main()

if __name__=="__main__":unittest.main()
