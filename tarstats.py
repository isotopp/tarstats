#! /usr/bin/env python3

import argparse
import sys
import tarfile
from json import dumps, JSONEncoder


class StatsEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Stats):
            return {"name": obj.name,
                    "size": obj.size,
                    "filecounter": obj.filecounter,
                    "dircounter": obj.dircounter,
                    "linkcounter": obj.linkcounter
                    }
        return JSONEncoder.default(self, obj)


class Stats:
    def __init__(self, name):
        self.name = name
        self.filecounter = 0
        self.dircounter = 0
        self.linkcounter = 0
        self.size = 0

    def __str__(self):
        return f"""Name: {self.name}
Total: {self.size}
Files: {self.filecounter}
Dirs: {self.dircounter}
Link: {self.linkcounter}
"""


def tarstats(filenames, json):
    for name in filenames:
        try:
            with tarfile.open(name, "r") as t:
                info = t.getmembers()
        except FileNotFoundError as e:
            print(f"Can't read '{name}': {e}", file=sys.stderr)
            sys.exit(1)

        stats = Stats(name)
        for file in info:
            if file.isfile():
                stats.size += file.size
                stats.filecounter = + 1

            if file.isdir():
                stats.dircounter += 1

            if file.issym():
                stats.linkcounter += 1

        if json:
            print(dumps(stats, cls=StatsEncoder))
        else:
            print(stats)


def main():
    parser = argparse.ArgumentParser(description="Print some stats about tarfiles.")
    parser.add_argument("-j", "--json", help="Print the stats as json.", action="store_true")
    parser.add_argument("tarfile", help="A tarfile to print stats on.", type=str, nargs='+')
    args = parser.parse_args()
    tarstats(args.tarfile, args.json)


if __name__ == "__main__":
    main()
