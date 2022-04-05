#Virtual Keyboard References: https://stackoverflow.com/questions/60136473/how-to-call-and-close-a-virtual-keyboard-made-by-tkinter-using-touchscreen-displ
#                             https://stackoverflow.com/questions/45237883/tkinter-check-which-entry-last-had-focus

import tkinter as tk
from datetime import datetime
import time
import pyautogui
import psycopg2
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.pyplot
from matplotlib import animation
import numpy
from MCP3008 import MCP3008
import subprocess
#import matlab.engine

conn = None
cur = None
clinic_id = None
patient_id = None
ecg_id = None
ecg_signal = [0 for i in range(23040)]
dt = None
focused_entry = None
page = 1
keyboard_window = None
uppercase = False
exists = False
error_called = False
plot = None
canvas = None
in_existing = False
in_new = False
anim = None
#eng = matlab.engine.start_matlab()

def return_to_main_screen():
    global clinic_id
    global patient_id
    global ecg_id
    global ecg_signal
    global dt
    global page
    global exists
    global error_called
    global plot
    global canvas
    global in_existing
    global in_new
    clinic_id = None
    patient_id = None
    ecg_id = None
    ecg_signal = [0 for i in range(23040)]
    dt = None
    exists = False
    error_called = False
    plot = None
    first_ent.delete(0, 'end')
    last_ent.delete(0, 'end')
    gender_ent.delete(0, 'end')
    phone_ent.delete(0, 'end')
    dob_ent.delete(0, 'end')
    address_txt.delete("1.0", 'end')
    clinic_id_entry.delete(0, 'end')

    #remove old components based on page
    if page == 1:
        greeting.pack_forget()
        bt_start.pack_forget()
    elif page == 2:
        clinic_login.pack_forget()
        clinic_id_entry.pack_forget()
        clinic_id_submit.pack_forget()
        hide_keyboard()
    elif page == 3:
        if in_existing:
            hide_keyboard()
            patient_details_lbl.place_forget()
            first_lbl.place_forget()
            first_ent.place_forget()
            last_lbl.place_forget()
            last_ent.place_forget()
            phone_lbl.place_forget()
            phone_ent.place_forget()
            dob_lbl.place_forget()
            dob_ent.place_forget()
            patient_info_submit.place_forget()
        elif in_new:
            hide_keyboard()
            patient_details_lbl.place_forget()
            first_lbl.place_forget()
            first_ent.place_forget()
            last_lbl.place_forget()
            last_ent.place_forget()
            gender_lbl.place_forget()
            gender_ent.place_forget()
            phone_lbl.place_forget()
            phone_ent.place_forget()
            dob_lbl.place_forget()
            dob_ent.place_forget()
            address_lbl.place_forget()
            address_txt.place_forget()
            patient_info_submit.place_forget()
        else:
            new_p.pack_forget()
            cur_p.pack_forget()
    elif page == 4:
        ecg_lbl.pack_forget()
        bt_ecg.pack_forget()
    elif page == 5:
        bt_retake.place_forget()
        bt_save.place_forget()
        bt_discard.place_forget()
        canvas.get_tk_widget().destroy()

    page = 1
    greeting.pack()
    bt_start.pack()

def pay_attention(event):
    global focused_entry
    global keyboard_window
    focused_entry = event.widget
    keyboard_window.lift(aboveThis=None)

def shutdown():
    command = "/usr/bin/sudo /sbin/shutdown -h now"
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print(output)

def make_connection():
    global conn
    global cur
    conn = psycopg2.connect(
        database="d7m2tm2bv4vs6i",
        user="abwyoewwerndai",
        password="3da2111338189bd701aa56da0f842a6b6b5ac62522fc8a4e3ac017c38c0a3abd",
        host="ec2-44-198-236-169.compute-1.amazonaws.com",
        port='5432'
    )
    print(conn)
    cur = conn.cursor()

def check_clinic_id():
    print("Clinic ID: ")
    print(clinic_id)
    make_connection()
    cur.execute("select clinic_id from clinic where clinic_id = "+str(clinic_id))
    matching_clinics = cur.fetchall()
    conn.commit()
    end_connection()
    if len(matching_clinics) >= 1:
        return 1
    return 0

