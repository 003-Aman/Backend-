from flask import Flask
from models import db
from bookmarks.routes import bookmarks_bp
from auth.routes import auth_bp, bcrypt

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bookmarks.db"

db.init_app(app)
bcrypt.init_app(app)

app.register_blueprint(bookmarks_bp)
app.register_blueprint(auth_bp)

with app.app_context():
    db.create_all()

app.run(debug=True, port =8000)
'''

**Run it:**
```
rm -f bookmarks.db
python3 app.py
```

**Test it:**
```
curl -X POST http://127.0.0.1:5000/signup -H "Content-Type: application/json" -d '{"username": "kaizen", "password": "mypassword123"}'
'''