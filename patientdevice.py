import psycopg2

#GUI interface on touchscreen

#Take ECG reading

#Display ECG reading

#Perform AI analysis

#Store patient data and ECG data in database
conn = psycopg2.connect(
    host="",
    database="heart",
    user="postgres",
    password="Seniordesign")

cur = conn.cursor()
cur.execute("INSERT INTO table...", values)
conn.commit()

cur.close()
conn.close()
