# Birthdays

A lightweight birthday tracker built with **Python + Flask** and **SQLite**, with a clean, responsive UI using **HTML/CSS** (Tailwind styles). Add birthdays, view the full list, and update entries with simple server-side validation.

## Live Demo

- https://birthdays-il22.onrender.com/

## Features

- Add and view birthday records
- Edit/update existing birthdays
- SQLite persistence (`birthdays.db`)
- Server-rendered pages using Jinja templates
- Input validation (required fields + valid month/day ranges)
- Responsive UI

## Tech Stack

- **Backend:** Python, Flask
- **Database:** SQLite (via `cs50` SQL helper)
- **Templating:** Jinja2
- **Frontend:** HTML, CSS (Tailwind)

## Getting Started (Local)

### 1) Install dependencies

```bash
pip install -r requirements.txt
```

### 2) Run the app

```bash
flask run
```

Then open the local URL shown in your terminal (usually `http://127.0.0.1:5000`).

## Project Structure (high level)

- `app.py` — Flask application, routes, validation, database queries
- `templates/` — Jinja templates (e.g., `index.html`)
- `static/` — CSS and other static assets
- `birthdays.db` — SQLite database file

## Notes

This project follows a simple CRUD pattern and is easy to extend with features like delete, search/filtering, reminders/notifications, or user accounts.
