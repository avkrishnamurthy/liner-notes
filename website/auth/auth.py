from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from website.models import User, Album, FavoriteAlbum
from werkzeug.security import generate_password_hash, check_password_hash
from website import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__, template_folder='templates')


@auth.route('/googlefbf8ec5188c80724.html')
def google_search_console():
    return render_template("googlefbf8ec5188c80724.html")

@auth.route('/')
def default():
    return redirect(url_for('auth.login', _external=True))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profiles.my_profile', _external=True))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('profiles.my_profile'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Username does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    session.clear()
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('profiles.my_profile', _external=True))
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        email_user = User.query.filter_by(email=email).first()
        username_user = User.query.filter_by(username=username).first()
        if email_user:
            flash('Email already in use.', category='error')
        elif username_user:
            flash("Username already in use.", category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        elif len(username) > 17:
            flash('Username must be less than 18 characters')
        else:
            new_user = User(email=email, username=username, first_name=first_name, password=generate_password_hash(
                password1, method='scrypt'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('profiles.my_profile'))

    return render_template("create_account.html", user=current_user)


@auth.route('/delete-account', methods=['POST'])
@login_required
def delete_account():
    password = request.form.get('password')
    user = User.query.filter_by(username=current_user.username).first()
    if check_password_hash(user.password, password):
        delete_user_account(current_user)
        flash('Your account has been successfully deleted.', 'success')
        logout_user()
        return redirect(url_for('auth.login', _external=True))
    else:
        flash('Password does not match. Account deletion failed.', 'error')
        return redirect(url_for('profiles.my_profile'))

def delete_user_account(user):
    user_albums = Album.query.filter_by(user_id=user.id).all()
    for album in user_albums:
        db.session.delete(album)
    user_favorites = FavoriteAlbum.query.filter_by(user_id=user.id).all()
    for favorite in user_favorites:
        db.session.delete(favorite)

    for follow in current_user.following:
            follow.follower.remove(current_user)
    for followee in current_user.follower:
        followee.following.remove(current_user)

    # Step 4: Delete the User
    db.session.delete(user)

    # Commit the changes to the database
    db.session.commit()