#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 14:27:48 2017

@author: Filmon
"""

from Tkinter import *
import Tkinter as tk
import tkMessageBox
from tkFileDialog   import askopenfilename 
import matplotlib

#--------Welcome Window------------

#tkMessageBox.showinfo('Window Title', "Welcome! :)")





def openButton():
    
    name= askopenfilename() 
    print name
    

def doNothing():
    
    #opening photo. have to convert to a gif file in Python 2.7. have to write out the whole path unless the file is already in the path
    photo = PhotoImage(file='/Users/Filmon/UW/GUI/Practice/thenewboston/giphy.gif')
    #you cannot just show the image, you have to set it as, a label then place the label in thr root
    label = Label(root, image=photo)
    label.pack()

    root.mainloop()



#main window
root = Tk()



#---------toolbar------------

menu = Menu(root)
#tells program that its configuring a menu for the variable menu
root.config(menu = menu)

#create sub menu to put in the menu
subMenu = Menu(menu)
#cascade in tkinter means drop down menu
#parameters are the name of the drop down and what goes in the menu
menu.add_cascade(label="File", menu=subMenu)

#adds what you want in the drop down menu
subMenu.add_command(label="Open...", command=openButton)
subMenu.add_command(label="New...", command=doNothing)

#adds separator in drop down menu for organization
subMenu.add_separator()

#adds Exit submenu
subMenu.add_command(label="Exit", command = doNothing)

#make another menu item
editMenu = Menu(menu)
menu.add_cascade(label="Edit", menu=editMenu)
editMenu.add_command(label="Redo", command = doNothing) 




    
    




#this will stop the window form closing
root.mainloop()

