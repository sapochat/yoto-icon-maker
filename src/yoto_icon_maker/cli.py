from __future__ import annotations

import argparse
import json
from .validator import render_preview, validate_icon


def main() -> int:
    parser = argparse.ArgumentParser(prog="yoto-icon")
    sub = parser.add_subparsers(dest="command", required=True)
    verify = sub.add_parser("verify", help="validate a 16x16 icon")
    verify.add_argument("icon")
    verify.add_argument("--preview")
    verify.add_argument("--preview-size", type=int, default=256)
    verify.add_argument("--max-colors", type=int, default=8)
    verify.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report = validate_icon(args.icon, args.max_colors)
    if args.preview:
        render_preview(args.icon, args.preview, args.preview_size)
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
