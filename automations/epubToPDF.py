"""
1. turn a epub file into a pdf

IMPROVEMENTS
hard coding the path of the input file
hard coding the path of the output file
title of the output file 
loading for the output
one file vs multiple
check file path"""

import aspose.pdf as ap

# Create EpubLoadOptions
load_options = ap.EpubLoadOptions()

# Load the EPUB document into a Document object
doc_path = input("Paste the path of the epub file here: ")
document = ap.Document(rf"{doc_path}", load_options)
# Save the output as a PDF file
document.save("output.pdf")
print("EPUB converted to PDF successfully.")
