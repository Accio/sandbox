from flask import Flask

webapp = Flask(__name__)

@webapp.route("/")
def home():
    return ("<h1>Hello</h1>")

@webapp.route("/user")
def user():
    user_dict = {'first': 'Jitao David', 'last': 'Zhang', 'email': 'jitao_david.zhang@roche.com'}

    html = """
    <dl>
      <dt>first name</dt>
      <dd>{first}</dd>
      <dt>Last name</dt>
      <dd>{last}</dd>
      <dt>E-mail</dt>
      <dd>{email}</dd>
    </dl>
    """.format(**user_dict)

    return html


	
