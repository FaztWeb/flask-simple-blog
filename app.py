from flask import (
    Flask,
    render_template,
    flash,
    redirect,
    url_for,
    session,
    logging,
    request,
)

from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from wtforms.fields.html5 import EmailField
from passlib.hash import sha256_crypt
from functools import wraps

# routes
from pages import pages

app = Flask(__name__)
app.register_blueprint(pages)

# mysql settings
app.config["MYSQL_HOST"] = "127.0.0.1"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "faztpassword"
app.config["MYSQL_DB"] = "flaskblog"
app.config[
    "MYSQL_CURSORCLASS"
] = "DictCursor"  # to return a dictionary instead of a tuple

# init mysql
mysql = MySQL(app)


@app.route("/posts")
def postsPage():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM posts")
    posts = cur.fetchall()
    cur.close()

    if result > 0:
        return render_template("posts.html", posts=posts)
    else:
        msg = "No posts found"
        return render_template("posts.html", msg=msg)


@app.route("/posts/<string:id>")
def postPage(id):
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM posts WHERE id = %s", [id])
    post = cur.fetchone()
    cur.close()
    return render_template("post.html", post=post)


class RegisterForm(Form):
    name = StringField("Name", [validators.Length(min=1, max=50)])
    username = StringField("Username", [validators.Length(min=3, max=25)])
    email = EmailField("Email", [validators.Length(min=6, max=60)])
    password = PasswordField(
        "Password",
        [
            validators.DataRequired(),
            validators.EqualTo("confirm", message="Password do not match"),
        ],
    )
    confirm = PasswordField("Confirm Password")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # create a cursor
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)",
            (name, email, username, password),
        )

        mysql.connection.commit()
        cur.close()
        flash("You are now register and can login", "success")
        redirect(url_for("login"))
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        cur = mysql.connection.cursor()

        result = cur.execute("SELECT * FROM users WHERE username = %s", [username])

        if result > 0:
            data = cur.fetchone()
            saved_password = data["password"]
            cur.close()

            if sha256_crypt.verify(password, saved_password):
                session["logged_in"] = True
                session["username"] = data["username"]
                flash("You're now logged in", "success")
                return redirect(url_for("dashboard"))
            else:
                error = "User not foudn"
                return render_template("login.html", error=error)

        else:
            error = "User not foudn"
            return render_template("login.html", error=error)

    return render_template("login.html")


def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("Unauthorized. Login first", "danger")
            return redirect(url_for("login"))

    return wrap


@app.route("/dashboard")
@is_logged_in
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


@app.route("/logout")
def logout():
    session.clear()
    flash("you are now logged out", "success")
    return redirect(url_for("login"))


class ArticleForm(Form):
    title = StringField("Title", [validators.Length(min=1, max=200)])
    content = TextAreaField("Content", [validators.Length(min=30)])


@app.route("/add_post", methods=["GET", "POST"])
@is_logged_in
def add_post():
    form = ArticleForm(request.form)
    if request.method == "POST" and form.validate():
        title = form.title.data
        content = form.content.data

        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO posts (title, content, author) VALUES(%s, %s, %s)",
            (title, content, session["username"]),
        )
        mysql.connection.commit()
        cur.close()

        flash("Post saved", "success")
        redirect(url_for("dashboard"))

    return render_template("add_article.html", form=form)


@app.route("/edit_post/<id>", methods=["GET", "POST"])
@is_logged_in
def edit_post(id):

    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM posts WHERE id = %s", [id])
    post = cur.fetchone()
    mysql.connection.commit()
    cur.close()

    form = ArticleForm(request.form)

    # populate values in the form
    form.title.data = post["title"]
    form.content.data = post["content"]

    if request.method == "POST" and form.validate():
        title = request.form["title"]
        content = request.form["content"]

        cur = mysql.connection.cursor()

        cur.execute(
            "UPDATE posts SET title = %s, content = %s WHERE id = %s",
            (title, content, id),
        )
        mysql.connection.commit()
        cur.close()

        flash("Post updated", "success")
        return redirect(url_for("dashboard"))

    return render_template("edit_post.html", form=form)


@app.route("/delete_post/<string:id>", methods=["POST"])
@is_logged_in
def delete_post(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM posts WHERE id = %s", [id])
    mysql.connection.commit()
    cur.close()

    flash("Article deleted", "sucess")
    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    app.secret_key = "somsecretkey"
    app.run(debug=True, port=3000)
