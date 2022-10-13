# from hashlib import blake2b
# import os
# from tkinter import S 

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from sqlalchemy import false
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from flask_mail import Mail, Message

from helpers import apology, login_required, email_validation, input_validation

# Configure application
app = Flask(__name__)

# Configure mail server
app.config['MAIL_SERVER'] = 'smtp-mail.outlook.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'purryadopt@outlook.com'
app.config['MAIL_PASSWORD'] = 'ccacacacaca!10Oct'
app.config['MAIL_USE_TLS'] = True
mail = Mail(app)


# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///adoption.db") 

# Forbidden characters global variable
forbidden_characters = ["!",";","?", "/","'","*","%",":","$",">","<","=","~","&","|","#","^"]

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


@app.route("/donations", methods=["GET"])
def donations():
    """Page where user can make three different donations types"""
    
    return render_template("/donations.html")


@app.route("/advice", methods=["GET"])
def advice():
    """Page where users can see useful advice regarding their cats"""
    
    return render_template("advice.html")


@app.route("/contact", methods=["GET","POST"])
def contact():
    """Page displaying contact info"""

    # As via form sending
    if request.method == "POST":

        return render_template("contact.html")

    # Just GET the page
    else:
        return render_template("contact.html")


@app.route("/one_time_donation", methods=["GET","POST"])
def one_time_donation():
    """"One Time donation page"""

    # Page is initiated through POST, for example by submitting the one time payment form
    if request.method == "POST":
        
        # Get input by input, validating it
        sum = request.form.get('sum')
        
        card_number = request.form.get('card_number')
        
        expiration_date = request.form.get('expiration_date')

        card_code = request.form.get('card_code')

        cardholder_name = request.form.get('cardholder_name')

        email_address = request.form.get('email_address')

        # Double checking, making sure no field is empty:
        if not sum:
            return apology("Please provide sum", 403)

        elif not cardholder_name:
            return apology("Please provide cardholder name", 403)

        elif not email_address:
            return apology("Please provide email address", 403)

        # Email validation
        for i in range(len(email_characters)):
            if email_characters[i] not in email_address:
                return apology("Provide valid email address", 400)
        
        for i in range(len(forbidden_characters)):
            if forbidden_characters[i] in email_address:
                return apology("Forbidden character: " + forbidden_characters[i],  400)

        # Make sure cardholder input has no malicious characters
        for i in range(len(forbidden_characters)):
            if forbidden_characters[i] in cardholder_name:
                return apology("Charcater not allowed: " + forbidden_characters[i], 403)
 
        # Make sure it is made only of numbers
        if not sum.isnumeric() or not card_number.isnumeric() or not expiration_date.isnumeric() or not card_code.isnumeric():
            return apology("Please provide only numbers when necessary", 403)
        
        # Promt the user to input data correctly
        if len(expiration_date) != 6:
            return apology("Please input data correctly -- Expiration Date", 403)

        elif len(card_code) < 3 or len(card_code) > 4:
            return apology("Please input data correctly -- Card Code", 403)

        elif len(card_number) > 16 or len(card_number) < 15:
            return apology("Please input data correctly -- Card Number", 403)


        # Send email to thank for the donation
        mail_msg = Message("Thank you for your donation!", sender='purryadopt@outlook.com', recipients=[email_address])
        mail_msg.body = "Thank you for your donation to our foundation! You are the meow-est!" 
        
        mail.send(mail_msg)

        # Once the form was submitted, go back to /donations
        return render_template("/donations.html")
    
    # The page is initiated by GET, for example by simply opening it
    else:
        return render_template("/one_time_donation.html")


