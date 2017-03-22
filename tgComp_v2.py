from sys import argv
import re
import csv

######## agreements #############################
def agreements(row):
	row = cleanUp(row)

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
				if(row[i][j]==row[i2][j]):
					agreements += 1
				total+=1

	agreements = str(agreements) + "/" + str(total)

	return(agreements)
######## agreements #############################


######## clean-up ############################
def cleanUp(labels):

	for i in range(len(labels)):
		labels[i] = labels[i].strip()
		#-1 means there IS NOT a space and thus this has only one label
		if(labels[i].find(" ")==-1):
			#a boundary tone WOULD have a % mark so -1 means this is NOT a boundary tone
			if(labels[i].find("%")==-1):
				#add a space at the end to hold the place of a boundary tone annotation
				labels[i] = labels[i] + " "
			#if this IS a boundary tone...
			else:
				#add a space at the beginning to hold the place of a pitch accent annotation
				labels[i] = " " + labels[i]
		labels[i] = labels[i].split(" ")

	return(labels)
######## clean-up ############################


######## order columns #######################
def orderColumns():
	with open(argv[1],"r", newline="") as original:
		reader = csv.reader(original, delimiter=',')
		colNames = next(reader)
		orderedNames = []

		for i in range(len(colNames)-1):
			before = colNames[i-1].find("Tones")
			current = colNames[i].find("Breaks")
			if(before != -1 and current != -1):
				agrmtCol = len(colNames)-1
				orderedNames.append(colNames[agrmtCol])
			orderedNames.append(colNames[i])

		with open(argv[1], "w", newline="") as ordered:
			writer = csv.DictWriter(ordered,fieldnames=orderedNames)
			writer.writeheader()
			original.seek(0)
			for row in csv.DictReader(original):
				writer.writerow(row)
######## order columns #######################


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

		## REGEX for file name
		compFileName = re.compile("(([\w\s-]*\/)*)([\w\s-]+\.csv)")
			#group 1 matches path
			#group 3 matches file name
		orderedFileName = compFileName.search(argv[1]).group(1) + "ordered_" + compFileName.search(argv[1]).group(3) + ".csv"
		with open(orderedFileName, "w", newline="") as agreementsCSV:
			writer = csv.writer(agreementsCSV)
			writer.writerows(table)

	orderColumns()
######## main ################################

main()
