"""
1. turn a epub file into a pdf

hard coding the path of the input file
hard coding the path of the output file
title of the output file 
loading for the output
one file vs multiple"""

import aspose.pdf as ap

# Create EpubLoadOptions
load_options = ap.EpubLoadOptions()

# Load the EPUB document into a Document object
document = ap.Document(r"path to epub file here", load_options)

# Save the output as a PDF file
document.save("output.pdf")
print("EPUB converted to PDF successfully.")
