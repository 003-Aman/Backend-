# This file answers ONE question: "How does everything connect?"
# It doesn't handle any requests itself.
# It just creates the server, plugs things in, and starts listening.

from flask import Flask

from models import db
# The database tool from models.py

from bookmarks.routes import bookmarks_bp
# The bookmarks department from bookmarks/routes.py
# "bookmarks.routes" = go into bookmarks folder, open routes.py

from auth.routes import auth_bp, bcrypt
# The auth department + password tool from auth/routes.py


app = Flask(__name__)
# Create the server

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bookmarks.db"
# "Store the database in a file called bookmarks.db"


# --- CONNECT TOOLS ---
# These were created with empty parentheses in their files
# Now we connect them to the app

db.init_app(app)
# "Database, meet the app"

bcrypt.init_app(app)
# "Bcrypt, meet the app"


# --- PLUG IN BLUEPRINTS ---
# Like installing apps on a phone
# Without these lines, the routes exist but the server ignores them

app.register_blueprint(bookmarks_bp)
# All bookmark routes are now live

app.register_blueprint(auth_bp)
# All auth routes are now live


# --- CREATE TABLES ---
with app.app_context():
    db.create_all()
# Look at all models (User, Bookmark)
# Create their tables in the database if they don't exist yet


# --- START ---
app.run(debug=True, port=8000)
# Turn on the server on port 8000
# (port 5000 was taken by AirPlay on your Mac)