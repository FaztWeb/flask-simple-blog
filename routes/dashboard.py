from flask import Blueprint, render_template
from utils.mysql import mysql
from middlewares.is_authenticated import is_authenticated

dashboard_blueprint = Blueprint("dashboard", __name__)


@dashboard_blueprint.route("/dashboard")
@is_authenticated
def dashboard():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM posts")
    posts = cur.fetchall()
    cur.close()

    if result > 0:
        return render_template("dashboard.html", posts=posts)
    else:
        msg = "No articles found"
        return render_template("dashboard.html", msg=msg)
