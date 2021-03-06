from sys import argv
import re
import csv

##### TextGrid Class #####
class TextGrid:

	def __init__(self,name):
		## REGEX for file name
		textGridFileName = re.compile("(([\w\s-]*\/)*)(\w+)?_([\w\s-]+)\.TextGrid")
			#group 1 matches path
			#group 3 matches person's name (or whatever is before an underscore)
			#group 4 matches file name (minus the name and underscore)

		#name is location of .TextGrid
		self.name = name
		#a TextGrid object is created for each argument, which includes the script (the script is argv[0]), so this if statement makes sure we don't try to find a name that isn't there
		if(textGridFileName.search(name)):
			#labeler is name of person who named
			self.labeler = textGridFileName.search(name).group(3)
		self.xmin = []
		self.xmax = []
		self.words = []
		self.tones = []
		self.breaks = []
		self.misc = []
#########################

##### lining up annotations with words #####
def lineUpTiers(tier,xmax):
	linedUp = []
	i = 0
	for t in tier:
		while((float(t[0])-.03)>float(xmax[i]) and i<len(xmax)-1):
			linedUp.append("")
			i+=1
		if(float(t[0])-.03<=float(xmax[i])):
			if(len(linedUp)==i):
				linedUp.append(t[1])
			else:
				linedUp[i]+=" " + t[1]
	while(len(linedUp)<len(xmax)):
		linedUp.append("")
	return(linedUp)
###########################################

def main():

	##### regexes #####
	textGridFileName = re.compile("(([\w\s-]*\/)*)(\w+)?_([\w\s-]+)\.TextGrid")
		#group 1 matches path
		#group 3 matches person's name (or whatever is before an underscore)
		#group 4 matches file name (minus the name and underscore)
	itemTier = re.compile("item \[\d+\]:")
	tierClass = re.compile("class = \"(\w+)Tier\"")
	tierName = re.compile("name = \"(\w+)\"")
	boundary = re.compile("(intervals|points) \[\d+\]:")
	points = re.compile("(xm(in|ax)|number) = (\d+(\.\d+)?)")
	content = re.compile("(text|mark) = \"(.*)\"")
	###################

	##### initializing lists #####
	#column names for final spreadsheet
	table = [["xmin","xmax","words"]]
	#list to access textgrids
	tg = []
	##############################

	##### arguments #####
	for textFile in argv:
		tg.append(TextGrid(textFile))
		#add a column in the table for each tier for each person
		if(len(tg)!=1):
			table[0].append("")
			table[0].append("")
			table[0].append("")
	#####################

	##### walk through each .TextGrid #####
	#skip the first one bc that's the script, not a textgrid
	for tgIndex in range(1,len(tg)):

		print("\ntextgrid #" + str(tgIndex) + ": ")
		print(tg[tgIndex].name + "\n")

		currentTierType = ""
		currentTierName = ""

		with open(tg[tgIndex].name) as textgrid:
			lines = textgrid.readlines()
			#put grid in list, line by line
			for i in range(len(lines)):
				current = lines[i]
				#if the line declares a new tier
				if(itemTier.search(current)):
					#move to next line, the class line
					i+=1
					current = lines[i]
					currentTierType = tierClass.search(current).group(1).lower()

					#move to next line, the name line
					i+=1
					current = lines[i]
					currentTierName = tierName.search(current).group(1).lower()

				#if intervals or points
				if(boundary.search(current)):
					#move to next line
					i+=1
					current = lines[i]
					#get minimum/single point
					pointType = points.search(current).group(1)
					point = points.search(current).group(3)

					#phonemes tier breaks these lines
					if(currentTierType=="interval" and currentTierName!="phones"):
						#store xmin
						(tg[tgIndex].xmin).append(point)

						#move to next line
						i+=1
						current = lines[i]
						#get max
						pointType = points.search(current).group(1)
						point = points.search(current).group(3)

						#store xmax
						tg[tgIndex].xmax.append(point)

					#move to next line
					i+=1
					current = lines[i]
					#get text
					#phonemes tier breaks these lines
					if(currentTierName!="phones"):
						contentType = content.search(current).group(1)
						text = content.search(current).group(2)

					#add word, tone, break or misc to csv
					if(currentTierName=="words"):
						tg[tgIndex].words.append(text)
					elif(currentTierName=="tones"):
						tg[tgIndex].tones.append((point,text))
					elif(currentTierName=="breaks"):
						tg[tgIndex].breaks.append((point,text))
					elif(currentTierName=="misc"):
						tg[tgIndex].misc.append((point,text))

		tg[tgIndex].tones = lineUpTiers(tg[tgIndex].tones,tg[1].xmax)
		tg[tgIndex].breaks = lineUpTiers(tg[tgIndex].breaks,tg[1].xmax)
		tg[tgIndex].misc = lineUpTiers(tg[tgIndex].misc,tg[1].xmax)



		##### putting it into a 2-d list for the csv later #####
		### create column names
		#columns that already exist are xmin, xmax, and words
		#so the base number is 2 and we increment by the number of files there are
		toneIndex = 2 + tgIndex
		breakIndex = toneIndex + len(tg)-1 #remember that the first name in tg is the script file
		miscIndex = breakIndex + len(tg)-1
		table[0][toneIndex] = tg[tgIndex].labeler + "Tones"
		table[0][breakIndex] = tg[tgIndex].labeler + "Breaks"
		table[0][miscIndex] = tg[tgIndex].labeler + "Misc"

		### put in the words and where they happen
		#if its the first textgrid, that's the words, xmins, and xmaxs we will use
		if(tgIndex==1):
			for i in range(len(tg[1].xmin)):
				table.append([])
				for j in range(len(table[0])):
					table[i+1].append("")
					if(j==0):
						print(tg[1].xmin[i])
						table[i+1][j] = tg[1].xmin[i]
					elif(j==1):
						print(tg[1].xmax[i])
						table[i+1][j] = tg[1].xmax[i]
					elif(j==2):
						print(tg[1].words[i])
						table[i+1][j] = tg[1].words[i]

		### fill in each person's annotations
		#for each row
		for i in range(len(tg[1].xmin)):
			#for each column
			for j in range(len(table[i])):
				#if the column is the tone column
				if(j==toneIndex):
					table[i+1][j] = tg[tgIndex].tones[i]
				#if the column is the break column
				elif(j==breakIndex):
					table[i+1][j] = tg[tgIndex].breaks[i]
				#if the column is the misc column
				elif(j==miscIndex):
					table[i+1][j] = tg[tgIndex].misc[i]
		########################################################

	##### write to .CSV #####

	######### IMPORTANT ########
	# THIS NEW FILE NAME FITS THE NAMING CONVENTIONS OF THE SPRING 2017 INTONATION AND EVIDENCE SOUND FILES
	# YOU MAY HAVE TO CHANGE THIS NAME NOT TO CAUSE ERRORS
	# e.g. sara_SC-S2H2-P02-R3-A29.TextGrid becomes SC-S2H2-P02-R3-A29.csv
	# also it maintains the path
	newFileName = textGridFileName.search(argv[1]).group(1) + textGridFileName.search(argv[1]).group(4) + ".csv"
	print(newFileName)
	#########

	with open(newFileName, "w", newline="") as labelsCSV:
		print("\n.csv opened for: " + labelsCSV.mode)
		writer = csv.writer(labelsCSV)
		writer.writerows(table)
	#########################

main()
