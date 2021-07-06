from flask import Blueprint, request, session, flash, redirect, url_for, render_template
from passlib.hash import sha256_crypt
from extensions.mysql import mysql
from models.register_form import RegisterForm

auth_blueprint = Blueprint("auth", __name__)

@auth_blueprint.route("/register", methods=["GET", "POST"])
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
        redirect(url_for("auth.login"))
    return render_template("auth/register.html", form=form)


@auth_blueprint.route("/login", methods=["GET", "POST"])
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
                return redirect(url_for("dashboard.dashboard"))
            else:
                error = "User not foudn"
                return render_template("auth/login.html", error=error)

        else:
            error = "User not foudn"
            return render_template("auth/login.html", error=error)

    return render_template("auth/login.html")


@auth_blueprint.route("/logout")
def logout():
    session.clear()
    flash("you are now logged out", "success")
    return redirect(url_for("auth.login"))
