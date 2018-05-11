from flask import (
        Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flasktd.auth import login_required
from flasktd.db import get_db

bp = Blueprint('todo', __name__)


