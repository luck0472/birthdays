"""Birthdays Flask application."""

from cs50 import SQL
from flask import Flask, redirect, render_template, request

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")


# Validation rules
MONTH_DAY_LIMITS = {
    1: 31,
    2: 29,
    3: 31,
    4: 30,
    5: 31,
    6: 30,
    7: 31,
    8: 31,
    9: 30,
    10: 31,
    11: 30,
    12: 31,
}

REQUIRED_FIELDS_ERROR = "Please enter name, month, and day."


def validate_month_and_day(month_text, day_text):
    """Validate month/day values and return normalized integers."""
    try:
        month = int(month_text)
        day = int(day_text)
    except (TypeError, ValueError):
        return "Month and day must be numbers.", None, None

    if month not in MONTH_DAY_LIMITS:
        return "Month must be between 1 and 12.", None, None

    max_day = MONTH_DAY_LIMITS[month]
    if day < 1 or day > max_day:
        return f"Day must be between 1 and {max_day} for month {month}.", None, None

    return None, month, day


def parse_birthday_form(form):
    """Read and trim birthday fields from a submitted form."""
    return (
        form.get("name", "").strip(),
        form.get("month", "").strip(),
        form.get("day", "").strip(),
    )


def validate_birthday_input(name, month, day):
    """Validate birthday input fields and return normalized values."""
    if not name or not month or not day:
        return REQUIRED_FIELDS_ERROR, None, None

    return validate_month_and_day(month, day)


def get_edit_row(edit_id):
    """Fetch a single birthday row for edit mode."""
    if edit_id is None:
        return None

    edit_rows = db.execute("SELECT * FROM birthdays WHERE id = ?", edit_id)
    if len(edit_rows) == 1:
        return edit_rows[0]

    return None


def render_home(error=None, edit_row=None):
    """Render the home page with optional error and edit row context."""
    rows = db.execute("SELECT * FROM birthdays")
    return render_template(
        "index.html",
        rows=rows,
        edit_row=edit_row,
        error=error,
        month_day_limits=MONTH_DAY_LIMITS,
    )


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    """Show all birthdays and handle add birthday form submissions."""
    if request.method == "POST":
        name, month, day = parse_birthday_form(request.form)

        error, month_value, day_value = validate_birthday_input(name, month, day)
        if error:
            return render_home(error=error)

        db.execute(
            "INSERT into birthdays (name, month, day) values(?, ?, ?)",
            name,
            month_value,
            day_value,
        )

        return redirect("/")

    edit_id = request.args.get("edit_id", type=int)
    return render_home(edit_row=get_edit_row(edit_id))


@app.route("/update", methods=["POST"])
def update():
    """Handle birthday updates from the edit modal."""
    birthday_id = request.form.get("id", "").strip()
    name, month, day = parse_birthday_form(request.form)

    try:
        birthday_id_value = int(birthday_id)
    except (TypeError, ValueError):
        return redirect("/")

    edit_row = {
        "id": birthday_id_value,
        "name": name,
        "month": month,
        "day": day,
    }

    error, month_value, day_value = validate_birthday_input(name, month, day)
    if error:
        return render_home(error=error, edit_row=edit_row)

    db.execute(
        "UPDATE birthdays SET name = ?, month = ?, day = ? WHERE id = ?",
        name,
        month_value,
        day_value,
        birthday_id_value,
    )

    return redirect("/")


@app.route("/delete", methods=["POST"])
def delete():
    """Delete a birthday by its id."""
    birthday_id = request.form.get("id")

    db.execute("DELETE FROM birthdays WHERE id = ?", birthday_id)

    return redirect("/")

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)