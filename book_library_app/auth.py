from flask import abort, jsonify,request
from book_library_app import db,app
from book_library_app.models import User


@app.route('/register', methods=['POST'])
def register():
    user = User()
    request_register = request.json
    if User.query.filter(User.username == request_register['username']).first():
        abort(409, description=f'User with username {request_register["username"]} already exists')
    if User.query.filter(User.email == request_register['email']).first():
        abort(409, description=f'User with email {request_register["email"]} already exists')
    request_register['password'] = User.generate_hashed_password(request_register['password'])

    user.email = request_register["email"]
    user.password = request_register["password"]
    user.username = request_register["username"]

    db.session.add(user)
    db.session.commit()

    token = user.generate_jwt()

    return jsonify({
        'success': True,
        'token': token
    }), 201


@app.route('/login', methods=['POST'])
def login():
    request_register = request.json
    user = User.query.filter(User.username == request_register['username']).first()
    if not user:
        abort(401, description="Invalid credential")
    if not user.is_password_valid(request_register['password']):
        abort(401, description="Invalid credential")
#error 401 jest nie zaimplementowany jak wszystkie errory zreszta

    token = user.generate_jwt()

    return jsonify({
        'success': True,
        'token': token
    }), 201