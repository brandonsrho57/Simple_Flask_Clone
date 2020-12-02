import sqlite3

con = sqlite3.connect('twitter_database.db')
cur = con.cursor()

print('================================================================================')
print('users')
print('================================================================================')
sql = """
select * from users;
"""
cur.execute(sql)
for row in cur.fetchall():
    print('id=', row[0])
    print('username=', row[1])
    print('password=', row[2])
    print('age=', row[3])
    print('================')

print('================================================================================')
print('messages')
print('================================================================================')
sql = """
select * from messages;
"""
cur.execute(sql)
for row in cur.fetchall():
    print('id=', row[0])
    print('sender_id=', row[1])
    print('message=', row[2])
    print('created at=', row[3])
    print('================')
