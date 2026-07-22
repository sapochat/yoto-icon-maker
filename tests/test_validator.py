import tempfile
import unittest
from pathlib import Path
from PIL import Image, ImageDraw

from yoto_icon_maker.validator import render_preview, validate_icon


class ValidatorTests(unittest.TestCase):
    def make_icon(self, path: Path, *, black=False, size=(16, 16), mode="RGBA"):
        image = Image.new(mode, size, (0, 0, 0, 0) if mode == "RGBA" else (255, 0, 255))
        if mode == "RGBA":
            draw = ImageDraw.Draw(image)
            draw.rectangle((3, 6, 12, 10), fill=(70, 120, 150, 255))
            draw.rectangle((7, 3, 8, 6), fill=(180, 190, 200, 255))
            if black:
                draw.point((4, 7), fill=(0, 0, 0, 255))
        image.save(path, "PNG")

    def test_valid_icon_and_preview(self):
        with tempfile.TemporaryDirectory() as tmp:
            icon = Path(tmp) / "icon.png"
            preview = Path(tmp) / "preview.png"
            self.make_icon(icon)
            report = validate_icon(icon)
            self.assertTrue(report.ok, report.errors)
            render_preview(icon, preview)
            with Image.open(preview) as image:
                self.assertEqual(image.size, (256, 256))
                self.assertEqual(image.mode, "RGB")

    def test_rejects_visible_black(self):
        with tempfile.TemporaryDirectory() as tmp:
            icon = Path(tmp) / "black.png"
            self.make_icon(icon, black=True)
            report = validate_icon(icon)
            self.assertFalse(report.ok)
            self.assertEqual(report.pure_black_pixels, 1)

    def test_rejects_wrong_size(self):
        with tempfile.TemporaryDirectory() as tmp:
            icon = Path(tmp) / "large.png"
            self.make_icon(icon, size=(32, 32))
            report = validate_icon(icon)
            self.assertFalse(report.ok)
            self.assertTrue(any("expected 16x16" in e for e in report.errors))


if __name__ == "__main__":
    unittest.main()
