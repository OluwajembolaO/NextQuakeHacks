from flask import Flask, redirect, render_template, request, jsonify, session
from flask_session import Session
from profanity import profanity
import sqlite3

from functions import create_databases, date, fetch_therapy_data, generateImage, login_required, qotd
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

con = sqlite3.connect("mental.db", check_same_thread=False)
cur = con.cursor()
create_databases()


@app.route('/therapy', methods=['POST'])
@login_required
def find_therapy():
    data = request.get_json()

    if data['location'] == "" or 'location' not in data: 
        return jsonify({'error': 'Location is required.'}), 400
    location = data['location']

    therapies = fetch_therapy_data(location)
    if not therapies: return jsonify({'error': 'No therapists found nearby.'}), 404

    return jsonify(therapies)


@app.route('/gallery', methods=['GET', 'POST'])
@login_required
def gallery():
    if request.method == "POST":
        search_by = request.form.get("search")
        sort_by = request.form.get("current")
        
        return render_template("gallery.html")
    return render_template("gallery.html")


@app.route("/")
@login_required
def home():
    username = cur.execute("SELECT username FROM users WHERE id = ?", 
                           (session["user_id"],)).fetchone()
    if not username: return redirect("/login")

    q = qotd()
    if not q: return render_template("error.html", error="Sorry! Something is wrong with the quote API!")
    return render_template("index.html", qu=q, user=username[0])


@app.route('/login', methods=['GET', 'POST'])
def login():
    session.clear()
    if request.method == "POST":
        username = request.form.get("username").rstrip()
        password = request.form.get("password")

        if not (username and password): 
            return render_template("error.html", error="Fill out all required fields!")

        check = cur.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchall()
        if not (check and check_password_hash(check[0][2], password)): 
            return render_template("error.html", error="Incorrect username or password!")

        session["user_id"] = check[0][0]
        return redirect("/")
    return render_template("login.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        username = request.form.get("username").rstrip()
        password = request.form.get("password")
        confirmation = request.form.get("confirmpassword")

        if not (username and password and confirmation): 
            return render_template("error.html", error="Fill out all required fields!")
        if len(username) > 25: 
            return render_template("error.html", error="Username exceeds 25 characters!")
        if profanity.contains_profanity(username): 
            return render_template("error.html", error="Username likely contains profanity, choose another username >:(")
        if password != confirmation: 
            return render_template("error.html", error="Password does not match retyped password!")

        try: cur.execute("INSERT INTO users (username, hash_password) VALUES (?, ?)", (username, generate_password_hash(password)))
        except sqlite3.IntegrityError: return render_template("error.html", error="Username already taken!")

        con.commit()
        return redirect("/login")
    return render_template("register.html")


@app.route("/whiteboard", methods=['GET', 'POST'])
@login_required
def whiteboard():
    username = cur.execute("SELECT username FROM users WHERE id = ?", 
                           (session["user_id"],)).fetchone()
    
    if request.method == 'POST':
        story = request.form.get("story")
        if profanity.contains_profanity(story): 
            return render_template("error.html", error="Story likely contains profanity, reword your story :P")
        
        url = generateImage(story)
        if not url: return render_template("error.html", error="Sorry! Something is wrong with the image API!")

        cur.execute("INSERT INTO images (user_id, url, description, date) VALUES (?, ?, ?, ?)",
                    (session["user_id"], url, story, date()))
        con.commit()

        return render_template("whiteboard.html", image=url, user=username[0])
    return render_template("whiteboard.html", user=username[0])


if __name__ == '__main__':
    app.run(debug=True)