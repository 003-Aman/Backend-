#WITH SQLITE NOW WE COME TO DATABASES

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bookmarks.db"
db = SQLAlchemy(app)

class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(200), nullable=False)

with app.app_context():
    db.create_all()

@app.route("/bookmarks", methods=["GET"])
def get_bookmarks():
    bookmarks = Bookmark.query.all()
    result = []
    for b in bookmarks:
        result.append({"id": b.id, "title": b.title, "url": b.url})
    return jsonify(result)

@app.route("/bookmarks", methods=["POST"])
def add_bookmark():
    data = request.json
    bookmark = Bookmark(title=data["title"], url=data["url"])
    db.session.add(bookmark)
    db.session.commit()
    return jsonify({"id": bookmark.id, "title": bookmark.title, "url": bookmark.url}), 201

@app.route("/bookmarks/<int:bookmark_id>", methods=["DELETE"])
def delete_bookmark(bookmark_id):
    bookmark = Bookmark.query.get(bookmark_id)
    if bookmark:
        db.session.delete(bookmark)
        db.session.commit()
        return jsonify({"message": "Bookmark deleted"})
    return jsonify({"error": "Bookmark not found"}), 404

@app.route("/bookmarks/<int:bookmark_id>", methods=["PUT"])
def update_bookmark(bookmark_id):
    bookmark = Bookmark.query.get(bookmark_id)
    if bookmark:
        data = request.json
        bookmark.title = data.get("title", bookmark.title)
        bookmark.url = data.get("url", bookmark.url)
        db.session.commit()
        return jsonify({"id": bookmark.id, "title": bookmark.title, "url": bookmark.url})
    return jsonify({"error": "Bookmark not found"}), 404

app.run(debug=True)