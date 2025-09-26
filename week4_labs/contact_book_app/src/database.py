# database.py
import sqlite3
def init_db():
    """Initializes the database and creates the contacts table if it doesn't exist."""
    conn = sqlite3.connect('contacts.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT,
    email TEXT
    )
    ''')
    conn.commit()
    return conn

def add_contact_db(conn, name, phone, email):
    """Adds a new contact to the database."""
    cursor = conn.cursor()
    cursor.execute("INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)", (" ".join([x.capitalize() for x in name.split()]), phone, email))
    conn.commit()

def get_all_contacts_db(conn, query=""):
    """Retrieves all contacts from the database."""
    cursor = conn.cursor()
    if query:
        cursor.execute("SELECT * FROM contacts WHERE LOWER(name) LIKE ? OR phone LIKE ? or LOWER(email) LIKE ?",
                       (f"%{query}%", f"%{query.lstrip('+63') if query.startswith('+63') else query.lstrip('0')}%", f"%{query}%"))
    else:
        cursor.execute("SELECT * FROM contacts")

    return cursor.fetchall()


def update_contact_db(conn, contact_id, name, phone, email):
    """Updates an existing contact in the database."""
    cursor = conn.cursor()
    cursor.execute("UPDATE contacts SET name = ?, phone = ?, email = ? WHERE id = ?", (name, phone, email, contact_id))
    conn.commit()

def delete_contact_db(conn, contact_id):
    """Deletes a contact from the database."""
    cursor = conn.cursor()
    cursor.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
    conn.commit()