from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

from PIL import Image


@dataclass
class ValidationReport:
    path: str
    format: str | None
    size: tuple[int, int]
    mode: str
    opaque_colors: int
    transparent_pixels: int
    pure_black_pixels: int
    opaque_bbox: tuple[int, int, int, int] | None
    errors: list[str]
    warnings: list[str]

    @property
    def ok(self) -> bool:
        return not self.errors

    def as_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["ok"] = self.ok
        return data


def validate_icon(path: str | Path, max_colors: int = 8) -> ValidationReport:
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(path)

    with Image.open(path) as loaded:
        original_format = loaded.format
        original_mode = loaded.mode
        original_size = loaded.size
        image = loaded.convert("RGBA")

    errors: list[str] = []
    warnings: list[str] = []
    if original_format != "PNG":
        errors.append(f"format is {original_format}, expected PNG")
    if original_size != (16, 16):
        errors.append(f"size is {original_size[0]}x{original_size[1]}, expected 16x16")
    if original_mode != "RGBA":
        errors.append(f"mode is {original_mode}, expected RGBA")

    colors = image.getcolors(maxcolors=257)
    if colors is None:
        errors.append("image has more than 256 RGBA colors")
        colors = []

    transparent_pixels = sum(count for count, color in colors if color[3] == 0)
    opaque_entries = [(count, color) for count, color in colors if color[3] > 0]
    opaque_colors = len(opaque_entries)
    pure_black_pixels = sum(count for count, color in opaque_entries if color[:3] == (0, 0, 0))

    if transparent_pixels == 0:
        errors.append("no transparent pixels found")
    if pure_black_pixels:
        errors.append(f"contains {pure_black_pixels} visible pure-black pixel(s)")
    if opaque_colors > max_colors:
        warnings.append(f"uses {opaque_colors} opaque colors; target is <= {max_colors}")

    bbox = image.getchannel("A").getbbox()
    if bbox is None:
        errors.append("image is fully transparent")
    elif bbox[0] == 0 or bbox[1] == 0 or bbox[2] == 16 or bbox[3] == 16:
        warnings.append(f"sprite touches an edge; opaque bounding box is {bbox}")

    return ValidationReport(
        path=str(path), format=original_format, size=original_size, mode=original_mode,
        opaque_colors=opaque_colors, transparent_pixels=transparent_pixels,
        pure_black_pixels=pure_black_pixels, opaque_bbox=bbox,
        errors=errors, warnings=warnings,
    )


def render_preview(path: str | Path, output: str | Path, size: int = 256) -> Path:
    path, output = Path(path), Path(output)
    if size <= 0 or size % 16:
        raise ValueError("preview size must be a positive multiple of 16")
    with Image.open(path) as loaded:
        image = loaded.convert("RGBA")
    black = Image.new("RGBA", (16, 16), (0, 0, 0, 255))
    black.alpha_composite(image)
    output.parent.mkdir(parents=True, exist_ok=True)
    black.resize((size, size), Image.Resampling.NEAREST).convert("RGB").save(output, "PNG", optimize=True)
    return output
