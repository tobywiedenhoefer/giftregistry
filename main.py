from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm
from os import environ

from create_db import app, db, User, Gift, Holidays, create_users


@app.route('/')
def splash():
    return render_template('home.html', title="Home")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit() and request.method == "POST":
        flash('Account created!')
        return redirect(url_for('splash'))
    return render_template('signup.html', title='Sign Up', form=form)


@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)


if __name__ == "__main__":
    app.run(
        debug = True
    )
