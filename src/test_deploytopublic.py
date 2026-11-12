import tempfile
import unittest
from pathlib import Path

from deploytopublic import deploy_to_public


class TestDeployToPublic(unittest.TestCase):
    def test_creates_target_and_copies_nested_static_files(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "static"
            target = root / "public"
            (source / "images").mkdir(parents=True)
            (source / "index.css").write_text("body {}")
            (source / "images" / "logo.txt").write_text("logo")

            deploy_to_public(source, target)

            self.assertEqual((target / "index.css").read_text(), "body {}")
            self.assertEqual((target / "images" / "logo.txt").read_text(), "logo")

    def test_replaces_existing_target_contents(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "static"
            target = root / "public"
            source.mkdir()
            target.mkdir()
            (source / "new.txt").write_text("new")
            (target / "old.txt").write_text("old")

            deploy_to_public(source, target)

            self.assertTrue((target / "new.txt").exists())
            self.assertFalse((target / "old.txt").exists())


if __name__ == "__main__":
    unittest.main()
