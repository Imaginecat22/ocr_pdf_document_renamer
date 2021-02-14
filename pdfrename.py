#!/usr/bin/env python3
from os import path
import os
import sys
import subprocess


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
import re
from string import punctuation

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


def getdocpictures(doc_filepath, doc_name):
	images = convert_from_path(doc_name)
	imgfilepath = doc_filepath + '/' + 'convertedimages/'	
	if not os.path.exists(imgfilepath):
		os.makedirs(imgfilepath)
	
	for i in range(len(images)):
		images[i].save(imgfilepath + 'page' + str(i) + '.jpg', 'JPEG')	
	return imgfilepath, len(images)

def findext(dr, ext):
	retpath = path.join(dr, "*.{}".format(ext)) 
	print("rp: ", retpath)
	return glob(retpath)

def getkeywords(text):
	result = []
	pos_tag = ['PROPN', 'ADJ', 'NOUN']
	doc = nlp(text)
	#print("noun chunks: \n")
	ctr = 0
	doctitle = ''
	for item in doc.noun_chunks:
		temp = str(item)
		t2 = temp.split()
		if (ctr < 5) and (t2[0] != "510"):
			doctitle += str(item) + " "
			ctr += 1
	print("Doctitle: ", doctitle)	
	#print("sents: \n")
	dcheck = ''
	for item in doc.sents:
		dcheck += str(item) + "\n\n"
	#print("dcheck: \n", dcheck)

	try:
		print("nested try block")
		date = dparser.parse(dcheck) #  , fuzzy=True)
	except:
		print("nested except block")
		dates = datefinder.find_dates(dcheck)	 #text instead of dcheck
		ctr = 0
		for d in dates:
			print("date ", d)
			#this will get the last date
			if ctr < 1:
				date = d
			ctr += 1
	
	#print("fnldate: ", str(date.date()))
	result = doctitle + '[' + str(datedate()) + ']'
	print("result: ", result)
	return result

if watch_path[0] == "~":
	watch_path = watch_path[1:] 
	print("new wp: ", watch_path)
	watch_path = '/home/imagi' + watch_path
files = findext(watch_path, "pdf")

print("File list: ", files)

docname = files[0] #files[pdf] 
imgpath, picnum = getdocpictures(watch_path, docname)
text = ''
for i in range(picnum):  
	picname = 'page' + str(i) + '.jpg'
	text += pytesseract.image_to_string(imgpath + picname) 
	text += '--------------------------------------------\n'
newtitle = getkeywords(text)

