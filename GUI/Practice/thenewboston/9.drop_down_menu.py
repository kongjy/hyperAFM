'''
DROP DOWN MENUS
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
subMenu.add_command(label="Now Project...", command=doNothing)
subMenu.add_command(label="New...", command=doNothing)

#adds separator in drop down menu for organization
subMenu.add_separator()

#adds Exit submenu
subMenu.add_command(label="Exit", command = doNothing)

#maake another menu item
editMenu = Menu(menu)
menu.add_cascade(label="Edit", menu=editMenu)
editMenu_add.command(label="Redo", command = doNothing) 


root.mainloop()
