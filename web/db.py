import sqlite3
from sqlite3 import Error


# create a database connection to a SQLite database
connection = sqlite3.connect("usersdata.db")
c = connection.cursor()

def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT, password TEXT, email TEXT)')

def add_userdata(username, password, email):
    c.execute('INSERT INTO userstable(username, password, email) VALUES (?,?,?)', (username, password, email))
    connection.commit()

def login_user(username, password):
    c.execute('SELECT password FROM userstable WHERE username =? AND password=?', (username, password))
    data = c.fetchall()
    return data

def validate_hashed_password(username):
    c.execute('SELECT password FROM userstable WHERE username =?', (username,))
    hashed_pwd = c.fetchall()
    return hashed_pwd

def validate_username(username):
    """
    check if the username already exists
    """
    pass

def view_all_users():
    c.execute('SELECT * FROM userstable')
    data = c.fetchall()
    return data