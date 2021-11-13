import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from MCP3008 import MCP3008
from datetime import datetime
import time
import psycopg2
import os
import subprocess

heroku_app_name = "remoteheart"
raw_db_url = subprocess.run(
    ["heroku", "config:get", "DATABASE_URL", "--app", heroku_app_name],
    capture_output=True
).stdout

DATABASE_URL = raw_db_url

conn = None
cur = None
clinic_id = None
patient_id = None
ecg_id = None
ecg_signal = List()
dt = None
page = 1
adc = MCP3008()

window = tk.Tk()
def back_page():
    match page:
        case 2:
            clinic_login.pack_forget()
            clinic_id_entry.pack_forget()
            clinic_id_submit.pack_forget()
            greeting.pack()
            bt_start.pack()
            exit()
        case 3:
            patient_details_lbl.pack_forget()
            first_lbl.pack_forget()
            first_ent.pack_forget()
            last_lbl.pack_forget()
            last_ent.pack_forget()
            gender_lbl.pack_forget()
            gender_ent.pack_forget()
            phone_lbl.pack_forget()
            phone_ent.pack_forget()
            dob_lbl.pack_forget()
            dob_ent.pack_forget()
            address_lbl.pack_forget()
            address_txt.pack_forget()
            patient_info_submit.pack_forget()
            clinic_login.pack()
            clinic_id_entry.pack()
            clinic_id_submit.pack()
            exit()
        case 4:
            ecg_lbl.pack_forget()
            bt_ecg.pack_forget()
            first_lbl.pack()
            first_ent.pack()
            last_lbl.pack()
            last_ent.pack()
            gender_lbl.pack()
            gender_ent.pack()
            phone_lbl.pack()
            phone_ent.pack()
            dob_lbl.pack()
            dob_ent.pack()
            address_lbl.pack()
            address_txt.pack()
            patient_info_submit.pack()
            exit()
        case 5:
            bt_retake.pack_forget()
            bt_save.pack_forget()
            bt_discard.pack_forget()
            ecg_lbl.pack()
            bt_ecg.pack()
            exit()


def pg_two():
    page = 2
    frame = Frame(window)
    frame.pack()
    mainmenu = Menu(frame)
    mainmenu.add_command(label = "Back", command= back_page)
    window.config(menu = mainmenu)
    greeting.pack_forget()
    bt_start.pack_forget()
    clinic_login.pack()
    clinic_id_entry.pack()
    clinic_id_submit.pack()

def pg_three():
    page = 3
    make_connection()
    clinic_id = clinic_id_entry.get()
    if check_clinic_id(clinic_id)>0:
        clinic_login.pack_forget()
        clinic_id_entry.pack_forget()
        clinic_id_submit.pack_forget()
        patient_details_lbl.pack()
        first_lbl.pack()
        first_ent.pack()
        last_lbl.pack()
        last_ent.pack()
        gender_lbl.pack()
        gender_ent.pack()
        phone_lbl.pack()
        phone_ent.pack()
        dob_lbl.pack()
        dob_ent.pack()
        address_lbl.pack()
        address_txt.pack()
        patient_info_submit.pack()
    else:
        error_lbl.pack()
        clinic_login.pack()
        clinic_id_entry.pack()
        clinic_id_submit.pack()

def pg_four():
    page = 4
    store_patient(first_ent.get(), last_ent.get(), gender_ent.get(), phone_ent.get(), dob_ent.get()) #address)
    patient_details_lbl.pack_forget()
    first_lbl.pack_forget()
    first_ent.pack_forget()
    last_lbl.pack_forget()
    last_ent.pack_forget()
    gender_lbl.pack_forget()
    gender_ent.pack_forget()
    phone_lbl.pack_forget()
    phone_ent.pack_forget()
    dob_lbl.pack_forget()
    dob_ent.pack_forget()
    address_lbl.pack_forget()
    address_txt.pack_forget()
    patient_info_submit.pack_forget()
    ecg_lbl.pack()
    bt_ecg.pack()

def return_to_patient_info():
    patient_details_lbl.pack()
    first_lbl.pack()
    first_ent.pack()
    last_lbl.pack()
    last_ent.pack()
    gender_lbl.pack()
    gender_ent.pack()
    phone_lbl.pack()
    phone_ent.pack()
    dob_lbl.pack()
    dob_ent.pack()
    address_lbl.pack()
    address_txt.pack()
    patient_info_submit.pack()

