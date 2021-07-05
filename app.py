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

from posts import Posts

from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt

posts = Posts()

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/posts")
def postsPage():
    return render_template("posts.html", posts=posts)


@app.route("/posts/<string:id>")
def postPage(id):
    return render_template("post.html", id=id)


class RegisterForm(Form):
    name = StringField("Name", [validators.Length(min=1, max=50)])
    username = StringField("Username", [validators.Length(min=3, max=25)])
    email = StringField("Email", [validators.Length(min=6, max=60)])
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
    if request.method == 'POST' and form.validate():
        return render_template('register.html')
    return render_template('register.html', form=form)
        


if __name__ == "__main__":
    app.run(debug=True, port=3000)
