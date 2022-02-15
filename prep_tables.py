import psycopg2

if __name__ == "__main__":
    conn = psycopg2.connect(
        database="d7m2tm2bv4vs6i",
        user="abwyoewwerndai",
        password="3da2111338189bd701aa56da0f842a6b6b5ac62522fc8a4e3ac017c38c0a3abd",
        host="ec2-44-198-236-169.compute-1.amazonaws.com",
        port='5432'
    )
    print(conn)
    cur = conn.cursor()

    cur.execute("INSERT INTO Clinic(clinic_id, name, phone, address) VALUES(%s,%s,%s,%s)",("1", "Clinic1", "2221113333", "413 Redwood Drive"))
    conn.commit()

    cur.close()
    conn.close()
