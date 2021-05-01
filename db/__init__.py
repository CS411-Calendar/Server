from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from config import app
from datetime import datetime
from flask_migrate import Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Invite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    to = db.Column(db.String(320), db.ForeignKey('calendar.id'), nullable=False)
    calendar = db.relationship('Calendar')

    name = db.Column(db.String(50), nullable=False)
    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(100))

    def json(self):
        return jsonify({
            "id": self.id,
        })

    def __repr__(self):
        return '<Invite %r>' % self.id


class Attendee(db.Model):
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

    @staticmethod
    def createOrGet(inviteId, calendarId):
        attendee = Attendee.query.get([inviteId, calendarId])
        if not attendee:
            return Attendee(inviteId=inviteId, calendarId=calendarId), True
        return attendee, False

    def json(self):
        return jsonify({
            "inviteId": self.inviteId,
            "calendarId": self.calendarId
        })

    def __repr__(self):
        return '<Attendee %r>' % self.id


class Calendar(db.Model):
    # id is the calendar email canonically
    id = db.Column(db.String(320), primary_key=True)
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    @staticmethod
    def createOrGet(id):
        calendar = Calendar.query.get(id)
        if not calendar:
            return Calendar(id=id), True
        return calendar, False
    
    def json(self):
        return jsonify({
            "id": self.id
        })
        
    def __repr__(self):
        return '<Calendar %r>' % self.id


def init():
    db.create_all()
    db.session.commit()