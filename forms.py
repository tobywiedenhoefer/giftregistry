from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo

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


class LoginForm(FlaskForm):
    email = StringField('Email', validators=all_validators('email'))
    username = StringField('Username', validators=all_validators('username'))
    password = PasswordField('Password', validators=all_validators('password'))
    remember = BooleanField('Remember Me')

    submit = SubmitField('Login')
