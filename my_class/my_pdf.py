#!/usr/bin/env python3

#import dateparser
import os
from wand.image import Image
import shutil

import pytesseract 
import spacy
import en_core_web_md

import dateutil.parser as dparser
import datetime
from datetime import date
import re
from string import punctuation

import datefinder

class PDF:
	def __init__(self, title, path, verbose = False, testing = 0):
		self.verbose = verbose
		self.testing = testing
		self.home = path
		self.title = title
		self.date = self.get_date()
		self.today = date.today()
		self.pdf_path = os.path.join(self.home, self.title)
		self.img_path = os.path.join(self.pdf_path + 'convertedimages')
		self.words = []
		self.num_pages = self.get_pdf_images()
		self.text = self.get_text()
		self.nlp = en_core_web_md.load()
		self.doc = self.nlp(self.text)

	def get_new_title(self): 
		newtitle = self.get_keywords_for_title()
		for i in range(self.num_pages):  
			os.remove(self.img_path + 'page' + str(i) + '.jpg')
		return newtitle

	def get_date(self):
		if len(self.title) == 21:
			if self.title[:3] == 'IMG_':
			#IMG_yyyymmdd_000#
				date = self.title[4:11]
				if self.verbose:
					print("titledate: ", date)
			else:
				date = ''
		else:
			date = ''

		return date

	
	def get_text(self):
		text = ''
		for i in range(self.num_pages):  
			picname = 'page' + str(i) + '.jpg'
			text += pytesseract.image_to_string(self.img_path + picname, lang = 'eng', config = ' --psm 1') 
			text += '--------------------------------------------\n'
		return text


	def get_pdf_images(self):
		pdf_images = Image(filename=self.home + self.title, resolution=500)
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

	def get_keywords_for_title(self):
		result = []
		pos_tag = ['PROPN', 'ADJ', 'NOUN']

		#I struggle to remember what's going on here....
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

		mydate = self.get_parsed_date()
		
		#print("fnldate: ", str(date.date()))
		result = doctitle + '[' + str(mydate.date()) + ']'
		print("new title: ", result)
		return result

	def get_parsed_date(self):
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
			if self.date != '':
				year = self.date[0:3]
				mon = self.date[4:5]
				day = self.date[6:7]
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
		return mydate