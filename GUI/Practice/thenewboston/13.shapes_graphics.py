'''
SHAPES AND GRAPHICS
'''

from tkinter import *

root = Tk()

#making a canvas to draw on
canvas = Canvas(root, width=200, height=100)
canvas.pack()

#all lines by default will be black
#set parameters for the line- first parameters will tell where to begin,
#the other two will tell how big it wil be
blackLine = canvas.create_line(0,0, 200, 50)
redLine = canvas.create_line(0,100, 200, 50, fill="red")

#create rectangle
greenBox = canvas.create_rectangle(25,25, 130, 60, fill = "green")

#if we want to delete a graphic 
#canvas.delete(redLine)

root.mainloop()
