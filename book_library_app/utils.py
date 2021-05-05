from book_library_app import app,login_manager
from book_library_app.models import User

@login_manager.user_loader
def load_user(user_id):
    print(user_id)
    return User.query.get(str(user_id))