def find_patient(first, last, phone, dob):
    global cur
    global conn
    global patient_id
    make_connection()
    cur.execute("SELECT patient_id FROM Patient WHERE first_name = %s AND last_name = %s AND dob = %s AND phone = %s", (first, last, psycopg2.Date(int(dob[4:8]), int(dob[0:2]), int(dob[2:4])), phone))
    res = cur.fetchone()
    if not res == None:
        patient_id = res[0]
        print(patient_id)
    else:
        patient_id = None
    conn.commit()
    end_connection()
    if patient_id == None:
        patient_details_lbl.place_forget()
        first_lbl.place_forget()
        first_ent.place_forget()
        last_lbl.place_forget()
        last_ent.place_forget()
        phone_lbl.place_forget()
        phone_ent.place_forget()
        dob_lbl.place_forget()
        dob_ent.place_forget()
        patient_info_submit.place_forget()
        new_p.pack()
        cur_p.pack()
        new_patient()

def store_patient(first, last, gender, phone, dob, address):
    global cur
    global conn
    global patient_id
    make_connection()
    sql = "INSERT INTO Patient(first_name, last_name, gender, dob, phone, address) VALUES (%s, %s, %s, %s, %s, %s) RETURNING patient_id"
    cur.execute(sql, (first,last,gender,psycopg2.Date(int(dob[4:8]), int(dob[0:2]), int(dob[2:4])),phone,address))
    patient_id = cur.fetchone()[0]
    conn.commit()
    end_connection()

def analyze_ecg():
    #ml_res = eng.analyzeECG(ecg_signal,nargout=1)
    global ecg_signal
    signal = ecg_signal[0:1280]
    numpy.savetxt('MATLAB_ws/R2021a/signal.csv', signal , delimiter=",")
    res = subprocess.Popen(["./analyzeECG.elf","signal.csv"],cwd="MATLAB_ws/R2021a/",stdin=subprocess.PIPE,stdout=subprocess.PIPE)
    (ml_res,err) = res.communicate(b'signal.csv')
    output = open('./MATLAB_ws/R2021a/results.txt','r')
    ml_res = output.readlines()[2]
    output.close()
    return ml_res.split()
    #pass

def store_ecg():
    #store ecg record
    global cur
    global conn
    global ecg_id
    global ecg_signal
    global dt
    bt_retake.place_forget()
    bt_save.place_forget()
    bt_discard.place_forget()
    canvas.get_tk_widget().destroy()
    load_screen.pack()
    #ml_res = []
    ml_res = analyze_ecg()
    print(ml_res)
    make_connection()
    sql = "INSERT INTO ECG_Reading(reading, date_time_taken, ml_res) VALUES (%s, %s, %s) RETURNING ecg_id"
    signal = [a*1000 for a in ecg_signal]
    cur.execute(sql, (signal,dt, ml_res))
    ecg_id = cur.fetchone()[0]
    conn.commit()
    print(ecg_id)
    end_connection()
    link_records()
    load_screen.pack_forget()
    return_to_patient_info()

def link_records():
    global cur
    global conn
    global ecg_id
    global patient_id
    global clinic_id
    make_connection()
    cur.execute("INSERT INTO TakeMeasurement(patient_id, ecg_id, clinic_id) VALUES(%s, %s, %s)",(patient_id,ecg_id, clinic_id))
    conn.commit()
    end_connection()


def end_connection():
    global cur
    global conn
    cur.close()
    conn.close()

def type(event):
    global uppercase
    global focused_entry
    #focused_entry.insert("end", event)
    #entry = window.focus_get()
    #entry.insert("end", event)
    entry = focused_entry
    pyautogui.press(event)

    if event == "space":
        event = ' '
    elif event == 'return':
        event = '\n'
    elif event == 'tab':
        event = '\t'

    if event == 'delete':
        if isinstance(entry, tk.Entry):
            entry.delete(len(entry.get())-1,'end')
        else:
            entry.delete('end - 2c', 'end')
    elif event == 'caps lock':
        uppercase = not uppercase
    else:
        if uppercase:
            event = event.upper()
        else:
            event = event.lower()
        entry.insert('end',event)
    return

