from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

from os import environ

from models import app, db, User, Gift, Holidays, bcrypt


db.create_all()


@app.route('/')
def splash():
    """
    Splash page
    """
    return render_template('home.html', title="Home")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    User can sign up.
    """
    form = RegistrationForm()

    if form.validate_on_submit() and request.method == "POST":

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)

        db.session.add(user)
        db.session.commit()
        print(User.query.all())


        flash('Account created, please login.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html', title='Sign Up', form=form)


@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)


if __name__ == "__main__":
    app.run(
        debug = True
    )
