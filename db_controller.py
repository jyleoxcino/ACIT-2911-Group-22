import sqlite3
from sqlite3 import Error 
    
class Database_Controller():
    def __init__(self):
        self.path = "./database.db"

        self.conn = self.create_connection()
        self.create_tables()

    def create_connection(self):
        conn = None
        try:
            conn = sqlite3.connect("./sqliteDB/database.db")
            return conn
        except Error as e:
            print(e)

    def create_tables(self):
        sql_queries = """
            CREATE TABLE IF NOT EXISTS events (
                event_id INTEGER PRIMARY KEY,
                title TEXT,
                description TEXT,
                start_date DATE,
                end_date DATE,
                completion_status BOOLEAN
            );
            CREATE TABLE IF NOT EXISTS tags (
                tag_id INTEGER PRIMARY KEY,
                tag_name TEXT
            );
            CREATE TABLE IF NOT EXISTS event_tags (
                event_id INTEGER,
                tag_id INTEGER,
                FOREIGN KEY (event_id) REFERENCES events(event_id),
                FOREIGN KEY (tag_id) REFERENCES tags(tag_id),
                PRIMARY KEY (event_id, tag_id)
            );
            CREATE TABLE IF NOT EXISTS schedules (
                schedule_id INTEGER PRIMARY KEY,
                title TEXT,
                description TEXT,
                start_date DATE,
                end_date DATE,
                days_of_week TEXT
            );
            CREATE TABLE IF NOT EXISTS schedule_tags (
                schedule_id INTEGER,
                tag_id INTEGER,
                FOREIGN KEY (schedule_id) REFERENCES schedules(schedule_id),
                FOREIGN KEY (tag_id) REFERENCES tags(tag_id),
                PRIMARY KEY (schedule_id, tag_id)
            );
        """

        with self.conn:
            c = self.conn.cursor()
            c.executescript(sql_queries)

    def query_week(self, week_start):
        query = """SELECT * FROM events WHERE date(end_date) between ? and ?"""

        if self.conn is not None:
            c = self.conn.cursor()
            params = (week_start.strftime(
                "%Y-%m-%d"), (week_start + timedelta(days=6)).strftime("%Y-%m-%d"))
            data = c.execute(query, params)
        return data

    def create_event(self, data):
        if data is None:
            return
        else:
            self.data = data

        title = self.data['title']
        description = self.data['description']
        start_date = self.data['start_date']
        end_date = self.data['end_date']
        status = self.data['completion_status']

        sql = """INSERT INTO events(description,start_date,end_date,completion_status, title) VALUES(?,?,?,?,?);"""
        params = (description, start_date, end_date, status, title)
        print("event has been created")
        c = self.conn.cursor()
        c.execute(sql, params)
        self.conn.commit()

    def delete_event(self, data):
        c = self.conn.cursor()
        deleteQuery = """DELETE FROM events WHERE event_id = ?"""
        values = (data, )
        c.execute(deleteQuery, values)
        self.conn.commit()
        print(data, "has been deleted from the database.")

    def update_event(self, data):
        if data is None:
            return
        else:
            self.data = data

        event_id = self.data['event_id']
        title = self.data['title']
        description = self.data['description']
        start_date = self.data['start_date']
        end_date = self.data['end_date']
        completion_status = self.data['completion_status']

        sql = """UPDATE events SET title = ?, description = ?, start_date= ?, end_date = ?, completion_status = ? WHERE event_id = ? """

        params = (title, description, start_date,
                  end_date, completion_status, event_id)

        c = self.conn.cursor()
        c.execute(sql, params)
        self.conn.commit()

    def get_schedule_tags(self, schedule_id):
        pass

    def get_event_tags(self, event_id):
        query = """SELECT * FROM event_tags WHERE event_id = ?"""
        params = (event_id, )
        c = self.conn.cursor()
        data = c.execute(query, params)
        return data

    def get_tags(self, data):
        tag_names = []
        query = f'SELECT * FROM tags WHERE tag_id = ?'
        c = self.conn
        for tag_id in data:
            params = (tag_id[1], )
            data = c.execute(query, params)
            tag_names.append(data.fetchone()[1])
        return tag_names

    def get_all_tags(self):
        query = """ SELECT * FROM tags"""
        c = self.conn.cursor()
        cursor = c.execute(query)
        data = cursor.fetchall()
        return data

    def search_data(self, check, searchText):

        if check == "*":
            if searchText in "Completed":
                query = f"select * from events where title like '%{searchText}%' or description like '%{searchText}%' or start_date like '%{searchText}%' or end_date like '%{searchText}%' or completion_status = '1'"
            elif searchText in "Incomplete":
                query = f"select * from events where title like '%{searchText}%' or description like '%{searchText}%' or start_date like '%{searchText}%' or end_date like '%{searchText}%' or completion_status = '0'"
            else:
                query = f"select * from events where title like '%{searchText}%' or description like '%{searchText}%' or start_date like '%{searchText}%' or end_date like '%{searchText}%'"
        elif check == "completion_status":
            if 'I' in searchText:
                query = f"select * from events where {check} = '0'"
            elif 'C' in searchText:
                query = f"select * from events where {check} = '1'"
            else:
                query = ""

        else:
            query = f"select * from events where {check} like '%{searchText}%'"

        return query

    def create_schedule(self, data):
        self.edit_flag = 0
        if data is None:
            return
        else:
            self.data = data
        title = self.data['title']
        # tags = self.data['tags']
        description = self.data['description']
        start_date = self.data['start_date']
        end_date = self.data['end_date']
        query = """INSERT INTO schedules(title,description,start_date,end_date) VALUES(?,?,?,?)"""
        param1 = (title, description, start_date, end_date)
        c = self.conn.cursor()
        c.execute(query, param1)
        self.conn.commit()

    def delete_schedule(self, data):
        c = self.conn.cursor()
        deleteQuery = """DELETE FROM schedules WHERE schedule_id = ?"""
        values = (data, )
        c.execute(deleteQuery, values)
        self.conn.commit()

    def edit_schedule(self, data):
        if data is None:
            return
        else:
            self.data = data
        title = self.data['title']
        schedule_id = self.data['schedule_id']
        description = self.data['description']
        start_date = self.data['start_date']
        end_date = self.data['end_date']
        sql = """UPDATE schedules SET title = ?, description = ?, start_date = ?, end_date = ?  WHERE schedule_id = ? """
        params = (title, description, start_date, end_date, schedule_id)
        c = self.conn.cursor()
        c.execute(sql, params)
        self.conn.commit()
