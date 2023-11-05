## Only run one time to init table users 

import sqlite3

try: 
    # Connect to DB and create a cursor
    cnt = sqlite3.connect('user.db')
    # create table client
    cnt.execute('''CREATE TABLE client (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                NAME TEXT UNIQUE,
                PASSWORD TEXT,
                IPADDRESS TEXT,
                PORT INTEGER
                );''')
    
    # create table file
    cnt.execute('''CREATE TABLE file (
                FILE_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                CLIENT_ID INTEGER REFERENCES client (ID),
                NAME TEXT
                );''')
    cnt.commit()
# Handle errors
except sqlite3.Error as error:
    print('Error occured - ', error)
# Close DB Connection irrespective of success or failure
finally:
    if cnt:
        cnt.close()
        print('SQLite Connection closed')