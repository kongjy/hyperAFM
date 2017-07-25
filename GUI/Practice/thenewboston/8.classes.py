'''
USING CLASSES
'''

#imports all of tkinter
from tkinter import *

#set variable to make a window 
root = Tk()


#creates class 
class FilmonsButtons:

    #__init__ is a function that doesn't need to be called, it just runs
    #master is used to call the root (open a window) everytime class is run 
    def __init__(self, master):
        #set variable to Frame to create frame in the main windoe
        frame= Frame (master)
        frame.pack()

        self.printButton = Button (frame, text = "Print Message", command=self.printMessage)
        #display it on screen
        self.printButton.pack(side=LEFT)

        self.quitButton = Button (frame, text = "Quit", command = frame.quit)
        self.quitButton.pack(side=LEFT)

    def printMessage(self):
        print("Hey this worked!")

#have to make object
b = FilmonsButtons(root)






#stop program from shuting down
root.mainloop()
