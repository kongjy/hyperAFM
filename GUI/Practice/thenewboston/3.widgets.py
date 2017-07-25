'''

'''

from Tkinter import *

#makes a window
root = Tk()

#puts label directly into root
one = Label(root, text="One", bg="red", fg="white")
#calls it to used in program
one.pack()

#another label
two = Label(root, text="Two", bg="green", fg="black")
#fill=X will fill teh window as long as the X value is
two.pack(fill=X)

#another label
three = Label(root, text="Three", bg="blue", fg="white")
three.pack(side=LEFT, fill = Y)

















#stops the program from closing
root.mainloop()
