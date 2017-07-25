'''
GRID LAYOUT
'''

#astrixs means import all
from tkinter import *

 #makes the window
root = Tk()

#creates two labels 
label_1 = Label(root, text="Name")
label_2 = Label(root, text="Password")
#entry works like input, there will be two blank spaces
entry_1 = Entry (root)
entry_2 = Entry (root)


#Positioning where the labels will go
#Do not need to put in column if 0,it is default
#use sticky=E to align text to the right, E is East
label_1.grid(row=0, sticky=E)
label_2.grid(row=1, sticky=E)

#Positioning where the entries will go
entry_1.grid(row=0, column=1)
entry_2.grid(row=1, column=1)


#adds a checkbox 
c = Checkbutton(root, text="Keep me logged in please :)")
#write where we want it to be placed
#use columnspan=2 so that we can use both columns of the window
c.grid(columnspan=2)

#stops program from closing
root.mainloop()
