import sqlite3
conn = sqlite3.connect("Diseases.db")
c = conn.cursor()

diseases_data = [
    ('Early Blight','This disease is early blight.'),
    ('Late Blight','This disease is late blight.')
]

c.executemany('INSERT INTO diseases (name, description) VALUES (?,?)', diseases_data)
conn.commit()
conn.close()