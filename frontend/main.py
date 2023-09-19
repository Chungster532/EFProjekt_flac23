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
            session.permanent = True  # <--- makes the permanent session
            user = request.form["userid"]
            session["user"] = user
            return redirect("/")
    else:
        if "user" in session:
            return redirect("/")
        return render_template("login.html")

@app.route("/createpost/")
def createpost():
    #   if "user" in session:
    return render_template("createpost.html", usr="userid")
    #else:
    #    return redirect(("/login/"))

if __name__ == "__main__":
    app.run(debug=True)


                                     