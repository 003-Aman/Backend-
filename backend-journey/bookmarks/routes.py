from flask import Blueprint, jsonify, request
from models import db, Bookmark
from middleware import get_logged_in_user

bookmarks_bp = Blueprint("bookmarks", __name__)


def bookmark_to_dict(b):
    return {
        "id": b.id,
        "title": b.title,
        "url": b.url,
        "tags": b.tags.split(",") if b.tags else []
    }


@bookmarks_bp.route("/bookmarks", methods=["GET"])
def get_bookmarks():
    user = get_logged_in_user()
    if not user:
        return jsonify({"error": "You must be logged in"}), 401
    tag = request.args.get("tag", "")
    if tag:
        bookmarks = Bookmark.query.filter(
            Bookmark.user_id == user["user_id"],
            Bookmark.tags.contains(tag)
        ).all()
    else:
        bookmarks = Bookmark.query.filter_by(user_id=user["user_id"]).all()
    result = []
    for b in bookmarks:
        result.append(bookmark_to_dict(b))
    return jsonify(result)


@bookmarks_bp.route("/bookmarks/search", methods=["GET"])
def search_bookmarks():
    user = get_logged_in_user()
    if not user:
        return jsonify({"error": "You must be logged in"}), 401
    query = request.args.get("q", "")
    if len(query) == 0:
        return jsonify({"error": "Please provide a search term with ?q=something"}), 400
    results = Bookmark.query.filter(
        Bookmark.user_id == user["user_id"],
        Bookmark.title.contains(query)
    ).all()
    output = []
    for b in results:
        output.append(bookmark_to_dict(b))
    return jsonify(output)


@bookmarks_bp.route("/bookmarks", methods=["POST"])
def add_bookmark():
    user = get_logged_in_user()
    if not user:
        return jsonify({"error": "You must be logged in"}), 401
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    if "title" not in data or "url" not in data:
        return jsonify({"error": "Both title and url are required"}), 400
    if len(data["title"]) == 0 or len(data["url"]) == 0:
        return jsonify({"error": "Title and url cannot be empty"}), 400
    tags = ",".join(data.get("tags", []))
    bookmark = Bookmark(
        title=data["title"],
        url=data["url"],
        user_id=user["user_id"],
        tags=tags
    )
    db.session.add(bookmark)
    db.session.commit()
    return jsonify(bookmark_to_dict(bookmark)), 201


@bookmarks_bp.route("/bookmarks/<int:bookmark_id>", methods=["PUT"])
def update_bookmark(bookmark_id):
    user = get_logged_in_user()
    if not user:
        return jsonify({"error": "You must be logged in"}), 401
    bookmark = Bookmark.query.get(bookmark_id)
    if not bookmark:
        return jsonify({"error": "Bookmark not found"}), 404
    if bookmark.user_id != user["user_id"]:
        return jsonify({"error": "This is not your bookmark"}), 403
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    bookmark.title = data.get("title", bookmark.title)
    bookmark.url = data.get("url", bookmark.url)
    if "tags" in data:
        bookmark.tags = ",".join(data["tags"])
    db.session.commit()
    return jsonify(bookmark_to_dict(bookmark))


@bookmarks_bp.route("/bookmarks/<int:bookmark_id>", methods=["DELETE"])
def delete_bookmark(bookmark_id):
    user = get_logged_in_user()
    if not user:
        return jsonify({"error": "You must be logged in"}), 401
    bookmark = Bookmark.query.get(bookmark_id)
    if not bookmark:
        return jsonify({"error": "Bookmark not found"}), 404
    if bookmark.user_id != user["user_id"]:
        return jsonify({"error": "This is not your bookmark"}), 403
    db.session.delete(bookmark)
    db.session.commit()
    return jsonify({"message": "Bookmark deleted"})
