DROP TABLE IF EXISTS hours_worked;

CREATE TABLE hours_worked (
    date TEXT DEFAULT (date('now', 'localtime')) PRIMARY KEY,
    new_dev INTEGER DEFAULT 0,
    old_dev INTEGER DEFAULT 0,
    analytics INTEGER DEFAULT 0,
    other INTEGER DEFAULT 0
);