from flask import Flask, redirect, url_for, render_template, request
from backend.api import *
from datetime import timedelta

def generate_feed(response):
    html_content = "<html><head><title>Post List</title></head><body>"
    
    for post in (response):
        html_content += f"""<div style='background-color: #06060e; padding: 10px; margin-bottom: 10px; width: 60%; margin-left: auto; margin-right: auto; border-radius: 15px;'>
<div style='max-width: 400px; margin: 0 auto;'>
<img src='{post['image']}' alt='Post Image' style='max-width: 100%;'><br>
<h2>{post['title']}</h2>
<p>{post['description']}</p>
<p>User ID: {post['userId']}</p>
</div>
</div>"""
    
    html_content += "</body></html>"
    
    with open('frontend/templates/tempfeed.html', 'w') as html_file:
        html_file.write(html_content)

def generate_profile(response):
    html_content = "<html><head><title>Post List</title></head><body>"
    
    for post in response:
        html_content += f"""<div style='background-color: #06060e; padding: 10px; margin-bottom: 10px; width: 60%; margin-left: auto; margin-right: auto; border-radius: 15px;'>
<div style='max-width: 400px; margin: 0 auto;'>
<img src='{post['image']}' alt='Post Image' style='max-width: 100%;'><br>
<h2>{post['title']}</h2>
<p>{post['description']}</p>
<p>User ID: {post['userId']}</p>
</div>
</div>"""
    
    html_content += "</body></html>"
    
    with open('frontend/templates/profiles.html', 'w') as html_file:
        html_file.write(html_content)
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
    resp = redirect(url_for("login"))
    resp.set_cookie('Session-Cookie=""')
    return resp

@app.route("/createpost/")
def createpost():
    if "user" in session:
        if request.method == 'POST':
            imagefile = request.files['imagefile']
            if imagefile:
                image_data = imagefile.read()
                encoded_image = base64.b64encode(image_data).decode('utf-8')
                return render_template("createpost.html", encoded_image=encoded_image)
        return render_template("createpost.html")
    else:
        return redirect("/login/")
    
@app.route("/account/")
def account():
    generate_profile(getPostsOfUser("90c0d8c2-c1d6-47b1-80d6-091d620601ad"))    
    return render_template("account.html")

@app.route("/registration/")
def registration():
    return render_template("registration.html")

if __name__ == "__main__":
    app.register_blueprint(api)
    app.run(port=5000, host='0.0.0.0')
                                     
    app.run(port=5000, host='0.0.0.0')
                                     