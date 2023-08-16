import sqlite3
conn = sqlite3.connect("Diseases.db")
c = conn.cursor()
c.execute('''
             CREATE TABLE if not exists diseases(
                 name TEXT PRIMARY KEY,
                 description TEXT
             )
             ''')

conn.commit()
conn.close()