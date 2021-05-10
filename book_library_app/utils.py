from book_library_app import app,login_manager
from book_library_app.models import User
from contextlib import contextmanager

from book_library_app import db

@login_manager.user_loader
def load_user(user_id):
    print(user_id)
    return User.query.get(str(user_id))

@contextmanager
def session_scope():
    session = db.session
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
