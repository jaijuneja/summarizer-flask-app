from flask import Blueprint, render_template

news = Blueprint('news', __name__)


@news.route('/')
def index():
    return render_template('news/index.html')