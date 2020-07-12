from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, ColumnDefault
from sqlalchemy.orm import relationship
import json

db = SQLAlchemy()
ENV = 'prod'
database_path = 'postgres://localhost:5432/concierge'
prod_database = 'postgres://oyfluxjrleohjc:1a8880c54e9afda6dd6ef73e5c8fa6b3d43c479bbe11df6b7e556f3e5bb13b57@ec2-18-214-119-135.compute-1.amazonaws.com:5432/dfb499e5tqqfqi'


def setup_db(app, database_path=database_path):
    if ENV == 'dev':
        app.debug = True
        app.config['SQLALCHEMY_DATABASE_URI'] = database_path

    if ENV == 'prod':
        app.debug = False
        app.config['SQLALCHEMY_DATABASE_URI'] = prod_database

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    db.create_all()


def drop_and_create_all():
    db.drop_all()
    db.create_all()


class Restaurant(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    cuisine_id = Column(Integer, ForeignKey('cuisine.id'), nullable=False)
    location_id = Column(Integer, ForeignKey('location.id'), nullable=False)
    age_policy_id = Column(
        Integer, ForeignKey('age_policy.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)
    rating = Column(Integer)
    address = Column(String(120), nullable=False)
    phone_number = Column(String(30))
    prebooking_required = Column(Boolean, nullable=False)

    cuisine = relationship('Cuisine', backref='restaurant', lazy=True)
    category = relationship('Category', backref='restaurant', lazy=True)
    age_policy = relationship('Age_policy', backref='restaurant', lazy=True)
    location = relationship('Location', backref='restaurant', lazy=True)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def public_info(self):
        return {
            'id': self.id,
            'name': self.name,
            'cuisine': self.cuisine.name,
            'location': self.location.name
        }

    def detailed_info(self):
        return {
            'id': self.id,
            'name': self.name,
            'cuisine': self.cuisine.name,
            'location': self.location.name,
            'age_policy': self.age_policy.age,
            'category': self.category.name,
            'rating': self.rating,
            'address': self.address,
            'phone_number': self.phone_number,
            'prebooking_required': self.prebooking_required
        }

    def __repr__(self):
        return f'<{self.id} : {self.name}>'


class Category(db.Model):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(40), nullable=False)

    def format(self):
        return {
            'id': self.id,
            'name': self.name
        }

    def __repr__(self):
        return f'<{self.id} : {self.name}>'


class Cuisine(db.Model):
    __tablename__ = 'cuisine'

    id = Column(Integer, primary_key=True)
    name = Column(String(40), nullable=False)

    def format(self):
        return {
            'id': self.id,
            'name': self.name
        }

    def __repr__(self):
        return f'<{self.id} : {self.name}>'


class Location(db.Model):
    __tablename__ = 'location'

    id = Column(Integer, primary_key=True)
    name = Column(String(60), nullable=False)

    def format(self):
        return {
            'id': self.id,
            'name': self.name
        }

    def __repr__(self):
        return f'<{self.id} : {self.name}>'


class Age_policy(db.Model):
    __tablename__ = 'age_policy'

    id = Column(Integer, primary_key=True)
    age = Column(Integer, nullable=False)

    def format(self):
        return {
            'id': self.id,
            'age': self.age
        }

    def __repr__(self):
        return f'<{self.id} : {self.age}>'


class Notes(db.Model):
    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True)
    note = Column(Text, nullable=False)
    restaurant_id = Column(Integer, nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            self.id: self.note
        }

    def __repr__(self):
        return f'<{self.id} : rest_id({self.restaurant_id})>'
