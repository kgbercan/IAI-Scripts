from sys import argv
import re
import csv

######## matches #############################
def matches(word):

	print("PART 1")
	###cleaning up
	for i in range(len(word)):
		word[i] = word[i].strip()
		print("i: " + word[i], end=" ")
		word[i] = word[i].split(" ")

		for j in range(len(word[i])):
			print("j: " + word[i][j], end=" ")

		print()

	print("\n\nPART 2")
	###comparing
	#for each labeler on this word
	for i in range(len(word)-1):
		#for each label on the word
		for j in range(len(word[i])):
			#variable to walk through next labelers
			i2 = i
			#while there's another labeler to compare
			while(i2<len(word)-1):
				#increment the labeler index
				i2 += 1
				#for each label on the next labeler's word
				for k in range(len(word[i2])):
					#print("\nJ: " + word[i][j])
					#print("K: " + word[i2][k])
					#compare here
					if(word[i][j]==word[i2][k]):
						print("\n" + word[i][j] + " MATCHES " + word[i2][k] + "\n")



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