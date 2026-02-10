"""Core API for reading tar archive statistics.

This module contains the reusable, non-CLI functionality of `tarstats`.
Import from here when embedding tarstats behavior in other Python programs.

Typical usage
-------------

Single archive:

    from tarstats.core import tarstat

    stats = tarstat("archive.tgz")
    print(stats.to_dict())

Multiple archives with a computed total:

    from tarstats.core import tarstats

    archives, summary = tarstats(["a.tgz", "b.tgz"])
    for item in archives:
        print(item.to_text(human=False))
    print(summary.to_dict())

Main API
--------

- :func:`tarstat(path) -> Stats`
- :func:`tarstats(paths) -> tuple[list[Stats], Stats]`
- :class:`Stats` (value object with formatting helpers)
- :class:`StatsEncoder` (JSON encoding helper for :class:`Stats`)
"""

from __future__ import annotations

import tarfile
from dataclasses import dataclass
from json import JSONEncoder
from os import stat
from typing import Any


@dataclass
class Stats:
    """Summary counters for a tar archive."""

    name: str
    total: bool = False
    size: int = 0
    filesize: int = 0
    filecounter: int = 0
    dircounter: int = 0
    symlinkcounter: int = 0
    hardlinkcounter: int = 0
    devcounter: int = 0

    def to_dict(self) -> dict[str, str | int]:
        return {
            "type": "total" if self.total else "archive",
            "name": self.name,
            "size": self.size,
            "filesize": self.filesize,
            "files": self.filecounter,
            "dirs": self.dircounter,
            "symlinks": self.symlinkcounter,
            "hardlinks": self.hardlinkcounter,
            "dev": self.devcounter,
        }

    def to_text(self, *, human: bool = False) -> str:
        return (
            f"type: {'total' if self.total else 'archive'}\n"
            f"name: {self.name}\n"
            f"size: {human_rounded_units(self.size, human=human)}\n"
            f"filesize: {human_rounded_units(self.filesize, human=human)}\n"
            f"files: {human_thousand_sep(self.filecounter, human=human)}\n"
            f"dirs: {human_thousand_sep(self.dircounter, human=human)}\n"
            f"symlinks: {human_thousand_sep(self.symlinkcounter, human=human)}\n"
            f"hardlinks: {human_thousand_sep(self.hardlinkcounter, human=human)}\n"
            f"devices: {human_thousand_sep(self.devcounter, human=human)}\n"
        )

    def __add__(self, other: Any) -> Stats:
        if not isinstance(other, Stats):
            raise TypeError("other object must be an instance of Stats")

        self.size += other.size
        self.filesize += other.filesize
        self.filecounter += other.filecounter
        self.dircounter += other.dircounter
        self.symlinkcounter += other.symlinkcounter
        self.hardlinkcounter += other.hardlinkcounter
        self.devcounter += other.devcounter
        return self


class StatsEncoder(JSONEncoder):
    """JSON encoder for Stats objects."""

    def default(self, obj: Any) -> Any:
        if isinstance(obj, Stats):
            return obj.to_dict()
        return super().default(obj)


def human_thousand_sep(number: int, *, human: bool) -> str:
    if not human:
        return str(number)
    return f"{number:,}"


def human_rounded_units(number: int, *, human: bool) -> str:
    if not human:
        return str(number)

    units = "KMGTPEZY"
    if number < 0:
        raise ValueError("negative numbers not supported")

    counter = 0
    while number > 1000:
        number //= 1000
        counter += 1

    if counter >= len(units):
        raise ValueError("maximum supported range exceeded")

    if counter == 0:
        return str(number)
    return f"{number}{units[counter - 1]}"


def tarstat(filename: str) -> Stats:
    with tarfile.open(filename, "r") as archive:
        info = archive.getmembers()

    result = Stats(filename)
    for member in info:
        if member.isfile():
            result.size += member.size
            result.filecounter += 1
        if member.isdir():
            result.dircounter += 1
        if member.issym():
            result.symlinkcounter += 1
        if member.islnk():
            result.hardlinkcounter += 1
        if member.isdev():
            result.devcounter += 1

    result.filesize = stat(filename).st_size
    return result


def tarstats(filenames: list[str]) -> tuple[list[Stats], Stats]:
    archives: list[Stats] = []
    summary = Stats("total", total=True)

    for name in filenames:
        stats = tarstat(name)
        archives.append(stats)
        summary += stats

    return archives, summary
