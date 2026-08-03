from __future__ import annotations

import argparse
import json
from .validator import render_preview, validate_icon


def positive_int(value: str) -> int:
    try:
        parsed = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be an integer") from exc
    if parsed <= 0:
        raise argparse.ArgumentTypeError("must be greater than zero")
    return parsed


def preview_size(value: str) -> int:
    parsed = positive_int(value)
    if parsed % 16:
        raise argparse.ArgumentTypeError("must be a multiple of 16")
    return parsed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="yoto-icon")
    sub = parser.add_subparsers(dest="command", required=True)
    verify = sub.add_parser("verify", help="validate a 16x16 icon")
    verify.add_argument("icon")
    verify.add_argument("--preview")
    verify.add_argument("--preview-size", type=preview_size, default=256)
    verify.add_argument("--max-colors", type=positive_int, default=8)
    verify.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    try:
        report = validate_icon(args.icon, args.max_colors)
        if args.preview:
            render_preview(args.icon, args.preview, args.preview_size)
    except (FileNotFoundError, OSError, ValueError) as exc:
        parser.error(str(exc))
    if args.json:
        print(json.dumps(report.as_dict(), indent=2))
    else:
        print(f"RESULT: {'PASS' if report.ok else 'FAIL'}")
        print(f"size={report.size[0]}x{report.size[1]} mode={report.mode} opaque_colors={report.opaque_colors}")
        for warning in report.warnings:
            print(f"WARNING: {warning}")
        for error in report.errors:
            print(f"ERROR: {error}")
        if args.preview:
            print(f"preview: {args.preview}")
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
