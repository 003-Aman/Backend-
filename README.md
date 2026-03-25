# Bookmarks REST API

A backend API for managing bookmarks with user authentication, tags, and protected routes.

**Live URL:** https://kaizen-bookmarks-api.onrender.com

## What it does

Users can sign up, log in, and manage their own personal bookmarks. Each bookmark can have tags for easy filtering. All routes are protected — you need a valid token to access your data.

## Tech Stack

- Python
- Flask
- SQLAlchemy (ORM)
- SQLite (Database)
- Bcrypt (Password hashing)
- JWT (Authentication tokens)
- Gunicorn (Production server)
- Render (Deployment)

## API Endpoints

| Method | URL | What it does |
|--------|-----|-------------|
| POST | /signup | Create a new account |
| POST | /login | Log in and receive a token |
| GET | /bookmarks | Get your bookmarks |
| GET | /bookmarks?tag=python | Filter bookmarks by tag |
| GET | /bookmarks/search?q=flask | Search bookmarks by title |
| POST | /bookmarks | Create a new bookmark |
| PUT | /bookmarks/:id | Update a bookmark |
| DELETE | /bookmarks/:id | Delete a bookmark |

## How to run locally
```bash
git clone https://github.com/003-Aman/Backend-.git
cd backend-journey
pip install -r requirements.txt
python app.py
```

## Example usage

Sign up:
```bash
curl -X POST http://127.0.0.1:8000/signup -H "Content-Type: application/json" -d '{"username": "testuser", "password": "password123"}'
```

Log in:
```bash
curl -X POST http://127.0.0.1:8000/login -H "Content-Type: application/json" -d '{"username": "testuser", "password": "password123"}'
```

Create a bookmark (use token from login):
```bash
curl -X POST http://127.0.0.1:8000/bookmarks -H "Content-Type: application/json" -H "Authorization: YOUR_TOKEN" -d '{"title": "Google", "url": "https://google.com", "tags": ["search", "tools"]}'
```

## Features

- Secure password hashing with Bcrypt
- JWT token authentication with 24-hour expiration
- User-owned bookmarks — your data is private
- Tag system with filtering
- Input validation on all routes
- Organized codebase with Flask Blueprints
```

