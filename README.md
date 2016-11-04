# IAI-Scripts
Code for [Intonation and Evidence CREU Project](http://anita.simmons.edu/~creu/IntonationAndEvidence/index.html)

## tgToCsv_v2.py
A python program which takes at least one .TextGrid file (created with [Praat](http://www.fon.hum.uva.nl/praat/)) and parses the file(s) into a .CSV, making it easier to compare annotations made by different users.

Example usage:
```
> python3 tgToCsv_v2.py karina_f2bcprlp1.TextGrid emily_f2bcprlp1.TextGrid sara_f2bcprlp1.TextGrid
```

## tgToCsv_v1.py
An earlier version of the above which puts one .TextGrid file (specified in the code, not via arguments on the command line) into a spreadsheet

Example usage:
```
> python3 tgToCsv_v1.py
```

## tgComp_v2.py
A python program which takes one .CSV file (for best results, use the output file created with `tgToCsv_v2.py`) and compares each annotator's labels for each word, assigning a point for each matching pair of labels. It creates a new .CSV, named `ordered_[originalCSVname].csv`, with an "agreements" column.

**The point system:** The program adds a points for each pair of matching pitch accents and for each pair of matching boundary tones. A point is also added for each pair of an empty label for a pitch accent and each pair of an empty label for a boundary tone, i.e., if there simply is no pitch accent or no boundary tone, that counts as a match or an agreement and the annotators get a point. Thus, the total points possible is twice the number of annotators.

Example usage:
```
> python3 tgToCsv_v2.py karina_f2bcprlp1.TextGrid emily_f2bcprlp1.TextGrid sara_f2bcprlp1.TextGrid
> python3 tgComp_v2.py melnicoveLabels.csv
```
