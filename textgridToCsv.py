import re
import csv


def lineUpTiersWithWords(tier, xmax):
	newList = []
	i = 0
	for markup in tier:
		if((float(markup[0])-.05)<float(xmax[len(newList)])):
			newList.append(markup[1])
		else:
			newList.append("")
	return(newList)

def main():
	textgrid1 = open("karina_f2bcprlp1.TextGrid")
	print(".TextGrid to be read: " + textgrid1.name)
	labelsCSV =  open("melnicoveLabels.csv","a")
	print(".csv opened for: " + labelsCSV.mode)

	#regexes
	itemTier = re.compile("item \[\d+\]:")
	tierClass = re.compile("class = \"(\w+)Tier\"")
	tierName = re.compile("name = \"(\w+)\"")
	boundary = re.compile("(intervals|points) \[\d+\]:")
	points = re.compile("(xm(in|ax)|number) = (\d+(\.\d+)?)")
	content = re.compile("(text|mark) = \"(.*)\"")

	currentTierType = ""
	currentTierName = ""

	xmin = []
	xmax = []
	words = []
	tones = []
	breaks = []
	misc = []

	#put textgrid in list
	lines = textgrid1.readlines()

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
			i=i+1
			current = lines[i]
			#get min/single point
			pointType = points.search(current).group(1)
			point = points.search(current).group(3)
			print(pointType + ": " + point)

			if(currentTierType=="interval"):
				#store xmin
				xmin.append(point)

				#move to next line
				i=i+1
				current = lines[i]
				#get max
				pointType = points.search(current).group(1)
				point = points.search(current).group(3)
				print(pointType + ": " + point)

				#store xmax
				xmax.append(point)
			
			#move to next line
			i=i+1
			current = lines[i]
			#get text
			contentType = content.search(current).group(1)
			text = content.search(current).group(2)
			print(contentType + ": " + text)

			#add word, tone, break or misc to csv
			if(currentTierName=="words"):
				words.append(text)
			elif(currentTierName=="tones"):
				tones.append((point,text))
			elif(currentTierName=="breaks"):
				breaks.append((point,text))
			elif(currentTierName=="misc"):
				misc.append((point,text))

	tones = lineUpTiersWithWords(tones,xmax)
	print(tones)
	breaks = lineUpTiersWithWords(breaks,xmax)
	print(breaks)
	misc = lineUpTiersWithWords(misc,xmax)


	textgrid1.close()
	print(".TextGrid closed: " + str(textgrid1.closed))
	labelsCSV.close()
	print(".csv closed: " + str(labelsCSV.closed))
	print("\n\n")


main()