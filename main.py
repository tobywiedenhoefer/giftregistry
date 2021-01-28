from flask import Flask, render_template, request, flash, redirect, url_for, request
from forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required

from os import environ

from models import app, db, User, Gift, Holidays, bcrypt, login_manager


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


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('splash'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            get_next = request.args.get('next')

            if get_next:
                return redirect(url_for(get_next))
            else:
                return redirect(url_for('splash'))

        else:
            print('unsuccessful')
            flash('Login Unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')


if __name__ == "__main__":
    app.run(
        debug = True
    )
