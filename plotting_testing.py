import tkinter as tk
from datetime import datetime
import time
import pyautogui
import psycopg2
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import numpy

ecg_signal = [i/100 for i in range(3601)]
plot = None
canvas = None

def plot_ecg():
    global ecg_signal
    global window
    global plot
    global canvas
    matplotlib.use('TkAgg')
    fig = Figure(figsize = (8,4), dpi = 100)
    t = [i/360 for i in range(3601)]
    x = ecg_signal
    plot = fig.add_subplot(111)
    plot.plot(t, x, color='red')
    plot.set_xlabel("Time [s]")
    plot.set_ylabel("Voltage [mV]")

    canvas = FigureCanvasTkAgg(fig, master = window)
    canvas.draw()
    canvas.get_tk_widget().place(x=0,y=50)


window = tk.Tk()
window.geometry("800x480")
bt_retake = tk.Button(
    text="Retake",
    width=10,
    height = 2
)
bt_save = tk.Button(
    text="Save",
    width=10,
    height = 2
)
bt_discard = tk.Button(
    text="Discard",
    width=10,
    height = 2
)
bt_retake.place(x=5,y=5)
bt_save.place(x=145,y=5)
bt_discard.place(x=285,y=5)
plot_ecg()
window.mainloop()
