from flask import Flask
from flask import render_template
import sqlite3

webapp = Flask(__name__)

@webapp.route("/")
def home():
    return ("<h1>Hello</h1>")

@webapp.route("/user")
def user():
    user_dict = {'first': 'Jitao David', 'last': 'Zhang', 'email': 'jitao_david.zhang@roche.com'}

    return render_template("user.html", user=user_dict)

	
@webapp.route('/todo/all', methods=['GET'])
def show_alla_todos():
    db = sqlite3.connect("todo.sqlite3")
    cur = db.execute('SELECT * FROM todoTbl')
    rows = cur.fetchall()
    return render_template('todos.html', rows = rows);
