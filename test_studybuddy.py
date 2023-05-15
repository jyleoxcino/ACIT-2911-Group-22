import pytest
from unittest.mock import patch, mock_open

from studybuddy import Database_Controller, Main

@pytest.fixture
def app():
    db_controller = Database_Controller()
    yield db_controller
    db_controller.conn.close()

def test_create_event(app):
    data = {
        'title': 'Test Title',
        'description': 'Test Description',
        'start_date': '2023-05-07',
        'end_date': '2023-05-07',
        'completion_status': 0
    }

    c = app.conn.cursor()
    c.execute("INSERT INTO events (title, description, start_date, end_date, completion_status) VALUES (?, ?, ?, ?, ?)",
              (data['title'], data['description'], data['start_date'], data['end_date'], data['completion_status']))

    event_id = c.lastrowid
    query = "SELECT * FROM events WHERE event_id = ?"
    params = (event_id, )
    result = c.execute(query, params).fetchone()

    assert result is not None
    assert result[1] == data['title']
    assert result[2] == data['description']
    assert result[3] == data['start_date']
    assert result[4] == data['end_date']
    assert result[5] == data['completion_status']

def test_delete_event(app):
    event_id = 1

    app.delete_event(event_id)

    query = "SELECT * FROM events WHERE event_id = ?"
    params = (event_id,)
    result = app.conn.execute(query, params).fetchone()

    assert result is None

def test_update_event(app):
    updated_data = {
        'event_id': 2,
        'title': 'Updated Event',
        'tags': 'Updated Tags',
        'description': 'Updated Description',
        'start_date': '2023-05-11',
        'end_date': '2023-05-12',
        'completion_status': 1
    }

    event_id = updated_data['event_id']
    app.update_event(updated_data)

    query = "SELECT * FROM events WHERE event_id = ?"
    params = (event_id,)
    result = app.conn.execute(query, params).fetchone()

    assert result is not None
    assert result[1] == updated_data['title']
    assert result[2] == updated_data['description']
    assert result[3] == updated_data['start_date']
    assert result[4] == updated_data['end_date']
    assert result[5] == updated_data['completion_status']