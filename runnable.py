import tkinter as tk
from datetime import datetime
import time




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
    pass

def check_clinic_id(clin_id):
    return 1

def store_patient(first, last, gender, phone, dob):
    pass

def store_ecg():
    pass

def link_records():
    pass

def end_connection():
    pass

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
    text="Remote Heart Diagnosis System",
    width=100,
    height = 7,
    font=("Chalkboard",40)
    )
clinic_login = tk.Label(
    text="Please enter your Clinic ID",
    width=100,
    height=5)
bt_start = tk.Button(
    text="Get Started",
    width=20,
    height = 4,
    fg='white',
    highlightbackground='green',
    font=("Chalkboard",35),
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
    command = store_ecg()
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
