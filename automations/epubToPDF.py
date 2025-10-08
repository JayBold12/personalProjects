"""
1. turn a epub file into a pdf

IMPROVEMENTS
hard coding the path of the output file -- fixed
title of the output file--fixed
loading for the output to produce--fixed in terminal
one file vs multiple
check file path
location of the output file( default to desktop but optional to other places)
loading for the output to produce"""

import aspose.pdf as ap
import tqdm
import time
from alive_progress import alive_bar
from alive_progress.styles import showtime, Show
import os
import shutil


#1.move the epub file from my downloads to my books folder
source_path = r"path"
source_files = []
for filename in os.listdir(source_path):
    if filename.endswith(".epub"):
        full_path = os.path.join(source_path, filename)
        source_files.append(full_path)

destination_path = r"path"
if not os.path.exists(destination_path):
    os.makedirs(destination_path)

try:
    for file in source_files:
        shutil.move(file, destination_path)
        print(f"File '{file}' moved successfully to '{destination_path}'")
except FileNotFoundError:
    print(f"Error: Source file '{file}' not found.")
except Exception as e:
    print(f"An error occurred: {e}")

#2. convert the epub file to a pdf
#3. delete the epub file
"""
# Create EpubLoadOptions
for x in range(1):
    with alive_bar(x, title="Loading", length=20, bar="bubbles") as bar:
load_options = ap.EpubLoadOptions()


# Load the EPUB document into a Document object
doc_path = input("Paste the path of the epub file here: ")
#document = ap.Document(rf"{doc_path}", load_options)
# Save the output as a PDF file

output_title = ""
index = -1
for i in tqdm.tqdm(range(100)):
    while doc_path[index] != '\\':
        output_title += doc_path[index]
        index -= 1
    time.sleep(0.05)
output_title = output_title[::-1]

    
#document.save(f"{output_title}.pdf")
#print("EPUB converted to PDF successfully.")

"""
