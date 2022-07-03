# OCR PDF Renamer
Uses OCR to extract keywords from a pdf and gives it a useful name

# Installation
To install this package, simply run `python3 -m pip install ocr_pdf_renamer`.

## Wand ImageMagick security policy error (Ubuntu)
If you see an error that looks like:

    wand.exceptions.PolicyError: attempt to perform an operation not allowed by the security policy `PDF' @ error/constitute.c/IsCoderAuthorized/421

Then see this [stackoverflow](https://stackoverflow.com/questions/52998331/imagemagick-security-policy-pdf-blocking-conversion) article for guidance.

The short version to the fix is as follows:
Remove this whole following section from /etc/ImageMagick-6/policy.xml:

    <!-- disable ghostscript format types -->
    <policy domain="coder" rights="none" pattern="PS" />
    <policy domain="coder" rights="none" pattern="PS2" />
    <policy domain="coder" rights="none" pattern="PS3" />
    <policy domain="coder" rights="none" pattern="EPS" />
    <policy domain="coder" rights="none" pattern="PDF" />
    <policy domain="coder" rights="none" pattern="XPS" />

Hopefully this helps.

# Documentation
## How to Use
First, configure the main file `pdfrename_refactor.py` with:
* auto True/False
* testing 0 or 1 (should be true/false, huh?)

Auto will determine if it will get all the files in the directory automatically, or if you manually want to tell it which files to select.

Testing will determine if I use just one of the files in my test directory or not.

Finally, run that file and it should ask you to put in the info it needs.

# Classes
1. my_pdf.py
2. renamer.py


# TODO
1. create a new develop branch for updates
2. add a keywords file instead of hard-coding in a naughty-list
3. add a categories file which will create a folder for those categories, and filter documents with keywords for each category

# Dependencies:
- tesseract (pytesseract)
- wand
- spacy
- glob
- datefinder
