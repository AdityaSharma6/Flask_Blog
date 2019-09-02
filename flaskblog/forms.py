from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed # 1) Allows for the uploading of files. 2) Specifies the type of file that you want to upload
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField # 1) Specifies the data type. 2) Enables a password field to input passwords. 3) Enables submissions. 4) It is used for the "remember me" boxes
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError # Used for form validation. 1) it means that you can make certain fields require data. 2) The fields that information is entered into can take specific lengths. 3) This enables people to input emails. It checks the validity of the input, ensuring only emails are inputted. 4) If the validation recponses fail, it will raise a validation error
from flaskblog.models import User

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
        user = User.query.filter_by(username = username.data).first() # This queries the db to check if the username exists
        if user: # If the user object != None meaning, if the user object exists. Then it means that the inputted username is taken
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

class UpdateAccountForm(FlaskForm):
    username = StringField("Username", validators = [DataRequired(), Length(min = 2)])
    email = StringField("Email", validators = [DataRequired(), Length(min = 5), Email()])
    submit = SubmitField("Update")
    picture = FileField("Update Profile Picture", validators=[FileAllowed(["jgp", "png"])])

    def validate_username(self, username):
        if username.data != current_user.username: # Username is the field defined above. .data brings the raw text inputted
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("That username is taken. Please choose another.")
    
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("That email is taken. Please choose another.")



# Whenever we are using forms, we need to make sure that it is secure
# We need to set a secret key -- it'll protect against modifying cookies and cross-site requests.