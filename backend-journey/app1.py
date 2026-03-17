from flask import Flask, jsonify, request # 

app = Flask(__name__)

bookmarks = []

@app.route("/bookmarks", methods=["GET"])
def get_bookmarks():
    return jsonify(bookmarks)

@app.route("/bookmarks", methods=["POST"])
def add_bookmark():
    data = request.json
    bookmark = {
        "id": len(bookmarks) + 1,
        "title": data["title"],
        "url": data["url"]
    }
    bookmarks.append(bookmark)
    return jsonify(bookmark), 201

@app.route("/bookmarks/<int:bookmark_id>", methods=["DELETE"])
def delete_bookmark(bookmark_id):
    for bookmark in bookmarks:
        if bookmark["id"] == bookmark_id:
            bookmarks.remove(bookmark)
            return jsonify({"message": "Bookmark deleted"})
    return jsonify({"error": "Bookmark not found"}), 404

@app.route("/bookmarks/<int:bookmark_id>", methods=["PUT"])
def update_bookmark(bookmark_id):
    data = request.json
    for bookmark in bookmarks:
        if bookmark["id"] == bookmark_id:
            bookmark["title"] = data.get("title", bookmark["title"])
            bookmark["url"] = data.get("url", bookmark["url"])
            return jsonify(bookmark)
    return jsonify({"error": "Bookmark not found"}), 404

app.run(debug=True)