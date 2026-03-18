# ============================================================
# BOOKMARKS API — Your First Backend Project
# ============================================================
# This is a REST API that lets users create, read, update,
# delete, and search bookmarks. Data is stored permanently
# in a SQLite database.
#
# To run: python3 app.py
# To test: use curl commands or visit URLs in your browser
# ============================================================


# --- IMPORTS ---
# Flask: the framework that creates our web server
# jsonify: converts Python dictionaries/lists into JSON format
#          (JSON is the standard format APIs use to send data)
# request: lets us read data that the client sends to us
#          - request.json reads the body of POST/PUT requests
#          - request.args reads query parameters from the URL (?key=value)
from flask import Flask, jsonify, request

# SQLAlchemy: the translator between Python and the database
# It lets us use Python code instead of writing raw SQL commands
from flask_sqlalchemy import SQLAlchemy


# --- APP SETUP ---
# Create the Flask application (this is our server)
app = Flask(__name__)

# Tell Flask where the database file lives
# "sqlite:///bookmarks.db" means: use SQLite, store data in a file
# called bookmarks.db in the current folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bookmarks.db"

# Create the SQLAlchemy connection to our database
# We'll use 'db' to interact with the database throughout the app
db = SQLAlchemy(app)


# --- DATABASE MODEL ---
# A model is a Python class that describes a table in the database.
# Think of it as designing a spreadsheet — you define the columns,
# what type of data each column holds, and any rules.
#
# This creates a table that looks like:
# | id (auto) | title (text, required) | url (text, required) |
# |-----------|------------------------|----------------------|
#
# db.Model in parentheses means: this class inherits database
# abilities from SQLAlchemy. Without it, the class would just be
# a regular Python object with no connection to the database.
class Bookmark(db.Model):
    # id: a number that uniquely identifies each bookmark
    # primary_key=True means:
    #   - every bookmark gets a unique id automatically (1, 2, 3...)
    #   - this is how we find specific bookmarks in the database
    id = db.Column(db.Integer, primary_key=True)

    # title: text up to 100 characters
    # nullable=False means this field cannot be blank — every
    # bookmark must have a title
    title = db.Column(db.String(100), nullable=False)

    # url: text up to 200 characters
    # nullable=False means this field cannot be blank either
    url = db.Column(db.String(200), nullable=False)


# --- CREATE THE DATABASE TABLE ---
# This looks at all our models (just Bookmark for now) and creates
# the actual tables in the database file. If the table already
# exists, it skips it — safe to run every time.
with app.app_context():
    db.create_all()


# ============================================================
# ROUTES — Each route handles a different type of request
# ============================================================
# Our API follows the REST pattern:
#   GET    /bookmarks          → read all bookmarks
#   GET    /bookmarks/search   → search bookmarks by title
#   POST   /bookmarks          → create a new bookmark
#   PUT    /bookmarks/<id>     → update an existing bookmark
#   DELETE /bookmarks/<id>     → delete a bookmark
# ============================================================


# --- READ ALL BOOKMARKS ---
# Method: GET
# URL: /bookmarks
# What it does: returns every bookmark in the database
# Test: visit http://127.0.0.1:5000/bookmarks in your browser
@app.route("/bookmarks", methods=["GET"])
def get_bookmarks():
    # Bookmark.query.all() asks the database "give me every row
    # in the bookmarks table" — returns a list of Bookmark objects
    bookmarks = Bookmark.query.all()

    # The database gives us Bookmark objects, but we need to send
    # JSON to the client. So we convert each object into a dictionary.
    result = []
    for b in bookmarks:
        result.append({"id": b.id, "title": b.title, "url": b.url})

    # jsonify converts our Python list of dictionaries into JSON
    # and sends it back to the client
    return jsonify(result)


# --- SEARCH BOOKMARKS ---
# Method: GET
# URL: /bookmarks/search?q=something
# What it does: finds bookmarks where the title contains the search term
# Test: http://127.0.0.1:5000/bookmarks/search?q=Python
@app.route("/bookmarks/search", methods=["GET"])
def search_bookmarks():
    # request.args.get("q", "") reads the ?q= value from the URL
    # If the URL is /bookmarks/search?q=Python, then query = "Python"
    # If no ?q= is provided, query defaults to an empty string ""
    query = request.args.get("q", "")

    # If the search term is empty, tell the client they need to provide one
    # 400 status code means "bad request" — the client made an error
    if len(query) == 0:
        return jsonify({"error": "Please provide a search term with ?q=something"}), 400

    # Ask the database: "find all bookmarks where the title contains
    # this search term." .contains() does a partial match — so searching
    # for "Py" would match "Python Tutorial" and "Python Flask Guide"
    results = Bookmark.query.filter(Bookmark.title.contains(query)).all()

    # Convert results to dictionaries and return as JSON
    output = []
    for b in results:
        output.append({"id": b.id, "title": b.title, "url": b.url})
    return jsonify(output)


