'''
BINDING FUNCTIONS TO WIDGET
    click a button to call a function from your computer program
'''

#adds all of tkinter program
from Tkinter import *






#adds a window
root = Tk()


#make a function to print name to be called when button is hit
def printName():
    print("Filmon Abraham")

#set parametes for button
#command tells program that when clicked, call a function
button_1 = Button(root, text="Say my name", command = printName)

#make this display on screen
button_1.pack()








#stops program
root.mainloop()
