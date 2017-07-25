'''
Frame
'''

from Tkinter import *

#the window
root = Tk()


#making an invisible container on the top part of the main root
topFrame = Frame(root)
#this packs the frame in the window
topFrame.pack()

#making an invisible container on the bottom part of the main root
bottomFrame = Frame(root)
#this packs the frame in the window on the bottom part
#we dont have to write out the side for both frames because it's assumed
bottomFrame.pack(side=BOTTOM)



#making a button, have to place where you want it, name it, and color
button1= Button(topFrame, text="Button 1", fg="red")
button2= Button(topFrame, text="Button 2", fg="blue")
button3= Button(topFrame, text="Button 3", fg="green")
button4= Button(bottomFrame, text="Button 4", fg="purple")

#this tells the program to run it
#if nothing in parameters of pack, the buttons will appear stacked in the middle
button1.pack(side=LEFT)
button2.pack(side=LEFT)
button3.pack(side=LEFT)
button4.pack(side=BOTTOM)


#this will stop the window form closing
root.mainloop()
