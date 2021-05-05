import re
from flask import request,url_for
from book_library_app import db
from marshmallow import Schema, fields, validate, validates, ValidationError  #pip install marshmallow obrabia dane z bazy w format json
from  datetime import datetime
from flask_sqlalchemy import BaseQuery
from typing import Tuple
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from flask import current_app
from flask_login import UserMixin
from datetime import datetime, date, timedelta
from marshmallow import Schema, fields, validate, validates, ValidationError
from werkzeug.security import generate_password_hash, check_password_hash

from book_library_app import db

from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.sql.expression import BinaryExpression

#Tworzymy clase ktora bedzie reprezentowala tabele w bazie dancyh

class Author(db.Model):
    #to jest atrybut z bazy danych to tablename
    __tablename__ = "authors"
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(50),nullable=False)  # nullable False oznacza,ze przy dodawaniu nowego obiektu to pole nie moze byc puste
    last_name = db.Column(db.String(50), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    books = db.relationship('Book', back_populates='author',cascade='all,delete-orphan')

    def __repr__(self):
        return f'<{self.__class__.__name__}>: {self.first_name} {self.last_name}'
    def to_json(self):
        author_to_json ={
            "id" : self.id,
            "first_name" : self.first_name,
            "last_name" : self.last_name,
            "birth_date" : self.birth_date
        }
        return author_to_json


class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True, index=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    @staticmethod
    def generate_hashed_password(password: str) -> str:
        return generate_password_hash(password)

    def is_password_valid(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    def generate_jwt(self) -> bytes:
        payload = {
            'user_id': self.id,
            'exp': datetime.utcnow() + timedelta(minutes=current_app.config.get('JWT_EXPIRED_MINUTES', 30))
        }
        return jwt.encode(payload, current_app.config.get('SECRET_KEY'))
    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return str(self.id)
    # @LoginManager.user_loader
    # def load_user(self,user_id):
    #     return User.query.get(int(user_id))

    # @login_manager.user_accessed
    # def load_user(self,user_id):
    #     print("test_logowania")
    #     return User.query.get(int(user_id))

class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    isbn = db.Column(db.BigInteger, nullable=False, unique=True)
    number_of_pages = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=False)
    author = db.relationship('Author', back_populates='books')

    def __repr__(self):
        return f'{self.title} - {self.author.first_name} {self.author.last_name}'
    def to_json(self):
        book_to_json={
            "id": self.id,
            "title": self.title,
            "isbn": self.isbn,
            "number_of_pages": self.number_of_pages,
            "description": self.description,
            "author": str(self.author.first_name) + ' ' + str(self.author.last_name)
        }


# #Schema dziedziczy z pakietu marshmalow ktory obrabia dane z bazy na jsona
# class AuthorSchema(Schema):
#     id = fields.Integer(dump_only=True)
#     first_name = fields.String(required=True, validate=validate.Length(max=50))
#     last_name = fields.String(required=True, validate=validate.Length(max=50))
#     birth_date = fields.Date('%d-%m-%Y', required=True)