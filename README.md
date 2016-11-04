# IAI-Scripts
Code for [Intonation and Evidence CREU Project](http://anita.simmons.edu/~creu/IntonationAndEvidence/index.html)

## tgToCsv_v2.py

### Description
A python program which takes at least one .TextGrid file (created with [Praat](http://www.fon.hum.uva.nl/praat/)) and parses the file(s) into a .CSV, making it easier to compare annotations made by different users.

### Example usage
```
> python3 tgToCsv_v2.py karina_f2bcprlp1.TextGrid emily_f2bcprlp1.TextGrid sara_f2bcprlp1.TextGrid
```

## tgToCsv_v1.py

### Description
An earlier version of the above which puts one .TextGrid file (specified in the code, not via arguments on the command line) into a spreadsheet

### Example usage
```
> python3 tgToCsv_v1.py
```

## tgComp_v2.py

### Description
A python program which takes one .CSV file (for best results, use the output file created with `tgToCsv_v2.py`) and compares each annotator's labels for each word, assigning a point for each matching pair of labels. It creates a new .CSV, named `ordered_[originalCSVname].csv`, with an "agreements" column.

### The point system
The program adds a point for each pair of matching pitch accents and for each pair of matching boundary tones. A point is also added for each pair of an empty label for a pitch accent and each pair of an empty label for a boundary tone, i.e., if there simply is no pitch accent or no boundary tone, that counts as a match or an agreement and the annotators get a point. Thus, the total points possible is twice the number of annotators.

**Example case:** For a given word, A marks `H* L-L%`, B marks `L-L%`, and C marks `L-L%`, accumulating 4 out of 6 points.

- A's pitch accent, in this case: H\*,  matches no one else's (0 points)
- A's boundary tone, in this case: L-L%, matches B's and C's (2 points)
- B's pitch accent, in this case: no label, matches C's (1 point)
- B's boundary tone, in this case: L-L%, matches C's (1 point)

### Example usage
```
> python3 tgToCsv_v2.py karina_f2bcprlp1.TextGrid emily_f2bcprlp1.TextGrid sara_f2bcprlp1.TextGrid
> python3 tgComp_v2.py textgrid.csv
```

## tgComp_v1.py

### Description
A python program which takes one .CSV file (for best results, use the output file created with `tgToCsv_v2.py`) and compares each annotator's labels for each word, assigning a point for each matching pair of labels. It creates a new .CSV, named `ordered_[originalCSVname].csv`, with an "agreements" column.

### The point system
The program adds a point for each pair of matching labels. The point system does not distinguish between pitch accents and boundary tones, and it does not gives points for lack of a label *except for* cases where a pair of annotators includes 0 labels at all.

**Example case:** For a given word, A marks `H* L-L%`, B marks `L-L%`, and C marks `L-L%`, accumulating 3 out of 5 points.

- A's first label, in this case: H\*,  matches no other labels (0 points)
- A's second label, in this case: L-L%, matches a label by B and a label by C (2 points)
- B's first and only label, in this case: L-L%, matches a label by C (1 point)

###Example usage
```
> python3 tgToCsv_v2.py karina_f2bcprlp1.TextGrid emily_f2bcprlp1.TextGrid sara_f2bcprlp1.TextGrid
> python3 tgComp_v1.py textgrid.csv
```
