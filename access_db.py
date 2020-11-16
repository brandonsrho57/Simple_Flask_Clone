import sqlite3

con = sqlite3.connect('twitter_database.db')
cur = con.cursor()

sql = """
select * from users;
"""
cur.execute(sql)
results = cur.fetchall()

print('Results = ', results)

for row in results:
    print('=============================')

    print('Row = ', row)
    print('ID = ', row[0])
    print('Username = ', row[1])
    print('Password = ', row[2])
    print('Age = ', row[3])

    print('=============================')

sql = """
select * from messages;
"""
cur.execute(sql)
results = cur.fetchall()

print('Messages = ', results)

for row in results:
    print('=============================')

    print('Row = ', row)
    print('Message ID = ', row[1])
    print('Sender ID = ', row[2])
    print('Message = ', row[3])
    print('Created At = ', row[4])

    print('=============================')