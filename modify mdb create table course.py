import pyodbc

DBfile = 'D:/master.mdb'
conn = pyodbc.connect('DRIVER={Microsoft Access Driver (*.mdb)};DBQ='+DBfile)
cur = conn.cursor()

string = "CREATE TABLE courses (id integer, course_name varchar(45), course_level integer, school_id integer)"
cur.execute(string)
conn.commit()