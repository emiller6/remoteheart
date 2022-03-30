from MCP3008 import MCP3008
import time
import tkinter as tk
from datetime import datetime
import time
import pyautogui
import psycopg2
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import numpy

ecg_signal = [i/100 for i in range(201)]
plot = None
canvas = None

def run_ecg():
    global ecg_signal
    adc = MCP3008()
    for i in range(201):
        value = adc.read(channel = 0)
        voltage = value / 1023.0 * 3.3
        ecg_signal[i] = voltage
        time.sleep(1/128)

def plot_ecg():
    global ecg_signal
    global window
    global plot
    global canvas
    matplotlib.use('TkAgg')
    fig = Figure(figsize = (8,4), dpi = 100)
    t = [i/128 for i in range(201)]
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
run_ecg()
plot_ecg()
window.mainloop()
