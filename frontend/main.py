from flask import Flask, redirect, url_for, render_template, request, session
from datetime import timedelta


app = Flask(__name__)
app.secret_key = "dYVXfvWUUywT86uvSFzwdM19Nk3RNK"

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["userid"]
        session["user"] = user
        return redirect(url_for("user"))
    else:
        if "user" in session:
            return redirect(url_for("user"))

        return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)

@app.route("/createpost/", methods=["POST", "GET"])
def createpost():
    #if "user" in session:
    return render_template("create-post.html", usr="userid") 
    else:
        return render_template("login.html")
                                     