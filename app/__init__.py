from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

# Add configuration to Flask via config object
app.config.from_object(Config)

# Create database instance
db = SQLAlchemy(app)

# Create Flask Migrate instance
migrate = Migrate(app, db)

from app import routes, models