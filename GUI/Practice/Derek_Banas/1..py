from tkinter import *
from tkinter import ttk

root = Tk()

root.title ("First GUI")

frame = Frame(root)

labelText = StringVar()

label = Label (frame, textvariable = labelText)



button = Button(frame, text="Click me")

labelText.set ("I am label")

label.pack()
button.pack()
frame.pack()



root.mainloop()
