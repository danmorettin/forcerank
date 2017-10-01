
## Introduction

This program uses time series data for public securities and force ranks them
according to the distance (in percent) they are above/below their moving
average. The historical rankings are also  calculated. The results are put
into an excel spreadsheet.

This program requires an existing collection of sqlite3 databases containing
the historical data for each ticker.

## Program Set-Up

This application should be installed using setup.py. From inside the main repo,
run the command in the terminal:
```bash
python setup.py develop
```
Note that the filenames are hard-coded in. Update them to your actual
locations for where your databases are located, etc.

## Running Program

This application is designed to be run from the command line from the main repo
directory. The  command line interface can be run from inside the main repo
as 'python bin/cli.py'. Update the inputs in bin/cli.py as desired.

## Testing

Test discovery is done from inside the main repo by running the command
```bash
pytest -v
```
