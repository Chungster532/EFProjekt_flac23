from flask import Flask, redirect, url_for, render_template, request
from backend.api import *
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "dYVXfvWUUywT86uvSFzwdM19Nk3RNK"
app.permanent_session_lifetime = timedelta(minutes=5)

@app.route("/")
def home():
    try:
        authRequired(request)
        logged = True
    except:
        logged = False
    return render_template("feed.html", posting=False, posts=addCommentsToPost(addUsersToPosts(getFeed())), loggedin=logged)

@app.route("/login/", methods=["POST", "GET"])
def login():
    return render_template("loginTemplate.html", loggedin=False)
    
@app.route("/logout/")
def logout():
    resp = redirect(url_for("login"))
    resp.set_cookie('Session-Cookie=""')
    return resp
    
@app.route("/account/")
def account():
    try:
        usrID = authRequired(request)
    except:
        return redirect('/login/')
    return render_template("account.html", posting=False, users=[getUserByID(usrID)], posts=getPostsOfUser(usrID), loggedin=True)

@app.route('/account/<userID>/')
def usrAccount(userID):
    try:
        usrID = authRequired(request)
        if userID == usrID:
            return redirect('/account/')
    except:
        pass
    return render_template("account.html", posting=False, users=[getUserByID(userID)], posts=getPostsOfUser(userID), loggedin=True)

@app.route('/comment/<postID>/')
def postcomment(postID):
    try:
        usrID = authRequired(request)
    except:
        return redirect('/login/')
    return render_template("postcomment.html", posting=True, users=[usrID], posts=[get_post(postID)], loggedin=True)

@app.route("/registration/")
def registration():
    return render_template("register.html", loggedin=False)

@app.route("/createpost/")
def createPost():
    try:
        usrID = authRequired(request)
    except:
        return redirect('/login/')
    return render_template("createpost.html", loggedin=True)

@app.route("/resetpw/")
def resetpw():
    try:
        usrID = authRequired(request)
    except:
        return redirect('/login/')
    return render_template("resetpw.html", loggedin=True)

if __name__ == "__main__":
    app.register_blueprint(api)
    app.run(port=5000, host='0.0.0.0')    