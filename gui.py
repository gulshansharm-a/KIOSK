import tkinter as tk
from PIL import Image, ImageTk

def display_message():
    print("Button clicked!")

def main():
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
    img_path = 'home.png'
    original_image = Image.open(img_path)
    resized_image = original_image.resize((W, H))
    bg_image = ImageTk.PhotoImage(resized_image)

    # Create a label to display the background image
    label = tk.Label(root, image=bg_image)
    label.place(x=0, y=0, relwidth=1, relheight=1)

    # Load the button image and resize
    button_img_path = 'homebutton.png'
    original_button_image = Image.open(button_img_path)
    
    # Resize button image while maintaining the aspect ratio
    aspect_ratio = original_button_image.height / original_button_image.width
    new_height = int(aspect_ratio * 400)
    resized_button_image = original_button_image.resize((400, new_height))

    button_image = ImageTk.PhotoImage(resized_button_image)

    # Create a button widget using the resized image
    button = tk.Button(root, image=button_image, command=display_message, borderwidth=0)
    button.image = button_image  # Keep a reference to prevent GC
    
    # Margin values
    x_margin = 20
    y_margin = 20

    # Place the button at the bottom-left corner with margin
    button.place(x=x_margin, y=H - resized_button_image.height - y_margin)

    # Start the GUI event loop
    root.mainloop()

if __name__ == '__main__':
    main()
