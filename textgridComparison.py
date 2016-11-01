from sys import argv
import re
import csv

######## matches #############################
def matches(word):

	print("PART 1")
	for i in range(len(word)):
		word[i] = word[i].strip()
		print("i: " + word[i], end=" ")
		word[i] = word[i].split(" ")

		for j in range(len(word[i])):
			print("j: " + word[i][j], end=" ")

		print()

	print("\n\nPART 2")
	for i in range(len(word)-1):
		for j in range(len(word[i])-1):
			for k in range(len(word[i+1])):
				if(word[i][j]==word[i+1][k]):
					print("\n" + word[i][j] + " MATCHES " + word[i+1][k] + "\n")

	print("\nEND OF MATCHES()\n")

######## matches #############################

######## main ################################

def main():

	#open file
	with open(argv[1],"r", newline="") as tgCsv:
		reader = csv.reader(tgCsv, delimiter=',')

		for row in reader:
			#subtract 3 from length of spreadshet because xmin, xmax, and word are not useful
			numColumns = len(row) - 3
			#divide remaning columns by 3 (tones, breaks, misc) to get # of people
			numAnnotators = int(numColumns/3)
			#saves the columns for each person's tones
			r = []
			for i in range(3,3+numAnnotators):
				r.append(row[i])
			matches(r)

######## main ################################

main()