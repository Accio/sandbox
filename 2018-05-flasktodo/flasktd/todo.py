from flask import (
        Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flasktd.auth import login_required
from flasktd.db import get_db

bp = Blueprint('todo', __name__)

@bp.route('/')
def index():
    db = get_db()
    todos = db.execute(
        'SELECT t.id, name, description, created, deadline, user_id, user_name'
        ' FROM todo t JOIN user u ON t.user_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('todo/index.html', todos=todos)

