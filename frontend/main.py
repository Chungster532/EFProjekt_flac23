from flask import Flask, redirect, url_for, render_template, request
from backend.api import *
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "dYVXfvWUUywT86uvSFzwdM19Nk3RNK"
app.permanent_session_lifetime = timedelta(minutes=5)

@app.route("/")
def home():
    print([getCommentsFromPost(p['id']) for p in getFeed()])
    return render_template("feed.html", posting=False, posts=addCommentsToPost(addUsersToPosts(getFeed())))

@app.route("/login/", methods=["POST", "GET"])
def login():
    return render_template("loginTemplate.html")
    
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
    return render_template("account.html", posting=False, users=[getUserByID(usrID)], posts=getPostsOfUser(usrID))

@app.route('/account/<userID>/')
def usrAccount(userID):
    try:
        usrID = authRequired(request)
        if userID == usrID:
            return redirect('/account/')
    except:
        pass
    return render_template("external_account.html", posting=False, users=[getUserByID(userID)], posts=getPostsOfUser(userID))

@app.route('/comment/<postID>/')
def postcomment(postID):
    try:
        usrID = authRequired(request)
    except:
        return redirect('/login/')
    return render_template("postcomment.html", posting=True, users=[usrID], posts=[get_post(postID)])

@app.route("/registration/")
def registration():
    return render_template("register.html")

@app.route("/createpost/")
def createPost():
    return render_template("createpost.html")

@app.route("/resetpw/")
def resetpw():
    return render_template("resetpw.html")

@app.route("/editprofile/")
def editprofile():
    try:
        usrID = authRequired(request)
    except:
        return redirect('/login/')
    return render_template("editprofile.html", users=[usrID])

def resetpw():
    return render_template("resetpw.html")


if __name__ == "__main__":
    app.register_blueprint(api)
    app.run(port=5000, host='0.0.0.0')    