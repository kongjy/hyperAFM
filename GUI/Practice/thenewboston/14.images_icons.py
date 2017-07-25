'''
IMAGES AND ICONS
'''

from Tkinter import *


root = Tk()

#opening photo. have to convert to a gif file in Python 2.7. have to write out the whole path unless the file is already in the path
photo = PhotoImage(file='/Users/Filmon/UW/GUI/Practice/thenewboston/shrek.gif')
#you cannot just show the image, you have to set it as, a label then place the label in thr root
label = Label(root, image=photo)
label.pack()

root.mainloop()
