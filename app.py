import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from sqlalchemy import false
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
forbidden_characters = ["!",";","?", "/","'","*","%",":","$","-","+",">","<","=","~","&","|","#","^"]

# Forbidden characters in comments specifically
forbidden_comment_characters = ["'","*","%", "$","-","+",">","<","=","~","&","|","#","^"]

# Email characters
email_characters = ["@", "."]

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

@app.route("/one_time_donation", methods=["GET", "POST"])
def one_time_donation():

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST": 
        
        

        return render_template("/one_time_donation.html")

    # User reached route via GET (as by clicking a link or via redirect)
    else:        
        return render_template("/one_time_donation.html")


@app.route("/regular_donations", methods=["GET", "POST"])
def regulalr_donations():

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST": 
        
        

        return render_template("/regular_donations.html")

    # User reached route via GET (as by clicking a link or via redirect)
    else:        
        return render_template("/regular_donations.html")


@app.route("/TwoPercent_donation", methods=["GET", "POST"])
def TwoPercent_donation():

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST": 
        
        

        return render_template("/TwoPercent_donation.html")

    # User reached route via GET (as by clicking a link or via redirect)
    else:        
        return render_template("/TwoPercent_donation.html")



@app.route("/donations", methods=["GET", "POST"])
def donations():
    """Page where user can make three different donations types"""
    
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST": 
        
        

        return render_template("/donations.html")

    # User reached route via GET (as by clicking a link or via redirect)
    else:        
        return render_template("/donations.html")

@app.route("/news/purry-nobel-prize-nomenee", methods=["GET", "POST"])
def news_setup():
    """Setup of how every individual news page will work"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST": 

        # Get necessary info/input
        user = session["user_id"]
        
        comment = request.form.get('comment')

        # Filter comment input
        for i in range(len(forbidden_comment_characters)):
            if forbidden_comment_characters[i] in comment:
                return apology("Charcater not allowed: " + forbidden_comment_characters[i], 403)

        # Insert email, user ID and the comment itself, into the DB
        
        # Get email 
        email = db.execute("SELECT email FROM users WHERE id=?", user)

        email = email[0]['email']

        # Get username
        username = db.execute("SELECT username FROM users WHERE id=?", user)
        
        username = username[0]['username']

        # Update DB
        db.execute("INSERT INTO comments (user_id, username, email, comment) VALUES(?,?,?,?)", user, username, email, comment)

        # Get all comments' and their range range
        comments = db.execute("SELECT * FROM comments")

        r = int(len(comments))

        # Return page
        return render_template("/news/purry-nobel-prize-nomenee.html", comments=comments, r=r)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        # Get all comments' and their range range -- This is an unorhodox bug fix, the app wouldn't show the comments due to the Jinka syntax
        # When requested via Get, but it would, when requested via POST only.
        comments = db.execute("SELECT * FROM comments")

        r = int(len(comments))
        
        return render_template("/news/purry-nobel-prize-nomenee.html", comments=comments, r=r)


@app.route("/news", methods=["GET", "POST"])
def news():
    """News about the foundation, newsletter and comments!"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST": 

        # Get email
        email = request.form.get('email')

        # Email validation
        for i in range(len(email_characters)):
            if email_characters[i] not in email:
                return apology("Provide valid email address", 400)
        
        for i in range(len(forbidden_characters)):
            if forbidden_characters[i] in email:
                return apology("Character(s) not allowed", 400)

        # Storage
        db.execute("INSERT INTO newsletter (email) VALUES(?)", email)

        # Validation and storage complete, send confirmation email
        # mail_msg = Message("Welcome to Purry-Newsletter! Automated email, please do not reply!", sender='purryadopt@outlook.com', recipients=[email])
        # mail_msg.body = "Thank you for subscribing to our newsletter! Now you will be able to see our latest updates in real time!" 
        
        # mail.send(mail_msg)

        return render_template("news.html")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("news.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Get username & password & confirmation & email
        username = request.form.get('username')
        password = request.form.get('password') 
        confirmation = request.form.get('confirmation')
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
        if password != confirmation:
            return apology("Passwords do not match", 400)
        elif password == username:
            return apology("Password and username must not match", 400)
        
        # Email validation
        for i in range(len(email_characters)):
            if email_characters[i] not in email:
                return apology("Provide valid email address", 400)

        for i in range(len(forbidden_characters)):
            if forbidden_characters[i] in email:
                return apology("Character(s) not allowed", 400)

        # Generate password hash
        pwhash = generate_password_hash(password)
                
        # Add user to database
        db.execute("INSERT INTO users (username, hash, email) VALUES(?,?,?)", username, pwhash, email)

        # Remember which user has logged in
        new_user = db.execute("SELECT * FROM users WHERE username IS ?", username)

        session["user_id"] = new_user[0]["id"]

        # Set up automatic registration  mail

        # !!! Try to send verification link as well! !!!
        # mail_msg = Message("Welcome to Purry Adoption! Automate email. Please do not reply!", sender='purryadopt@outlook.com', recipients=[email])
        # mail_msg.body = "Thank you for joining us! Your username is: " + username + " and your password is: " + password + " . Please hold onto them carefully!"
        
        # mail.send(mail_msg)

        # Redirect user to home page (index)
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Get auth information
        username = request.form.get('username')
        password = request.form.get('password')

        # Ensure username/email was submitted
        if not username:
            return apology("Must provide username or email", 400)

        # Ensure password was submitted
        elif not password:
            return apology("must provide password", 400)

        # Query database for username and email
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

         # Ensure username/email exists and password is correct
        if (len(rows) != 1 or not check_password_hash(rows[0]["hash"], password)):
            return apology("invalid username/email and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/my_account", methods=["GET", "POST"])
@login_required
def my_account():
    """Users can view and interact with their account"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        

        return render_template("my_account.html")
    
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("my_account.html")

@app.route("/change_pass", methods=["GET", "POST"])
@login_required
def change_pass():
    """Allow users to change their password"""
    
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Get user ID
        user = session["user_id"]

        # Get password items for validation
        rows = db.execute("SELECT * FROM users WHERE id=?", user)
        
        actual_pass_hash = request.form.get('actual_pass')
        new_pass = request.form.get("new_pass")
        confirm_new_pass = request.form.get("confirm_new_pass")

        # Validate:

        # Check if actual password is correct
        if not check_password_hash(rows[0]["hash"], actual_pass_hash):
            return apology("Incorrect actual password", 403)
        
        # Check password's length
        elif len(new_pass) < 9 or len(new_pass) > 20:
            return apology("Password must be between 9 and 20 characters", 400)
            
        # Check password for forbidden characters
        for i in range(len(forbidden_characters)):
            if forbidden_characters[i] in new_pass:
                return apology("Character(s) not allowed - password", 400)

        # Check if 'New Password' and 'Confirm New Password' match
        if new_pass != confirm_new_pass:
            return apology("Passwords must match", 403)


        # Generate password hash for checking against current hash
        pwhash = generate_password_hash(new_pass)

        # Update old password hash with new
        db.execute("UPDATE users SET hash=? WHERE id =?", pwhash, user)

        return render_template("change_pass.html")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("change_pass.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


if __name__ == '__main__':
    print("I am being run directly")
    app.run(debug=True)
else:
    print("I am being imported")