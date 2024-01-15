import os
from dotenv import load_dotenv
from flask import Flask
from flask_bootstrap import Bootstrap5

from application.views.api_fetchers import ffxiv_cached_resources

bs5 = Bootstrap5()
COLLECT_CACHE = ""


def init_app():
    # Create app
    app = Flask(__name__, instance_relative_config=False)

    load_dotenv()  # Load first
    
    # Config app
    app.config["SECRET_KEY"] = os.environ["CSRF"]
    app.config["SECURITY_PASSWORD_SALT"] = os.environ["TOKEN_SALT"]
    app.config["CACHE_TYPE"] = "SimpleCache"
    app.config["CACHE_DEFAULT_TIMEOUT"] = 300

    # Apply app libraries
    bs5.init_app(app)
    from .views.api_fetchers import cache
    cache.init_app(app)

    # Set app blueprints
    from .views.main import main_page
    app.register_blueprint(main_page)
    return app