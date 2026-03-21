from flask import Blueprint, jsonify, request
from models import db, Bookmark

bookmarks_bp = Blueprint("bookmarks", __name__)

@bookmarks_bp.route("/bookmarks", methods=["GET"])
def get_bookmarks():
    bookmarks = Bookmark.query.all()
    result = []
    for b in bookmarks:
        result.append({"id": b.id, "title": b.title, "url": b.url})
    return jsonify(result)

@bookmarks_bp.route("/bookmarks/search", methods=["GET"])
def search_bookmarks():
    query = request.args.get("q", "")
    if len(query) == 0:
        return jsonify({"error": "Please provide a search term with ?q=something"}), 400
    results = Bookmark.query.filter(Bookmark.title.contains(query)).all()
    output = []
    for b in results:
        output.append({"id": b.id, "title": b.title, "url": b.url})
    return jsonify(output)

@bookmarks_bp.route("/bookmarks", methods=["POST"])
def add_bookmark():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    if "title" not in data or "url" not in data:
        return jsonify({"error": "Both title and url are required"}), 400
    if len(data["title"]) == 0 or len(data["url"]) == 0:
        return jsonify({"error": "Title and url cannot be empty"}), 400
    bookmark = Bookmark(title=data["title"], url=data["url"])
    db.session.add(bookmark)
    db.session.commit()
    return jsonify({"id": bookmark.id, "title": bookmark.title, "url": bookmark.url}), 201

@bookmarks_bp.route("/bookmarks/<int:bookmark_id>", methods=["PUT"])
def update_bookmark(bookmark_id):
    bookmark = Bookmark.query.get(bookmark_id)
    if bookmark:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
        bookmark.title = data.get("title", bookmark.title)
        bookmark.url = data.get("url", bookmark.url)
        db.session.commit()
        return jsonify({"id": bookmark.id, "title": bookmark.title, "url": bookmark.url})
    return jsonify({"error": "Bookmark not found"}), 404

@bookmarks_bp.route("/bookmarks/<int:bookmark_id>", methods=["DELETE"])
def delete_bookmark(bookmark_id):
    bookmark = Bookmark.query.get(bookmark_id)
    if bookmark:
        db.session.delete(bookmark)
        db.session.commit()
        return jsonify({"message": "Bookmark deleted"})
    return jsonify({"error": "Bookmark not found"}), 404
