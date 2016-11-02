from sys import argv
import re
import csv

######## agreements #############################
def agreements(row):

	print("PART 1")
	row = cleanUp(row)

	print("\n\nPART 2")
	###comparing
	agreements = 0
	total = 0
	#for each labeler on this word
	for i in range(len(row)-1):
		#for each label on the word
		for j in range(len(row[i])):
			#variable to walk through next labelers
			i2 = i
			#while there's another labeler to compare
			while(i2<len(row)-1):
				#increment the labeler index
				i2 += 1
				#for each label on the next labeler's word
				for k in range(len(row[i2])):
					total += 1
					#print("\nJ: " + row[i][j])
					#print("K: " + row[i2][k])
					if(row[i][j]==row[i2][k]):
						print("\n" + row[i][j] + " agreements " + row[i2][k] + "\n")
						agreements += 1

	agreements = str(agreements) + "/" + str(total)

	print("There are " + agreements + " agreements on this word.")
	print("\nEND OF agreements()\n")
	return(agreements)
######## agreements #############################


######## clean-up ############################
def cleanUp(labels):
	for i in range(len(labels)):
		labels[i] = labels[i].strip()
		print("i: " + labels[i], end=" ")
		labels[i] = labels[i].split(" ")

		for j in range(len(labels[i])):
			print("j: " + labels[i][j], end=" ")

		print()
	return(labels)
######## clean-up ############################


######## main ################################
def main():

	#open file
	with open(argv[1],"r", newline="") as tgCsv:
		reader = csv.reader(tgCsv, delimiter=',')
		table = []

		for row in reader:
			if(reader.line_num==1):
				#subtract 3 from length of spreadsheat because xmin, xmax, and word are not useful
				numColumns = len(row) - 3
				#divide remaning columns by 3 (tones, breaks, misc) to get # of people
				numAnnotators = int(numColumns/3)
				row.append("toneAgreements")
			else:
				#saves the columns for each person's tones
				r = []
				for i in range(3,3+numAnnotators):
					r.append(row[i])
				row.append(agreements(r))
			table.append(row)
			print(row)

		with open(argv[1], "w", newline="") as labelsCSV:
			writer = csv.writer(labelsCSV)
			writer.writerows(table)
######## main ################################

main()