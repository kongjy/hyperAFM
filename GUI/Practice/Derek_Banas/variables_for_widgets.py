'''

'''

from Tkinter import *

def get_data(event=None):
    print ("String :", strVar.get())
    print ("Integer :", intVar.get())
    print ("Double :", dblVar.get())
    print ("Boolean :", boolVar.get())

def bind_button(event=None):
    if boolVar.get():
        getDataButton.unbind("<Button-1>")
    else:
        getDataButton.bind("<Button-1>", get_data)

        
root = Tk()

#tkinteer variables used for widgets 
strVar = StringVar()
intVar = IntVar()
dblVar = DoubleVar()
boolVar = BooleanVar()

#set defaul values for these
strVar.set("Enter String")
intVar.set("Enter Integer")
dblVar.set("Enter Double")
boolVar.set("True")

strEntry = Entry(root, textvariable=strVar)
strEntry.pack(side=LEFT)

intEntry = Entry(root, textvariable=intVar)
intEntry.pack(side=LEFT)

dblEntry = Entry(root, textvariable=dblVar)
dblEntry.pack(side=LEFT)

checkButton = Checkbutton(root, text="Switch", variable = boolVar)
checkButton.bind ("<Button-1>", bind_button)
checkButton.pack(side=LEFT)

getDataButton = Button(root, text="Get Data")
getDataButton.bind("<Button-1>", get_data)
getDataButton.pack(side=LEFT)

root.mainloop()
