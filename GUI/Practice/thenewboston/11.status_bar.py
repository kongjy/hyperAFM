'''
DROP DOWN MENUS & CREATING A TOOLBAR & STATUS BAR
'''

from tkinter import *

def doNothing():
    print("ok I wont")


root = Tk()

menu = Menu(root)
#tells program that its configuring a menu for the variable menu
root.config(menu = menu)

#create sub menu to put in the menu
subMenu = Menu(menu)
#cacade in tkinter means drop down menu
#parameters are the name of the drop down and what goes in the menu
menu.add_cascade(label="File", menu=subMenu)

#adds what you want in the drop down menu
subMenu.add_command(label="New Project...", command=doNothing)
subMenu.add_command(label="New...", command=doNothing)

#adds separator in drop down menu for organization
subMenu.add_separator()

#adds Exit submenu
subMenu.add_command(label="Exit", command = doNothing)

#make another menu item
editMenu = Menu(menu)
menu.add_cascade(label="Edit", menu=editMenu)
editMenu.add_command(label="Redo", command = doNothing) 


'''
CREATING TOOLBAR
'''


toolbar = Frame(root, bg="blue")

###items in toolbar
##insertButt = Button(toolbar, text = "Insert Image", command = doNothing
## 
###padx gives you pixel pading. Padiing is extra space so everythin isnt so close
##insertButt.pack(side = LEFT, padx=2, pady=2)
##printButt = Button(toolbar, text = "Print", command = doNothing)
##printButt.pack (side=LEFT, padx=2, pady=2)
##
##toolbar.pack(side=TOP, fill=X)


'''
CREATING STATUS BAR
'''

#setting variable to make status
#bd stands for border, SUNKEN means place behind, anchor
#will tell where the text will go (Northh, South,etc.)
status = Label (root, text="Preparing to do nothing...", bd=1, relief=SUNKEN, anchor=W)
status.pack(side=BOTTOM, fill=X)






root.mainloop()
