import pyodbc

DBfile = 'D:/master.mdb'
conn = pyodbc.connect('DRIVER={Microsoft Access Driver (*.mdb)};DBQ='+DBfile)
cur = conn.cursor()

string = "CREATE TABLE courses_by_year (schYr integer, courses varchar(80))"
cur.execute(string)
conn.commit()