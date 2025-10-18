import sqlite3

def create_tables():
    conn = sqlite3.connect("medischedular.db")
    c = conn.cursor()

    # Users table
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            email TEXT,
            password TEXT
        )
    """)

    # Medicines table
    c.execute("""
        CREATE TABLE IF NOT EXISTS medicines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            medicine_name TEXT,
            dosage TEXT,
            time TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()


def register_user(username, email, password):
    try:
        conn = sqlite3.connect("medischedular.db")
        c = conn.cursor()
        c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                  (username, email, password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False


def check_login(username, password):
    conn = sqlite3.connect("medischedular.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    result = c.fetchone()
    conn.close()
    return result


def add_medicine(user_id, name, dosage, time):
    conn = sqlite3.connect("medischedular.db")
    c = conn.cursor()
    c.execute("INSERT INTO medicines (user_id, medicine_name, dosage, time) VALUES (?, ?, ?, ?)",
              (user_id, name, dosage, time))
    conn.commit()
    conn.close()


def get_medicines(user_id):
    conn = sqlite3.connect("medischedular.db")
    c = conn.cursor()
    c.execute("SELECT id, medicine_name, dosage, time FROM medicines WHERE user_id=?", (user_id,))
    data = c.fetchall()
    conn.close()
    return data


def delete_medicine(medicine_id):
    conn = sqlite3.connect("medischedular.db")
    c = conn.cursor()
    c.execute("DELETE FROM medicines WHERE id=?", (medicine_id,))
    conn.commit()
    conn.close()