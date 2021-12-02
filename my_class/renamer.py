#!/usr/bin/env python3

import os, sys
from datetime import date
from . import my_pdf
from glob import glob
import shutil

class PDF_Renamer:
	def __init__(self, auto = False, testing = 0):
		self.testing = testing
		self.auto = auto
		self.today = date.today()
		#self.watch_path = input("Please input file path to search: ")
		#print("Source Path Used: >" + self.watch_path)
		self.verbose = self.get_verbose()
		self.os = self.get_os() #0 = lin, 1 = mac, 2 = win
		self.home = self.get_home()
		self.pdfs = self.auto_decider()
	
	def run(self):
		if len(self.pdfs) == 0:
			print("No files found!")
			sys.exit(-1)
		else:
			for file in self.pdfs:
				pdf = my_pdf.PDF(file, self.home, True)
				newtitle = pdf.get_new_title()
				self.renamePDF(self.home, self.pdfs[file], newtitle)

	def renamePDF(self, doc_filepath, doc_name, newtitle):
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

	def get_os(self):
		print(sys.platform)
		if sys.platform == 'darwin':
			this_os = 1
		elif sys.platform == 'win32':
			this_os = 2
		else:
			this_os = 0
		return this_os

	def get_home(self):
		if self.os == 0 or self.os == 1:
			if self.testing:
				pdf_dir = "pdftest/"
			else:
				pdf_dir = "scanned_pdfs/"
			home = os.path.join(os.path.expanduser("~"), "Documents/" + pdf_dir)
		elif self.os == 2:
			home = os.path.join("Users" + os.getenv['username'] + "Documents/Scanned_PDFs/")
		if self.verbose:
			print(home)
		return home

	def get_verbose(self):
		verbose = 0
		vb = input("Verbose? (if you don't understand this, just ignore it): ")
		if len(vb) > 0:
			if vb[0] == "y" or "Y":
				verbose = 1
		return verbose

	def findext(self, dr, ext):
		retpath = os.path.join(dr, "*.{}".format(ext)) 
		if self.verbose:
			print("rp: ", retpath)
		return glob(retpath)
	
	def auto_decider(self):
		pdfs = []
		if not self.auto:
			pdfs.append(self.get_pdf_title())
		else:
			pdfs = self.get_pdfs()
		return pdfs

	def get_pdf_title(self):
		title = input("Please input title of pdf in your Documents directory:\n")
		if self.testing == 1:
			if title == "":
				title = "benchmark.pdf"

		if self.verbose:
			print(title)

		return title

	def get_pdfs(self):
		pdfs = []
		files = self.findext(self.home, "pdf")
		if self.verbose:
			print("File list: ", files)
		for f in range(len(files)):
			docname = files[f] 
			dname = docname.rpartition("/")
			if self.verbose:
				print("third partition	:", dname[2])
			pdfs.append(dname[2])
		return pdfs
