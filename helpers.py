from flask import redirect, render_template, request, session
from functools import wraps


# Creating my own methods for simplyfing code and avoding copy & paste in app.py
def email_validation(email, email_characters):
    """Email validation"""

    for i in range(len(email_characters)):
        if email_characters[i] not in email:
            return 1
        
    return 0

def input_validation(input, forbidden_characters):
    """Validate any input against forbidden characters"""

    for i in range(len(forbidden_characters)):
            if forbidden_characters[i] in input:
                return 1

    return 0

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

