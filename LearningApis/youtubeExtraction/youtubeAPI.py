import tkinter as tk
from tkinter import messagebox
import yt_dlp
import os
from pathlib import Path

# Function to download the video to the user's Desktop folder
def download_video(url):
    try:
        # Get the user's Desktop folder dynamically based on the OS
        desktop_folder = str(Path.home() / "Desktop")  # Works for both Windows, macOS, Linux

        # Define output path for the downloaded video in the Desktop folder
        output_path = os.path.join(desktop_folder, '%(title)s.%(ext)s')  # Save with the title of the video

        ydl_opts = {
            'outtmpl': output_path  # Set the output path to the Desktop folder
        }

        # Download the video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        messagebox.showinfo("Success", f"Video downloaded successfully!\nSaved to: {desktop_folder}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function triggered when the "Download Video" button is clicked
def on_download_button_click():
    url = url_entry.get()
    if not url:
        messagebox.showwarning("Input Error", "Please enter a valid YouTube URL.")
    else:
        download_video(url)

# Set up the main Tkinter window
root = tk.Tk()
root.title("YouTube Video Downloader")
root.geometry("400x200")  # You can adjust the size as needed

# Add a label and input field for the YouTube URL
url_label = tk.Label(root, text="Enter YouTube Video URL:")
url_label.pack(pady=10)

url_entry = tk.Entry(root, width=40)
url_entry.pack(pady=10)

# Add a "Download Video" button
download_button = tk.Button(root, text="Download Video", command=on_download_button_click)
download_button.pack(pady=20)

# Run the main loop of Tkinter
root.mainloop()