def build_keyboard(root):
    keys = [
        ['`',"1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "delete"],
        ['tab',"Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P",'\\'],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L",';',"'",'return'],
        ["caps lock", "Z", "X", "C", "V", "B", "N", "M", ',', '.', '/','space'],
    ]
    global keyboard_window
    keyboard_window = tk.Toplevel(root)
    keyboard_window.configure(background = "lightgray")
    keyboard_window.geometry('800x150+0-0')
    keyboard_window.lift(aboveThis=None)
    #keyboard_window.wm_attributes('-alpha', 0.7)

    for row_num, row_cont in enumerate(keys):
        col = 0
        for key in row_cont:
            columnspan = 1
            if key == "tab" or key == "delete":
                width = 5
            elif key == "caps lock" or key == "return":
                width = 5
            elif key == "shift":
                width = 5
            elif key == "space":
                width = 5
            else:
                width = 4
            tk.Button(keyboard_window, text=key, width=width, command=lambda value=key: type(value), bg="white", fg="black", takefocus = False).grid(row=row_num, column=col, columnspan=columnspan)
            col += columnspan

def pg_two():
    global page
    page = 2
    greeting.pack_forget()
    bt_start.pack_forget()
    clinic_login.pack()
    clinic_id_entry.pack()
    clinic_id_submit.pack()
    show_keyboard()

def pg_three():
    global page
    global new_p
    global cur_p
    global clinic_id
    global error_called
    page = 3
    clinic_id = clinic_id_entry.get()
    if check_clinic_id()>0:
        if error_called:
            error_lbl.pack_forget()
        clinic_login.pack_forget()
        clinic_id_entry.pack_forget()
        clinic_id_submit.pack_forget()
        new_p.pack()
        cur_p.pack()
        #patient_details_lbl.place(x=280, y=5)
        #first_lbl.place(x=130, y=55)
        #first_ent.place(x=210, y=55)
        #last_lbl.place(x=410, y=55)
        #last_ent.place(x=500, y=55)
        #gender_lbl.place(x=150, y=85)
        #gender_ent.place(x=410, y=85)
        #phone_lbl.place(x=305, y=115)
        #phone_ent.place(x=410, y=115)
        #dob_lbl.place(x=230, y=145)
        #dob_ent.place(x=410, y=145)
        #address_lbl.place(x=345, y=175)
        #address_txt.place(x=410, y=175)
        #patient_info_submit.place(x=270, y=230)

    else:
        page = 2
        error_called = True
        error_lbl.pack()
        clinic_login.pack()
        clinic_id_entry.pack()
        clinic_id_submit.pack()

def existing_patient():
    global exists
    global in_existing
    global in_new
    exists = True
    in_existing = True
    in_new = False
    new_p.pack_forget()
    cur_p.pack_forget()
    patient_details_lbl.place(x=280, y=5)
    first_lbl.place(x=130, y=55)
    first_ent.place(x=210, y=55)
    last_lbl.place(x=410, y=55)
    last_ent.place(x=500, y=55)
    phone_lbl.place(x=305, y=115)
    phone_ent.place(x=410, y=115)
    dob_lbl.place(x=230, y=145)
    dob_ent.place(x=410, y=145)
    patient_info_submit.place(x=270, y=230)

def new_patient():
    global exists
    global in_new
    global in_existing
    exists = False
    in_new = True
    in_existing = False
    new_p.pack_forget()
    cur_p.pack_forget()
    patient_details_lbl.place(x=280, y=5)
    first_lbl.place(x=130, y=55)
    first_ent.place(x=210, y=55)
    last_lbl.place(x=410, y=55)
    last_ent.place(x=500, y=55)
    gender_lbl.place(x=150, y=85)
    gender_ent.place(x=410, y=85)
    phone_lbl.place(x=305, y=115)
    phone_ent.place(x=410, y=115)
    dob_lbl.place(x=230, y=145)
    dob_ent.place(x=410, y=145)
    address_lbl.place(x=345, y=175)
    address_txt.place(x=410, y=175)
    patient_info_submit.place(x=270, y=230)

def pg_four():
    global page
    global in_existing
    global in_new
    in_existing = False
    in_new = False
    page = 4
    if exists:
        find_patient(first_ent.get(), last_ent.get(), phone_ent.get(), dob_ent.get())
    else:
        store_patient(first_ent.get(), last_ent.get(), gender_ent.get(), phone_ent.get(), dob_ent.get(), address_txt.get("1.0",'end-1c')) #address)
    hide_keyboard()
    patient_details_lbl.place_forget()
    first_lbl.place_forget()
    first_ent.place_forget()
    last_lbl.place_forget()
    last_ent.place_forget()
    gender_lbl.place_forget()
    gender_ent.place_forget()
    phone_lbl.place_forget()
    phone_ent.place_forget()
    dob_lbl.place_forget()
    dob_ent.place_forget()
    address_lbl.place_forget()
    address_txt.place_forget()
    patient_info_submit.place_forget()
    ecg_lbl.pack()
    bt_ecg.pack()

def return_to_patient_info():
    global page
    page = 3
    global patient_id
    global ecg_id
    bt_retake.place_forget()
    bt_save.place_forget()
    bt_discard.place_forget()
    canvas.get_tk_widget().destroy()

    new_p.pack()
    cur_p.pack()
    patient_id = None
    ecg_id = None
    first_ent.delete(0, 'end')
    last_ent.delete(0, 'end')
    gender_ent.delete(0, 'end')
    phone_ent.delete(0, 'end')
    dob_ent.delete(0, 'end')
    address_txt.delete("1.0", 'end')

def discard():
    global canvas
    canvas.get_tk_widget().destroy()
    return_to_patient_info()

def pg_five():
    global page
    ecg_lbl.pack_forget()
    bt_ecg.pack_forget()
    wait_screen.pack()
    page = 5
    run_ecg()
    plot_ecg()
    bt_retake.place(x=5,y=5)
    bt_save.place(x=145,y=5)
    bt_discard.place(x=285,y=5)

def plot_ecg():
    global ecg_signal
    global window
    global plot
    global canvas
    global anim
    window.configure(bg='white')
    matplotlib.use('TkAgg')
    fig = Figure(figsize = (8,4), dpi = 100)
    t = []
    x = []
    plot = fig.add_subplot(111)
    line, = plot.plot([], [], color='red')
    plot.set_xlabel("Time [s]")
    plot.set_ylabel("Voltage [V]")
    plot.set_xlim([0,3])
    plot.set_ylim([1,3])

    canvas = FigureCanvasTkAgg(fig, master = window)
    canvas.draw()
    canvas.get_tk_widget().place(x=0,y=50)
    global curr
    curr = 0
    def init():
        line.set_data([],[])
        return line,
    def animate(j):
        global curr
        global ecg_signal
        #x = numpy.linspace(0, 2, 1000)
        #y = numpy.sin(2 * numpy.pi * (x - 0.01 * i))+2
        i = curr
        t.append((i-1)/128)
        x.append(ecg_signal[i])
        line.set_data(t, x)
        curr = curr + 1
        return line,
    anim = animation.FuncAnimation(fig, animate, init_func = init, frames = 20, interval = 20, blit = True)

def run_ecg():
    global dt
    global ecg_signal
    adc = MCP3008()
    for i in range(23040):
        value = adc.read(channel = 0)
        voltage = value / 1023.0 * 3.3
        print(voltage)
        ecg_signal[i] = voltage
        time.sleep(1/128)
    make_connection()
    cur.execute("select current_timestamp")
    dt = cur.fetchone()[0]
    conn.commit()
    end_connection()
    wait_screen.pack_forget()


def redo_ecg():
    canvas.get_tk_widget().destroy()
    run_ecg()
    plot_ecg()

def show_keyboard():
    keyboard_window.deiconify()

def hide_keyboard():
    keyboard_window.withdraw()

window = tk.Tk()
window.geometry("800x480")

greeting = tk.Label(
    text="Welcome!\n\n Let's get started with your ECG.",
    width=100,
    height = 7,
    font=("Roboto Slab Light",30)
    )
clinic_login = tk.Label(
    text="\n\n\nPlease enter your Clinic ID.\n",
    width=100,
    height=3,
    font=("Roboto Slab Light", 30)
    )
bt_start = tk.Button(
    text="Begin",
    width=20,
    height = 2,
    fg='white',
    highlightbackground='navy blue',
    font=("Roboto Slab SemiBold",20),
    command = pg_two
)
clinic_id_submit = tk.Button(
    text="Submit",
    font=("Roboto Slab SemiBold",20),
    fg='white',
    highlightbackground='navy blue',
    width=20,
    height = 2,
    command = pg_three
)
patient_info_submit = tk.Button(
    text="Submit",
    font=("Roboto Slab SemiBold",20),
    width=20,
    height = 2,
    command = pg_four
)
clinic_id_entry = tk.Entry(width = 20)
clinic_id_entry.bind("<FocusIn>", pay_attention)
#Patient enters first, last, gender, phone, dob, address - improve entry data types??
patient_details_lbl = tk.Label(text="Patient Information",
    width=0,
    height=0,
    font=("Roboto Slab Light", 30)
    )
#font=("Gill Sans SemiBold",20),
first_lbl = tk.Label(text="First name:")
first_ent = tk.Entry(width=20)
first_ent.bind("<FocusIn>", pay_attention)
last_lbl = tk.Label(text="Last name:")
last_ent = tk.Entry(width=20)
last_ent.bind("<FocusIn>", pay_attention)
gender_lbl = tk.Label(text="Gender (M (male), F (female), O (other)):")
gender_ent = tk.Entry(width=5)
gender_ent.bind("<FocusIn>", pay_attention)
phone_lbl = tk.Label(text="Phone Number:")
phone_ent = tk.Entry(width=20)
phone_ent.bind("<FocusIn>", pay_attention)
dob_lbl = tk.Label(text="Date of Birth (MMDDYYYY):")
dob_ent = tk.Entry(width=10)
dob_ent.bind("<FocusIn>", pay_attention)
address_lbl = tk.Label(text="Address:")
address_txt = tk.Text(width=40, height=3)
address_txt.bind("<FocusIn>", pay_attention)

ecg_lbl = tk.Label(text="Please connect the probes to the patient and click below to begin the ECG reading.")
bt_ecg = tk.Button(
    text="Start ECG",
    width=20,
    height = 5,
    command = pg_five
)

bt_retake = tk.Button(
    text="Retake",
    width=10,
    height = 2,
    command = redo_ecg
)
bt_save = tk.Button(
    text="Save",
    width=10,
    height = 2,
    command = store_ecg
)
bt_discard = tk.Button(
    text="Discard",
    width=10,
    height = 2,
    command = discard
)

cur_p = tk.Button(
    text="Existing Patient",
    width=20,
    height = 5,
    command = existing_patient
)
new_p = tk.Button(
    text="New Patient",
    width=20,
    height = 5,
    command = new_patient
)

load_screen = tk.Label(
    text="Saving ECG...\nPlease Wait",
    width=100,
    height = 7,
    font=("Gill Sans Light",40)
    )

wait_screen = tk.Label(
    text="Collecting ECG...\nPlease Remain As Still As Possible",
    width=100,
    height = 7,
    font=("Gill Sans Light",40)
    )

error_lbl = tk.Label(text="Please try again")

build_keyboard(window)
hide_keyboard()
frame = tk.Frame(window)
frame.pack()
mainmenu = tk.Menu(frame)
mainmenu.add_command(label = "Shutdown", command=shutdown)
mainmenu.add_command(label = "Start Over", command=return_to_main_screen)
window.config(menu = mainmenu)
greeting.pack()
bt_start.pack()

window.mainloop()
