from flask import jsonify, request
from book_library_app import app, db
from book_library_app.models import Author
from datetime import datetime
from flask_login import login_required



@app.route('/api/v1/authors', methods=['GET'])
@login_required
def get_authors():
    authors = Author.query
    list_of_authors = []
    for author in authors:
        list_of_authors.append(author.to_json())
    return jsonify({'success': True, 'data': list_of_authors})


@app.route('/api/v1/authors/<int:author_id>', methods=['GET'])
def get_author(author_id: int):
    author = Author.query.filter(Author.id == author_id).one()
    return jsonify(author.to_json())


# obsluga POST ,z racji ze jest to metoda post to argument jest przegazany w requescie
@app.route('/api/v1/authors/<int:author_id>', methods=['PUT'])
def update_author(author_id: int):
    author = Author.query.filter(Author.id == author_id).one()
    if not author:
        message = f"Author with {author_id} not found"
    else:
        request_author = request.json
        # author.id = request_author["id"]
        author.first_name = request_author["first_name"]
        author.last_name = request_author["last_name"]
        author.birth_date = datetime.strptime(request_author["birth_date"], '%d-%m-%Y')
        message = "Author has been updated"
        db.session.commit()

    return jsonify({
        "message" : message
    })


@app.route('/api/v1/authors', methods=['POST'])
def create_authors():
    author = Author()
    request_author = request.json
    author.id = request_author["id"]
    author.first_name = request_author["first_name"]
    author.last_name = request_author["last_name"]
    author.birth_date = datetime.strptime(request_author["birth_date"], '%d-%m-%Y')

    db.session.add(author)
    db.session.commit()

    return jsonify({"succes": True, "info": "Author has been succesfful added"})


@app.route('/api/v1/authors/<int:author_id>', methods=['DELETE'])
def delete_author(author_id: int):
    author = Author.query.filter(Author.id == author_id).one()
    db.session.delete(author)
    db.session.commit()
    return jsonify({'success': True, 'data': f'Author with id {author_id} has been deleted'})
