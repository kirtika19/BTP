import sqlite3
conn = sqlite3.connect("Diseases.db")
c = conn.cursor()
c.execute(''' 
            DROP TABLE diseases
            ''')
c.execute('''
            
             CREATE TABLE  diseases(
                 disease_code TEXT PRIMARY KEY,
                 disease_name TEXT,
                 reason TEXT,
                 measures TEXT,
                 crop TEXT,
                 suggestions TEXT


             )
             ''')

conn.commit()
conn.close()