from tkinter import *

buttonClicked = False


def getlastupdated():
    global buttonClicked

    if buttonClicked:
        buttonClicked = False
        Label(root, text='Hi').pack()
    if not buttonClicked:
        buttonClicked = True
    return buttonClicked


root = Tk()
root.title("App")
Button(root, text="Get the last updated code", padx=30, pady=10, command=getlastupdated).pack()

root.mainloop()
