from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, ValidationError
from models import User

def all_validators(v: str) -> list:
    form_validators = {
        "email": [
            DataRequired(),
            Email()
        ],
        "username": [
            DataRequired(),
            Length(min=3, max=20)
        ],
        "password": [
            DataRequired(),
            Length(min=8, max=40)
        ],
        "confirm_password": [
            DataRequired(),
            EqualTo('password')
        ]
    }
    return form_validators[v]


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=all_validators('email'))
    username = StringField('Username', validators=all_validators('username'))
    password = PasswordField('Password', validators=all_validators('password'))
    confirm_password = PasswordField('Confirm Password', validators=all_validators('confirm_password'))

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
    email = StringField('Email', validators=all_validators('email'))
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')

    submit = SubmitField('Login')
