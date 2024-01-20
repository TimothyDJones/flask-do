import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

def get_db_connection(dbname="flask_blog.db"):
    conn = sqlite3.connect(dbname)
    conn.row_factory = sqlite3.Row
    return conn

def get_post_by_id(post_id=0):
    conn = get_db_connection()
    post = conn.execute("SELECT * FROM posts WHERE id = ?",
                        (post_id, )).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

app = Flask(__name__)
app.config["SECRET_KEY"] = "This is the S3cr3t key!"


@app.route("/")
def index():
    conn = get_db_connection()
    posts = conn.execute("SELECT * FROM posts").fetchall()
    conn.close()
    return render_template("index.html", posts=posts)

@app.route("/<int:post_id>")
def post(post_id):
    post = get_post_by_id(post_id)
    return render_template("post.html", post=post)

@app.route("/create", methods=("GET", "POST"))
def create():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        if not title:
            flash("Title required!")
        else:
            conn = get_db_connection()
            conn.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
                         (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for("index"))

    return render_template("create.html")

@app.route("/<int:id>/edit", methods=("GET", "POST"))
def edit(id):
    post = get_post_by_id(id)

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        if not title:
            flash("Title required!")
        else:
            conn = get_db_connection()
            conn.execute("UPDATE posts SET title = ?, content = ? "
                        "WHERE id = ?",
                         (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for("index"))

    return render_template("edit.html", post=post)

@app.route("/<int:id>/delete", methods=("POST", ))
def delete(id):
    post = get_post_by_id(id)
    conn = get_db_connection()
    conn.execute("DELETE from posts WHERE id = ?",
                 (id, ))
    conn.commit()
    conn.close()
    flash('"{}" successfully deleted!'.format(post["title"]))
    return redirect(url_for("index"))
