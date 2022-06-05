# Import the required Libraries
from tkinter import *
from tkinter import ttk, filedialog
from tkinter import filedialog as fd
from tkinter.filedialog import askopenfile

# Create an instance of tkinter frame
win = Tk()

# Set the geometry of tkinter frame
win.geometry("700x350")





# Add a Label widget
label = Label(win, text="Click the Button to browse the Files", font='Georgia 12')
label.pack(pady=10)

# Create a Button
ttk.Button(win, text="Browse", command=open_file).pack(pady=20)

win.mainloop()
