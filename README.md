# IAI-Scripts
Code for [Intonation and Evidence CREU Project](http://anita.simmons.edu/~creu/IntonationAndEvidence/index.html)

## tgToCsv.py
A python program which takes at least one .TextGrid file (created with [Praat](http://www.fon.hum.uva.nl/praat/)) and parses the file(s) into a .CSV, making it easier to compare annotations made by different users.

Example usage:
```
> python3 textgridToCsv_1.py karina_f2bcprlp1.TextGrid emily_f2bcprlp1.TextGrid sara_f2bcprlp1.TextGrid
```

## textgridToCsv.py
An earlier version of the above which puts one .TextGrid file (specified in the code, not via arguments on the command line) into a spreadsheet
