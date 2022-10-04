#version7 07/31/2018 add not covered in agenda section, complete the format of the output
#version6 07/25/2018 add the special keywords: isoc, irtf, plenaries, and hallway
#version5 07/24/2018 fix the bugs that the code will add addtional people(e.g. the code will add people who attend avtcore to the core list) 
#					 because the code use find function to find who has the core in their working groups, avtcore has the substring'core'
#version4 06/25/2018 the length of wg must longer or equal to three 
#Version3 05/14/2018 ignore the wrong number in front of the attendees 
#Version2 05/11/2018 access via url
#Version1 05/11/2018
#######################
##Author Xinrui Zhang##
#######################

import string
import io
import re
import urllib.request
#====Instructions====
#Enter two file names including .txt without' '
#First file is the plaintext from IETF Meeting Agenda 
#Second file is the html from IETF Attendees website from wiki ericsson 
#******This tool only works when the both file are "correct"*******
# The pattern of first file from trackdata IETF website should be same as agenda101,100...

#====Manually change=====
#Working groups which needs to be changed manully in the attendees page
#NetSlices == NFVRG
#OpsArea == opsawg
#Anwr == ANRW: TLS
#Din == DINRG



print('\n')

#fileName = 'https://wiki.lmera.ericsson.se/wiki/IETF_102_Attendees'	
fileName = input('Please input the corresponding attendance sheet.html:\n')########################URL for wiki page#############################
print('\n')

with urllib.request.urlopen(fileName) as response:
    text = response.read().decode('utf-8')

#get rid of the first part 
abd,second = text.split('</span></h2>')

content,abd = second.split('<div class="printfooter">')
#content,abd = second.split('</li></ul>\n')
def find_between(a, first, last):
	try:	
		start = a.index(first)+len(first)
		end = a.index( last, start)
		return a[start:end]
	except ValueError:
		return ""

frag =list()
frag = content.split('<p>')
#print(frag)

num = 0
names = list()#===================names============================#
rest = list()

for x in frag:

	para = x.find('.')
	
	if para != -1 :
		keep,throw=x.split('\n</p>')
		# number,name = keep.split(keep[para para+1])	
		names.append(keep[para+2 :])
		#after we get names other info is in the rest
		
		rest.append(throw)
		num = num + 1
	
	
wgs = list()#======================wgs==============================#
for y in rest:
	wg = find_between(y,'WGs:','</li>\n')
	#wgs stores all the wg that attendees want to attend
	wgs.append(wg)
#print(wgs)	

#Create initials
initials = list()#===================initials========================#

#here name could be three words but the initial would be two letters
for name in names:
	initial1 = name[0]
	para1 = name.find(' ')
	
	if( para1==-1):
		initials.append(initial1.lower())
	else:	
		initial2 = name[para1+1]	
		initials.append(initial1.lower()+initial2.lower())
		
#Handle the same-initial name	
for i in range(0, len(initials)):
	checkSame = initials[i]
	numberSame = 0	
	for countIni in range(i+1, len(initials)):
		if checkSame == initials[countIni]:
			numberSame += 1
			initials[countIni] +=str(numberSame) 
		

#make everyone a package
ppl = list()
for j in range(0, len(initials)):
		p = initials[j].lower() +' - '+ names[j].lower() + ' {'+wgs[j].lower()+' }'
		ppl.append(p) 
		
		
 
#=====from getWg&Bof=======#
#link = 'https://datatracker.ietf.org/meeting/102/agenda.txt'
link =  input('Please input the agenda .txt link name: ')    ########################URL for agenda page#############################

with urllib.request.urlopen(link) as response:
    ffile = response.read().decode('utf-8')
a,f = ffile.split('Welcome Reception')

# read line by line
lines = f.split('\n')
copi = lines

wgBof = list()
others = list()
for l in lines:
	para1 = l.find('BOF')
	para2 = l.find('WG')
	if para1 != -1 or para2 !=-1:
		wgBof.append(l)
	else:
		others.append(l)		

otherM = list()	
otherGroup = list()	
for o in others:	
	ofind = re.split('\s+',o)
	for ot in ofind:
		if ot.isupper():
			otherM.append(o)
			break
			
for r in otherM:
	gfind = re.split('\s+',r)
	if any(gg.isupper() for gg in gfind) and not gfind[0].isupper() and not gfind[0].islower() and gfind[0].isalpha():	
		for gg in gfind:
			if gg.islower():
				otherGroup.append(gg)
				break
			

bofData = list()
wgData = list()
	
for e in wgBof:
	para1 = e.find('BOF')
	para2 = e.find('WG')
	
	if para1!= -1:
		fin = re.split('\s+',e)
		for f in fin:
			if f.islower() and len(f)>=3:
				bofData.append(f)				
				break
		
	elif para2 != -1:
		fin = re.split('\s+',e)
		for f in fin:
			if f.islower() and len(f)>=3:
				wgData.append(f)
				break

bofData	= list(set(bofData))
########################print(bofData)
wgData = list(set(wgData))
otherGroup = list(set(otherGroup))	
 
for eg in otherGroup:
	wgData.append(eg)
