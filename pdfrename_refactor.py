#!/usr/bin/env python3

#This script is for running the new PDF class

from os import path
import sys
import subprocess
import importlib

#requires tesseract already be installed. Tesseract is the engine; 
#pytesseract is the wrapper/api that interacts with it
#sudo apt install tesseract-ocr
#possibly also,
#sudo apt install libtesseract-dev

def install(package):
	subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def download(tokenizer):
	subprocess.check_call([sys.executable, "-m", "spacy", "download", tokenizer])


def check_pkg(module, package=None, stop=False):
	try:
		importlib.import_module(module, package)
	except:
		if stop:
			if package is not None:
				print("could not import " + module + " from package " + package)
			else:
				print("could not import " + module + "!")
		else:
			install(module)
			check_pkg(module, package, stop=True)


check_pkg("glob", "glob")
check_pkg("pytesseract")
check_pkg("load", "spacy")
check_pkg("datefinder")
import spacy

try:
	nlp = spacy.load("en_core_web_md")
except:
	download("en_core_web_md")
#check_pkg("en_core_web_md")

from my_class import renamer

#if auto is set to True, it will grab all pdfs in the "scanned_pdfs" folder
#if auto is set to False, it will ask you for a specific pdf in that folder
#if testing is > 0, it will look in the "pdftest" folder instead of "scanned_pdfs" and specifically grab the "benchmark.pdf" file
renamer = renamer.PDF_Renamer(auto=True, testing=1)
renamer.run()