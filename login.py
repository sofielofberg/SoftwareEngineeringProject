from flask_login import LoginManager

import user

login_manager = LoginManager()


def init_login_manager(app):
    login_manager.init_app(app)
    login_manager.session_protection = "strong"
    login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return user.User.get_by_id(user_id)