#========The end of getWg&Bof========#

		
#add the special keywords: isoc, irtf, plenaries, anrw and hallway
wgData.append('isoc')
wgData.append('irtf')
wgData.append('plenaries')
wgData.append('anrw: tls')
wgData.append('hallway')


wgData.sort()
bofData.sort()
##########################print(wgData)
wgLoCase=list()



for it in wgs:
	wgLoCase.append(it.lower())
#wgLoCase stores all the wg that attendees want to attend



wgNotCover = list()
wgCover = list()
pplwg = list()

		
			
#print stuff#===================printing==============================#
print('\nThis page is generated from the '+fileName+', please do not edit!')
print('\n==Attendees==\n')

ppl.sort()

for test in ppl:
	 print('* '+ test)
print('Total #of ppl:'+str(num) )	 

print('\n==Working Groups==')	

for k in range(0,len(wgData)):
	findOne = wgData[k]
	if not (any(findOne in aa for aa in wgLoCase)):
		wgNotCover.append(findOne)
	else:	
		wgCover.append(findOne)
		print('\n* '+ findOne+ ': ', end="")
		for g in range(0,len(wgLoCase)):
			paraN1 = wgLoCase[g].find('('+findOne)
			paraN2 = wgLoCase[g].find(findOne+')')
			paraN3 = wgLoCase[g].find('('+findOne+')')
		
			if (paraN1 != -1 and not (wgLoCase[g][paraN1+len(findOne)]).isalpha()) or (paraN2 != -1 and not (wgLoCase[g][paraN2-1]).isalpha())or paraN3 != -1: 
				print('('+initials[g]+') ', end="")
				wgLoCase[g]= wgLoCase[g].replace(findOne,"")
			else:
				para2 = wgLoCase[g].find(findOne)
				if  para2 != -1: 	#=========new edit====fix the bug of using find function====================================#
					if (para2-1)>= 0 and para2+len(findOne)<len(wgLoCase[g]):
						if not((wgLoCase[g][para2-1]).isalpha()) and not((wgLoCase[g][para2+len(findOne)]).isalpha()):
							pplwg.append(initials[g])
							print(initials[g]+' ', end="")
							wgLoCase[g]= wgLoCase[g].replace(findOne,"")
					elif (para2-1)>= 0:
						if not((wgLoCase[g][para2-1]).isalpha()):
							pplwg.append(initials[g])
							print(initials[g]+' ', end="")
							wgLoCase[g]= wgLoCase[g].replace(findOne,"")
					elif para2+len(findOne)<len(wgLoCase):
						if not((wgLoCase[g][para2+len(findOne)]).isalpha()):
							pplwg.append(initials[g])
							print(initials[g]+' ', end="")
							wgLoCase[g]= wgLoCase[g].replace(findOne,"")
					else:
						pplwg.append(initials[g])
						print(initials[g]+' ', end="")
						wgLoCase[g]= wgLoCase[g].replace(findOne,"")
						
					

print('\n')
print('==Working Groups Not Covered==\n')

for wgn in wgNotCover:
	print (wgn, end=" ")

print('\n')
print('==BoF==')

bofCover = list()
bofNotCover = list()
pplbof = list()


for k in range(0,len(bofData)):
	findOne = bofData[k]
	if not (any(findOne in aa for aa in wgLoCase)): #wgLoCase contains working groups and bofs
		bofNotCover.append(findOne)
	else:	
		#wgCover.append(findOne)
		print('\n* '+ findOne+ ': ', end="")
		for g in range(0,len(wgLoCase)):
			paraN1 = wgLoCase[g].find('('+findOne)
			paraN2 = wgLoCase[g].find(findOne+')')
			paraN3 = wgLoCase[g].find('('+findOne+')')
			
			#here it assumes that the bof names are independent of each other 
			#(e.g. names that have same part dont exist)
			#like core and avtcore
			#othewize, it needs to be changed like the working group part 
			if paraN1 != -1 or paraN2 != -1 or paraN3 != -1:
				print('('+initials[g]+') ', end="")
				wgLoCase[g]= wgLoCase[g].replace(findOne,"")
			else:
				para2 = wgLoCase[g].find(findOne)
				if para2 != -1:
					pplbof.append(initials[g])
					print(initials[g]+' ', end="")
					wgLoCase[g]= wgLoCase[g].replace(findOne,"")
		
	
print('\n')
print('==BoFs Not Covered==\n')					
					
for bof in bofNotCover:
	print (bof, end=" ")

	
#add the part to print out the stuff that is not in the agenda

import json
def listToStringWithoutBrackets(tttt):
	return json.dumps(tttt).replace('(','').replace(')','')

print('\n')	
print('==Not Covered in Agenda==')

#get rid of parentheses
wgLoCase = json.loads(listToStringWithoutBrackets(wgLoCase))

for g in range(0,len(wgLoCase)):
	if any(char.isalpha() for char in wgLoCase[g]):
		print('\n* '+initials[g]+":", end="")
		flag = False
		for char in wgLoCase[g]:
			if char.isalpha():
				flag= True
				print(char, end="")
			elif (char in string.punctuation or char in string.whitespace)and flag==True:
				flag = False
				print(char, end="")

print('\n')
print('\n[[gp_source|Information on tools used to extract coverage information from the attendees list]]\n')


