"""Minimal CLI entry point for Material Evidence Consistency Guard."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from validate_input import validate_input


TOOL_VERSION = "0.1.0"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Initialize a Material Evidence Consistency Guard run and write run metadata."
        )
    )
    parser.add_argument("input_dir", help="Directory containing review input files.")
    parser.add_argument(
        "--out",
        dest="output_dir",
        required=True,
        help="Directory where output artifacts should be written.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Allow writing run metadata into an existing output directory.",
    )
    return parser


def run(input_dir: Path, output_dir: Path, overwrite: bool = False) -> int:
    if not input_dir.is_dir():
        print(f"error: input directory does not exist: {input_dir}", file=sys.stderr)
        return 2

    validation_result = validate_input(input_dir)
    if not validation_result["ok"]:
        for error in validation_result["errors"]:
            print(f"error: {error}", file=sys.stderr)
        return 2

    if output_dir.exists() and not output_dir.is_dir():
        print(f"error: output path is not a directory: {output_dir}", file=sys.stderr)
        return 2

    if output_dir.exists() and not overwrite:
        print(
            f"error: output directory already exists: {output_dir}; use --overwrite to continue",
            file=sys.stderr,
        )
        return 2

    output_dir.mkdir(parents=True, exist_ok=True)

    run_meta = {
        "input_dir": str(input_dir),
        "output_dir": str(output_dir),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": "initialized",
        "tool_version": TOOL_VERSION,
    }

    run_meta_path = output_dir / "run-meta.json"
    run_meta_path.write_text(
        json.dumps(run_meta, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return run(Path(args.input_dir), Path(args.output_dir), overwrite=args.overwrite)


if __name__ == "__main__":
    raise SystemExit(main())
