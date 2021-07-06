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
from wtforms.fields.html5 import EmailField
from passlib.hash import sha256_crypt

posts = Posts()

app = Flask(__name__)

# mysql settings
app.config["MYSQL_HOST"] = "127.0.0.1"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "faztpassword"
app.config["MYSQL_DB"] = "flaskblog"
app.config["MYSQL_CURSORCLASS"] = "DictCursor" # to return a dictionary instead of a tuple

# init mysql
mysql = MySQL(app)


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
        flash('You are now register and can login', 'success')
        redirect(url_for('login'))
    return render_template("register.html", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        cur = mysql.connection.cursor()

        result = cur.execute('SELECT * FROM users WHERE username = %s', [username])

        if result > 0:
            data = cur.fetchone()
            saved_password = data['password']

            if sha256_crypt.verify(password, saved_password):
                session['logged_in'] = True
                session['username'] = data['username'] 
                flash("You're now logged in", "success")
                return redirect(url_for('dashboard'))
            else:
                error = 'User not foudn'
                return render_template('login.html', error = error)
            cur.close()

        else:
            error = 'User not foudn'
            return render_template('login.html', error = error)

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == "__main__":
    app.secret_key="somsecretkey"
    app.run(debug=True, port=3000)
