import io
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from PIL import Image, ImageDraw

from yoto_icon_maker.cli import main


class CliTests(unittest.TestCase):
    def make_icon(self, path: Path):
        image = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        draw.rectangle((4, 4, 11, 11), fill=(70, 120, 150, 255))
        image.save(path, "PNG")

    def run_cli(self, *args: str):
        stdout = io.StringIO()
        stderr = io.StringIO()
        code = 0
        with redirect_stdout(stdout), redirect_stderr(stderr):
            try:
                code = main(list(args))
            except SystemExit as exc:
                code = exc.code
        return code, stdout.getvalue(), stderr.getvalue()

    def test_missing_file_reports_argparse_error(self):
        code, stdout, stderr = self.run_cli("verify", "/tmp/yoto-icon-missing.png")

        self.assertEqual(code, 2)
        self.assertEqual(stdout, "")
        self.assertIn("error:", stderr)
        self.assertIn("/tmp/yoto-icon-missing.png", stderr)
        self.assertNotIn("Traceback", stderr)

    def test_invalid_preview_size_is_rejected_before_preview(self):
        with tempfile.TemporaryDirectory() as tmp:
            icon = Path(tmp) / "icon.png"
            preview = Path(tmp) / "preview.png"
            self.make_icon(icon)

            code, stdout, stderr = self.run_cli(
                "verify", str(icon), "--preview", str(preview), "--preview-size", "17"
            )

            self.assertEqual(code, 2)
            self.assertEqual(stdout, "")
            self.assertIn("must be a multiple of 16", stderr)
            self.assertFalse(preview.exists())

    def test_invalid_max_colors_is_rejected(self):
        code, stdout, stderr = self.run_cli("verify", "icon.png", "--max-colors", "0")

        self.assertEqual(code, 2)
        self.assertEqual(stdout, "")
        self.assertIn("must be greater than zero", stderr)


if __name__ == "__main__":
    unittest.main()
