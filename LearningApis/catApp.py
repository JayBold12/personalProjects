import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk
import requests
import io

def display_image_from_url(url):
    # Download the image
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception if download fails

    # Open the image with PIL
    image = Image.open(io.BytesIO(response.content))

    # Resize the image dynamically based on the window size
    new_width = image.width // 2  # Resize based on window size
    new_height = image.height // 2  # Resize based on window size
    image = image.resize((new_width, new_height))

    # Convert the image to Tkinter-compatible format
    photo = ImageTk.PhotoImage(image)

    # If there is an existing image label, update it
    if hasattr(display_image_from_url, "image_label"):
        display_image_from_url.image_label.config(image=photo)
        display_image_from_url.image_label.image = photo  # Keep reference to avoid garbage collection
    else:
        # Create a new label for displaying the image
        label = tk.Label(image_frame, image=photo, bd=0, relief="flat")
        label.image = photo  # Keep reference to avoid garbage collection
        label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        display_image_from_url.image_label = label  # Save reference for later updates

    # Update the scroll region after adding the image
    image_frame.update_idletasks()

def reload_image():
    url = "https://cataas.com/cat"  # Replace with your URL
    display_image_from_url(url)


def get_random_cat_fact():
    url = "https://catfact.ninja/fact"
    response = requests.get(url)
    
    if response.status_code == 200:
        fact = response.json()['fact']
        return fact
    else:
        return "Failed to retrieve cat fact"


def display_cat_fact():
    # Get a random cat fact
    fact = get_random_cat_fact()
    
    # Update the label text with the retrieved cat fact
    cat_fact_label.config(text=f"Random Cat Fact: {fact}")


# Set up Tkinter root window
root = tk.Tk()
root.title("Cat Viewer")
root.geometry("400x700")
root.config(bg="#fafafa")  # Instagram-like light background color

# Modern Font
modern_font = font.nametofont("TkDefaultFont")
modern_font.actual()

# Create a title label
title_label = tk.Label(root, text="Cat Viewer", font=("Arial", 24, "bold"), bg="#fafafa", fg="#262626")
title_label.grid(row=0, column=0, padx=10, pady=20, sticky="nsew")

# Create a frame for image and facts section (Instagram-like centered content)
image_frame = tk.Frame(root, bg="#fafafa")
image_frame.grid(row=1, column=0, padx=10, pady=20, sticky="nsew")

# Configure row and column weights to make the layout responsive and center the image
image_frame.grid_rowconfigure(0, weight=1)  # This row should expand
image_frame.grid_columnconfigure(0, weight=1)  # This column should expand to center the image

# Create a label to display the cat fact
cat_fact_label = tk.Label(root, text="Fetching a random cat fact...", font=("Arial", 12), bg="#fafafa", fg="#262626", wraplength=350)
cat_fact_label.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

# Button to reload a new cat fact
reload_button = tk.Button(root, text="Get New Cat Fact", command=display_cat_fact, relief="flat", bg="#0095f6", fg="white", font=("Arial", 12, "bold"), padx=20, pady=10)
reload_button.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

# Start by displaying the first cat fact and initial image
display_cat_fact()
reload_image()

# Button to reload the image
button = tk.Button(root, text="Reload Image", command=reload_image, relief="flat", bg="#0095f6", fg="white", font=("Arial", 12, "bold"), padx=20, pady=10)
button.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")

# Configure row and column weights to make the layout responsive
root.grid_rowconfigure(0, weight=0)
root.grid_rowconfigure(1, weight=1, minsize=200)  # This row should expand
root.grid_rowconfigure(2, weight=0)
root.grid_rowconfigure(3, weight=0)
root.grid_rowconfigure(4, weight=0)

root.grid_columnconfigure(0, weight=1)  # This column should expand with the window

# Start the Tkinter main loop
root.mainloop()