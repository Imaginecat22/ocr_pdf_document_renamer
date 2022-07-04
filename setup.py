#!/usr/bin/env python3
from setuptools import find_packages, setup

LONG_DESCRIPTION = open("README.md", 'r')

setup(
    name='ocr_pdf_document_renamer',
    version='2.1.0',
    packages=find_packages(),
    license_files=('LICENSE',),
    author='Robert Walters',
    author_email='imaginecat22@gmail.com',
    description="Uses OCR to extract keywords from a pdf and gives it a useful name",
    long_description=LONG_DESCRIPTION,
    install_requires=['wand', 'spacy', 'pytesseract', 'datefinder', 'glob2'],
)

