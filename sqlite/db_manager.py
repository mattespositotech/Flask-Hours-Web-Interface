import sqlite3
from datetime import datetime
from dateutil.relativedelta import relativedelta

def adjust_month(months=0):
    date = datetime.now()
    adjusted_date = date + relativedelta(months=months)
    return adjusted_date.strftime("%Y-%m-%d")

def get_db_connection():
    conn = sqlite3.connect('sqlite/database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_all_data(query="SELECT * FROM hours_worked ORDER BY date"):
    conn = get_db_connection()
    rows = conn.execute(query).fetchall()
    return [dict(row) for row in rows]

def get_all_data_from_this_month():
    return get_data_adjusted_from_current_month()

def get_data_adjusted_from_current_month(adj_mon=0):
    month = adjust_month(adj_mon)
    query = f"SELECT * FROM hours_worked WHERE strftime('%Y-%m', date) = '{month[:7]}' ORDER BY date"
    return get_all_data(query)

def get_all_future_data():
    current_month = datetime.now().strftime('%Y-%m')
    query = f"SELECT * FROM hours_worked WHERE strftime('%Y-%m', date) > '{current_month}' ORDER BY date"
    return get_all_data(query)

def get_hours_by_date(date):
    query = "SELECT * FROM hours_worked WHERE date = ?"

    conn = get_db_connection()
    hours_by_date = conn.execute(query, (date,)).fetchone()

    return hours_by_date

def insert_into_db(data):
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO hours_worked (new_dev, old_dev, analytics, other) 
            VALUES (?, ?, ?, ?)
        """, (data['new_dev'], data['old_dev'], data['analytics'], data['other']))
        conn.commit()
    except sqlite3.Error as er:
        return er.sqlite_errorcode

    conn.close()
    return 0

def update_hours(data):
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            UPDATE hours_worked SET 
                new_dev = ?, 
                old_dev = ?, 
                analytics = ?, 
                other = ? 
            WHERE date = ?
        """, (data['new_dev'], data['old_dev'], data['analytics'], data['other'], data['date']))
        conn.commit()
    except sqlite3.Error as er:
        return er.sqlite_errorcode

    conn.close()
    return 0

def upsert_hours(data):
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO hours_worked (date, new_dev, old_dev, analytics, other) 
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(date)
            DO UPDATE SET
                new_dev = excluded.new_dev,
                old_dev = excluded.old_dev,
                analytics = excluded.analytics,
                other = excluded.other
        """, (data['date'], data['new_dev'], data['old_dev'], data['analytics'], data['other']))
        conn.commit()
    except sqlite3.Error as er:
        return er.sqlite_errorcode

    conn.close()
    return 0

def delete_from_db(date):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM hours_worked 
        WHERE date = ?
    """, (date,))

    conn.commit()
    conn.close()