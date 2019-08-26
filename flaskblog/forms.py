from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import *

class RegistrationForm(FlaskForm):
    # It is good practice to segment different parts of a website into different code files
    # When specifying the type of field you want, if its a String, use the StringField method
    # You can specify validators, certain conditions that need to be passed when filling out the field)
    username = StringField("Username", validators = [DataRequired(), Length(min=2)])
    email = StringField("Email", validators = [DataRequired(), Length(min=5), Email()]) # You can validate if an email exists by using the Email() method
    password = PasswordField("Password", validators = [DataRequired(), Length(min = 8)])
    confirm_password = PasswordField("Confirm Password", validators = [DataRequired(), EqualTo("password")]) # You would need to hash the password for security. Use Flask's inbuilt system called Bcrypt
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError("That username is taken, please choose another.")
    
    def validate_email(self, email): # Email is a parameter because with back-end development, it represents the field in the object when it is created.
        user = User.query.filter_by(email = email.data.lower()).first() 
        if user:
            raise ValidationError("That email is taken, please choose another.")

class LoginForm(FlaskForm):
    # It is good practice to segment different parts of a website into different code files
    # When specifying the type of field you want, if its a String, use the StringField method
    # You can specify validators, certain conditions that need to be passed when filling out the field
    username = StringField("Username", validators = [DataRequired(), Length(min=2, max=26)])
    email = StringField("Email", validators = [DataRequired(), Length(min=2), Email()]) # You can validate if an email exists by using the Email() method
    remember = BooleanField("Remember Me")
    password = PasswordField("Password", validators = [DataRequired()])
    login = SubmitField("Login")

# Whenever we are using forms, we need to make sure that it is secure
# We need to set a secret key -- it'll protect against modifying cookies and cross-site requests.