from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User class."""

    __tablename__= "users"

    username = db.Column(db.String(20), 
                        primary_key=True, 
                        nullable=False, 
                        unique=True)

    password = db.Column(db.Text, 
                        nullable=False)

    email = db.Column(db.String(50), 
                        nullable=False, 
                        unique=True)

    first_name = db.Column(db.String(30), 
                            nullable=False)

    last_name = db.Column(db.String(30), 
                            nullable=False)

    def __repr__(self):
        return f"<User username={self.username} password={self.password} email={self.password} first_name={self.first_name} last_name={self.last_name}>"
    
    @classmethod
    def register(cls, username, pwd, email, first_name, last_name):
        hashed = bcrypt.generate_password_hash(pwd)
        hashed_utf8 = hashed.decode("utf8")
        user = cls(
            username=username, 
            password=hashed_utf8, 
            email=email, 
            first_name=first_name, 
            last_name=last_name
            )
        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, pwd):
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, pwd):
            return user
        else:
            return False

class Feedback(db.Model):
    """User Feedback class"""

    __tablename__= "feedback"

    id = db.Column(db.Integer, 
                    primary_key=True, 
                    autoincrement=True)
    
    title = db.Column(db.Text, 
                        nullable=False)

    content = db.Column(db.Text, 
                        nullable=False)
    
    username = db.Column(db.String(20), 
                        db.ForeignKey('users.username'), 
                        nullable=False)

    user = db.relationship('User', backref="feedback")