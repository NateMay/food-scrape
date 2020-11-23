import sqlite3

DB_FILENAME = 'food_data.sqlite'

def run_commands(commands):
    conn = sqlite3.connect(DB_FILENAME)
    cur = conn.cursor()

    for command in commands:
        print(f'running command: {command}', "\n")
        if type(command) is tuple:
            cur.execute(*command)
        else:
            cur.execute(command)

    conn.commit()
    conn.close()


def drop_tables():
    drop_categories = 'DROP TABLE IF EXISTS "Categories";'
    drop_foods = 'DROP TABLE IF EXISTS "Foods";'

    run_commands([
        drop_categories,
        drop_foods,
    ])


def create_tables():
    create_categories = '''CREATE TABLE IF NOT EXISTS "Categories" (
      "Id"               INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
      "Name"             TEXT NOT NULL,
      "Description"      TEXT,
      "Parent"           TEXT
  );
  '''

    create_foods = '''CREATE TABLE IF NOT EXISTS "Foods" (
      "Id"               INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
      "Name"             TEXT NOT NULL,
      "Description"      TEXT,
      "Image_src"        TEXT,
      "Category1"        TEXT,         
      "Category2"        TEXT         
  );
  '''

    run_commands([
        create_categories,
        create_foods
    ])

