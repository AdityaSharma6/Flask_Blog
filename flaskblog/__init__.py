from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config["SECRET_KEY"] = "6f46279c17c9e1969a06a9cf83f1fd57" # Safety Code. Helps with security. It is liked with {{ form.hidden_tag() }}
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db" # Can specify aa relative path with 3 forward slashes and uri
db = SQLAlchemy(app) # Create a database. Represent db structure as classes (models). It is intuitive
bcrypt = Bcrypt(app)
LoginManager = LoginManager(app) # Adds db functionality in background

# In the __init__ file, you can import variables: from flaskblog import app, db, bcrypt
from flaskblog import routes