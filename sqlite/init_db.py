import sqlite3
import random
from datetime import datetime, timedelta

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

for i in range(30):
    date = datetime.now() - timedelta(days=i)

    cur.execute(f'''
        INSERT INTO hours_worked(date, new_dev, old_dev, analytics, other)
        VALUES (?, ?, ?, ?, ?)
    ''', (date.strftime('%Y-%m-%d'), random.randint(0, 10), random.randint(0, 10), random.randint(0, 10), random.randint(0, 10)))

connection.commit()
connection.close()