from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, ValidationError
from models import User


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[
            DataRequired(),
            Email()
        ])
    username = StringField('Username', validators=[
            DataRequired(),
            Length(min=3, max=20)
        ])
    password = PasswordField('Password', validators=[
            DataRequired(),
            Length(min=8, max=40)
        ])
    confirm_password = PasswordField('Confirm Password', validators=[
            DataRequired(),
            EqualTo('password')
        ])

    submit = SubmitField('Sign up')

    def validate_username(self, username):
        """
        Checks db to see if username has been taken.
        """

        user = User.query.filter_by(username=username.data).first()

        if user:
            raise ValueError('Username already exists. Please choose another.')

    def validate_email(self, email):
        """
        Checks db to see if email already registered.
        """

        user = User.query.filter_by(email=email.data).first()

        if user:
            raise ValueError('This email already has an account. Would you like to sign in?')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
            DataRequired(),
            Email()
        ])
    password = PasswordField('Password', validators=[
        DataRequired()
        ])
    remember = BooleanField('Remember Me')

    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    email = StringField('Email', validators=[
            DataRequired(),
            Email()
        ])
    username = StringField('Username', validators=[
            DataRequired(),
            Length(min=3, max=20)
        ])
    picture = FileField('Update Profile Picture', validators=[
        FileAllowed(['jpg', 'png'])
        ])

    submit = SubmitField('Update')

    def validate_username(self, username):
        """
        Checks db to see if username has been taken.
        """
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()

            if user:
                raise ValueError('Username already exists. Please choose another.')


    def validate_email(self, email):
        """
        Checks db to see if email already registered.
        """
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()

            if user:
                raise ValueError('This email already has an account. Would you like to sign in?')


class GiftForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=100)])
    link = StringField('Link', validators=[Length(min=0, max=100)])
    description = TextAreaField('Description', validators=[Length(min=0, max=300)])

    submit = SubmitField('Add')

class UpdateGiftForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=100)])
    link = StringField('Link', validators=[Length(min=0, max=100)])
    description = TextAreaField('Description', validators=[Length(min=0, max=300)])

    submit = SubmitField('Update')
