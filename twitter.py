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
    messages = [
        {'text': "What's popping?", 'username': 'Jacob'},
        {'text': "I will make America Great Again", 'username': 'Trump'},
        {'text': "Baseball is the best sport", 'username': 'Nick'},
    ]
    con = sqlite3.connect('twitter_database.db')
    cur = con.cursor()
    sql = """
        SELECT sender_id, message FROM messages;
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
        messages.append({
            'text': result[1],
            'username': username
        })
    con = sqlite3.connect('twitter_database.db')
    cur = con.cursor()

    login_successful = logged_in(
        cur=cur,
        username=request.cookies.get('username'),
        password=request.cookies.get('password'),
    )

    if login_successful:
        return render_template(
            'root.html',
            username=request.cookies.get('username'),
            messages=messages,
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

@app.route('/create_message')
def create_message():
    return render_template('create_message.html')

@app.route('/create_user')
def create_user():
    return render_template('create_user.html')

@app.route('/logout')
def logout():
    res = make_response(render_template(
        'logout.html'
    ))
    res.set_cookie('username', '', expires=0)
    res.set_cookie('password', '', expires=0)
    return res

@app.route('/static/<path>')
def static_directory(path):
    return send_from_directory('static', path)

app.run()