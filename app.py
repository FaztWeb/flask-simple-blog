from flask import Flask
from config import MYSQL_DB, MYSQL_HOST, MYSQL_PASSWORD, MYSQL_USER

# importing routes
from routes.pages import pages
from routes.auth import auth_blueprint
from routes.dashboard import dashboard_blueprint
from routes.posts import posts_blueprint

# initializing app
app = Flask(__name__)

# MySQL settings
app.config["MYSQL_HOST"] = MYSQL_HOST
app.config["MYSQL_USER"] = MYSQL_USER
app.config["MYSQL_PASSWORD"] = MYSQL_PASSWORD
app.config["MYSQL_DB"] = MYSQL_DB
app.config[
    "MYSQL_CURSORCLASS"
] = "DictCursor"  # to return a dictionary instead of a tuple

# routes
app.register_blueprint(pages)
app.register_blueprint(auth_blueprint)
app.register_blueprint(dashboard_blueprint)
app.register_blueprint(posts_blueprint)
