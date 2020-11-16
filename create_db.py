import sqlite3

con = sqlite3.connect('twitter_database.db')
cur = con.cursor()

sql = """
create table messages (
    id integer primary key,
    message_id integer not null,
    sender_id integer not null,
    message text not null,
    created_at timestamp not null default current_timestamp
    );
"""
cur.execute(sql)

sql = """
insert into messages (message_id, sender_id, message, created_at) values (10, 1, 'Hi Mike', '2020-10-01 15:30:25');
"""
cur.execute(sql)
con.commit()

sql = """
insert into messages (message_id, sender_id, message, created_at) values (11, 2, 'I love CS', '2020-10-01 16:30:30');
"""
cur.execute(sql)
con.commit()

sql = """
insert into messages (message_id, sender_id, message, created_at) values (12, 3, 'I hate reading', '2020-10-01 22:37:55');
"""
cur.execute(sql)
con.commit()

sql = """
insert into messages (message_id, sender_id, message, created_at) values (13, 4, 'Age of Empires is a great game', '2020-10-01 04:16:22');
"""
cur.execute(sql)
con.commit()

sql = """
insert into messages (message_id, sender_id, message, created_at) values (14, 5, 'lol', '2020-10-01 20:30:40');
"""
cur.execute(sql)
con.commit()

sql = """
create table users (
    id integer primary key,
    username text not null unique,
    password text not null,
    age integer
    );
"""
cur.execute(sql)

sql = """
insert into users (username, password, age) values ('brandon', '00000', 21);
"""
cur.execute(sql)
con.commit()

sql = """
insert into users (username, password, age) values ('mike', 'abcdef', 35);
"""
cur.execute(sql)
con.commit()

sql = """
insert into users (username, password, age) values ('jonathan', 'password', 10);
"""
cur.execute(sql)
con.commit()