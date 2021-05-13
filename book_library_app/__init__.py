from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from config import Config





app = Flask(__name__)
app.config.from_object(Config)
login_manager = LoginManager()
login_manager.init_app(app)


db = SQLAlchemy(app)
#migrate sluzy do miggracji bazy danych
migrate = Migrate(app, db)

from book_library_app import authors
from book_library_app import books
from book_library_app import models
from book_library_app import auth
from book_library_app import orders
from book_library_app import db_manage_commands
from book_library_app import errors

#test polaczenie do bazy dancyh
# results = db.session.execute('show databases')
# for row in results:
#     print(row)

# chcac stworzyc nowa baze w comand linie mysql komenda create database nazwa_bazy
#przesylajac argumenty do bazy przekazujemy je jawnie czuli name="Jan itp

# from book_library_app import authors
# from book_library_app import books
# from book_library_app import models
# from book_library_app import auth
# from book_library_app import db_manage_commands
# from book_library_app import errors
