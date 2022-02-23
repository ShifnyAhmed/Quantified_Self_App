from flask import Blueprint, render_template, request, flash, redirect,url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        from .models import User

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again!', category='error')

        else:
            flash('User does not exist.', category='error')
    return render_template("login.html", user=current_user)


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        fullname = request.form.get('name')
        city = request.form.get('city')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        from .models import User
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email is already taken, try another email.', category='error')
        elif len(fullname) < 3:
            flash('Full name must be greater than 2 characters.', category='error')
        elif len(email) < 6:
            flash('Email must be greater than 5 characters.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        else:

            from . import db
            # Add user to the database
            new_user = User(fullname=fullname, email=email,  password=generate_password_hash(password1, method='sha256'), city=city)
            db.session.add(new_user)
            db.session.commit()
            flash('Successfully signed up.', category='success')

    return render_template("sign_up.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out from our application.', category='success')
    return redirect(url_for('auth.login'))
