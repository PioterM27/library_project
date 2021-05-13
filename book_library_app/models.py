import jwt
from datetime import datetime, date, timedelta

from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from book_library_app import db

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
    book = db.relationship('Book',back_populates='user', secondary='orders')
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
    available = db.Column(db.Boolean, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=False)
    author = db.relationship('Author', back_populates='books')
    user = db.relationship("User",back_populates="book", secondary='orders')

    def __repr__(self):
        return f'{self.title} - {self.author.first_name} {self.author.last_name}'
    def to_json(self):
        book_to_json={
            "id": self.id,
            "title": self.title,
            "isbn": self.isbn,
            "number_of_pages": self.number_of_pages,
            "description": self.description,
            "author": str(self.author.first_name) + ' ' + str(self.author.last_name),
            "available":self.available
        }
        return  book_to_json
        #tu chyba book to json trzba zwrocic

class OrderBook(db.Model):
    __tablename__ = "orders"
    # id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    orders_date = db.Column(db.DateTime, nullable=False)
    expired_date = db.Column(db.DateTime, nullable=False)
    def to_json(self):
        orders_to_json ={
            # "id" : self.id,
            "book_id" : self.book_id,
            "user_id" : self.user_id,
            "title" : self.title,
            "orders_date":self.orders_date,
            "expired_date": self.expired_date
        }
        return orders_to_json
# #Schema dziedziczy z pakietu marshmalow ktory obrabia dane z bazy na jsona
# class AuthorSchema(Schema):
#     id = fields.Integer(dump_only=True)
#     first_name = fields.String(required=True, validate=validate.Length(max=50))
#     last_name = fields.String(required=True, validate=validate.Length(max=50))
#     birth_date = fields.Date('%d-%m-%Y', required=True)