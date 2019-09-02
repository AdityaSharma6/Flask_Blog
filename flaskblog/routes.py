from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required



posts = [
    {
        "author": "Aditya Sharma",
        "title": "First Blog",
        "content": "I am the king of Wakanda",
        "date_posted": "April 20, 2018"
    },
    {
        "author": "King Sharma",
        "title": "Second Blog",
        "content": "Wakanda is Mine Now",
        "date_posted": "April 20, 2018"
    }
]

@app.route("/") # This is a route (decoration) that handles the backend work.
@app.route("/home")
def home():
    return (render_template("home.html", posts=posts))


@app.route("/about")
def about():
    return (render_template("about.html", title="About"))

@app.route("/register", methods=['GET', 'POST']) # In the routes, you would use the parameter "methods" to input certain requests in LIST Format.
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8") # Since the object in def Register() is of the Register Class. It will have its variables as objects. You specify the mini-object you want to access and then write .data to access its data
        user = User(username=form.username.data, email=form.email.data.lower(), password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success') # If the user's data is valid, then it will show this flash.
        return (redirect(url_for('login'))) # The url_for method will redirect you to a route that has the function called home
    else:
        flash("Your account could not be created. Please try again.")
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods= ["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    # Since a login form has different fields, we want to make sure that the fields are entered correctly.  
    if form.validate_on_submit(): # It is essentially checking if any validation errors are raised. If validation errors that we specified in the forms.py are not raised, then it will proceed
        user = User.query.filter_by(email=form.email.data.lower()).first() # It will check if the user exists in the database by quering based off the inputted email.
        if user and bcrypt.check_password_hash(user.password, form.password.data): # If the user exists (the email is in the db) and the password they entered is the same as the password in the db. It performs its check by unhashing the value in the db and comparing it to the form data.
                flash(f"You have successfully logged into your account!", "success")
                login_user(user, remember=form.remember.data) # This is the method that logs in the user
                next_page = request.args.get("next") # Args is a dictionary. This is used because when we attempt to access a page that can only be accessed after logging in, when we login we click again to reach our page. But this will remember which page we were trying to access and will store it. It will retrieve the query from the link
                if next_page: # If there is a positive value in "next_page" send the user to the page they were about to access
                    return redirect(next_page)
                else: # Otherwise, send the user to the home page
                    return (redirect(url_for("home")))
        else:
            flash(f"Your email or password was incorrect. Please try again!", "danger")
    return render_template("login.html", title = "Login", form=form)

@app.route("/logout", methods = ["GET", "POST"])
def logout():
    logout_user()
    return (redirect(url_for("home")))

@app.route("/account", methods = ["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated!", "success")
        return redirect(url_for("home"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for("static", filename = "profile_pics/" + current_user.image_file)
    print(image_file)
    return render_template("account.html", title = "Account", image_file=image_file, form=form)
