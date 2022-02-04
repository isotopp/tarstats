#! /usr/bin/env python3

import tarfile
import click
from json import dumps, JSONEncoder


class StatsEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Stats):
            return {"size": obj.size,
                    "filecounter": obj.filecounter,
                    "dircounter": obj.dircounter,
                    "linkcounter": obj.linkcounter
                    }
        return JSONEncoder.default(self, obj)


class Stats:
    def __init__(self):
        self.filecounter = 0
        self.dircounter = 0
        self.linkcounter = 0
        self.size = 0

    def __str__(self):
        return f"""Total: {self.size}
Files: {self.filecounter}
Dirs: {self.dircounter}
Link: {self.linkcounter}
"""

    def __repr__(self):
        return f"{self.size=} {self.filecounter=} {self.dircounter=} {self.linkcounter}"


@click.command()
@click.argument('filename', type=click.Path(exists=True), nargs=-1)
@click.option('-j', '--json/--no-json', default=False, help="Print the tar stats as JSON.")
def tarstats(filename, json):
    for name in filename:
        with tarfile.open(name, "r") as t:
            info = t.getmembers()

        stats = Stats()
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


if __name__ == "__main__":
    tarstats()
