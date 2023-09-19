from flask import Flask, redirect, url_for, render_template, request, session
from datetime import timedelta
from api import *

with open('frontend/mountain.txt', 'r') as f:
    img = f.read()

response = [
        {
            "description": "it ain't much but its honest work",
            "id": "5cc47b38-f651-4f21-91fd-0466349de941",
            "image": img,
            "timestamp": "10000000.0",
            "title": "1. Post hurraaa",
            "userId": "6c5c1db5-23d0-4524-b045-aefd622307aa"
        },
        {
            "description": "hij",
            "id": "a43d4030-12ec-4024-bd95-1a3e53e8debe",
            "image": img,
            "timestamp": "1695111195.372656",
            "title": "abc",
            "userId": "6c5c1db5-23d0-4524-b045-aefd622307ab"
        }
    ]

print

def generate_feed(response):
    html_content = "<html><head><title>Post List</title></head><body>"
    
    for post in (response):
        html_content += "<div style='border: 1px solid #ccc; padding: 10px; margin-bottom: 10px;'>"
        html_content += f"<div style='max-width: 400px; margin: 0 auto;'>"
        html_content += f"<img src='{post['image']}' alt='Post Image' style='max-width: 100%;'><br>"
        html_content += f"<h2>{post['title']}</h2>"
        html_content += f"<p>{post['description']}</p>"
        html_content += f"<p>User ID: {post['userId']}</p>"
        html_content += "</div>"
        html_content += "</div>"
    
    html_content += "</body></html>"
    
    with open('frontend/templates/tempfeed.html', 'w') as html_file:
        html_file.write(html_content)

def generate_profile(response):
    html_content = "<html><head><title>Post List</title></head><body>"
    
    for post in response:
        html_content += f'''<div class="abc">
<div style='max-width: 400px; margin: 0 auto;'>
<img src='{post['image']}' alt='Post Image' style='max-width: 100%;'><br>
<h2 class="text">{post['title']}</h2>
<p class="text">{post['description']}</p>
</div>
</div>'''
    
    html_content += "</body></html>"
    
    with open('frontend/templates/profiles.html', 'w') as html_file:
        html_file.write(html_content)

#print(html)


app = Flask(__name__)
app.secret_key = "dYVXfvWUUywT86uvSFzwdM19Nk3RNK"
app.permanent_session_lifetime = timedelta(minutes=5)

@app.route("/")
def home():
    generate_feed((getFeed(0, 10))) 

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
    
@app.route("/logout/")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

@app.route("/createpost/")
def createpost():
    if "user" in session:
        imagefile = flask.request.files.get('imagefile', '')
        return render_template("createpost.html")
    else:
        return redirect(("/login/"))

@app.route("/account/")
def account():
    generate_profile(getPostsOfUser("90c0d8c2-c1d6-47b1-80d6-091d620601ad"))    
    return render_template("account.html")

if __name__ == "__main__":
    app.register_blueprint(api)
    app.run()
                                     