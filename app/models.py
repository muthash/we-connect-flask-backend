import datetime

from flask_bcrypt import Bcrypt
from app import db


class BaseModel(db.Model):
    """Base model from which all other models will inherit from"""
    __abstract__ = True

    def save(self):
        """Save the given object to the database"""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Deletes a given object"""
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def update(class_name, row_id, **kwargs):
        """Update selected columns in given row in a table"""
        row = class_name.query.filter_by(id=row_id).first()
        for column in kwargs:
            setattr(row, column, kwargs[column])
        db.session.commit()


class User(BaseModel):
    """This class defines the users table"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(256), nullable=False)
    registered_on = db.Column(db.DateTime, default=db.func.current_timestamp())
    last_login = db.Column(db.DateTime, default=db.func.current_timestamp())
    status = db.Column(db.Integer, default=0)
    business_ = db.relationship('Business', backref='owner', cascade="all, delete-orphan", lazy=True)
    user_reviews = db.relationship('Review', backref='reviewer', cascade="all, delete-orphan", lazy=True)

    def __init__(self, email, username, password, status=0):
        """Initialize the user with the user details"""
        self.email = email
        self.username = username
        self.password = Bcrypt().generate_password_hash(password).decode()
        self.registered_on = datetime.datetime.now()
        self.last_login = datetime.datetime.now()
        self.status = status

    def password_is_valid(self, password):
        """Check the password against its hash"""
        return Bcrypt().check_password_hash(self.password, password)

    def __repr__(self):
        return 'user: {}'.format(self.username)


class Business(BaseModel):
    """This class defines the business table"""

    __tablename__ = 'business'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(256), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    reviews = db.relationship('Review', backref='belongs', cascade="all, delete-orphan", lazy=True)

    def __init__(self, name, description, category, location, user_id):
        """Initialize the business with the businesses details"""
        self.name = name
        self.description = description
        self.category = category
        self.location = location
        self.user_id = user_id
    
    def serialize(self):
        """Return a dictionary"""
        return {
            'business_name': self.name,
            'description': self.description,
            'category': self.category,
            'location': self.location
        }


    def __repr__(self):
        return 'business: {}'.format(self.name)


class Review(BaseModel):
    """This class defines the review table"""

    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(256), nullable=False)
    rating = db.Column(db.Integer, default=1)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    business_id = db.Column(db.Integer, db.ForeignKey('business.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, description, rating, business_id, user_id):
        """Initialize the user with the user details"""
        self.description = description
        self.rating = rating
        self.business_id = business_id
        self.user_id = user_id

    def serialize(self):
        """Return a dictionary"""
        return {
            'review': self.description,
            'rating': self.rating
        }

    def __repr__(self):
        return 'review: {}'.format(self.description)


class BlacklistToken(BaseModel):
    """This class defines the review table"""

    __tablename__ = 'blacklist_token'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)
    revoked = db.Column(db.Boolean, default=True)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    def __repr__(self):
        return 'token: {}'.format(self.token)
