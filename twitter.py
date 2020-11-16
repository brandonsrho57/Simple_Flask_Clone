from flask import Flask, render_template, send_from_directory
import sqlite3

app = Flask(__name__)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/')
def root():
    return render_template('base.html')
    logged_in = True
    username = 'brandon'

    con = sqlite3.connect('twitter_database.db')
    cur = con.cursor()

    sql = """
        SELECT sender_id, message FROM messages;
    """
    cur.execute(sql)

    results = cur.fetchall()
    messages = []
    for row in results:
        messages.append({
            'text': row[3],
            'username': row[2],
        })
    messages = [
        {'text': "What's popping?", 'username': 'Jacob'},
        {'text': "I will make America Great Again", 'username': 'Trump'},
        {'text': "Baseball is the best sport", 'username': 'Nick'},
    ]

    if logged_in:
        return render_template(
            'base.html',
            username=username,
            messages=messages,
        )
    else:
        return render_template('login.html')

@app.route('/create_message')
def create_message():
    return render_template('create_message.html')

@app.route('/create_user')
def create_user():
    return render_template('create_user.html')

@app.route('/logout')
def logout():
    return render_template('logout.html')

app.run()