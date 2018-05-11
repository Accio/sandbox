from flask import Flask
from flask import render_template
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from sqlalchemy import Column, Date, String, Integer

webapp = Flask(__name__)
webapp.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.sqlite3'

@webapp.route("/")
def home():
    html = """
    <h1>Hello, this is an experimental page</h1>
    <p> Subpage <a href="/user">user</a> </p>
    <p> Subpage <a href="/todo/all">all todos</a> </p>
    """
    return (html)

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

db = SQLAlchemy(webapp)

class Todos(db.Model):
    __tablename__ = 'todoTbl'
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    name = Column(String)
    deadline = Column(Date)

    def __init__(self, date, name, deadline):
        self.date = date
        self.name = name
        self.deadline = deadline

    @property
    def serialize(self):
        '''return as a json object so that we can use it in RESTful API'''
        return {'id': self.id,
                'date': self.date.strftime('%Y-%m-%d'),
                'name': self.name,
                'deadline': self.date.strftime('%Y-%m-%d')}

@webapp.route('/dbdisplay')
def display():
    return render_template('dbdisplay.html',
            todos = Todos.query.all())

@webapp.route('/api/all')
def app_all():
    todos = Todos.query.all()
    return jsonify(json_list = [todo.serialize for todo in todos])
