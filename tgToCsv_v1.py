import re
import csv

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
	##### regexes #####
	itemTier = re.compile("item \[\d+\]:")
	tierClass = re.compile("class = \"(\w+)Tier\"")
	tierName = re.compile("name = \"(\w+)\"")
	boundary = re.compile("(intervals|points) \[\d+\]:")
	points = re.compile("(xm(in|ax)|number) = (\d+(\.\d+)?)")
	content = re.compile("(text|mark) = \"(.*)\"")
	###################

	##### initializers #####
	currentTierType = ""
	currentTierName = ""

	xmin = []
	xmax = []
	words = []
	tones = []
	breaks = []
	misc = []
	########################

	##### open and read textgrid #####
	textgrid1 = open("emily_f2bcprlp1.TextGrid")
	print(".TextGrid to be read: " + textgrid1.name)

	lines = textgrid1.readlines()
	textgrid1.close()
	print(".TextGrid closed: " + str(textgrid1.closed))
	##################################

	#put textgrid in list
	#line by line
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
				xmin.append(point)

				#move to next line
				i+=1
				current = lines[i]
				#get max
				pointType = points.search(current).group(1)
				point = points.search(current).group(3)

				#store xmax
				xmax.append(point)

			#move to next line
			i+=1
			current = lines[i]
			#get text
			contentType = content.search(current).group(1)
			text = content.search(current).group(2)

			#add word, tone, break or misc to csv
			if(currentTierName=="words"):
				words.append(text)
			elif(currentTierName=="tones"):
				tones.append((point,text))
			elif(currentTierName=="breaks"):
				breaks.append((point,text))
			elif(currentTierName=="misc"):
				misc.append((point,text))

	tones = lineUpTiers(tones,xmax)
	breaks = lineUpTiers(breaks,xmax)
	misc = lineUpTiers(misc,xmax)

	##### create 2-d array to hold textgrid #####
	table = [["xmin","xmax","words","tones","breaks","misc"]]
	for i in range(len(xmin)):
		table.append([xmin[i],xmax[i],words[i],tones[i],breaks[i],misc[i]])
	for i in range(15):
		print(table[i])
	#############################################

	##### write to .CSV #####
	#labelsCSV =  open("melnicoveLabels.csv","a")
	with open("emily.csv", "w", newline="") as testCSV:
		print("\n.csv opened for: " + testCSV.mode)
		writer = csv.writer(testCSV)
		writer.writerows(table)
	#########################

main()
