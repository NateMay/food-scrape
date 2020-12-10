import sqlite3

DB_FILENAME = 'food_data.sqlite'


def run_commands(commands):
    # takes a list of SQL commands and executes them all
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
    # drop tables to delete the previous runs
    run_commands([
        'DROP TABLE IF EXISTS "wiki_category";',
        'DROP TABLE IF EXISTS "wiki_food_category";',
        'DROP TABLE IF EXISTS "wiki_food";',
        'DROP TABLE IF EXISTS "fdc_food";',
        'DROP TABLE IF EXISTS "fdc_wiki_link";'
    ])


def create_tables():
    wiki_category = '''CREATE TABLE IF NOT EXISTS "wiki_category" (
        "id"               INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        "name"             TEXT NOT NULL,
        "description"      TEXT,
        "wiki_url"         TEXT,
        "parent_category"  TEXT);'''

    wiki_food = '''CREATE TABLE IF NOT EXISTS "wiki_food" (
        "id"               INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        "name"             TEXT NOT NULL,
        "description"      TEXT,
        "wiki_url"         TEXT,
        "image_src"        TEXT,
        "category1"        TEXT,         
        "category2"        TEXT);'''

    wiki_food_category = '''CREATE TABLE IF NOT EXISTS "wiki_food_category" (
        "id"                INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        "food_id"           INTEGER,
        "category_id"       INTEGER);'''

    fdc_food = '''CREATE TABLE IF NOT EXISTS "fdc_food" (
        "id"               INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        "name"             TEXT NOT NULL,
        "fdcid"            TEXT NOT NULL,
        "score"            DECIMAL(18, 6),
        "publishedDate"    TEXT,
        "foodCode"         TEXT,
        "dataType"         TEXT,
        "commonNames"      TEXT,
        "descriptions"     TEXT);'''

    fdc_nutrient = '''CREATE TABLE IF NOT EXISTS "fdc_nutrient" (
        "id"                 INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        "fdcid"              TEXT NOT NULL,
        "nutrientNumber"     TEXT NOT NULL,
        "unitName"           TEXT NOT NULL,
        "value"              DECIMAL(18, 6));'''

    fdc_wiki_link = '''CREATE TABLE IF NOT EXISTS "fdc_wiki_link" (
        "id"               INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        "name"             TEXT NOT NULL,
        "fdc_id"           TEXT NOT NULL,
        "wiki_id"          TEXT NOT NULL);'''

    run_commands([
        wiki_category,
        wiki_food,
        wiki_food_category,
        fdc_food,
        fdc_wiki_link,
        fdc_nutrient
    ])


def insert_all(categories):
    conn = sqlite3.connect(DB_FILENAME)
    cur = conn.cursor()

    for category in categories:
        print(category)
        cur.execute(*category.insert_cmd())
        category.update_id(cur.lastrowid)

        for food in category.foods:
            cur.execute(
                *food.insert_cmd([category.parent_category, category._id]))
            cur.execute(
                *("INSERT INTO wiki_food_category VALUES(NULL, ?, ?)", (cur.lastrowid, category._id)))

    conn.commit()
    conn.close()


def query_db_by(term):
    # Queries the foods by name and description
    conn = sqlite3.connect(DB_FILENAME)
    cur = conn.cursor()
    cur.execute('SELECT * FROM wiki_food WHERE name LIKE ?', (term, ))
    in_name = cur.fetchall()
    cur.execute('SELECT * FROM wiki_food WHERE description LIKE ?', (term, ))
    in_desc = cur.fetchall()
    conn.commit()
    conn.close()
    return in_name + in_desc


def get_category_name(_id):
    conn = sqlite3.connect(DB_FILENAME)
    cur = conn.cursor()
    cur.execute('SELECT name FROM wiki_category WHERE id = ?', (_id, ))
    result = cur.fetchone()
    conn.commit()
    conn.close()

    return result[0] if result else None


def connect_fdc_wiki(fdc, wiki):
    conn = sqlite3.connect(DB_FILENAME)
    cur = conn.cursor()
    fdc_id = fdc.get('fdcId')
    print(wiki)

    # need to get wiki_food._id
    cur.execute('INSERT INTO fdc_wiki_link VALUES(NULL, ?, ?, ?)',
                (wiki[1], fdc_id, wiki[0]))

    cur.execute('INSERT INTO fdc_food VALUES(NULL, ?, ?, ?, ?, ?, ?, ?, ?)', (
        fdc.get('description'),
        fdc_id,
        fdc.get('score'),
        fdc.get('publishedDate'),
        fdc.get('foodCode'),
        fdc.get('dataType'),
        fdc.get('commonNames'),
        fdc.get('additionalDescriptions')
    ))

    for nutrient in fdc.get('foodNutrients'):
        cur.execute('INSERT INTO fdc_nutrient VALUES(NULL, ?, ?, ?, ?)', (
            fdc_id,
            nutrient.get('nutrientNumber'),
            nutrient.get('unitName'),
            nutrient.get('value'),
        ))
    
    conn.commit()
    conn.close()
