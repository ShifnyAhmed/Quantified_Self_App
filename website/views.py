from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

views = Blueprint('views', __name__)


@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)


@views.route('/view-profile', methods=['GET', 'POST'])
@login_required
def view_profile():
    return render_template("profile_page.html", user=current_user)


@views.route('/edit-profile-page', methods=['GET', 'POST'])
@login_required
def edit_profile_page():
    try:
        if request.method == 'POST':
            email = request.form.get('email')
            fullname = request.form.get('name')
            city = request.form.get('city')
            user_id = current_user.id
            current_user_email = current_user.email

            from .models import User
            user = User.query.filter_by(email=email).first()
            if user and current_user_email != email:
                flash('Email is already taken, try another email.', category='error')
            elif len(fullname) < 3:
                flash('Full name must be greater than 2 characters.', category='error')
            elif len(email) < 4:
                flash('Email must be greater than 3 characters.', category='error')
            else:
                from .models import User
                edit_user = User.query.get(user_id)

                from . import db

                edit_user.fullname = fullname
                edit_user.email = email
                edit_user.city = city

                db.session.commit()
                flash('Profile Updated Successfully.', category='success')
                return redirect(url_for('views.view_profile'))
    except Exception as e:
        print(e)
        flash('Something went wrong.', category='error')
    return render_template("edit_profile_page.html", user=current_user)
