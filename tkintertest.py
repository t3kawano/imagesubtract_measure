

import tkinter as tk

# Create the window
window = tk.Tk()
window.title("Text Entry Box")

# Create the text entry box
entry_box = tk.Entry(window)
entry_box.pack()

# Define the function to print the text
def print_text(event):
    print(entry_box.get())

# Bind the function to the Return key
entry_box.bind("<Return>", print_text)

# Start the event loop
window.mainloop()