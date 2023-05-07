import datetime
import sqlite3
from sqlite3 import Error
import json

with open('./data.json', "r") as file:
    data = json.load(file)

connection = None

try:
    connection = sqlite3.connect("./sqliteDB/database.db")
except Error as err:
    print(err)

c = connection.cursor()

query = "INSERT INTO note (title, description, begin_date, end_date, completion_status) VALUES (?, ?, ?, ?, ?)"

for item in data:
    values = (item['title'], item['description'], item['begin_date'], item['end_date'], item['completion_status'])
    c.execute(query,values)
    
connection.commit()
connection.close()