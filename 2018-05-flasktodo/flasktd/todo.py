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
        'SELECT t.id, name, description, created, deadline, user_id, username'
        ' FROM todo t JOIN user u ON t.user_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('todo/index.html', todos=todos)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        deadline = request.form['deadline']
        error = None

        if not name:
            error = 'Name is required'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                    'INSERT INTO todo (name, description, deadline, user_id)'
                    ' VALUES (?, ?, ?, ?)',
                    (name, description, deadline, g.user['id'])
            )
            db.commit()
            return redirect(url_for('todo.index'))
    return render_template('todo/create.html')

def get_todo(id, check_author=True):
    todo = get_db().execute(
                'SELECT t.id, name, description, deadline, created,'
                'user_id, username'
                ' FROM todo t JOIN user u ON t.user_id = u.id'
                ' WHERE t.id = ?',
            (id,)
            ).fetchone()

    if todo is None:
        abort(404, 'Todo id {0} does not exist'.format(id))

    if check_author and todo['user_id'] !=g.user['id']:
        abort(403)

    return todo 

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    todo = get_todo(id)

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        deadline = request.form['deadline']
        error = None

        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE todo SET name = ?, description = ?, deadline = ?'
                ' WHERE id = ?',
                (name, description, deadline, id)
            )
            db.commit()
            return redirect(url_for('todo.index'))

    return render_template('todo/update.html', todo=todo)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_todo(id)
    db = get_db()
    db.execute('DELETE FROM todo WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('todo.index'))