@app.route("/regular_donations", methods=["GET", "POST"])
def regular_donations():
    """"Regular donations page"""
        
    if request.method == "POST":
        
        # Get input by input, validating it
        sum = request.form.get('sum')
        
        card_number = request.form.get('card_number')
        
        expiration_date = request.form.get('expiration_date')

        card_code = request.form.get('card_code')

        cardholder_name = request.form.get('cardholder_name')

        email_address = request.form.get('email_address')

        number_months = request.form.get('number_months')

        # Double checking, making sure no field is empty:
        if not sum:
            return apology("Please provide sum", 403)

        elif not cardholder_name:
            return apology("Please provide cardholder name", 403)

        elif not email_address:
            return apology("Please provide email address", 403)

        elif not number_months:
            return apology("Please provide number months", 403)


        # Email validation
        for i in range(len(email_characters)):
            if email_characters[i] not in email_address:
                return apology("Provide valid email address", 400)

        for i in range(len(forbidden_characters)):
            if forbidden_characters[i] in email_address:
                return apology("Forbidden character: " + forbidden_characters[i],  400)

        # Make sure cardholder input has no malicious characters
        for i in range(len(forbidden_characters)):
            if forbidden_characters[i] in cardholder_name:
                return apology("Charcater not allowed: " + forbidden_characters[i], 403)
 
        # Make sure it is made only of numbers
        if not sum.isnumeric() or not card_number.isnumeric() or not expiration_date.isnumeric() or not card_code.isnumeric():
            return apology("Please provide only numbers when necessary", 403)
        
        # Promt the user to input data correctly
        if len(expiration_date) != 6:
            return apology("Please input data correctly -- Expiration Date", 403)

        elif len(card_code) < 3 or len(card_code) > 4:
            return apology("Please input data correctly -- Card Code", 403)

        elif len(card_number) > 16 or len(card_number) < 15:
            return apology("Please input data correctly -- Card Number", 403)

        elif int(number_months) < 1:
            return apology("Number months must be a positive number", 403)

        # Hash sensitive data
        card_number = generate_password_hash(card_number)

        expiration_date = generate_password_hash(expiration_date)

        card_code = generate_password_hash(card_code)

        
        # Input to DB
        db.execute("INSERT INTO regular_donations (sum, card_number, cardholder_name, exp_date, security_code, email, number_months) VALUES(?,?,?,?,?,?,?)", 
                                                    sum, card_number, cardholder_name, expiration_date, card_code, email_address, number_months)
        
        # Send email to thank for the donation
        mail_msg = Message("Thank you for your regular donation!", sender='purryadopt@outlook.com', recipients=[email_address])
        mail_msg.body = "Thank you for regularly donating to our foundation! You are the meow-est!" 
        
        mail.send(mail_msg)

        # Once the form was submitted, go back to /donations
        return render_template("/donations.html")

    else:

        return render_template("/regular_donations.html")


