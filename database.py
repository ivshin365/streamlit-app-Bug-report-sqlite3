import sqlite3
import pandas as pd

conn = sqlite3.connect('database2.db')
print("Opened database successfully")

conn.execute('CREATE TABLE pnr_bugs (id INTEGER PRIMARY kEY AUTOINCREMENT, author TEXT, bug_type TEXT, description TEXT, date TEXT, bug_severity INT, solution TEXT)')

df = pd.DataFrame()
print("Table created successfully")
conn.close()
