import argparse
from sys import exit, stderr
from typing import Optional

from .tarstats import tarstats

args: Optional[argparse.Namespace] = None


def main():
    global args # bah!

    parser = argparse.ArgumentParser(description="Print some stats about tarfiles.")
    parser.add_argument("-j", "--json", help="Print the stats as json.", action="store_true")
    parser.add_argument("-H", "--human", help="Print numbers with rounded units or thousand separators", action="store_true")
    parser.add_argument("-t", "--totals", help="Also print a total over all tarfiles.", action="store_true")
    parser.add_argument("tarfile", help="A tarfile to print stats on.", type=str, nargs='+')
    args = parser.parse_args()

    if args.json and args.human:
        print("Options --json and --human are mutually exclusive.", file=stderr)
        exit(2)

    tarstats(args.tarfile, args.json, args.totals)


if __name__ == "__main__":
    main()
