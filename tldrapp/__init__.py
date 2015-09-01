from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from cache import cache
from helpers import pretty_date

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Database
db = SQLAlchemy(app)

# Cache
cache.init_app(app)

# Error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('errors/404.html'), 404

# Add jinja helpers
app.jinja_env.globals.update(pretty_date=pretty_date)

from .views.home import home
from .views.quickipedia import quickipedia
from .views.news import news

# Register blueprint(s)
app.register_blueprint(home)
app.register_blueprint(quickipedia, url_prefix='/quickipedia')
app.register_blueprint(news, url_prefix='/news')

# Build the database:
db.create_all()