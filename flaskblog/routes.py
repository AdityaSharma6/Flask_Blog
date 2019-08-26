from flask import render_template, url_for, flash, redirect
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post


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
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8") # Since the object in def Register() is of the Register Class. It will have its variables as objects. You specify the mini-object you want to access and then write .data to access its data
        user = User(username = form.username.data, email = form.email.data.lower(), password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success') # If the user's data is valid, then it will show this flash.
        return (redirect(url_for('login'))) # The url_for method will redirect you to a route that has the function called home
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods= ["GET", "POST"])
def login():
    form = LoginForm()
    # Since a login form has different fields, we want to make sure that the fields are entered correctly.
    if form.validate_on_submit():
        flash(f"{form.username.data} has successfully logged into their account!", "success")
        return (redirect(url_for("home")))
    return render_template("login.html", title = "Login", form=form)