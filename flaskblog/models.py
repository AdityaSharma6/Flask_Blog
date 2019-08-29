from datetime import datetime
from flaskblog import db, login_manager
from flask_login import UserMixin
''' This is the database models. It specifies the structure of the database. 
    It also enables you to run checks/ scripts on certain GETS/POSTS from/to the db
'''

@login_manager.user_loader
def load_user(user_id): # This returns the user given the user's id. 
    return User.query.get(int(user_id)) # .get() is faster than .query(user_id = id).first()

class User(db.Model, UserMixin):
    # By setting somethign to have unique = True, if a sign-up is done with a field that already exists, the website will throw an error. We must redirect the page.
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable = False) # Unique user names, can't be empty
    email = db.Column(db.String(150), unique = True, nullable = False) # Unique emails, can't be empty
    image_file = db.Column(db.String(20), nullable = False, default = "default.jpg") # Not unique pictures (allow for sharing)
    password = db.Column(db.String(60), nullable = False) # Passwords will be hashed
    # This database shares a relationship with another database. This is described by the db.relationship base. It is liked by author ID. It is a 1 - Many relationship
    posts = db.relationship("Post", backref="author", lazy = True) # A backref is like adding another column. Lazy means that SQLAlchemy will load as necessary 

    def __repr__(self):
        return (f"User('{self.username}', '{self.email}', '{self.image_file}','{self.password}')")

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable = False)
    date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    content = db.Column(db.Text, nullable = False)
    upload = db.Column(db.String(20), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False) # This is a foreign key. There will be many Posts for 1 User id. The table it is connected to is specified in db.foreignkey(USER.id)

    def __repr__(self):
        return (f"Post('{self.title}', '{self.date_posted}', '{self.content}')")
