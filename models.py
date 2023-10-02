"""Models for Flask Feedback Exercise."""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

Bcrypt = Bcrypt()
db = SQLAlchemy()


def connect_db(app):
    """Connect this database to Flask app and call."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """User."""

    __tablename__ = "users"

    username = db.Column(
        db.String(20),
        nullable=False,
        unique=True,
        primary_key=True,
    )
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    feedback = db.relationship("Feedback", backref="user", cascade="all, delete")

    # class methods

    @classmethod
    def authenticate(cls, username, password):
        """Validate that user exists and password is correct. Return user if valid; else return False."""

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False


class Feedback(db.Model):
    """Feedback."""

    __tablename__ = "feedback"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(
        db.String(20),
        db.ForeignKey("users.username"),
        nullable=False,
    )
