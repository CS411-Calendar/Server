from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    calendarId = db.Column(db.string(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

class EventScheduler(db.Model):
    __tablename__ = "eventscheduler"
    id = db.Column(db.Integer, primary_key=True)
    


    
def init():
    db.create_all()
    admin = User(username='admin', email='admin@example.com')
    db.session.add(admin)
    db.session.commit()