import sqlite3

def initialize_database():
    conn = sqlite3.connect("incidents.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS incidents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT NOT NULL,
        details TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()

def log_incident(attack_type, details):
    conn = sqlite3.connect("incidents.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO incidents (type, details) VALUES (?, ?)", (attack_type, details))
    conn.commit()
    conn.close()

def reset_database():
    conn = sqlite3.connect("incidents.db")
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS incidents")  # Drop the incidents table
    initialize_database()  # Recreate the incidents table
    conn.close()
