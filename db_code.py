import sqlite3
from random import randint
conn = None
curs = None

def open_db():
    global conn, curs
    conn = sqlite3.connect("data.sqlite")
    curs = conn.cursor()

def close():
    curs.close()
    conn.close()

def do(request):
    curs.execute(request)
    conn.commit()

def clear_db():
    open_db()
    do("DROP TABLE IF EXISTS site_content")
    do("DROP TABLE IF EXISTS user")
    close()

def create():
    open_db()
    curs.execute("PRAGMA foreign_keys= on")
    do("""
        CREATE TABLE IF NOT EXISTS user(
        id INTEGER PRIMARY KEY,
        login VARCHAR,
        name VARCHAR,
        password VARCHAR,
        photo VARCHAR,
        about VARCHAR)
       """)

    close()

def add_user(user):
    with open(user["image"], "rb") as file:
        photo = file.read()
    open_db()
    curs.execute("INSERT INTO user (login, name, password, about, photo) VALUES (?,?,?,?,?)",
                            (user["login"], user["name"], user["password"], user["about"], photo))
    conn.commit()
    close()

def get_content():
    open_db()
    curs.execute("SELECT * FROM quiz ORDER BY id")
    result = curs.fetchall()
    close()
    return result

def get_user(name, password):
    open_db()
    curs.execute("SELECT id, login FROM user WHERE login=(?) AND password=(?)", (name, password))
    result = curs.fetchone()
    close()
    return result

def run():
    clear_db()
    create()

if __name__ == "__main__":
    run()

