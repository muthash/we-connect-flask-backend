import datetime

from app import db
from flask_bcrypt import Bcrypt


class BaseModel(db.Model):
    """Base model fromwhich all other models will inherit from"""
    def save(self):
        """Save a user to the database"""
        try:   
            db.session.add(self)
            db.session.commit()

        except Exception:
            db.session.rollback()

    def delete(self):
        """Deletes a given user"""
        try:   
            db.session.delete(self)
            db.session.commit()

        except Exception:
            db.session.rollback()

    def update(self, id, **kwargs):
        """Update selected columns in given row"""
        row_to_update = User.query.filter_by(id=id).first()
        try:
            for key, value in kwargs.items():
                setattr(row_to_update, key, value)
            db.session.commit()

        except Exception:
            db.session.rollback()


class User(BaseModel):
    """This class defines the users table"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(256), nullable=False)
    registered_on = db.Column(db.DateTime, default=db.func.current_timestamp())
    last_login = db.Column(db.DateTime, default=db.func.current_timestamp())
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, email, username, password, admin=False):
        """Initialize the user with the user details"""
        self.email = email
        self.username = username
        self.password = Bcrypt().generate_password_hash(password).decode()
        self.registered_on = datetime.datetime.now()
        self.last_login = datetime.datetime.now()
        self.admin = admin
    
    def password_is_valid(self, password):
        """Check the password against its hash"""
        return Bcrypt().check_password_hash(self.password, password)



