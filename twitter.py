from flask import Flask, render_template, send_from_directory, request, make_response
import sqlite3

app = Flask(__name__)

def logged_in(cur, username, password):
    sql = """
        SELECT username,password FROM users where username=? and password=?;
    """
    cur.execute(sql, (username, password))
    rows = cur.fetchall()

    if len(list(rows)) == 0:
        return False
    else:
        return True

@app.route('/')
def root():
    con = sqlite3.connect('twitter_database.db')
    cur = con.cursor()
    sql = """
        SELECT sender_id, message, created_at, id FROM messages;
    """
    cur.execute(sql)
    results = cur.fetchall()
    messages = []
    for result in results:
        sql = """
            SELECT username FROM users WHERE id=?
        """
        cur.execute(sql, (result[0],))
        username_rows = cur.fetchall()
        for username_row in username_rows:
            username = username_row[0]
        messages.insert(0, {
            'text': result[1],
            'username': username,
            'created_at': result[2],
            'id': result[3]
        })
    if logged_in:
        return render_template(
            'root.html',
            username=request.cookies.get('username'),
            messages=messages
        )
    else:
        return render_template(
            'root.html',
            messages=messages,
        )

@app.route('/login', methods=['get', 'post'])
def login():
    if request.form.get('username'):
        con = sqlite3.connect('twitter_database.db')
        cur = con.cursor()
        login_successful = logged_in(
            cur=cur,
            username=request.form.get('username'),
            password=request.form.get('password'),
        )
        if login_successful:
            res = make_response(render_template(
                'login.html',
                login_successful=True,
                username=request.form.get('username'),
            ))
            res.set_cookie('username', request.form.get('username'))
            res.set_cookie('password', request.form.get('password'))
            return res
        else:
            return render_template(
                'login.html',
                login_unsuccessful=True,
            )
    else:
        return render_template(
            'login.html',
            login_default=True,
        )

@app.route('/create_user', methods=['get', 'post'])
def create_user():
    if request.method == 'GET':
        return render_template('create_user.html')
    con = sqlite3.connect('twitter_database.db')
    cur = con.cursor()
    username = request.form.get('username')
    password = request.form.get('password')
    repeatpassword = request.form.get('repeatpassword')
    age = request.form.get('age')
    if password == repeatpassword:
        try:
            sql = """
            INSERT into users (username,password,age) values (?,?,?);
            """
            cur.execute(sql, (username, password, age))
            con.commit()
            return "You successfully created an account!"
        except sqlite3.IntegrityError:
            return "The username already exists!"
    else:
        return "Passwords don't match! Please try again."



@app.route('/create_message', methods=['get', 'post'])
def create_message():
    # logged_in = True
    if request.form.get('message'):
        con = sqlite3.connect('twitter_database.db')
        cur = con.cursor()
        sql = """
            SELECT id, username FROM users;
        """
        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
            if row[1] == request.cookies.get('username'):
                sender_id = row[0]
            print(row)
        message = request.form.get('message')
        con = sqlite3.connect('twitter_database.db')
        cur = con.cursor()
        sql = """
        INSERT INTO messages (sender_id, message) VALUES (?, ?);
        """
        cur.execute(sql, (sender_id, message,))
        con.commit()
        if len(message) == 0:
            message_successful = False
        else:
            message_successful = True

        if message_successful:
            res = make_response(render_template(
                'create_message.html',
                message_successful=True,
                username=request.cookies.get('username'),
                password=request.cookies.get('password'),
                message=request.form.get('message')
            ))
            return res
        else:
            return render_template(
                'create_message.html',
                username=request.cookies.get('username'),
                password=request.cookies.get('password'),
                message_unsuccessful=True
            )
    else:
        res = make_response(render_template(
            'create_message.html',
            username=request.cookies.get('username'),
            password=request.cookies.get('password'),
            message_default=True
        ))
        return res

@app.route('/logout')
def logout():
    res = make_response(render_template(
        'logout.html'
    ))
    res.set_cookie('username', '', expires=0)
    res.set_cookie('password', '', expires=0)
    return res

@app.route('/edit_message/<id>')
def edit_message(id):
    if request.form.get('edit_message'):
        con = sqlite3.connect('twitter_database.db')
        cur = con.cursor()

        sql = """
            SELECT id FROM users;
        """
        cur.execute(sql)

        message = request.form.get('edit_message')
        con = sqlite3.connect('twitter_database.db')
        cur = con.cursor()
        sql = """
        UPDATE messages SET message=? WHERE id=?;
        """
        cur.execute(sql, (id,))
        con.commit()

        if len(message) == 0:
            edit_message_successful = False
        else:
            edit_message_successful = True

        if edit_message_successful:
            res = make_response(render_template(
                'edit_message.html',
                edit_message_successful=True,
                username=request.cookies.get('username'),
                password=request.cookies.get('password'),
                message=request.form.get('edit_message')
            ))
            return res
        else:
            return render_template(
                'edit_message.html',
                username=request.cookies.get('username'),
                password=request.cookies.get('password'),
                edit_message_unsuccessful=True
            )
    else:
        res = make_response(render_template(
            'edit_message.html',
            username=request.cookies.get('username'),
            password=request.cookies.get('password'),
            edit_message_default=True
        ))
        return res

@app.route('/delete_message/<id>')
def delete_message(id):
    con = sqlite3.connect('twitter_database.db')
    cur = con.cursor()
    if logged_in(
        cur=cur,
        username=request.cookies.get('username'),
        password=request.cookies.get('password'),
    ):
        sql = """
        DELETE FROM messages WHERE id=?;
        """
        cur.execute(sql, (id,))
        con.commit()
        res = make_response(render_template(
            'delete_message.html',
            username=request.cookies.get('username'),
            password=request.cookies.get('password'),
            ))
        return res

@app.route('/delete_user/<username>')
def delete_user(username):

    con = sqlite3.connect('twitter_database.db')
    cur = con.cursor()

    if logged_in(
            cur=cur,
            username=request.cookies.get('username'),
            password=request.cookies.get('password'),
    ):
        sql = """
        DELETE FROM users WHERE username=?;
        """
        cur.execute(sql, (username,))
        con.commit()
        res = make_response(render_template(
            'delete_user.html',
        ))
        res.set_cookie('username', '', expires=0)
        res.set_cookie('password', '', expires=0)

        return res
    return render_template('root.html')

@app.route('/static/<path>')
def static_directory(path):
    return send_from_directory('static', path)

@app.route('/mike')
def mike():
    return render_template('mike.html')

app.run()