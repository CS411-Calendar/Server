from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from config import app
from datetime import datetime
from flask_migrate import Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):

    id = db.Column(db.String(75), primary_key=True)
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def json(self):
        return jsonify({
            "id": self.id
        })

    def __repr__(self):
        return '<User %r>' % self.id


class Invite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    ownerId = db.Column(db.String(75), db.ForeignKey('user.id'), nullable=False)
    owner = db.relationship('User')
    name = db.Column(db.String(50), nullable=False)
    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(75))

    def json(self):
        return jsonify({
            "id": self.id,
            "ownerId": self.ownerId
        })

    def __repr__(self):
        return '<Invite %r>' % self.id


class InviteCalendar(db.Model):
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    inviteId = db.Column(db.Integer, db.ForeignKey('invite.id'), nullable=False)
    invite = db.relationship('Invite')
    calendarId = db.Column(db.String(320), db.ForeignKey('calendar.id'), nullable=False)
    calendar = db.relationship('Calendar')
    __table_args__ = (
        db.PrimaryKeyConstraint(
            inviteId, calendarId,
        ),
    )

    def json(self):
        return jsonify({
            "inviteId": self.inviteId,
            "calendarId": self.calendarId
        })

    def __repr__(self):
        return '<InviteCalendar %r>' % self.id


class Calendar(db.Model):
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    id = db.Column(db.String(320), primary_key=True)

    def json(self):
        return jsonify({
            "id": self.id
        })
        
    def __repr__(self):
        return '<Calendar %r>' % self.id

def init():
    db.create_all()
    db.session.commit()