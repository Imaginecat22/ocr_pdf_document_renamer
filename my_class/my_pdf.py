#!/usr/bin/env python3

#import dateparser
import os
import sys
from wand.image import Image
import shutil
import glob

#not sure if this package name is correct in both cases
import pytesseract 
#import spacy
#import en_core_web_md


import dateutil.parser as dparser
import datetime
from datetime import date
import re
from string import punctuation

#import datefinder

class PDF:
	def __init__(self, verbose = False, testing = 0):
		self.verbose = verbose
		self.testing = testing
		self.os = None
		self.home = self.get_home()
		self.doc = self.get_pdf_title()
		self.num_pages = None
		self.newtitle = get_keywords()
		self.words = []
		self.date = ''
		self.today = date.today()
		self.pdf_path = os.path.join(self.home, self.doc)
		self.img_path = os.path.join(self.pdf_path + 'convertedimages')
		#self.nlp = en_core_web_md.load()
		self.run()

	def run(self):
		"""
		docname = self.doc
		imgpath = self.img_path
		picnum = self.num_pages
		titledatestring = self.date

			newtitle = getkeywords(text, titledatestring)
			renamePDF(watch_path, files[f], picnum, newtitle)
			for i in range(picnum):  
				os.remove(imgpath + 'page' + str(i) + '.jpg')
		"""
		self.num_pages = self.get_pdf_images()
		dname = self.doc.rpartition("/")
		if self.verbose:
			print("third partition	:", dname[2])

	def get_pdf_title(self):
		title = input("Please input title of pdf in your Documents directory:\n")
		if self.testing == 1:
			if title == "":
				title = "benchmark.pdf"

		if self.verbose:
			print(title)

		return title

	def get_home(self):
		print(sys.platform)
		if sys.platform == 'darwin':
			self.os = 1
		elif sys.platform == 'win32':
			self.os = 2
		else:
			self.os = 0
		
		if self.os == 0 or self.os == 1:
			home = os.path.join(os.path.expanduser("~"), "Documents")
		elif self.os == 2:
			home = os.path.join("Users" + os.getenv['username'] + "Documents")
		if self.verbose:
			print(home)
		return home

	def get_date(self, dname):
		if len(dname[2]) == 21:
			title = dname[2]
			if title[:3] == 'IMG_':
			#IMG_yyyymmdd_000#
				self.date = title[4:11]
				if self.verbose:
					print("titledate: ", self.date)
	
	def get_text(self):
		text = ''
		for i in range(self.num_pages):  
			picname = 'page' + str(i) + '.jpg'
			text += pytesseract.image_to_string(self.img_path + picname, lang = 'eng', config = ' --psm 1') 
			text += '--------------------------------------------\n'
		return text


	def get_pdf_images(self):
		pdf_images = Image(self.doc, resolution=500)
		images = pdf_images.convert(".jpg")
		if not os.path.exists(self.img_path):
			os.makedirs(self.img_path)
		
		for i in images.sequence:
			page = pdf_images(image=i)
			page.save(filename=self.img_path + 'page' + str(i) + '.jpg')
		return len(images)

	def get_words(self):
		return ""

	def findext(self, dr, ext):
		retpath = os.path.join(dr, "*.{}".format(ext)) 
		if self.verbose:
			print("rp: ", retpath)
		return glob(retpath)


	def filterfunc(self, strlist, substrlist):
		return [tstr for tstr in strlist if not any(sub in tstr for sub in substrlist)]

	def charfiltfunc(self, tstr):
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
	def myfilter(self, noun_chunks):
		naughtylist = ['APT_318', 'APT#_318', 'APT_#_318', 'APT_#318', 
				'Nashville', 'NASHVILLE', '37209', 
				'400-2173', '(423)400-2173', '4234002173',
				'510_Old_Hickory', 'Old_Hickory_Blvd', 'OLD_HICKORY']
		nounlist = []
		chunkslist = []
		for item in noun_chunks:
			noun = str(item)
			nnoun = self.charfiltfunc(noun)
			if len(nnoun) > 2:
				nounlist.append(nnoun)
		
		chunkslist = self.filterfunc(nounlist, naughtylist)	
		if self.verbose:
			print("chunkslist: ", chunkslist)
		
		
		
		return chunkslist
"""
	def get_date(self, tds):
		#print("sents: \n")
		dcheck = ''
		for item in self.doc.sents:
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
				if self.verbose:
					print("date ", d)
				
				yint = int(d.year)	
				if yint > 2015 and yint <= int(self.today.year):
					bestdates.append(d)
					if self.verbose:
						print("good date: ", d)
					#if d.year > year:
					#	year = d.year
			if dates:
				mydate = bestdates[0]
			else:
				mydate = self.today

			
"""
	def get_keywords(self, text, tds):
		result = []
		pos_tag = ['PROPN', 'ADJ', 'NOUN']

		#I struggle to remember what's going on here....

		self.doc = self.nlp(text)
		#print("noun chunks: \n")
		ctr = 0
		doctitle = ''
		chunks = list(self.doc.noun_chunks)
		chunks = self.myfilter(chunks)
		for item in chunks: #doc.noun_chunks:
			temp = str(item)
			t2 = temp.split()
			if (ctr < 5) and (t2[0] != "510"):
				doctitle += str(item) + "-"
				ctr += 1
		
		#I need to filter out (most) punctuation, and replace spaces with underscores			
		if self.verbose:
			print("Doctitle: ", doctitle)	

		mydate = self.get_date()
		
		#print("fnldate: ", str(date.date()))
		result = doctitle + '[' + str(mydate.date()) + ']'
		print("new title: ", result)
		return result

	def renamePDF(self, doc_filepath, doc_name, numpgs, newtitle):
		newfilepath = doc_filepath + '/' + 'convertedPDFtitles/'	
		if not os.path.exists(newfilepath):
			os.makedirs(newfilepath)
		copypath = doc_name
		if self.verbose:
			print("cpypath: ", copypath)
			print("newfilepath: ", newfilepath)
		shutil.copy(copypath, newfilepath)
		docnameonly = doc_name[doc_name.rindex('/') + 1 : ] 
		if self.verbose:
			print("dname: ", docnameonly)
		renamepath = newfilepath + docnameonly
		if self.verbose:
			print("renamepath: ", renamepath)
		fnltitle = newfilepath + newtitle + '.pdf'
		if self.verbose:
			print("fnltitle: ", fnltitle)
		os.rename(renamepath, fnltitle) 
