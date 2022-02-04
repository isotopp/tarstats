# tarstats - Generate some statistics about a tarfile.

A simple Python commandline application that collects statistics about tarfiles.

## Installation

```console
$ pip3 install .
```

The dot after `install` is important.

## Usage

Get help:

```console
$ tarstats -h
usage: tarstats [-h] [-j] [-t] tarfile [tarfile ...]

Print some stats about tarfiles.

positional arguments:
  tarfile       A tarfile to print stats on.

optional arguments:
  -h, --help    show this help message and exit
  -j, --json    Print the stats as json.
  -t, --totals  Also print a total over all tarfiles.
```

Get stats:

```console
$ tarstats testtar.tgz
type: archive
name: testtar.tgz
size: 112640
filesize: 547
files: 2
dirs: 1
symlinks: 1
hardlinks: 0
devices: 0
```

Get stats in json:

```
$ tarstats -j testtar.tgz
{"type": "archive", "name": "testtar.tgz", "size": 112640, "filesize": 547, "files": 2, "dirs": 1, "symlinks": 1, "hardlinks": 0, "dev": 0}
```

Get stats (in json) for more than one file + totals:

```console
$ tarstats -tj testtar.tgz testtar.tgz
{"type": "archive", "name": "testtar.tgz", "size": 112640, "filesize": 547, "files": 2, "dirs": 1, "symlinks": 1, "hardlinks": 0, "dev": 0}
{"type": "archive", "name": "testtar.tgz", "size": 112640, "filesize": 547, "files": 2, "dirs": 1, "symlinks": 1, "hardlinks": 0, "dev": 0}
{"type": "total", "name": "total", "size": 225280, "filesize": 1094, "files": 4, "dirs": 2, "symlinks": 2, "hardlinks": 0, "dev": 0}
```
