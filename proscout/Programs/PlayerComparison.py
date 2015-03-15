from Tkinter import Label, Entry, Button, Tk, mainloop, Frame, LEFT, BOTH, TOP, Scrollbar, RIGHT, Y, W, Canvas, NS
import Tkconstants
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib import pyplot as plt
from proscout.python_api.analyze_tools import TwoPlayerComparison

def compare_button():
    p1 = e1.get()
    p2=e2.get()
    f, ax = TwoPlayerComparison(p1, p2).make_barchart()
    canvas = Canvas(frame, width=1200, height=600) # This is the dimensions of the visible area
    canvas.grid(row=1, column=1, sticky='NSEW')

    xScrollbar = Scrollbar(frame, orient='horizontal')
    yScrollbar = Scrollbar(frame)

    xScrollbar.grid(row=2, column=1, sticky=Tkconstants.EW)
    yScrollbar.grid(row=1, column=2, sticky=Tkconstants.NS)

    canvas.config(xscrollcommand=xScrollbar.set)
    xScrollbar.config(command=canvas.xview)
    canvas.config(yscrollcommand=yScrollbar.set)
    yScrollbar.config(command=canvas.yview)

    # plug in the figure
    figAgg = FigureCanvasTkAgg(f, canvas)
    mplCanvas = figAgg.get_tk_widget()
    mplCanvas.grid(row=1, column=1)
    mplCanvas.config(height=800, width=1200) # These are the dimensions of the figure

    # and connect figure with scrolling region
    canvas.create_window(0, 0, window=mplCanvas)
    canvas.config(scrollregion=canvas.bbox(Tkconstants.ALL))
    # The idea here is that we put a canvas on a canvas on a frame
    # The outer canvas has the scroll bar
    # The inner canvas contain the image




    

master = Tk() # Start app

Label(master, text="Player 1").grid(row=0, sticky=W)
Label(master, text="Player2").grid(row=1, sticky=W)
e1 = Entry(master)
e2 = Entry(master)
e1.grid(row=0, column=1, sticky='nw')
e2.grid(row=1, column=1, sticky='nw')
# Add buttons and input

def quit():
    master.quit()
    master.destroy()
    
## Add buttons
Button(master, text='Quit', command=quit).grid(row=3, column=0, sticky='nw', pady=4)
Button(master, text='Compare', command =compare_button).grid(row=3, column=1, pady=4, sticky='nw')

#Create a frame
frame = Frame()
frame.grid(row=4, column=1, sticky='nsew')

mainloop( )
