'''komendy sluzace do dodawania usuwanaia i aktualizacji bazy danych z poziomu aplikacjui'''

import json
from pathlib import Path
from datetime import datetime

from book_library_app import app, db
from book_library_app.models import Author,Book

#nie wiem co to robi, app.cli tworzy grupe comend we flasku jak z terminala wywolamy flask to sie tam wyswietli


def load_json_data(file_name: str) -> list:
    json_path = Path(__file__).parent / 'samples' / file_name
    with open(json_path) as file:
        data_json = json.load(file)
    return data_json

@app.cli.group()
def db_manage():
    '''Database managment commands'''
    pass

@db_manage.command()
def add_data():
    """Add sample data to database"""
    try:
        data_json = load_json_data('authors.json')
        for item in data_json:
            item['birth_date'] = datetime.strptime(item['birth_date'], '%d-%m-%Y').date()
            author = Author(**item)
            db.session.add(author)

        data_json = load_json_data('books.json')
        for item in data_json:
            book = Book(**item)
            db.session.add(book)

        db.session.commit()
        print('Data has been successfully added to the database')
    except Exception as exc:
        print("Unexpected error: {}".format(exc))

@db_manage.command()
def remove_data():
    """Remove all data from the database"""
    try:
        db.session.execute('DELETE FROM books')
        db.session.execute('ALTER TABLE books AUTO_INCREMENT = 1')
        db.session.execute('DELETE FROM authors')
        db.session.execute('ALTER TABLE authors AUTO_INCREMENT = 1')
        db.session.commit()
        print('Data has been successfully removed from the database')
    except Exception as exc:
        print("Unexpected error: {}".format(exc))
