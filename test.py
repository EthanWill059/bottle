import sqlite3
import time

time.sleep(2)
db = sqlite3.connect('users.db')
user = 'ethanw'
#db.execute("UPDATE USERS SET admin = True WHERE username = ?", (user,))
db.commit()
cur = db.execute("SELECT admin FROM USERS WHERE username = ?", (user,))
row = cur.fetchone()
print(row[0])