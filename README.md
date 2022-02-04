# tarstats - Generate some statistics about a tarfile.

A simple Python commandline application that collects statistics about tarfiles.

## Installation

$ pip3 install .

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
Name: testtar.tgz
Total: 112640
Files: 1
Dirs: 1
Link: 1
```

Get stats in json:

```
$ tarstats -j testtar.tgz
{"name": "testtar.tgz", "size": 112640, "filecounter": 1, "dircounter": 1, "linkcounter": 1}
```

Get stats (in json) for more than one file + totals:

```console
$ tarstats -j -t testtar.tgz testtar.tgz
{"name": "testtar.tgz", "size": 112640, "filecounter": 1, "dircounter": 1, "linkcounter": 1}
{"name": "testtar.tgz", "size": 112640, "filecounter": 1, "dircounter": 1, "linkcounter": 1}
{"name": "total", "size": 225280, "filecounter": 2, "dircounter": 2, "linkcounter": 2}
```
