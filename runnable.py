#Virtual Keyboard References: https://stackoverflow.com/questions/60136473/how-to-call-and-close-a-virtual-keyboard-made-by-tkinter-using-touchscreen-displ
#                             https://stackoverflow.com/questions/45237883/tkinter-check-which-entry-last-had-focus

import tkinter as tk
from datetime import datetime
import time
import pyautogui
import psycopg2
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

conn = None
cur = None
clinic_id = None
patient_id = None
ecg_id = None
ecg_signal = [i/100 for i in range(3601)]
dt = None
focused_entry = None
page = 1
keyboard_window = None
uppercase = False

def pay_attention(event):
    global focused_entry
    global keyboard_window
    focused_entry = event.widget
    keyboard_window.lift(aboveThis=None)

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

def find_patient(first, last, dob, phone):
    make_connection()
    dob_date = psycopg2.Date(int(dob[4:8]), int(dob[0:2]), int(dob[2:4]))
    if phone != NULL:
        cur.execute("SELECT patient_id FROM Patient WHERE first_name = %s AND last_name = %s AND dob = %s AND phone = %s",first, last, dob_date, phone)
    else:
        cur.execute("SELECT patient_id FROM Patient WHERE first_name = %s AND last_name = %s AND dob = %s",first, last, dob_date)
    exists = cur.fetchone()[0]
    conn.commit()
    end_connection()
    return exists

def store_patient(first, last, gender, phone, dob):
    global cur
    global conn
    global patient_id
    make_connection()
    sql = "INSERT INTO Patient(first_name, last_name, gender, dob, phone) VALUES (%s, %s, %s, %s, %s) RETURNING patient_id"
    cur.execute(sql, (first,last,gender,psycopg2.Date(int(dob[4:8]), int(dob[0:2]), int(dob[2:4])),phone))
    patient_id = cur.fetchone()[0]
    conn.commit()
    end_connection()
    pass

def store_ecg():
    fig.close()

def link_records():
    #make_connection()
    #cur.execute("INSERT INTO TakeMeasurement(patient_id, ecg_id, clinic_id) VALUES(%s, %s, %s)",(patient_id,ecg_id, clinic_id))
    #conn.commit()
    #end_connection()
    pass

def end_connection():
    global cur
    global conn
    cur.close()
    conn.close()
    pass

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
        ["caps lock", "Z", "X", "C", "V", "B", "N", "M", ',', '.', '/'],
        ['space']
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
                width = 4
            elif key == "caps lock" or key == "return":
                width = 4
            elif key == "shift":
                width = 4
            elif key == "space":
                width = 80
                columnspan = 12
            else:
                width = 3
            tk.Button(keyboard_window, text=key, width=width, command=lambda value=key: type(value), bg="white", fg="black", takefocus = False).grid(row=row_num, column=col, columnspan=columnspan)
            col += columnspan

def pg_two():
    page = 2
    frame = tk.Frame(window)
    frame.pack()
    mainmenu = tk.Menu(frame)
    mainmenu.add_command(label = "Back")
    window.config(menu = mainmenu)
    greeting.pack_forget()
    bt_start.pack_forget()
    clinic_login.pack()
    clinic_id_entry.pack()
    clinic_id_submit.pack()
    show_keyboard()

def pg_three():
    global clinic_id
    page = 3
    clinic_id = clinic_id_entry.get()
    if check_clinic_id()>0:
        clinic_login.pack_forget()
        clinic_id_entry.pack_forget()
        clinic_id_submit.pack_forget()
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
    else:
        page = 2
        error_lbl.pack()
        clinic_login.pack()
        clinic_id_entry.pack()
        clinic_id_submit.pack()

def pg_four():
    page = 4
    store_patient(first_ent.get(), last_ent.get(), gender_ent.get(), phone_ent.get(), dob_ent.get()) #address)
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
    page = 3
    bt_retake.pack_forget()
    bt_save.pack_forget()
    bt_discard.pack_forget()
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
    show_keyboard()

def discard():
    fig.close()
    return_to_patient_info()

def pg_five():
    ecg_lbl.pack_forget()
    bt_ecg.pack_forget()
    page = 5
    run_ecg()
    plot_ecg()
    bt_retake.pack()
    bt_save.pack()
    bt_discard.pack()
    link_records()

def plot_ecg():
    global ecg_signal
    global window
    global fig
    close('all')
    fig = Figure(figsize = (50,25), dpi = 1000)
    fig.clf()
    t = [i/360 for i in range(3601)]
    x = ecg_signal
    plot = fig.add_subplot(111)
    plot.plot(x,t)

    canvas =FigureCanvasTkAgg(fig, master = window)
    canvas.draw()
    canvas.get_tk_widget().pack()
    toolbar = NavigationToolbar2Tk(canvas,window)
    toolbar.update()
    canvas.get_tk_widget().pack()

def run_ecg():
    pass

def redo_ecg():
    fig.close()
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
    font=("Gill Sans Light",40)
    )
clinic_login = tk.Label(
    text="\n\n\nPlease enter your Clinic ID.\n",
    width=100,
    height=5,
    font=("Gill Sans Light", 30)
    )
bt_start = tk.Button(
    text="Begin",
    width=20,
    height = 2,
    fg='white',
    highlightbackground='navy blue',
    font=("Gill Sans SemiBold",20),
    command = pg_two
)
clinic_id_submit = tk.Button(
    text="Submit",
    font=("Gill Sans SemiBold",20),
    fg='white',
    highlightbackground='navy blue',
    width=20,
    height = 2,
    command = pg_three
)
patient_info_submit = tk.Button(
    text="Submit",
    font=("Gill Sans SemiBold",20),
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
    font=("Gill Sans Light", 30)
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
address_txt = tk.Text(width=50, height=3)
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
    width=20,
    height = 5,
    command = redo_ecg
)
bt_save = tk.Button(
    text="Save",
    width=20,
    height = 5,
    command = store_ecg
)
bt_discard = tk.Button(
    text="Discard",
    width=20,
    height = 5,
    command = discard
)

error_lbl = tk.Label(text="Please try again")

build_keyboard(window)
hide_keyboard()
greeting.pack()
bt_start.pack()

window.mainloop()
