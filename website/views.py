from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

views = Blueprint('views', __name__)


@views.route('/')
@login_required
def home():
    from .models import Tracker
    tracker = Tracker.query.all()
    return render_template("home.html", user=current_user, tracker=tracker)


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


@views.route('/add-tracker-page', methods=['GET', 'POST'])
@login_required
def add_tracker_page():
    try:
        if request.method == 'POST':
            name = request.form.get('name')
            description = request.form.get('description')
            tracker_type = request.form.get('type')
            settings = request.form.get('settings')

            from .models import Tracker
            current_user_id = current_user.id
            tracker = Tracker.query.filter_by(name=name).first()
            if tracker and current_user_id == tracker.user_id:
                flash('The tracker "' + name + '" is already added by you.', category='error')
                return redirect(url_for('views.home'))
            else:
                from . import db
                new_tracker = Tracker(name=name, description=description, tracker_type=tracker_type, settings=settings,
                                      user_id=current_user_id)
                db.session.add(new_tracker)
                db.session.commit()
                flash('New Tracker Added.', category='success')
                return redirect(url_for('views.home'))
    except Exception as e:
        print(e)
        flash('Something went wrong.', category='error')
    return render_template("add_tracker_page.html", user=current_user)


@views.route('/delete-tracker/<int:record_id>', methods=['GET', 'POST'])
@login_required
def delete_tracker(record_id):
    try:
        from .models import Tracker
        Tracker_details = Tracker.query.get(record_id)
        Tracker_name = Tracker_details.name
        from . import db
        db.session.delete(Tracker_details)
        db.session.commit()
        flash(Tracker_name + ' Tracker Removed Successfully.', category='success')
    except Exception as e:
        print(e)
        flash('Something went wrong.', category='error')
    return redirect(url_for('views.home'))


@views.route('/edit-tracker/<int:record_id>', methods=['GET', 'POST'])
@login_required
def edit_tracker(record_id):
    from .models import Tracker
    this_tracker = Tracker.query.get(record_id)
    this_tracker_name = this_tracker.name
    try:
        if request.method == 'POST':
            name = request.form.get('name')
            description = request.form.get('description')
            tracker_type = request.form.get('type')
            settings = request.form.get('settings')

            current_user_id = current_user.id
            tracker = Tracker.query.filter_by(name=name).first()
            if tracker and tracker.user_id == current_user_id and this_tracker_name != name:
                flash('The tracker "' + name + '" is already added by you, Try a new name for your tracker.',
                      category='error')
            else:
                from . import db

                this_tracker.name = name
                this_tracker.description = description
                this_tracker.tracker_type = tracker_type
                this_tracker.settings = settings

                db.session.commit()
                flash('Tracker Updated Successfully.', category='success')
                return redirect(url_for('views.home'))
    except Exception as e:
        print(e)
        flash('Something went wrong.', category='error')

    return render_template("edit_tracker_page.html", user=current_user, tracker=this_tracker)


@views.route('/add-log-page/<int:record_id>', methods=['GET', 'POST'])
@login_required
def add_log(record_id):
    from .models import Tracker, Log
    this_tracker = Tracker.query.get(record_id)
    import datetime
    now = datetime.datetime.now()
    try:
        if request.method == 'POST':
            when = request.form.get('date')
            value = request.form.get('value')
            notes = request.form.get('notes')
            from . import db
            new_log = Log(timestamp=when, value=value, notes=notes, tracker_id=record_id, user_id=current_user.id)
            db.session.add(new_log)
            db.session.commit()
            flash('New Log Added For '+this_tracker.name+' Tracker', category='success')
            return redirect(url_for('views.home'))
    except Exception as e:
        print(e)
        flash('Something went wrong.', category='error')
    return render_template("add_log_page.html", user=current_user, tracker=this_tracker, now=now)
