import re
import csv

def main():
	##### open textgrid #####
	textgrid1 = open("karina_f2bcprlp1.TextGrid")
	print(".TextGrid to be read: " + textgrid1.name)
	#################

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


	##### read .TextGrid #####

	#put textgrid in list
	lines = textgrid1.readlines()
	textgrid1.close()
	print(".TextGrid closed: " + str(textgrid1.closed))

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
			#get minimum/single point
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

	# print("\n XMIN: ")
	# print(xmin)
	# print("\n XMAX: ")
	# print(xmax)
	# print("\n WORDS: ")
	# print(words)
	print("\n TONES: ")
	print(tones)

	##### create 2-d array to hold textgrid #####
	table = [["xmin","xmax","words"]]
	for i in range(len(xmin)):
		table.append([xmin[i],xmax[i],words[i]])
	for i in range(len(table)):
		print(table[i])
	#############################################

	##### open .CSV #####
	#labelsCSV =  open("melnicoveLabels.csv","a")
	with open("test.csv", "w", newline="") as testCSV:
		print("\n.csv opened for: " + testCSV.mode)
		writer = csv.writer(testCSV)
		writer.writerows(table)
	#####################

	print("\n\n")


main()