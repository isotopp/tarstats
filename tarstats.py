#! /usr/bin/env python3

import argparse
import tarfile
from  sys import exit
from json import dumps, JSONEncoder
from typing import Any, List
from os import stat


class StatsEncoder(JSONEncoder):
    """ Helper class for json.dumps(..., cls=StatsEncoder).
        Returns a JSON representation of a Stats object. """
    def default(self, obj: Any) -> Any:
        if isinstance(obj, Stats):
            return {
                "type": "total" if obj.total else "archive",
                "name": obj.name,
                "size": obj.size,
                "filesize": obj.filesize,
                "files": obj.filecounter,
                "dirs": obj.dircounter,
                "symlinks": obj.symlinkcounter,
                "hardlinks": obj.hardlinkcounter,
                "dev": obj.devcounter,
            }
        return JSONEncoder.default(self, obj)


class Stats:
    """ Stats is a value object designed to hold statistics gathered from a tarfile. """
    def __init__(self, name: str, total: bool = False):
        self.total = total
        self.name = name
        self.size = 0
        self.filesize = 0
        self.filecounter = 0
        self.dircounter = 0
        self.symlinkcounter = 0
        self.hardlinkcounter = 0
        self.devcounter = 0

    def __str__(self) -> str:
        """ Return a printable version of the value object, as k/v pairs, one per line.
            The keynames match the JSON representation by StatsJSONEncoder, literally.
            """
        is_total = "total" if self.total else "archive"
        return f"""type: {is_total}
name: {self.name}
size: {self.size}
filesize: {self.filesize}
files: {self.filecounter}
dirs: {self.dircounter}
symlinks: {self.symlinkcounter}
hardlinks: {self.hardlinkcounter}
devices: {self.devcounter}
"""

    def __add__(self, other: Any):
        """ This method allows us to add two `Stats` objects. The summary counters of `self`
            are incremented by the summary counters of `other`.

            Note: self.name is not changed. self.total is not set to True.
            If the self instance is supposed to be a total, you need to make the
            required adjustments manually.
            """
        if not isinstance(other, Stats):
            raise TypeError("other object must be an instance of Stats.")

        self.size += other.size
        self.filesize += other.filesize
        self.filecounter += other.filecounter
        self.dircounter += other.dircounter
        self.symlinkcounter += other.symlinkcounter
        self.hardlinkcounter += other.hardlinkcounter
        self.devcounter =+ other.devcounter
        return self


def tarstat(filename: str) -> Stats:
    """
    Read and parse a tarfile, return summary counters of the content.

    :param filename: The filename of a tar archive that is supposed
                     to be parseable by Python's tarfile module.
    :return: A Stats instance that contains summary counters about the tar archives content.
    """
    with tarfile.open(filename, "r") as t:
        info = t.getmembers()

    # info is now a list of TarfileInfo objects.
    # We go through them to add them up.
    stats = Stats(filename)
    for file in info:
        if file.isfile():
            stats.size += file.size
            stats.filecounter += 1

        if file.isdir():
            stats.dircounter += 1

        if file.issym():
            stats.symlinkcounter += 1

        if file.islnk():
            stats.hardlinkcounter += 1

        if file.isdev():
            stats.devcounter += 1

    st = stat(filename)
    stats.filesize = st.st_size

    return stats


def tarstats(filenames: List[str], json: bool, totals: bool):
    """
    Goes through a list of filenames, and executes tarstat() on each.
    Prints a representation of the Stats object for each archive,
    in json format if the json flag is True.
    Also maintains a summary object if totals is True, and
    prints this at the end, in json, if the json flag is True.

    :param filenames: a List of filenames.
    :param json: if set, the output will be in json format.
    :param totals: if set, a summary object will be printed as well.
    """
    summary = Stats("total", total=True)

    for name in filenames:
        try:
            stats = tarstat(name)
        except FileNotFoundError as e:
            print(f"Can't read '{name}': {e}", file=sys.stderr)
            exit(1)

        # Print intermediate results
        if json:
            print(dumps(stats, cls=StatsEncoder))
        else:
            print(stats)

        if totals:
            summary += stats

    if totals:
        if json:
            print(dumps(summary, cls=StatsEncoder))
        else:
            print(summary)


def main():
    parser = argparse.ArgumentParser(description="Print some stats about tarfiles.")
    parser.add_argument("-j", "--json", help="Print the stats as json.", action="store_true")
    parser.add_argument("-t", "--totals", help="Also print a total over all tarfiles.", action="store_true")
    parser.add_argument("tarfile", help="A tarfile to print stats on.", type=str, nargs='+')
    args = parser.parse_args()
    tarstats(args.tarfile, args.json, args.totals)


if __name__ == "__main__":
    main()
