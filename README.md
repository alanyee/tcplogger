TCP Logger
=========================

Unix-like logging for TCP connections

## Usage	
```
usage: log.py [-h] [-f [filename]] [-c cachefile] [-C]

Unix-like TCP Logger

optional arguments:
  -h, --help            show this help message and exit
  -f [filename], --filename [filename]
                        Writes to specified filename
  -c cachefile, --cache cachefile
                        Loads from specified cache
  -C, --clear           Clears cache
```

## Done
* PEP 8
* Dynamic dictionary cache
* Dynamically determines misconfigured UID
* Program to manipulate cache offline
* Unix-like behavior
* Programs are now executable

## WIP
* Make Python 2/3 compatible

## TODOS
* Correctly maps TCP connections to active process
* Replace object-oriented programming with functional
