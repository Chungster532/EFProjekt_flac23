from flask import Flask, redirect, url_for, render_template, request
from sys import path
path.append('../')
from backend.api import *

with open('frontend/mountain.txt', 'r') as f:
    img = f.read()

def generate_html(response):
    html_content = "<html><head><title>Post List</title></head><body>"
    
    for post in response:
        html_content += "<div style='border: 1px solid #ccc; padding: 10px; margin-bottom: 10px;'>"
        html_content += f"<div style='max-width: 400px; margin: 0 auto;'>"
        html_content += f"<img src='{post['image']}' alt='Post Image' style='max-width: 100%;'><br>"
        html_content += f"<h2>{post['title']}</h2>"
        html_content += f"<p>{post['description']}</p>"
        html_content += f"<p>User ID: {post['userId']}</p>"
        html_content += "</div>"
        html_content += "</div>"
    
    html_content += "</body></html>"
    
    with open('frontend/templates/postTemplate.html', 'w') as html_file:
        html_file.write(html_content)
#print(html)


app = Flask(__name__)
app.secret_key = "dYVXfvWUUywT86uvSFzwdM19Nk3RNK"

@app.route("/")
def home():
    generate_html(getFeed()) 
    return render_template("index.html")

@app.route("/login/", methods=["GET"])
def login():
    return render_template("login.html")
    
@app.route("/logout/")
def logout():
    return redirect(url_for("login"))

@app.route("/createpost/")
def createpost():
    return render_template("createpost.html")

@app.route("/account/")
def account():
    return render_template("account.html")

if __name__ == "__main__":
    app.register_blueprint(api)
    app.run()
                                     