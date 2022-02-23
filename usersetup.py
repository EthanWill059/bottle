from sqlite3 import connect
from time import sleep

db = connect('users.db')
db.execute('''CREATE TABLE USERS
         (USERNAME          TEXT    NOT NULL,
         PASSWORD          TEXT    NOT NULL,
         ADMIN             BOOL    NOT NULL);''')
sleep(1)
db.execute("INSERT INTO USERS (username, password, admin) VALUES ('ethanw','ticketadmin', True)")
db.commit()