import sqlite3

con = sqlite3.connect('twitter_database.db')
cur = con.cursor()

sql0 = '''
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    age INTEGER
);
'''
cur.executescript(sql0)

sql1 = '''
insert into users (username, password, age) values 
    ('brandon', '05071999', 21),
    ('kristi', '092000', 20),
    ('susie', '031369', 51),
    ('shin', '111165', 55),
    ('richie', '12345', 13),
    ('toby', '54321', 4)
'''
cur.executescript(sql1)
con.commit()

sql2 = '''
create table messages (
    id integer primary key,
    sender_id integer not null,
    message text not null,
    created_at timestamp not null default current_timestamp
    );
'''
cur.executescript(sql2)

sql4 = '''
insert into messages (sender_id, message) values 
    (1, 'All problems in computer science can be solved by another level of indirection. But that usually will create another problem.'),
    (2, 'Simplicity is prerequisite for reliability.'),
    (3, 'It''s harder to read code than to write it.'),
    (4, 'Don''t repeat yourself. Every piece of knowledge must have a single, unambiguous, authoritative representation within a system.'),
    (5, 'There are only two hard things in computer science: cache invalidation and naming things.');
'''
cur.executescript(sql4)
con.commit()