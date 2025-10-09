import aspose.pdf as ap
import os
import shutil

def get_downloads_folder():
    #get to the downloads folder on the computer
    home_directory = os.path.expanduser('~')
    downloads_path = os.path.join(home_directory, "Downloads")
    return downloads_path

def main():
    #get to the downloads folder on the computer
    home_directory = os.path.expanduser('~')
    downloads_path = os.path.join(home_directory, "Downloads")
    #look for pub files to convert to a pdf
    epub_paths = []
    for file in os.listdir(downloads_path):
        if file.endswith(".epub"):
            file_path = os.path.join(downloads_path, file)
            epub_paths.append(file_path)
    #find destination folder if it exists on the desktop directory
    desktop_path = os.path.join(home_directory, "Desktop")
    destination_path = os.path.join(desktop_path, "Books Test")
    if not os.path.exists(destination_path):
        os.makedirs(destination_path)
    # try to send epubs to the destination
    try:
        for path in epub_paths:
            shutil.move(path, destination_path)
            print(f"path '{path}' move successfully to '{destination_path}'")
    except FileNotFoundError:
        print(f"Error: Source file '{file}' not found.")
    except Exception as e:
        print(f"An error occured: {e}")
    #convert epub files in the new folder to pdfs
    load_options = ap.EpubLoadOptions()
    for file in os.listdir(destination_path):
        if file.endswith(".epub"):
            full_path = os.path.join(destination_path, file)
            try:
                document = ap.Document(full_path, load_options)
                output_path = os.path.join(destination_path, f"{os.path.splitext(file)[0]}.pdf")
                document.save(output_path)
                print(f"Converted '{file}' to PDF at '{output_path}'")
            except Exception as e:
                print(f"Error converting '{file}': {e}")

    #after conversion delete the old epub files
    files_to_delete = []
    for file in os.listdir(destination_path):
        if file.endswith(".epub"):
            print(f"{file}")
            files_to_delete.append(file)



"""

# Specify the path to the file you want to delete
file_path = "my_file.txt" 

# Check if the file exists before attempting to delete it (optional but recommended)
if os.path.exists(file_path):
    try:
        os.remove(file_path)
        print(f"File '{file_path}' deleted successfully.")
    except PermissionError:
        print(f"Permission denied: Unable to delete '{file_path}'.")
    except Exception as e:
        print(f"An error occurred while deleting '{file_path}': {e}")
else:
    print(f"File '{file_path}' not found.")
"""


if __name__ == "__main__":
    main()
