'''
MESSAGEBOX
'''

from Tkinter import *
#imports the tkinter message box
import tkMessageBox
#import Tkinter.messagebox

root= Tk()

tkMessageBox.showinfo('Window Title', "Welcome! :)")

#stores response as a variable
answer = tkMessageBox.askquestion('Question 1', 'Are you vegan??')

if answer == "yes":
    print ("okay good job")


root.mainloop()


