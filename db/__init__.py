from flask_sqlalchemy import SQLAlchemy
from config import app
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.String(75), primary_key=True)
    
    def __repr__(self):
        return '<User %r>' % self.id


class Invite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ownerId = db.Column(db.String(75), db.ForeignKey('user.id'), nullable=False)
    owner = db.relationship('User')
    def __repr__(self):
        return '<Invite %r>' % self.id


class InviteCalendar(db.Model):
    inviteId = db.Column(db.Integer, db.ForeignKey('invite.id'), nullable=False)
    invite = db.relationship('Invite')
    calendarId = db.Column(db.String(320), db.ForeignKey('calendar.id'), nullable=False)
    calendar = db.relationship('Calendar')
    __table_args__ = (
        db.PrimaryKeyConstraint(
            inviteId, calendarId,
        ),
    )
    def __repr__(self):
        return '<InviteCalendar %r>' % self.id


class Calendar(db.Model):
    id = db.Column(db.String(320), primary_key=True)
    def __repr__(self):
        return '<Calendar %r>' % self.id

def init():
    db.create_all()
    # admin = User()
    # db.session.add(admin)
    db.session.commit()