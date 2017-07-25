'''

making a window

'''

from Tkinter import *


#this creates a blank window
root = Tk()

#this creates a label

theLabel = Label(root, text="young ugly gods")

#pack tell the comp to put theLabel anywhere or the first place it can fit it
theLabel.pack()

#mainloop puts this in an infinate loop so that the screen doesnt
#close after it runs
root.mainloop()





##from tkinter import *
##
##class Window(Frame):
##
##    def __init__ (self, master = None) :
##
##        Frame.__init__(self, master)
##
##        self.master = master
##
##root = Tk()
##
##app = Window(root)
##
##root.mainloop()
##
##w = Canvas ( master, option=value, ... )
