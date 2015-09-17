import pyodbc

DBfile = 'D:/master.mdb'
conn = pyodbc.connect('DRIVER={Microsoft Access Driver (*.mdb)};DBQ='+DBfile)
cur = conn.cursor()

string = "ALTER TABLE Siswa ADD rereg_status VARCHAR(60)"
cur.execute(string)
conn.commit()

conn.close()