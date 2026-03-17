from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/")
def home():
    return "The kitchen is open!"

@app.route("/greet")
def greet():
    name = request.args.get("name", "stranger")
    return jsonify({
        "message": f"Hello, {name}! Welcome to the backend."
    })

app.run(debug=True)


