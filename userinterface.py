import tkinter as tk
window = tk.Tk()
def pg_two():
    greeting.pack_forget()
    bt_start.pack_forget()
    clinic_login.pack()
    clinic_id_entry.pack()
    clinic_id_submit.pack()

def pg_three():
    #eventually only works if clinic ID validated
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
    
def pg_four():
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
#Patient enters first, last, gender, phone, dob, address
patient_details_lbl = tk.Label(text="Patient Information")
first_lbl = tk.Label(text="First name:")
first_ent = tk.Entry(width=50)
last_lbl = tk.Label(text="Last name:")
last_ent = tk.Entry(width=50)
gender_lbl = tk.Label(text="Gender:")
gender_ent = tk.Entry(width=5)
phone_lbl = tk.Label(text="Phone Number:")
phone_ent = tk.Entry(width=25)
dob_lbl = tk.Label(text="Date of Birth (MMDDYYYY):")
dob_ent = tk.Entry(width=25)
address_lbl = tk.Label(text="Address:")
address_txt = tk.Text(width=50, height=10)

greeting.pack()
bt_start.pack()

window.mainloop()

