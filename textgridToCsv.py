import re

textgrid1 = open("karina_f2bcprlp1.TextGrid")
print(".TextGrid to be read: " + textgrid1.name)

#regexes
itemTier = re.compile("item \[\d\]:")
tierClass = re.compile("class = \"(\w+)Tier\"")
tierName = re.compile("name = \"(\w+)\"")
boundary = re.compile("(intervals|points) \[\d\]:")

currentTierType = ""
currentTierName = ""

#put textgrid in list
lines = textgrid1.readlines()
#line by line
for i in range(len(lines)):
	current = lines[i]
	#if the line declares a new tier
	if(itemTier.search(current)):
		#move to next line
		i+=1
		#the class line
		current = lines[i]
		#set current tier type
		currentTierType = tierClass.search(current).group(1).lower()
		#move to next line
		i+=1
		#the name line
		current = lines[i]
		#set the current tier name
		currentTierName = tierName.search(current).group(1).lower()
	#if intervals or points
	if(boundary.search(current)):
		#move to next line
		#get min
		#move to next line
		#get max
		#move to next line
		#get text



#look for name = "words"
#for each intervals in words
	#next row, col "xmin" = xmin
	#^ row, col "xmax" = xmax
	#^ row, col "text" = text
#look for name = "tones"
#for each points
	#while number > current row.xmax, increment row
	#row, col "tones" = mark
#look for name = "breaks"
#for each points
	#while abs(number - current row.xmax) > abs(number - row++.xmax)
	#increment row
	#row, col "breaks" = mark
#look for name = "misc"
#for each points
	#while number > current row.xmax, increment row
	#row, col "misc" = mark


textgrid1.close()
print(".TextGrid closed: " + str(textgrid1.closed))
labelsCSV =  open("melnicoveLabels.csv","a")
print(".csv opened for: " + labelsCSV.mode)
labelsCSV.close()
print(".csv closed: " + str(labelsCSV.closed))
print("\n\n")