def pg_five():
    page = 5
    run_ecg()
    plot_ecg()
    bt_retake.pack()
    bt_save.pack()
    bt_discard.pack()
    link_records()
    return_to_patient_info()

def plot_ecg():
    fig = Figure(figsize = (50,25), dpi = 1000)
    fig.clf()
    t = [i/360 for i in range(3601)]
    x = ecg_signal
    plot = fig.add_subplot(111, clear = true)
    plot.plot(x,t)

    canvas =FigureCanvasTkAgg(fig, master = window)
    canvas.draw()
    canvas.get_tk_widget().pack()
    toolbar = NavigationToolbar2Tk(canvas,window)
    toolbar.update()
    canvas.get_tk_widget().pack()

def run_ecg():
    ecg_signal = List()
    #need to control sample speed
    for i in range(3601):
        value = adc.read(channel = 0)
        ecg_signal.append(value/1023.0 * 3.3)
        time.sleep(1/360)
    dt = datetime.now()

def redo_ecg():
    run_ecg()
    plot_ecg()

greeting = tk.Label(
    text="Remote Heart Diagnosis System",
    width=100,
    height=25)
clinic_login = tk.Label(
    text="Please enter your Clinic ID",
    width=100,
    height=5)
bt_start = tk.Button(
    text="Get Started",
    width=20,
    height = 5,
    command = pg_two
)
clinic_id_submit = tk.Button(
    text="Submit",
    width=20,
    height = 5,
    command = pg_three
)
patient_info_submit = tk.Button(
    text="Submit",
    width=20,
    height = 5,
    command = pg_four
)
clinic_id_entry = tk.Entry(width = 50)
#Patient enters first, last, gender, phone, dob, address - improve entry data types??
patient_details_lbl = tk.Label(text="Patient Information")
first_lbl = tk.Label(text="First name:")
first_ent = tk.Entry(width=50)
last_lbl = tk.Label(text="Last name:")
last_ent = tk.Entry(width=50)
gender_lbl = tk.Label(text="Gender (M (male), F (female), O (other)):")
gender_ent = tk.Entry(width=5)
phone_lbl = tk.Label(text="Phone Number:")
phone_ent = tk.Entry(width=25)
dob_lbl = tk.Label(text="Date of Birth (MMDDYYYY):")
dob_ent = tk.Entry(width=25)
address_lbl = tk.Label(text="Address:")
address_txt = tk.Text(width=50, height=10)

ecg_lbl = tk.Label(text="Please connect the probes to the patient and click below to begin the ECG reading.", width=50)
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
    command = return_to_patient_info
)

error_lbl = tk.Label(text="Please try again")

greeting.pack()
bt_start.pack()

#need power on/off triggers - start GUI, turn off display, end database connection

def make_connection():
    conn = psycopg2.connect(
        DATABASE_URL, sslmode='require')
        #may need more to this
    cur = conn.cursor()

def check_clinic_id(clin_id):
    cur.execute("SELECT COUNT(name) FROM Clinic WHERE clinic_id = %s",clin_id)
    exists = cur.fetchone()[0]
    conn.commit()
    return exists

def find_patient(first, last, dob, phone):
    if phone != NULL:
        cur.execute("SELECT patient_id FROM Patient WHERE first_name = %s AND last_name = %s AND dob = %s AND phone = %s",first, last, dob, phone)
    else:
        cur.execute("SELECT patient_id FROM Patient WHERE first_name = %s AND last_name = %s AND dob = %s",first, last, dob)
    exists = cur.fetchone()[0]
    conn.commit()
    return exists

def store_patient(first, last, gender, phone, dob):
    #fix data types for values
    cur.execute("INSERT INTO Patient(first_name, last_name, gender, phone, dob) VALUES(%s,%s,%s,%s,%s) RETURNING patient_id", (first, last, gender, phone, dob))
    patient_id = cur.fetchone()[0]
    conn.commit()

def store_ecg():
    #needs work- data types on values, ml?
    cur.execute("INSERT INTO ECG_Reading(reading, date_time_taken) VALUES(${ecg_signal},${dt}) RETURNING ecg_id")
    ecg_id = cur.fetchone()[0]
    conn.commit()

def link_records():
    cur.execute("INSERT INTO TakeMeasurement(patient_id, ecg_id, clinic_id) VALUES(%i,%i)",(patient_id,ecg_id, clinic_id))
    conn.commit()

def end_connection():
    cur.close()
    conn.close()


window.mainloop()
