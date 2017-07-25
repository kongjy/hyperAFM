#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 10:43:27 2017

@author: Filmon
"""




import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

import Tkinter as tk
import ttk

LARGE_FONT = ("Verdana", 12)


class Application(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        
        #inititalizing Tkinter
        tk.Tk.__init__(self, *args, **kwargs)
        
        #changing icon
        #tk.Tk.__init__(self, default = "icon.ico")
        
        #changing window title
        tk.Tk.wm_title(self, "HyperImage Program")
        
        
        #creating container
        container = tk.Frame(self)
        container.pack(side='top', fill = 'both', expand=True)
        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {} 
        
        for F in (StartPage, hyperimagePage, graphPage):
        
            frame = F(container, self)
            
            self.frames[F] = frame
                
            frame.grid (row=0, column = 0, sticky = "nsew")
            

        self.show_frame(StartPage)
    
    def show_frame(self, cont):
        
        frame = self.frames[cont]
        frame.tkraise()


            
class StartPage (tk.Frame):

    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)
        
        
        label = ttk.Label (self, text="Start Page", font= LARGE_FONT)
        label.pack(padx=10, pady =10)
        
        button1 = ttk.Button(self, text = "Hyper Image Page", 
                            command = lambda: controller.show_frame(PageOne))
        button1.pack()

     
        
        button2 = ttk.Button(self, text = "Graph Page", 
                             command = lambda: controller.show_frame(PageThree))
        button2.pack()




class hyperimagePage (tk.Frame): 

    
   filename = tkFileDialog.askopenfile(mode="r",filetypes=(("Description file","*.desc"),("All files","*.*")))
        
        
    def __init__(self, parent, controller, filename):
        
        tk.Frame.__init__(self, parent)
        
        label = ttk.Label (self, text="Hyper Image Page", font= LARGE_FONT)
        label.pack(padx=10, pady =10)
        
       
        
        
        self.submitButton = ttk.Button(self, text = "Submit",
                                   command = openHyperImage)
        self.submitButton.grid(row=0, column=0)
        
        self.usertext = StringVar()
        self.myentry = Entry(self.master, textvariable = self.usertext)
        self.myentry.grid(row= 1, column=0)
        
        self.counter = 0
        
        self.master.mainloop()
        
        
        
        
        
        
        
        button1 = ttk.Button(self, text = "Back to Start", 
                            command = lambda: controller.show_frame(StartPage))
        button1.pack()
        
    def printMessage(self):
        print self.usertext.get()
        
       
    
    

        
        
class graphPage (tk.Frame):
    
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        label = ttk.Label (self, text="Graph Page", font= LARGE_FONT)
        label.pack(padx=10, pady =10)

        
        
        button1 = ttk.Button(self, text = "Back to Start", 
                            command = lambda: controller.show_frame(StartPage))
        button1.pack()
        
        
        #placing in teh graph using matplotlib
        matplotlib.use()
        f = Figure (figsize = (5,5), dpi = 100 )
        a = f.add_subplot(111)
        a.plot([1,2,3,4,5,6,7], [1,5,3,7,9,3,5])
        
        canvas= FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        
        toolbar = NavigationToolbar2TkAgg (canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        

        
        

app = Application()
app.mainloop()
