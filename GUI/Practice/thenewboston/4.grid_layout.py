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
entry_1 = Enrty (root)
entry_2 = Enrty (root)


#Positioning where the labels will go
#Do not need to put in column if 0,it is default
label_1.grid(row=0, column=0)
label_2.grid(row=1, column=0)

#Positioning where the entries will go
entry_1.grid(row=0, column=1)
entry_2.grid(row=1, column=1)

#stops program from closing
root.mainloop()
