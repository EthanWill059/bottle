import sqlite3
from time import sleep


db = sqlite3.connect('tickets.db')
db.execute('''CREATE TABLE TICKETS
(ID                INTEGER PRIMARY KEY,        
 NAME              TEXT    NOT NULL,
 PHONENO           INT     NOT NULL,
 DATELOGGED        TEXT    NOT NULL,
 DEVICE            TEXT    NOT NULL,
 DETAILS           TEXT    NOT NULL,
 OPENSTATUS        BOOL    NOT NULL);''')


sleep(1)
db.execute("INSERT INTO TICKETS (name, phoneno, datelogged, device, details, openstatus) VALUES ('testing123', '0210210211', '2016-01-01 10:20:05.123', 'iPhone XS', 'testing', True)")
db.commit()
