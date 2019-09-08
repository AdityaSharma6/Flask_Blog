import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/") # This is a route (decoration) that handles the backend work.
@app.route("/home")
def home():
    posts = Post.query.all() # Grabs all the posts from database
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


def save_picture(form_picture):
    random_hex = secrets.token_hex(8) # Randomizing the uploaded file's name using hiex
    file_name, file_extension = os.path.splitext(form_picture.filename) # Grabbing the extension of the file
    picture_filename = random_hex + file_extension # Creating a new file name
    picture_path = os.path.join(app.root_path, "static/profile_pics", picture_filename) # Uploading the picture to a desired path
    
    output_size = (125, 125) # Specify size of image
    i = Image.open(form_picture) # Opened the picture and stored its contents
    i.thumbnail(output_size) # Resizing the picture to a thumbnail of the specified size
    i.save(picture_path) # Saving the picture 

    return picture_filename

@app.route("/account", methods = ["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data: #form.picture will just return the input type that it is expecting. it doesn't show if there actually is any data in there. So, we need to do form.picture.data
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated!", "success")
        return redirect(url_for("account"))
    elif request.method == "GET": # Until the request is POST (button click), there will be the information displayed
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for("static", filename = "profile_pics/" + current_user.image_file)
    
    return render_template("account.html", title = "Account", image_file=image_file, form=form)
    
@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id) # Will look for the post. If the post is not found, it will throw an 404 error
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id) # Will look for the post. If the post is not found, it will throw an 404 error
    if post.author != current_user: # Ensures that only the author of the post can access the post
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET': # There are continous get requests happening and until a post request happens (button press), this will keep being displayed
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))