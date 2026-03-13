from flask import Flask, render_template, request, redirect, session
from flask_socketio import SocketIO, send, emit
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "sparklinksecret"

socketio = SocketIO(app)

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


# HOME
@app.route("/")
def home():
    return render_template("index.html")


# ABOUT PAGE
@app.route("/about")
def about():
    return render_template("about.html")


# REGISTER
@app.route("/register", methods=["GET","POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db()

        conn.execute(
        "INSERT INTO users(name,email,password) VALUES (?,?,?)",
        (name,email,password)
        )

        conn.commit()

        return redirect("/login")

    return render_template("register.html")


# LOGIN
@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = get_db()

        user = conn.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (email,password)
        ).fetchone()

        if user:
            session["user_id"] = user["id"]
            return redirect("/dashboard")

    return render_template("login.html")


# DASHBOARD
@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db()

    user = conn.execute(
    "SELECT * FROM users WHERE id=?",
    (session["user_id"],)
    ).fetchone()

    return render_template("dashboard.html", user=user)


# PROFILE EDIT
@app.route("/profile", methods=["GET","POST"])
def profile():

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db()

    if request.method == "POST":

        age = request.form["age"]
        gender = request.form["gender"]
        location = request.form["location"]
        bio = request.form["bio"]

        photo = request.files.get("photo")

        filename = None

        if photo and photo.filename != "":
            filename = photo.filename
            photo.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        conn.execute("""

        UPDATE users
        SET age=?, gender=?, location=?, bio=?, profile_photo=?
        WHERE id=?

        """,(age,gender,location,bio,filename,session["user_id"]))

        conn.commit()

        return redirect("/dashboard")

    user = conn.execute(
    "SELECT * FROM users WHERE id=?",
    (session["user_id"],)
    ).fetchone()

    return render_template("profile.html", user=user)


# VIEW OTHER USER PROFILE
@app.route("/view_profile/<int:user_id>")
def view_profile(user_id):

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db()

    user = conn.execute(
    "SELECT * FROM users WHERE id=?",
    (user_id,)
    ).fetchone()

    return render_template("view_profile.html", user=user)


# DISCOVER USERS
@app.route("/discover")
def discover():

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db()

    users = conn.execute("""

    SELECT * FROM users
    WHERE id != ?

    """,(session["user_id"],)).fetchall()

    return render_template("discover.html", users=users)


# LIKE USER
@app.route("/like/<int:user_id>")
def like(user_id):

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db()

    current_user = session["user_id"]

    conn.execute(
    "INSERT INTO likes(user_id,liked_user_id) VALUES (?,?)",
    (current_user,user_id)
    )

    conn.commit()

    match = conn.execute(
    "SELECT * FROM likes WHERE user_id=? AND liked_user_id=?",
    (user_id,current_user)
    ).fetchone()

    if match:

        conn.execute(
        "INSERT INTO matches(user1_id,user2_id) VALUES (?,?)",
        (current_user,user_id)
        )

        conn.commit()

    return redirect("/discover")


# MATCHES
@app.route("/matches")
def matches():

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db()

    user_id = session["user_id"]

    matches = conn.execute("""

    SELECT users.*
    FROM matches
    JOIN users ON users.id = matches.user2_id
    WHERE matches.user1_id = ?

    UNION

    SELECT users.*
    FROM matches
    JOIN users ON users.id = matches.user1_id
    WHERE matches.user2_id = ?

    """,(user_id,user_id)).fetchall()

    return render_template("matches.html", matches=matches)


# CHAT PAGE
@app.route("/chat/<int:user_id>")
def chat(user_id):

    if "user_id" not in session:
        return redirect("/login")

    return render_template("chat.html", user_id=user_id)


# REALTIME MESSAGE
@socketio.on("message")
def handle_message(data):

    conn = get_db()

    sender = data["sender"]
    receiver = data["receiver"]
    message = data["message"]

    conn.execute(
    "INSERT INTO messages(sender_id,receiver_id,message) VALUES (?,?,?)",
    (sender,receiver,message)
    )

    conn.commit()

    send(data, broadcast=True)


# TYPING EVENT
@socketio.on("typing")
def typing():

    emit("typing", broadcast=True)


# LOGOUT
@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


if __name__ == "__main__":
    socketio.run(app, debug=True)