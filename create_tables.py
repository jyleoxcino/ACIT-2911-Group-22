import sqlite3
from sqlite3 import Error
import json, os, sys

if os.path.exists("./sqliteDB/database.db"):
    os.remove("./sqliteDB/database.db")

with open('./data.json', "r") as file:
    data = json.load(file)

connection = None

try:
    connection = sqlite3.connect("./sqliteDB/database.db")
except Error as err:
    print(err)

sql_queries = """
            CREATE TABLE events (
                event_id INTEGER PRIMARY KEY,
                title TEXT,
                description TEXT,
                start_date DATE,
                end_date DATE,
                completion_status INTEGER
            );
            CREATE TABLE tags (
                tag_id INTEGER PRIMARY KEY,
                tag_name TEXT
            );
            CREATE TABLE event_tags (
                event_id INTEGER,
                tag_id INTEGER,
                FOREIGN KEY (event_id) REFERENCES events(event_id),
                FOREIGN KEY (tag_id) REFERENCES tags(tag_id),
                PRIMARY KEY (event_id, tag_id)
            );
            CREATE TABLE schedules (
                schedule_id INTEGER PRIMARY KEY,
                title TEXT,
                description TEXT,
                start_date DATE,
                end_date DATE,
                days_of_week TEXT
            );
            CREATE TABLE schedule_tags (
                schedule_id INTEGER,
                tag_id INTEGER,
                FOREIGN KEY (schedule_id) REFERENCES schedules(schedule_id),
                FOREIGN KEY (tag_id) REFERENCES tags(tag_id),
                PRIMARY KEY (schedule_id, tag_id)
            );
        """

with connection:
    try:
        c = connection.cursor()
        c.executescript(sql_queries)
    except Error as e:
        print(e)
        print("Please delete the database located in ./sqliteDB and run this script again.")
        sys.exit(0)

query = "INSERT INTO events (title, description, start_date, end_date, completion_status) VALUES (?, ?, ?, ?, ?)"

for item in data:
    values = (item['title'], item['description'], item['begin_date'],
              item['end_date'], item['completion_status'])
    c.execute(query, values)

connection.commit()
connection.close()

print('Database has been created')