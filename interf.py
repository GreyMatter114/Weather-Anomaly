from tkinter import *
def quit(value=0):
    print('Hello, getting out of here')
    import sys; sys.exit(value)
widget = Button(None, text='Press me to quit' , command=lambda:quit(1))
widget.pack()
widget.mainloop()