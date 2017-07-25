'''
MOUSE CLICK EVENTS
'''

#opens all tkinter
from tkinter import *
#opens window
root = Tk()



#click mouse functions

def leftClick(event):
    print ("left")
def middleClick(event):
    print("middle")
def rightClick(event):
    print ("right")

    
#set parameters for the invisivle frame
frame = Frame(root, width=300, height=250)

#need a wdiget to bind an event to
frame.bind ("<Button 1>", leftClick)
frame.bind ("<Button 2>", middleClick)
frame.bind ("<Button 3>", rightClick)

#tell program to run
frame.pack()




#stops program
root.mainloop()
