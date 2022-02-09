import tkinter as tk
from datetime import datetime
import time
import psycopg2

conn = None
cur = None
clinic_id = None
patient_id = None
ecg_id = None
dt = None
page = 1

window = tk.Tk()
window.geometry("800x480")

def make_connection():
    conn = psycopg2.connect(
        database="my_database_name",
        user="my_user_name",
        password="pass",
        host="url",
        port='5432'
    )
    cur = conn.cursor()

def check_clinic_id():
    print("Clinic ID: ")
    print(clinic_id)
    make_connection()
    cur.execute("select clinic_id from Clinic where clinic_id == "+str(clinic_id))
    matching_clinics = cur.fetchall()
    conn.commit()
    end_connection()
    if(matching_clinics.length >= 1)
        return 1
    return 0

def find_patient(first, last, dob, phone):
    make_connection()
    if phone != NULL:
        cur.execute("SELECT patient_id FROM Patient WHERE first_name = %s AND last_name = %s AND dob = ${dob} AND phone = %s",first, last, dob, phone)
    else:
        cur.execute("SELECT patient_id FROM Patient WHERE first_name = %s AND last_name = %s AND dob = ${dob}",first, last)
    exists = cur.fetchone()[0]
    conn.commit()
    end_connection()
    return exists

def store_patient(first, last, gender, phone, dob):
    print("First: ")
    print(first)
    print("Last: ")
    print(last)
    print("Gender: ")
    print(gender)
    print ("Phone: ")
    print(phone)
    print("DOB: ")
    print(dob)
    make_connection()
    sql = "INSERT INTO Patient(first_name, last_name, gender, dob, phone) VALUES (%s, %s, %s, %s, %s) RETURNING patient_id"
    cur.execute(sql, (first,last,gender,dob,phone))
    patient_id = cur.fetchone()[0]
    conn.commit()
    end_connection()

def store_ecg():
    pass

def link_records():
    make_connection()
    cur.execute("INSERT INTO TakeMeasurement(patient_id, ecg_id, clinic_id) VALUES(%i,%i, %i)",(patient_id,ecg_id, clinic_id))
    conn.commit()
    end_connection()

def end_connection():
    cur.close()
    conn.close()

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

def pg_three():
    page = 3
    make_connection()
    clinic_id = clinic_id_entry.get()
    if check_clinic_id()>0:
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
    bt_retake.pack_forget()
    bt_save.pack_forget()
    bt_discard.pack_forget()
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
    ecg_lbl.pack_forget()
    bt_ecg.pack_forget()
    page = 5
    run_ecg()
    plot_ecg()
    bt_retake.pack()
    bt_save.pack()
    bt_discard.pack()
    link_records() #no links to doctor table currently

def plot_ecg():
    pass

def run_ecg():
    pass

def redo_ecg():
    run_ecg()
    plot_ecg()

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
#Patient enters first, last, gender, phone, dob, address - improve entry data types??
patient_details_lbl = tk.Label(text="Patient Information")
#font=("Gill Sans SemiBold",20),
first_lbl = tk.Label(text="First name:")
first_ent = tk.Entry(width=20)
last_lbl = tk.Label(text="Last name:")
last_ent = tk.Entry(width=20)
gender_lbl = tk.Label(text="Gender (M (male), F (female), O (other)):")
gender_ent = tk.Entry(width=5)
phone_lbl = tk.Label(text="Phone Number:")
phone_ent = tk.Entry(width=20)
dob_lbl = tk.Label(text="Date of Birth (MMDDYYYY):")
dob_ent = tk.Entry(width=10)
address_lbl = tk.Label(text="Address:")
address_txt = tk.Text(width=50, height=3)

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
    command = return_to_patient_info
)

error_lbl = tk.Label(text="Please try again")

greeting.pack()
bt_start.pack()


window.mainloop()

#need power on/off triggers - start GUI, turn off display, end database connection
