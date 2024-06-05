import sqlite3

def init_db():
    conn = sqlite3.connect('bulb_state.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS bulb_state (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            state TEXT,
            brightness INTEGER,
            color_temp INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            brightness INTEGER,
            color_temp INTEGER
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
