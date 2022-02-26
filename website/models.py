from . import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    city = db.Column(db.String(150))
    tracker = db.relationship('Tracker')
    log = db.relationship('Log')


class Tracker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(150))
    tracker_type = db.Column(db.String(150))
    settings = db.Column(db.String(150))
    log = db.relationship('Log')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(150))
    value = db.Column(db.Integer)
    notes = db.Column(db.String(150))
    tracker_id = db.Column(db.Integer, db.ForeignKey('tracker.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    added_date_time = db.Column(db.String(150))
