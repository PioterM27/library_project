from flask import Flask
from config import Config
from flask_sqlalchemy import  SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(Config)


db = SQLAlchemy(app)
#migrate sluzy do miggracji bazy danych
migrate = Migrate(app, db)

#test polaczenie do bazy dancyh
# results = db.session.execute('show databases')
# for row in results:
#     print(row)

# chcac stworzyc nowa baze w comand linie mysql komenda create database nazwa_bazy
#przesylajac argumenty do bazy przekazujemy je jawnie czuli name="Jan itp

from book_library_app import authors
from book_library_app import books
from book_library_app import models
from book_library_app import auth
from book_library_app import db_manage_commands
