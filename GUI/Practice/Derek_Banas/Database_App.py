#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 14:36:46 2017

DATABASE APP incomplete

SOURCE: https://www.youtube.com/watch?v=36StqYKofBU&index=26&list=PLGLfVvz_LVvTn3cK5e6LjhgGiSeVlIRwt
"""

from Tkinter import *
from Tkinter.import ttk
import sqlite3



class StudentDB:
    
    #Class Fields
    db_conn = 0
    theCursor = 0
    curr_student = 0 
    
    
    
    def setup_db(self):
        print  ("Setup DB")
        
        
    def stud_submit(self):
        print("Submit Stud")
        
        
    def update_listbox(self):
        print("Update LB")
       
        
    def load_student (self):
        print ("Load Stud")
        
    def update_student(self):
        print("Update Stud")
        
    def __init__(self, root):
        
root = Tk()
    root.title ("Student Database")
    root.geometry ("300x350")
    
    #-----1st Row------
    
    #first name 
    fn_label = Label (root, text="First Name")
    fn_label.grid (row= 0, column = 0, padx=10, pady=10, sticky=W)
    
    
    
    
    
    
    

studDB = StudentDB(root)

root.mainloop()