@app.route("/percent_donation", methods=["GET", "POST"])
def percent_donation():
    """"Percent donations page"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST": 
        
        # Get user input
        first_name = request.form.get('first_name')

        second_name = request.form.get('second_name')

        address = request.form.get('address')

        phone_number = request.form.get('phone_number')

        email = request.form.get('email_address')

        checkbox1 = request.form.get('checkbox1')
        
        checkbox2 = request.form.get('checkbox2')
            
        # Check if any input box is null
        if not first_name or not second_name or not address or not phone_number or not email or not checkbox1 or not checkbox2:
            return apology("Please complete all spaces, including the checkboxes", 400)

        # Specific validation
        
        # Forbidden characters validation
        for i in range(len(forbidden_characters)):
            if forbidden_characters[i] in first_name:
                return apology("Forbidden character: " + forbidden_characters[i],  400)
            elif forbidden_characters[i] in second_name:
                return apology("Forbidden character: " + forbidden_characters[i],  400)
            elif forbidden_characters[i] in address:
                return apology("Forbidden character: " + forbidden_characters[i],  400)
            elif forbidden_characters[i] in phone_number:
                return apology("Forbidden character: " + forbidden_characters[i],  400)
            elif forbidden_characters[i] in email:
                return apology("Forbidden character: " + forbidden_characters[i],  400)
            
        # Email validation
        for i in range(len(email_characters)):
            if email_characters[i] not in email:
                return apology("Provide valid email address", 400)
        
        
        # Input to DB
        db.execute("INSERT INTO percent_donations (first_name, second_name, address, phone_number, email) VALUES(?,?,?,?,?)", first_name, second_name,
                                                    address, phone_number, email)
        
        # Send email to thank for the donation
        mail_msg = Message("Thank you for your 3.5 percent imposit donation!", sender='purryadopt@outlook.com', recipients=[email])
        mail_msg.body = "Thank you for regularly donating to our foundation! You are the meow-est!" 
        
        mail.send(mail_msg)

        # Return to donations when done
        return render_template("/donations.html")

    # User reached route via GET (as by clicking a link or via redirect)
    else:        
        return render_template("/percent_donation.html")


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
        # Anyone can have a membership to this newsletter, but if they are logged in into an account, they could easily forgone it in 'My account'
        # But for that, we need their user_id as well, however, that field can be NULL in the DB too.

        # Storage
        email = request.form.get('email')
        
        # Email validation
        for i in range(len(email_characters)):
            if email_characters[i] not in email:
                return apology("Provide valid email address", 400)
        
        for i in range(len(forbidden_characters)):
            if forbidden_characters[i] in email:
                return apology("Character(s) not allowed", 400)

        # Check if we have a user here
        try: 
            user = session['user_id']
            db.execute("INSERT INTO newsletter (user_id, email) VALUES(?,?)", user, email)
        except:  
            # If not, just record the email with an USER ID of 0.
            db.execute("INSERT INTO newsletter (user_id, email) VALUES(?,?)", 0, email)

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


@app.route("/cancel_newsletter", methods=["GET", "POST"])
@login_required
def cancel_newsletter():
    """Here users can cancel their newsletter subscription instantly"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        # Get necessary info
        user = session['user_id']

        email = request.form.get('newsletter_email')

        # Email validation
        for i in range(len(email_characters)):
            if email_characters[i] not in email:
                return apology("Provide valid email address", 400)
        
        for i in range(len(forbidden_characters)):
            if forbidden_characters[i] in email:
                return apology("Forbidden character: " + forbidden_characters[i],  400)


        # Verify if the sent email belongs to the user himself
        verify_user_email = db.execute("SELECT email FROM users WHERE id=?", user)

        verify_user_email = verify_user_email[0]['email']

        if verify_user_email != email:
            return apology("Email must belong to you", 400)

        elif verify_user_email == email:
            db.execute("DELETE FROM newsletter WHERE email=?", email)

        return render_template("cancel_newsletter.html")


    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("cancel_newsletter.html")


@app.route("/my_account", methods=["GET", "POST"])
@login_required
def my_account():
    """Users can view and interact with their account"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        # Get user info
        user = session["user_id"]

        # Get deletion button for automation
        delete_account_btn = request.form['delete_account_btn']

        if delete_account_btn == 'Delete Acc.':
            db.execute("DELETE FROM users WHERE id=?", user)
            session.clear()    
            return render_template("donations.html")

        return render_template("my_account.html")
    
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        # Get Jinja Info
        user_id = session["user_id"]

        username = db.execute("SELECT username FROM users WHERE id=?", user_id)

        username = username[0]['username']
        
        return render_template("my_account.html", username=username, user_id=user_id)


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

@login_required
@app.route("/change_email", methods=["GET", "POST"])
def change_email():
    """Here users can choose to change their email address"""

    # If they send the form
    if request.method == "POST":

        # Get user and inputs
        user = session['user_id']   

        email = request.form.get('new_email')
        
        # Email validation
        if email_validation(email, email_characters) != 0:
            return apology("Provide valid email address", 403)

        if input_validation(email, forbidden_characters) != 0:
            output = input_validation(email, forbidden_characters)
            return apology("Forbidden character: " + forbidden_characters[output],  400)


        # Change email address
        db.execute("UPDATE users SET email=? WHERE id=?", email, user)

        # Send confirmation email 
        # mail_msg = Message("Email successfully changed!", sender='purryadopt@outlook.com', recipients=[email])
        # mail_msg.body = "You have succesfully changed your email!" 
        
        # mail.send(mail_msg)

        # Done, redirect to My Account
        return redirect("/my_account")

    # Just accessing the page via GET
    else:
        return render_template("/change_email.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


# End of file
if __name__ == '__main__':
    print("I am being run directly")
    app.run(debug=True)
else:
    print("I am being imported")