from flask import Flask, request, jsonify
from models import *
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate
import flask_excel as excel
from celery import Celery
from celery.schedules import crontab
from caching import cache
from worker import celery_init_app
from jinja2 import Template
from user_routes import user
from admin_routes import admin
from tasks import *
import os

app = Flask(__name__)

CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///LMS_v2_DB.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.app_context().push()
db.init_app(app)
migrate = Migrate(app, db) # Flask migrate config

# JWT authentication configuration
app.config['JWT_SECRET_KEY'] = os.urandom(24)
jwt = JWTManager(app)

# Managing blueprints to separate routes
app.register_blueprint(user, url_prefix="/api")
app.register_blueprint(admin, url_prefix="/api")

# Configuring Flask Cache using Redis
app.config["DEBUG"] = True
app.config['CACHE_TYPE'] = 'RedisCache'
app.config['CACHE_REDIS_HOST'] = 'localhost'
app.config['CACHE_REDIS_PORT'] = 6379
app.config['CACHE_REDIS_DB'] = 0
app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/0'
app.config["CACHE_DEFAULT_TIMEOUT"]= 300
cache.init_app(app) # Initialize cache

# Configuring celery to perform asynchoronous backend jobs
# Command to run celery worker: celery -A app:celery_app worker -l INFO
celery_app = celery_init_app(app)

# Configuring Flask Excel
excel.init_excel(app)

# Configuring CeleryBeat to perform tasks automatically
@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(hour=18, minute=53), daily_reminder.s(), name='add every 10')
    sender.add_periodic_task(crontab(minute=0, hour=0, day_of_month='1'), monthly_report.s(datetime.now().month - 1),  name="hello")


if __name__ == "__main__":
    app.run(debug=True)

# python3 app.py 
# celery -A app:celery_app worker -l INFO
# celery -A app:celery_app beat -l INFO
# ~/go/bin/MailHog
