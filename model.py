from flask_sqlalchemy import SQLAlchemy

# Instantiate a SQLAlchemy object.
db = SQLAlchemy()

class User(db.Model):
    """Data model for a user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    cal_id = db.Column(db.Integer,
                       db.ForeignKey('calendars.cal_id'),
                        nullable=True)
    name = db.Column(db.String(75),
                     nullable=False)
    username = db.Column(db.String(30),
                         nullable=False)
    password = db.Column(db.String(30),
                         nullable=False)

    # define relationship to calendars table
    calendar = db.relationship("Calendar", backref=db.backref("users"))

    def __repr__(self):
        """Returns readable info about an instance of a user object."""

        return f"<Name: {self.name}, Calendar_id: {self.cal_id}, Username: {username}>"

class Calendar(db.Model):
    """Data model for Calendar."""

    __tablename__ = 'calendars'

    cal_id = db.Column(db.Integer, 
                       autoincrement=True,
                       primary_key=True)
    house_addr = db.Column(db.String(50))

    house_name = db.Column(db.String(50))

    # define relationship to users table
    # db.relationship("User", backref=db.backref("calendars"))

    def __repr__(self): 
        """Returns readable info about an instance of a calendar object."""

        return f"<Calendar_id: {self.cal_id}, House_addr: {self.house_addr}, House_name: {self.house_name}>"


class Event(db.Model):
    """Data model for Event."""

    __tablename__ = 'events'

    event_id = db.Column(db.Integer,
                         autoincrement=True,
                         primary_key=True)
    cal_id = db.Column(db.Integer,
                       db.ForeignKey('calendars.cal_id'),
                       nullable=False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'),
                        nullable=False)
    event_type = db.Column(db.String(50),
                            nullable=False)
    start_time = db.Column(db.DateTime,
                           nullable=False)
    end_time = db.Column(db.DateTime,
                           nullable=False)
    approved = db.Column(db.Boolean)

    # define relationship to calendars table
    calendar = db.relationship("Calendar", backref=db.backref("events"))


    def __repr__(self):
         """Returns readable info about an instance of a calendar object."""

         return f"<Event_id: {self.event_id}, Event_type: {self.event_type}, User_id: {self.user_id}>"

# Connect db to app
def connect_to_db(app):
    """Connect the database to our Flask app."""
    # Configure to use our database.
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///calendars"
    app.config["SQLALCHEMY_ECHO"] = False
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

if __name__ == "__name__":

    from server import app
    connect_to_db(app)
    print("Connected to DB")










