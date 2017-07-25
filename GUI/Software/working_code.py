# -*- coding: utf-8 -*-
import matplotlib

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from Tkinter import *
import Tkinter as tk
import ttk 
from tkFileDialog   import askopenfilename

import os
import sys


sys.path.insert(0, '/Users/Filmon/UW/hyperAFM/hyperAFM/')
from util import HyperImage

# setting font and size for all text
LARGE_FONT= ("Verdana", 12)


# the class that contains all the pages for the actual application
# tk.TK is inherited to this class, importing Tk (from Tkinter application) to the tk application
class Application(tk.Tk):

    # init is the method that will always run when the class is called
    # self is implied no matter what, it is the first parameter of every method
    # *args is any argument that can be passed through here, ususally unlimited number of variables
    # *kwargs keywork argumemts, passing through dictionaries 
    def __init__(self, *args, **kwargs):

        # what we initialize
        tk.Tk.__init__(self, *args, **kwargs)


        # naming the application
        tk.Tk.wm_title(self, "Film 12 Topo Application")

        
        # creating a window 
        container = tk.Frame(self)
        # displaying the size of the window
        # side = top or bottom - choose where in the window you want the attribute to display
        # fill = X or Y or both - will stretch the window either direction, fill space that you have allotted
        # expand = True or False - beyond the limits that you set, fill in any more white space in the window 
        container.pack(side="top", fill="both", expand = True)
        # specify configuration, "0" = setting minimum size, "weight = 1" = setting priority
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # creating empty dictionary to hold all the pages from this whole program
        self.frames = {}

        # this will add each page into the "self.frames" tuple to raise the page when it is called
        # add class name of page to the parameters below when you want to navigate multiple pages 
        for F in (StartPage, PageOne, PageTwo, PageThree):

            frame = F(container, self)

            self.frames[F] = frame

            # sticky = defines how the widget is going to align and stretch, use “n” “s” “e” “w” or multiple 
            frame.grid(row=0, column=0, sticky="nsew")

        # says which page will show 
        self.show_frame(StartPage)
        
    # displays frame
    def show_frame(self, cont):

         
        frame = self.frames[cont]
        
        # puts page to the front 
        frame.tkraise()



# class for the first page shown
# inherit tk.Frame
class StartPage(tk.Frame):

    # this gets called first
    def __init__(self, parent, controller):

        # parent is the main class. In this case it is the "Application()" class
        tk.Frame.__init__(self,parent)
        # text at the top of the window in StartPage
        label = tk.Label(self, text="START", font=LARGE_FONT)
        # padx or pady - pixel pading, gives space
        label.pack(pady=20,padx=20)

        # button that vists the Hyper Image page
        # command calls the function but does not load after - "lambda" will run function so that the page will show
        button = ttk.Button(self, text="Hyper Image",
                            command=lambda: controller.show_frame(PageOne))
        button.pack()

        # button that vists the Topography page
        # "lambda" will run function so that the page will show
        button2 = ttk.Button(self, text="Topography",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()

        # button that vists the Graph Page page
        # "lambda" will run function so that the page will show
        button3 = ttk.Button(self, text="Graph Page",
                            command=lambda: controller.show_frame(PageThree))
        button3.pack()
        







class PageOne(tk.Frame): #hyper image page
 
    def __init__(self, parent, controller):

        # parent is the main class. In this case it is the "Application()" class
        tk.Frame.__init__(self, parent)

        # title for the Hyper Image page
        label = tk.Label(self, text="Hyper Image Page", font=LARGE_FONT)
        label.pack(pady=20, padx=10)

        
        # method that will give user option of which files to open
        def openFile():
            global fileName
            fileName = askopenfilename()
            
        # "File Open" button
        button = ttk.Button(self, text='File Open', command=openFile)
        button.pack()


        
            
        # entry for the x pixel
        def xEntry():
            global xVar

            xVar = IntVar()
            instruction = Label(self, text="x-pixel")
            instruction.pack()
            
            # this is the command that makes the entry bos
            xEntry = Entry(self, textvariable = xVar)
            xEntry.pack()

            # convert to string
            if xEntry == str:
                
                xVar = StringVar()


        # entry for the y pixel                   
        def yEntry():
    
            global yVar

            yVar = IntVar()
            instruction = Label(self, text="y-pixel")
            instruction.pack()
            yEntry = Entry(self, textvariable = yVar)
            yEntry.pack()

            if yEntry == str :

                yVar = StringVar()


        # entry for the range pixel
        def rangeEntry():
            global rVar

            rVar = IntVar()
            instruction = Label(self, text="range")
            instruction.pack()
            rangeEntry = Entry(self, textvariable = rVar)
            rangeEntry.pack()
                       
            if rangeEntry == str:
                
                rVar = StringVar()




            
        def open_files():

            print fileName
            
            
            xPixel=xVar.get()
            yPixel=yVar.get()
            rRange=rVar.get()
            
            Hyper58 = HyperImage(fileName)

            hyperimage = Hyper58.hyper_image[xPixel, yPixel, rRange]

            plt.imshow(hyperimage)


        
        def submitButton():
            
            # the Submit button 
            button = ttk.Button(self, text='Submit', command=open_files)
            button.pack(pady=10,padx=10)

    
            
            
         
             
        
        xEntry()
        yEntry()
        rangeEntry()
        submitButton() 
















class PageTwo(tk.Frame): # topography page

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Topography Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()














class PageThree(tk.Frame): # graph page

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        label = tk.Label(self, text="Graph Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        # graph details - size of figure 
        f = Figure(figsize=(5,5), dpi=100)
                       
        # adds subplot - 111 means there is only one chart 
        a = f.add_subplot(111)
        a.plot([1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5])

        
        # allows us to draw graph in window
        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        # added toolbar features at the bottom of the graph 
        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        
 
        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()



app = Application()
app.mainloop()




















