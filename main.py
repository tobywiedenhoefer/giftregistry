import os

from PIL import Image
from flask import Flask, render_template, request, flash, redirect, url_for, request
from flask_login import login_user, current_user, logout_user, login_required

from models import app, db, User, Gift, Holidays, bcrypt, login_manager
from forms import RegistrationForm, LoginForm, UpdateAccountForm, GiftForm, UpdateGiftForm


hashed_password = bcrypt.generate_password_hash("testtest").decode('utf-8')
user = User(username="test", email="test@test.com", password=hashed_password)
gift = Gift(user_id=1, title="OneTitle", link="Onelink", description="OneDescription")

db.session.add(user)
db.session.commit()
db.session.add(gift)
db.session.commit()

def save_picture(form_picture):
    _, extension = os.path.splitext(form_picture.filename)
    file_name = bcrypt.generate_password_hash(str(current_user.id))
    picture_path = os.path.join(app.root_path, 'static/account_pictures', file_name + extension)

    resize = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(resize)
    i.save(picture_path)

    return file_name


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
    if current_user.is_authenticated:
        return redirect(url_for('splash'))

    form = RegistrationForm()

    if form.validate_on_submit():

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
                if get_next[0] == "/":
                    get_next = get_next[1::]
                return redirect(url_for(get_next))
            return redirect(url_for('splash'))

        else:
            flash('Login Unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('splash'))


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    pfp = url_for('static', filename='account_pictures/' + current_user.image_file)

    if form.validate_on_submit() and request.method == 'POST':
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Account updated!", "success")
        return redirect(url_for('account'))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
        
    return render_template('account.html', title='Account', pfp=pfp, form=form)


@app.route("/gifts/add", methods=['GET', 'POST'])
@login_required
def add_gift():
    form = GiftForm()
    if form.validate_on_submit():
        gift = Gift(user_id=current_user.id, title=form.title.data, link=form.link.data, description=form.description.data)
        db.session.add(gift)
        db.session.commit()
        flash("Gift added! Add another?", "success")
        return redirect(url_for('add_gift'))
    return render_template('add_gift.html', title='Add Gift', form=form)


@login_required
@app.route("/wishlist")
def wishlist():
    gifts = Gift.query.filter_by(user_id=current_user.id).all()
    return render_template('wishlist.html', title="Wishlist", gifts=gifts)


@login_required
@app.route("/gift/<int:gift_id>", methods=['POST', 'GET'])
def view_gift(gift_id):
    gift = Gift.query.get_or_404(gift_id)
    form = UpdateGiftForm(title=gift.title, link=gift.link, description=gift.description)
    if form.validate_on_submit():
        gift.title = form.title.data
        gift.link = form.link.data
        gift.description = form.description.data
        db.session.commit()
        flash("Gift updated!", "success")
        print(Gift.query.all())
        return redirect(url_for('view_gift', gift_id=gift_id))
    return render_template('gift.html', title=gift.title, gift=gift, form=form)


if __name__ == "__main__":
    app.run(
        debug = True
    )
