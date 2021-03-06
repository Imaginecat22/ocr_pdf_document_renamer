#!/usr/bin/env python3

#TODO
#1. setup on TVPC and test there
from os import path
import os
import sys
import subprocess
import shutil
import re

#requires tesseract already be installed. Tesseract is the engine; 
#pytesseract is the wrapper/api that interacts with it
#sudo apt install tesseract-ocr
#possibly also,
#sudo apt install libtesseract-dev

def install(package):
	subprocess.check_call([sys.executable, "-m", "pip", "install", package])


try:
	from glob import glob
except:
	install("glob")
	try:
		from glob import glob
	except:
		print("could not import glob!")

try:
	from pdf2image import convert_from_path
except:
	install("pdf2image")
	try:
		from pdf2image import convert_from_path
	except:
		print("could not import pdf2image!")

try:
	from PIL import Image
except:
	install("python_pillow")
	try:
		from PIL import Image
	except:
		print("could not import pillow!")


#not sure if this package name is correct in both cases
try:
	import pytesseract 
except:
	install("pytesseract")
	try:
		import pytesseract 
	except:
		print("could not import pytesseract!")


try:
	import spacy
except:
	install("spacy")
	try:
		import spacy
	except:
		print("could not import spacy!")

try:
	import en_core_web_md
except:
	subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_md"])
	try:
		import en_core_web_md
	except:
		print("could not download medium spacy core")

nlp = en_core_web_md.load()

import dateutil.parser as dparser
import datetime
from datetime import date
import re
from string import punctuation

today = date.today()


try:
	import datefinder
except:
	install("datefinder")
	try:
		import datefinder
	except:
		print("could not import datefinder!")

#0 --------- verify file path
watch_path = input("Please input file path to search: ")
print("Source Path Used: >" + watch_path)
#print("Destination Path Used: >" + file_path)

verbose = 0
vb = input("Verbose? (if you don't understand this, just ignore it): ")
if len(vb) > 0:
	if vb[0] == "y" or "Y":
		verbose = 1

def getdocpictures(doc_filepath, doc_name):
	images = convert_from_path(doc_name, 500)
	imgfilepath = doc_filepath + '/' + 'convertedimages/'	
	if not os.path.exists(imgfilepath):
		os.makedirs(imgfilepath)
	
	for i in range(len(images)):
		images[i].save(imgfilepath + 'page' + str(i) + '.jpg', 'JPEG')	
	return imgfilepath, len(images)

def findext(dr, ext):
	retpath = path.join(dr, "*.{}".format(ext)) 
	if verbose:
		print("rp: ", retpath)
	return glob(retpath)


def filterfunc(strlist, substrlist):
	return [tstr for tstr in strlist if not any(sub in tstr for sub in substrlist)]

def charfiltfunc(tstr):
	if len(tstr) > 0:
		if tstr.find('|') != -1:
			tstr = tstr.replace('|', '', 100)
		
		if tstr.find('\n') != -1:
			tstr = tstr.replace('\n', '', 100)
		
		if tstr.find('\x0c') != -1:
			tstr = tstr.replace('\x0c', '', 100)

		if tstr.find('\\') != -1:
			tstr = tstr.replace('\\', '', 100)

		if tstr.find('.') != -1:
			tstr = tstr.replace('.', '', 100)

		if tstr.find('>') != -1:
			tstr = tstr.replace('>', '', 100)

		if tstr.find('<') != -1:
			tstr = tstr.replace('<', '', 100)

		if tstr.find('+') != -1:
			tstr = tstr.replace('+', '', 100)

		if tstr.find('=') != -1:
			tstr = tstr.replace('=', '', 100)
	
		if tstr.find(' ') != -1:
			tstr = tstr.replace(' ', '_', 100)
	
	return tstr
		

#this doesn't appear to be working/doing anything...
def myfilter(noun_chunks):
	naughtylist = ['APT_318', 'APT#_318', 'APT_#_318', 'APT_#318', 
			'Nashville', 'NASHVILLE', '37209', 
			'400-2173', '(423)400-2173', '4234002173',
			'510_Old_Hickory', 'Old_Hickory_Blvd', 'OLD_HICKORY']
	nounlist = []
	chunkslist = []
	for item in noun_chunks:
		noun = str(item)
		nnoun = charfiltfunc(noun)
		if len(nnoun) > 2:
			nounlist.append(nnoun)
	
	chunkslist = filterfunc(nounlist, naughtylist)	
	if verbose:
		print("chunkslist: ", chunkslist)
	
	
	
	return chunkslist
		

