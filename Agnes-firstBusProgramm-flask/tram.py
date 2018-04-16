from flask import Flask
import random

app = Flask(__name__)

@app.route("/")

def hello():
    return "<h1><font color='red'>The First Python Program of Agnes</font></h1><h3>16.04.2018</h3><p style='font-size:120px'>Hello, <bold>Agnes</bold>, I'm tram/bus Nr <span style='color:pink;font-size:120px'>" + str(random.randint(1,46)) + "</span>!<p>"
