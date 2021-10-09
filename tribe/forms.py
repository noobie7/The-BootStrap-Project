from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields.simple import TextField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from tribe.models import User

class RegistrationForm(FlaskForm):
    username = StringField('UserName', validators=[DataRequired(), Length(min = 3, max = 15)])
    email = StringField('Email', validators= [DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError('This username is already taken!')

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('This email is already taken!')
class LoginForm(FlaskForm):
    username = StringField('UserName', validators=[DataRequired(), Length(min = 3, max = 15)])
    password = PasswordField('Password', validators=[DataRequired(),Length(min = 5)])
    remember = BooleanField('Remember Me!')
    submit = SubmitField('Log in')

class UpdateAccountForm(FlaskForm):
    username = StringField('UserName', validators=[DataRequired(), Length(min = 3, max = 15)])
    email = StringField('Email', validators= [DataRequired(),Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

   

    def validate_username(self, username):
        if current_user.username != username.data:
            user = User.query.filter_by(username = username.data).first()
            if user:
                raise ValidationError('This username is already taken!')

    def validate_email(self, email):
        if current_user.email != email.data:
            user = User.query.filter_by(email = email.data).first()
            if user:
                raise ValidationError('This email is already taken!')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators= [DataRequired()])
    submit = SubmitField('Post')