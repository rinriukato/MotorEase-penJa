import tkinter as tk
from tkinter import messagebox

# Function to handle button click
def on_button_click():
    user_input = text_box.get()  # Get text from the text box
    messagebox.showinfo("Input", f"You entered: {user_input}")

# Create the main application window
root = tk.Tk()
root.title("Simple App")

# Add a text box
text_box = tk.Entry(root, width=30)
text_box.pack(pady=10)

# Add a button
button = tk.Button(root, text="Submit", command=on_button_click)
button.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()
