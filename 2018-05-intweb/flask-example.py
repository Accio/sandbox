from flask import Flask
from flask import render_template

webapp = Flask(__name__)

@webapp.route("/")
def home():
    return ("<h1>Hello</h1>")

@webapp.route("/user")
def user():
    user_dict = {'first': 'Jitao David', 'last': 'Zhang', 'email': 'jitao_david.zhang@roche.com'}

    return render_template("user.html", user=user_dict)

	
