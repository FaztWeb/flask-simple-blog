from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from extensions.mysql import mysql
from middlewares.is_authenticated import is_authenticated
from models.post_form import PostForm

posts_blueprint = Blueprint("posts", __name__)


@posts_blueprint.route("/posts")
def render_posts():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM posts")
    posts = cur.fetchall()
    cur.close()

    if result > 0:
        return render_template("posts/list_posts.html", posts=posts)
    else:
        msg = "No posts found"
        return render_template("posts/list_posts.html", msg=msg)


@posts_blueprint.route("/posts/<string:id>")
@is_authenticated
def render_post(id):
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM posts WHERE id = %s", [id])
    post = cur.fetchone()
    cur.close()
    return render_template("posts/post.html", post=post)


@posts_blueprint.route("/add_post", methods=["GET", "POST"])
@is_authenticated
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
        return redirect(url_for("dashboard.dashboard"))

    return render_template("posts/add_post.html", form=form)


@posts_blueprint.route("/edit_post/<id>", methods=["GET", "POST"])
@is_authenticated
def edit_post(id):

    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM posts WHERE id = %s", [id])
    post = cur.fetchone()
    mysql.connection.commit()
    cur.close()

    form = PostForm(request.form)

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
        return redirect(url_for("dashboard.dashboard"))

    return render_template("posts/edit_post.html", form=form)


@posts_blueprint.route("/delete_post/<string:id>", methods=["POST"])
@is_authenticated
def delete_post(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM posts WHERE id = %s", [id])
    mysql.connection.commit()
    cur.close()

    flash("Article deleted", "sucess")
    return redirect(url_for("dashboard.dashboard"))
