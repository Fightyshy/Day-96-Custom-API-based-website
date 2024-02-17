import os
from dotenv import load_dotenv
from flask import Flask
from flask_bootstrap import Bootstrap5

from .models.models import User

from .objects.api_fetchers import ffxiv_cached_resources

bs5 = Bootstrap5()


def init_app():
    # Create app
    app = Flask(__name__, instance_relative_config=False)

    load_dotenv()  # Load first

    # Config app
    app.config["SECRET_KEY"] = os.environ["CSRF"]
    app.config["SECURITY_PASSWORD_SALT"] = os.environ["TOKEN_SALT"]
    app.config["CACHE_TYPE"] = "FileSystemCache"
    app.config["CACHE_DIR"] = "./temp"
    app.config["CACHE_DEFAULT_TIMEOUT"] = 300
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///store.db"
    app.config["UPLOAD_DIRECTORY"] = os.path.join(
        app.root_path, "../uploaded-img/"
    )
    app.config["CACHE_THRESHOLD"] = 10
    # mail config
    app.config["MAIL_SERVER"] = "smtp.gmail.com"
    app.config["MAIL_PORT"] = "587"
    app.config["MAIL_USERNAME"] = os.environ["SENDER"]
    app.config["MAIL_PASSWORD"] = os.environ["SENDER_PASSWORD"]
    app.config["MAIL_DEFAULT_SENDER"] = os.environ["SENDER"]
    app.config["MAIL_USE_TLS"] = True
    app.config["MAIL_USE_SSL"] = True

    # Apply app libraries
    bs5.init_app(app)
    from .objects.api_fetchers import cache

    cache.init_app(app)

    from .models.models import db

    db.init_app(app)

    from .views.char_get import login_manager

    login_manager.init_app(app)
    @login_manager.user_loader
    def load_user(user_id):
        return db.get_or_404(User, user_id)
    
    from .views.auth import mail_manager
    mail_manager
    mail_manager.init_app(app)

    # substitute with actual caching solution or cache to file later
    # for now, filesystem cache to temp folder
    ffxiv_cached_resources()

    # Set app blueprints
    from .views.char_get import main_page
    from .views.card_maker import card_maker
    from .views.auth import auth

    app.register_blueprint(main_page)
    app.register_blueprint(card_maker)
    app.register_blueprint(auth)
    with app.app_context():
        db.create_all()
    return app
