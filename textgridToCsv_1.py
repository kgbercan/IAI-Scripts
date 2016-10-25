from sys import argv
import re
import csv

class TextGrid:
	def __init__(self,name):
		self.name=name
		self.xmin = []
		self.xmax = []
		self.words = []
		self.tones = []
		self.breaks = []
		self.misc = []

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

def main():

	##### arguments #####
	#column names for final spreadsheet
	col = ["xmin","xmax","words"]
	tg = []

	for textFile in argv:
		tg.append(TextGrid(textFile))
		if(len(tg)!=1):
			col.append("")
			col.append("")
			col.append("")
	#####################

	##### regexes #####
	itemTier = re.compile("item \[\d+\]:")
	tierClass = re.compile("class = \"(\w+)Tier\"")
	tierName = re.compile("name = \"(\w+)\"")
	boundary = re.compile("(intervals|points) \[\d+\]:")
	points = re.compile("(xm(in|ax)|number) = (\d+(\.\d+)?)")
	content = re.compile("(text|mark) = \"(.*)\"")
	###################

	##### walk through each .TextGrid #####


	#skip the first one bc that's the script, not a textgrid
	for tgIndex in range(1,len(tg)):

		print("\ntextgrid #" + str(tgIndex) + ": ")
		print(tg[tgIndex].name + "\n")

		currentTierType = ""
		currentTierName = ""

		with open(tg[tgIndex].name) as textgrid1:
			lines = textgrid1.readlines()
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

					if(currentTierType=="interval"):
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

		tg[tgIndex].tones = lineUpTiers(tg[tgIndex].tones,tg[tgIndex].xmax)
		tg[tgIndex].breaks = lineUpTiers(tg[tgIndex].breaks,tg[tgIndex].xmax)
		tg[tgIndex].misc = lineUpTiers(tg[tgIndex].misc,tg[tgIndex].xmax)

		#create column names
		toneIndex = 2 + tgIndex
		breakIndex = toneIndex + len(tg)-1
		miscIndex = breakIndex + len(tg)-1
		col[toneIndex] = tg[tgIndex].name[:3] + "Tones"
		col[breakIndex] = tg[tgIndex].name[:3] + "Breaks"
		col[miscIndex] = tg[tgIndex].name[:3] + "Misc"
	#######################################

	print(col)

	##### create 2-d array to hold textgrid #####
	table = [col]

	#for i in range(len(tg[1].xmin)):
	#	table.append([xmin[i],xmax[i],words[i],tones[i],breaks[i],misc[i]])
	# for i in range(15):
	# 	print(table[i])

	##### write to .CSV #####
	#labelsCSV =  open("melnicoveLabels.csv","a")
	with open("test.csv", "w", newline="") as testCSV:
		print("\n.csv opened for: " + testCSV.mode)
		writer = csv.writer(testCSV)
		writer.writerows(table)
	#########################

main()