# --- CREATE A BOOKMARK ---
# Method: POST
# URL: /bookmarks
# What it does: saves a new bookmark to the database
# Test: curl -X POST http://127.0.0.1:5000/bookmarks -H "Content-Type: application/json" -d '{"title": "Google", "url": "https://google.com"}'
@app.route("/bookmarks", methods=["POST"])
def add_bookmark():
    # request.json reads the JSON body that the client sent
    # If the client sent {"title": "Google", "url": "https://google.com"},
    # then data["title"] is "Google" and data["url"] is "https://google.com"
    data = request.json

    # --- VALIDATION ---
    # Before saving anything, check that the data is correct.
    # Never trust the client — always validate.

    # Check 1: did the client send any data at all?
    if not data:
        return jsonify({"error": "No data provided"}), 400

    # Check 2: did the client include both required fields?
    if "title" not in data or "url" not in data:
        return jsonify({"error": "Both title and url are required"}), 400

    # Check 3: are the fields actually filled in (not empty strings)?
    if len(data["title"]) == 0 or len(data["url"]) == 0:
        return jsonify({"error": "Title and url cannot be empty"}), 400

    # --- SAVE TO DATABASE ---
    # Create a new Bookmark object from our model
    # The id is generated automatically by the database
    bookmark = Bookmark(title=data["title"], url=data["url"])

    # db.session.add() stages the bookmark for saving
    # Think of it as putting a letter in the mailbox
    db.session.add(bookmark)

    # db.session.commit() actually saves it to the database
    # Think of it as the mailman picking up the letter — now it's permanent
    db.session.commit()

    # Send back the created bookmark as confirmation
    # 201 status code means "created successfully"
    return jsonify({"id": bookmark.id, "title": bookmark.title, "url": bookmark.url}), 201


# --- UPDATE A BOOKMARK ---
# Method: PUT
# URL: /bookmarks/<id> (example: /bookmarks/1)
# What it does: changes the title and/or url of an existing bookmark
# Test: curl -X PUT http://127.0.0.1:5000/bookmarks/1 -H "Content-Type: application/json" -d '{"title": "New Title"}'
#
# <int:bookmark_id> is a dynamic route — the number in the URL gets
# captured and passed into the function. So /bookmarks/3 means
# bookmark_id = 3
@app.route("/bookmarks/<int:bookmark_id>", methods=["PUT"])
def update_bookmark(bookmark_id):
    # Ask the database: "find the bookmark where id equals this number"
    # If found, returns a Bookmark object. If not found, returns None.
    bookmark = Bookmark.query.get(bookmark_id)

    if bookmark:
        data = request.json

        if not data:
            return jsonify({"error": "No data provided"}), 400

        # data.get("title", bookmark.title) means:
        # "If the client sent a new title, use it.
        #  If they didn't, keep the existing title."
        # This lets the client update just one field without
        # having to resend everything.
        bookmark.title = data.get("title", bookmark.title)
        bookmark.url = data.get("url", bookmark.url)

        # Commit the changes to make them permanent
        db.session.commit()

        return jsonify({"id": bookmark.id, "title": bookmark.title, "url": bookmark.url})

    # If no bookmark was found with that id, return a 404 error
    # 404 means "not found"
    return jsonify({"error": "Bookmark not found"}), 404


# --- DELETE A BOOKMARK ---
# Method: DELETE
# URL: /bookmarks/<id> (example: /bookmarks/1)
# What it does: removes a bookmark from the database permanently
# Test: curl -X DELETE http://127.0.0.1:5000/bookmarks/1
@app.route("/bookmarks/<int:bookmark_id>", methods=["DELETE"])
def delete_bookmark(bookmark_id):
    # Find the bookmark by id
    bookmark = Bookmark.query.get(bookmark_id)

    if bookmark:
        # Remove it from the database
        db.session.delete(bookmark)
        # Save the change
        db.session.commit()
        return jsonify({"message": "Bookmark deleted"})

    return jsonify({"error": "Bookmark not found"}), 404


# --- START THE SERVER ---
# This turns the server on and starts listening for requests
# debug=True does two things:
#   1. Auto-restarts the server when you change the code
#   2. Shows detailed error messages when something breaks
# You would turn this off in production (when real users are using it)
app.run(debug=True)