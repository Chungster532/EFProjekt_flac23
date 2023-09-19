from flask import Flask, redirect, url_for, render_template, request, session
from datetime import timedelta

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

def generate_html(response):
    html_content = "<html><head><title>Post List</title></head><body>"
    
    for post in response:
        html_content += f"<div style='border: 1px solid #ccc; padding: 10px; margin-bottom: 10px;'>"
        html_content += f"<img src='{post['image']}' alt='Post Image' style='max-width: 60%;'><br>"
        html_content += f"<h2>{post['title']}</h2>"
        html_content += f"<p>{post['description']}</p>"
        html_content += f"<p>User ID: {post['userId']}</p>"
        html_content += f"</div>"
    
    html_content += "</body></html>"
    
    with open('frontend/templates/postTemplate.html', 'w') as html_file:
        html_file.write(html_content)

generate_html(response)

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
    #print([render_template('postTemplate.html', **r) for r in response])
    #html = '\n'.join([render_template('postTemplate.html', **r) for r in response])
    #with open(r'.\templates\out.html', 'w') as f:
    #    f.write(html)
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
        return render_template("login copy.html")
    else:
        return redirect(("/login/"))

@app.route("/account/")
def account():
    return render_template("account.html")

if __name__ == "__main__":
    app.run()
                                     