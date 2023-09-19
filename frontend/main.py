from flask import Flask, redirect, url_for, render_template, request, session
from datetime import timedelta

response = [
        {
            "description": "hij",
            "id": "5cc47b38-f651-4f21-91fd-0466349de941",
            "image": "def",
            "timestamp": "10000000.0",
            "title": "abc",
            "userId": "6c5c1db5-23d0-4524-b045-aefd622307aa"
        },
        {
            "description": "hij",
            "id": "a43d4030-12ec-4024-bd95-1a3e53e8debe",
            "image": "def",
            "timestamp": "1695111195.372656",
            "title": "abc",
            "userId": "6c5c1db5-23d0-4524-b045-aefd622307ab"
        }
    ]
description = "hij"
userid = ["6c5c1db5-23d0-4524-b045-aefd622307aa", "a43d4030-12ec-4024-bd95-1a3e53e8debe"]
title = ["abc", "def"]
image = ""
timestamp = ["1695111195.372656", "1695111195.372656"]


#print(html)


app = Flask(__name__)
app.secret_key = "dYVXfvWUUywT86uvSFzwdM19Nk3RNK"
app.permanent_session_lifetime = timedelta(minutes=5)

@app.route("/")
def home(): 
    print([render_template('postTemplate.html', **r) for r in response])
    html = '\n'.join([render_template('postTemplate.html', **r) for r in response])
    return render_template("index.html", content=html)


@app.route("/login/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True  # <--- makes the permanent session
        user = request.form["userid"]
        session["user"] = user
        return redirect("/")
    else:
        if "user" in session:
            return redirect("/")

        return render_template("login.html")
    
@app.route("/logout/")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

@app.route("/createpost/")
def createpost():
    #   if "user" in session:
    return render_template("login copy.html", description=description, userid=userid, title=title)
    #else:
    #    return redirect(("/login/"))

if __name__ == "__main__":
    app.run(debug=True)

@app.route("/createpost/", methods=["POST", "GET"])
def createpost():
    #if "user" in session:
    return render_template("create-post.html", usr="userid")

response = [
        {
            "description": "hij",
            "id": "5cc47b38-f651-4f21-91fd-0466349de941",
            "image": "def",
            "timestamp": "10000000.0",
            "title": "abc",
            "userId": "6c5c1db5-23d0-4524-b045-aefd622307aa"
        },
        {
            "description": "hij",
            "id": "a43d4030-12ec-4024-bd95-1a3e53e8debe",
            "image": "def",
            "timestamp": "1695111195.372656",
            "title": "abc",
            "userId": "6c5c1db5-23d0-4524-b045-aefd622307ab"
        }
    ]
