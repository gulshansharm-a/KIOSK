import tkinter as tk
from tkinter import Listbox
from PIL import Image, ImageTk
import csv

# Global variables
symptoms = []
search_entry = None
suggestion_listbox = None
root = None 
W = 864
H = 559
def load_symptoms_from_csv(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            symptoms.extend(row)
entered_symptoms = []
labels_row = 0
labels_col = 0

def add_symptom():
    global search_entry, labels_row, labels_col

    symptom = search_entry.get()
    if symptom and symptom not in entered_symptoms:
        entered_symptoms.append(symptom)

        # Load the label background image and resize
        label_bg_img_path = 'redtB.png'  # Replace with your image path
        original_label_bg_image = Image.open(label_bg_img_path)
        resized_label_bg_image = original_label_bg_image.resize((100, 30))  # You can adjust the size here
        label_bg_image = ImageTk.PhotoImage(resized_label_bg_image)
        
        # Create a label to display the symptom
        symptom_label = tk.Label(root, text=symptom, image=label_bg_image, font=('Arial', 8), anchor='w')
        symptom_label.image = label_bg_image  # Keep a reference to prevent GC
        
        # Calculate placement
        x = 30 + (labels_col * (label_bg_image.width() + 10))  # 10 pixels spacing
        y = H/2 + 20 + (labels_row * (label_bg_image.height() + 10))
        
        symptom_label.place(x=x, y=y)
        
        # Update placement for next label
        labels_col += 1
        if labels_col > 2:  # Start a new row after 3 labels
            labels_col = 0
            labels_row += 1

def suggest_symptoms(event=None):
    global search_entry, suggestion_listbox

    input_text = search_entry.get()

    if suggestion_listbox:
        suggestion_listbox.destroy()

    if not input_text:
        return

    matching_symptoms = [s for s in symptoms if input_text.lower() in s.lower()]

    if not matching_symptoms:
        return

    suggestion_listbox = Listbox(root, bg="white")
    suggestion_listbox.place(x=30, y=H/2 + 30, width=350)  # Adjusted width to align with search frame
    for symptom in matching_symptoms:
        suggestion_listbox.insert(tk.END, symptom)
    suggestion_listbox.bind("<ButtonRelease-1>", fill_search_with_suggestion)

def fill_search_with_suggestion(event):
    global search_entry, suggestion_listbox
    index = suggestion_listbox.curselection()[0]
    selected_symptom = suggestion_listbox.get(index)
    search_entry.delete(0, tk.END)
    search_entry.insert(0, selected_symptom)
    suggestion_listbox.destroy()

def display_message():
    print("Button clicked!")

def search_action():
    query = search_entry.get()
    print(f"Searching for: {query}")
    add_symptom()

def on_entry_click(event):
    if search_entry.get() == 'Search...':
        search_entry.delete(0, tk.END)
        search_entry.config(fg='black')

def on_focusout(event):
    if not search_entry.get():
        search_entry.insert(0, 'Search...')
        search_entry.config(fg='grey')

def main():
    global search_entry

    # Create the main window (root)
    root = tk.Tk()
    root.title('Tkinter with Background Image')

    # Set the dimensions of the window
    W = 864
    H = 559
    root.geometry(f"{W}x{H}")

    # Disallow resizing of the window
    root.resizable(False, False)

    # Load and resize the background image using Pillow
    img_path = 'symptoms.png'
    original_image = Image.open(img_path)
    resized_image = original_image.resize((W, H))
    bg_image = ImageTk.PhotoImage(resized_image)

    # Create a label to display the background image
    label = tk.Label(root, image=bg_image)
    label.place(x=0, y=0, relwidth=1, relheight=1)

    # Search bar frame (Canvas for rounded corners)
    search_frame = tk.Canvas(root, bg='white', bd=0, highlightthickness=0)
    search_frame.place(x=30, y=H/2 - 80, width=350, height=50)
    search_frame.create_rounded_rect(0, 0, 350, 50, radius=25, fill='white')

    # Entry widget for the search bar
    search_entry = tk.Entry(search_frame, font=('Arial', 12), bg='white', relief=tk.FLAT, bd=0, fg='grey')
    search_entry.insert(0, 'Search...')
    search_entry.bind('<FocusIn>', on_entry_click)
    search_entry.bind('<FocusOut>', on_focusout)
    search_entry.bind('<KeyRelease>', suggest_symptoms)  # Added this line
    search_entry.place(x=10, y=10, width=290, height=30)


    # Load the search button image and resize
    search_btn_img_path = 'searchbutton.png'
    original_search_btn_image = Image.open(search_btn_img_path)
    resized_search_btn_image = original_search_btn_image.resize((30 , 30))
    search_btn_image = ImageTk.PhotoImage(resized_search_btn_image)

    # Search button
    search_btn = tk.Button(search_frame, image=search_btn_image, command=search_action, relief=tk.FLAT, bg='white', bd=0)
    search_btn.image = search_btn_image  # Keep a reference to prevent GC
    search_btn.place(x=300, y=10)

    # Load the button image and resize
    button_img_path = 'homebutton.png'
    original_button_image = Image.open(button_img_path)
    aspect_ratio = original_button_image.height / original_button_image.width
    new_height = int(aspect_ratio * 400)
    resized_button_image = original_button_image.resize((400, new_height))
    button_image = ImageTk.PhotoImage(resized_button_image)

    # Create a button widget using the resized image
    button = tk.Button(root, image=button_image, command=display_message, borderwidth=0)
    button.image = button_image  # Keep a reference to prevent GC
    x_margin = 20
    y_margin = 20
    button.place(x=x_margin, y=H - resized_button_image.height - y_margin)

    # Start the GUI event loop
    root.mainloop()

# Function to create a rounded rectangle on Canvas (for search bar background)
def _create_rounded_rect(self, x1, y1, x2, y2, **kwargs):
    """Draw a rounded rectangle."""
    radius = kwargs.pop('radius', 25)
    points = [x1+radius, y1,
              x1+radius, y1,
              x2-radius, y1,
              x2-radius, y1,
              x2, y1,
              x2, y1+radius,
              x2, y1+radius,
              x2, y2-radius,
              x2, y2-radius,
              x2, y2,
              x2-radius, y2,
              x2-radius, y2,
              x1+radius, y2,
              x1+radius, y2,
              x1, y2,
              x1, y2-radius,
              x1, y2-radius,
              x1, y1+radius,
              x1, y1+radius,
              x1, y1]
    return self.create_polygon(points, **kwargs, smooth=True)

tk.Canvas.create_rounded_rect = _create_rounded_rect

if __name__ == '__main__':
    load_symptoms_from_csv('../unique_symptoms.csv')  # Load the symptoms from your CSV

    main()
