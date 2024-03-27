from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

# Add the following line:
import models

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Run the following command to create the migration:
flask db migrate -m "create task table";

# Run the following command to apply the migration to the database:
flask db upgrade;

# Add the following lines:
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Run the following command to create the migrations folder:
flask db init;