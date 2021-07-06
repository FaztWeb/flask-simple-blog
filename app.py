from flask import Flask

# importing routes
from routes.pages import pages
from routes.auth import auth_blueprint
from routes.dashboard import dashboard_blueprint
from routes.posts import posts_blueprint

# initializing app
app = Flask(__name__)

# routes
app.register_blueprint(pages)
app.register_blueprint(auth_blueprint)
app.register_blueprint(dashboard_blueprint)
app.register_blueprint(posts_blueprint)
