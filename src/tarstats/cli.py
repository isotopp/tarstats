from __future__ import annotations

import argparse
import sys
from json import dumps

from .core import StatsEncoder, tarstats


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Print some stats about tarfiles.")
    parser.add_argument("-j", "--json", help="Print the stats as json.", action="store_true")
    parser.add_argument(
        "-H",
        "--human",
        help="Print numbers with rounded units or thousand separators.",
        action="store_true",
    )
    parser.add_argument(
        "-t", "--totals", help="Also print a total over all tarfiles.", action="store_true"
    )
    parser.add_argument("tarfile", help="A tarfile to print stats on.", type=str, nargs="+")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.json and args.human:
        print("Options --json and --human are mutually exclusive.", file=sys.stderr)
        return 2

    try:
        archives, summary = tarstats(args.tarfile)
    except FileNotFoundError as exc:
        print(f"Can't read '{exc.filename}': {exc}", file=sys.stderr)
        return 1

    for stats in archives:
        if args.json:
            print(dumps(stats, cls=StatsEncoder))
        else:
            print(stats.to_text(human=args.human))

    if args.totals:
        if args.json:
            print(dumps(summary, cls=StatsEncoder))
        else:
            print(summary.to_text(human=args.human))

    return 0
