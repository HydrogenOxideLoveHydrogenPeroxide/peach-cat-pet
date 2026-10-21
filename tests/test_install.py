"""Exercise the installer against real temporary Codex homes."""
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name) / "custom codex home"
        self.target = self.home / "pets" / "peach-cat"

    def run_installer(self, *args, root=ROOT):
        env = {**os.environ, "CODEX_HOME": str(self.home)}
        return subprocess.run(
            [sys.executable, str(root / "install.py"), *args],
            cwd=self.temp.name, env=env, text=True, capture_output=True,
        )

    def test_installs_exact_package_from_another_working_directory(self):
        result = self.run_installer()
        self.assertEqual(result.returncode, 0, result.stderr)
        for name in ("pet.json", "spritesheet.png"):
            self.assertEqual(
                (self.target / name).read_bytes(),
                (ROOT / "pets" / "peach-cat" / name).read_bytes(),
            )

    def test_existing_pet_is_not_overwritten_without_replace(self):
        self.target.mkdir(parents=True)
        (self.target / "keep.txt").write_text("my existing pet")
        result = self.run_installer()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("--replace", result.stderr)
        self.assertEqual((self.target / "keep.txt").read_text(), "my existing pet")
        self.assertFalse((self.target / "spritesheet.png").exists())

    def test_replace_backs_up_existing_pet_outside_pet_catalog(self):
        self.target.mkdir(parents=True)
        (self.target / "keep.txt").write_text("original")
        result = self.run_installer("--codex-home", str(self.home), "--replace")
        self.assertEqual(result.returncode, 0, result.stderr)
        backups = list((self.home / "pet-backups").glob("peach-cat-*"))
        self.assertEqual(len(backups), 1)
        self.assertEqual((backups[0] / "keep.txt").read_text(), "original")
        self.assertTrue((self.target / "pet.json").is_file())
        self.assertFalse((self.target / "keep.txt").exists())

    def test_damaged_download_is_rejected_before_install(self):
        copy = Path(self.temp.name) / "download"
        copy.mkdir()
        shutil.copy2(ROOT / "install.py", copy / "install.py")
        shutil.copy2(ROOT / "SHA256SUMS", copy / "SHA256SUMS")
        shutil.copytree(ROOT / "pets", copy / "pets")
        with (copy / "pets" / "peach-cat" / "spritesheet.png").open("ab") as f:
            f.write(b"damaged")
        result = self.run_installer(root=copy)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("checksum", result.stderr.lower())
        self.assertFalse(self.target.exists())


if __name__ == "__main__":
    unittest.main()