def getkeywords(text, tds):
	result = []
	pos_tag = ['PROPN', 'ADJ', 'NOUN']
	doc = nlp(text)
	#print("noun chunks: \n")
	ctr = 0
	doctitle = ''
	chunks = list(doc.noun_chunks)
	chunks = myfilter(chunks)
	for item in chunks: #doc.noun_chunks:
		temp = str(item)
		t2 = temp.split()
		if (ctr < 5) and (t2[0] != "510"):
			doctitle += str(item) + "-"
			ctr += 1
	
	#I need to filter out (most) punctuation, and replace spaces with underscores			
	if verbose:
		print("Doctitle: ", doctitle)	
	#print("sents: \n")
	dcheck = ''
	for item in doc.sents:
		dcheck += str(item) + "\n\n"
	#print("dcheck: \n", dcheck)

	try:
		mydate = dparser.parse(dcheck) #  , fuzzy=True)
	except:
		dates = datefinder.find_dates(dcheck)	 #text instead of dcheck
		bestdates = []
		if tds != '':
			year = tds[0:3]
			mon = tds[4:5]
			day = tds[6:7]
			tempdate = datetime.datetime(int(year), int(mon), int(day))
			bestdates.append(tempdate)
		ctr = 0
		year = 0
		for d in dates:
			#if verbose:
			#	print("date ", d)
			
			yint = int(d.year)	
			if yint > 2015 and yint <= int(today.year):
				bestdates.append(d)
				if verbose:
					print("good date: ", d)
				#if d.year > year:
				#	year = d.year
		if dates:
			mydate = bestdates[0]
		else:
			mydate = today
	
	#print("fnldate: ", str(date.date()))
	result = doctitle + '[' + str(mydate.date()) + ']'
	print("new title: ", result)
	return result

def renamePDF(doc_filepath, doc_name, numpgs, newtitle):
	newfilepath = doc_filepath + '/' + 'convertedPDFtitles/'	
	if not os.path.exists(newfilepath):
		os.makedirs(newfilepath)
	copypath = doc_name
	#if verbose:
	print("cpypath: ", copypath)
	print("newfilepath: ", newfilepath)
	shutil.copy(copypath, newfilepath)
	docnameonly = doc_name[doc_name.rindex('/') + 1 : ] 
	if verbose:
		print("dname: ", docnameonly)
	renamepath = newfilepath + docnameonly
	#if verbose:
	print("renamepath: ", renamepath)
	fnltitle = newfilepath + newtitle + '.pdf'
	#if verbose:
	print("fnltitle: ", fnltitle)
	os.rename(renamepath, fnltitle) 
	

if watch_path[0] == "~":
	watch_path = watch_path[1:] 
	if verbose:
		print("new wp: ", watch_path)
	watch_path = '/home/imagi' + watch_path
files = findext(watch_path, "pdf")

if verbose:
	print("File list: ", files)

docname = ''
try:
	docname = files[0] #files[pdf] 
except:
	print("No files found!")
	sys.exit(-1)

for f in range(len(files)):
	docname = files[f] 
	imgpath, picnum = getdocpictures(watch_path, docname)
	dname = docname.rpartition("/")
	titledatestring = ''
	if verbose:
		print("third partition	:", dname[2])
	if len(dname[2]) == 21:
		title = dname[2]
		if title[:3] == 'IMG_':
		#IMG_yyyymmdd_000#
			titledatestring = title[4:11]
			if verbose:
				print("titledate: ", titledatestring)
	text = ''
	for i in range(picnum):  
		picname = 'page' + str(i) + '.jpg'
		text += pytesseract.image_to_string(imgpath + picname, lang = 'eng', config = ' --psm 1') 
		text += '--------------------------------------------\n'
	newtitle = getkeywords(text, titledatestring)
	renamePDF(watch_path, files[f], picnum, newtitle)
	for i in range(picnum):  
		os.remove(imgpath + 'page' + str(i) + '.jpg')

