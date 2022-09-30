import os
from turtle import back

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
# from flask_mail import Mail, Message

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Configure mail class
# mail = Mail(app)

# Configure mail server
# app.config['MAIL_SERVER'] = 'smtp-mail.outlook.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USERNAME'] = 'purryadopt@outlook.com'
# app.config['MAIL_PASSWORD'] = 'ccacacacaca!10Oct'
# app.config['MAIL_USE_TLS'] = True
# mail = Mail(app)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///adoption.db") 

# Forbidden characters global variable
forbidden_characters = [";","?", "/","'","*","%",":","$","-","+",">","<","=","~","&","|", "#","^"]

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    """Main page for all visitos"""
    
    # This index will only use GET method
    return render_template("index.html")



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Check user input
    if request.method == "POST":

        # Get username & password
        username = request.form.get('username')
        password = request.form.get('password') 
        email = request.form.get('email')

        # Validation against forbidden characters
        for i in range(len(forbidden_characters)):
            if forbidden_characters[i] in username:
                return apology("Character(s) not allowed - username", 400)
            elif forbidden_characters[i] in password:
                return apology("Character(s) not allowed - password", 400)
            elif forbidden_characters[i] in email:
                return apology("Character(s) not allowed - email", 400)

        # Length of username and password and email
        if len(username) < 5 or len(username) > 20:
            return apology("Username length must be between 5 and 20 characters", 400)
        elif len(password) < 9 or len(password) > 20:
            return apology("Password must be between 9 and 20 characters", 400)
        elif len(email) < 3:
            return apology("Please provide a valid email address", 400)

        # Check for existing account
        username_existence = db.execute("SELECT username FROM users WHERE username=?", username)
        email_existance = db.execute("SELECT email FROM users WHERE email=?", email)

        if username_existence:
            return apology("Username already taken", 400)
        elif email_existance:
            return apology("Email already in use", 400)

        # Password validation

        

        # Email validation


        # Database insertion

        # Set up automatic registration  mail

        # !!! Try to send verification link as well! !!!
        # mail_msg = Message("Welcome to Purry Adoption!", sender='purryadopt@outlook.com', recipients=[email])
        # mail_msg.body = "Thank you for joining us! Your username is: " + username + " and your password is: " + password + " . Please hold onto them carefully!"
        
        # mail.send(mail_msg)

        # Redirect user to home page (this will have to be index) -- once I add it
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")



# @app.route("/login", methods=["GET", "POST"])
# def login():
#     """Log user in"""

#     # Forget any user_id
#     session.clear()

#     # User reached route via POST (as by submitting a form via POST)
#     if request.method == "POST":

#         # Ensure username was submitted
#         if not request.form.get("username"):
#             return apology("must provide username", 403)

#         # Ensure password was submitted
#         elif not request.form.get("password"):
#             return apology("must provide password", 403)

#         # Query database for username
#         rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

#         # Ensure username exists and password is correct
#         if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
#             return apology("invalid username and/or password", 403)

#         # Remember which user has logged in
#         session["user_id"] = rows[0]["id"]

#         # Redirect user to home page
#         return redirect("/")

#     # User reached route via GET (as by clicking a link or via redirect)
#     else:
#         return render_template("login.html")

# @app.route("/logout")
# def logout():
#     """Log user out"""

#     # Forget any user_id
#     session.clear()

#     # Redirect user to login form
#     return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)