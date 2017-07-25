Common Tkinter commands


Tk() - creates window
Menu() - creates menu at top of screen, "File" "Edit" "View"
command = - makes a commmand, used in parameters for buttons, etc
lambda: - allow you to use command more than once and so you can build a function out side of the command
label = - names button,
text = - writes text
Button () - creates a button
toolbar = - makes a toolbar
Frame = - makes a frame (invisible box or container), widget that will frame other widgets
padx or pady - pixel pading, gives space
sticky = - defines how the widget is going to expand, use “n” “s” “e” “w” or multiple 
anchor = N or S or E or W - this will tell you where the text will align, compass
fill = X or Y - will stretch the window either direction, fill space that you have allotted
.pack() - set after a variable, will place anywhere that fits in window
weight=1 - setting which container will get priority for space
Canvas() - blank white area to draw on
root.title("The Title") - creates window title
Entry() - use when u want user to be able to enter text
\n - newline 
pass - write under a function so that you don’t get an error when your writing code
*args - unlimited arguments, any number of variables, variables being passed through
**kwargs - passing through dictionaries in a parameter
class - a blueprint on how to create an object
self -represents the current object. This is a common first parameter for any method of a class
parent - represents a widget to act as the parent of the current object. All widgets in tkinter except the root window require a parent.
controller - represents some other object that is designed to act as a common point of interaction for several pages of widgets. It is an attempt to decouple the pages. That is to say, each page doesn't need to know about the other pages. If it wants to interact with another page, such as causing it to be visible, it can ask the controller to make it visible.
