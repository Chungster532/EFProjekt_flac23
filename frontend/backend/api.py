import uuid, datetime

from flask import Flask, redirect, url_for, render_template, session, Response
from flask import Blueprint, request, Request
import hashlib, jwt
from backend.database import DB
import base64

secret = 'abcdefg'

db = DB()

api = Blueprint('api', __name__, url_prefix='/api')

def sanitize(string:str) -> str:
    return string.replace('ö', 'oe').replace('ü', 'ue').replace('ä', 'ae').replace('à', 'a').replace('è', 'e').replace('é', 'e')

def authRequired(request:Request) -> str:
    print(request.headers)
    if 'Authentication' in request.headers:
        token = request.headers['Authentication'].split(' ')[1]
    elif 'Session-Cookie' in request.cookies:
        token = request.cookies['Session-Cookie']
    else:
        raise Exception('No Auth Token')
    payload = jwt.decode(token, secret, algorithms=["HS256"])
    if not payload:
        raise Exception('invalide token')
    if db.get_user_by_id(payload['id']) is None:
        raise Exception('invalide id')
    return payload['id']

def generateAuthTokenResponse(id:str) -> Response:
    token = jwt.encode({'id': id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)}, secret)
    resp = redirect('/')
    resp.set_cookie('Session-Cookie', token)
    resp.headers['Authorization'] = 'Bearer ' + token
    return resp

@api.route('/login', methods=["POST"])
def login():
    usr = request.form
    if usr['username'] == '':
        return render_template('loginTemplate.html', error='Username can not be emtpy', loggedin=False)
    if usr['password'] == '':
        return render_template('loginTemplate.html', error='Password can not be emtpy', loggedin=False)
    userDB = db.get_user_by_name(usr['username'])
    passwordHash = hashlib.sha512(usr['password'].encode()).hexdigest()
    if userDB is None:
        return render_template('loginTemplate.html', error='Username does not exist', loggedin=False)
    if not passwordHash == userDB['passwordHash']:
        return render_template('loginTemplate.html', error='Password is wrong', loggedin=False)
    return generateAuthTokenResponse(userDB['id'])

@api.route('/register', methods=["POST"])
def register():
    usr = request.form
    print(request.files)
    imagefile = request.files['image']
    print('usr')
    if not imagefile:
        raise Exception('')
    print(usr)
    image_data = imagefile.read()
    encoded_image = base64.b64encode(image_data).decode('utf-8')
    passwordHash = hashlib.sha512(usr['password'].encode()).hexdigest()
    dbUser = db.add_user(str(uuid.uuid4()), sanitize(usr['username']), passwordHash, sanitize(usr['description']), encoded_image)
    return generateAuthTokenResponse(dbUser['id'])

@api.route('/')
def main():
    try:
        authRequired(request)
    except:
        return redirect('/login/')
    return 'This is the flac API'

@api.route('/get_post/<postID>/', methods=["GET"])
def get_post(postID:str):
    print(f'requesting post with id: {postID}')
    return db.get_post_by_id(postID)

@api.route("/post", methods=["POST"])
def make_post():
    try:
        userToken = authRequired(request)
    except:
        return redirect('/login/')
    imagefile = request.files['image']
    if imagefile is None:
        return render_template('loginTemplate.html', error='Wähle ein Bild aus', loggedin=False)
    else:
        image_data = imagefile.read()
        encoded_image = base64.b64encode(image_data).decode('utf-8')
        newPost = db.add_post(str(uuid.uuid4()), userToken, sanitize(request.form['title']), f'data:image/png;base64,{encoded_image}', sanitize(request.form['description']), str(datetime.datetime.now().timestamp()))    
        print(f'creating post with id: {newPost["id"]}')
        if newPost is None:
            raise Exception('Post creation has failed')
        return redirect('/')

@api.route("/search", methods=['POST'])
def search():
    try:
        authRequired(request)
        logged = True
    except:
        logged = False
    return render_template('search.html', users=db.searchUser(request.form['q']), posts=db.searchPosts(request.form['q']), loggedin=logged)


@api.route("/feed/", methods=['GET'])
def feed(offset:int=0, numPosts:int=10):
    return {'results' : db.get_all_posts(numPosts, offset)[::-1]}

@api.route("/changepassword/", methods=["POST"])
def changePasswordEndpoint():
    try:
        userToken = authRequired(request)
    except:
        return redirect('/login/')
    usr = request.form
    if usr['username'] == '':
        return render_template("resetpw.html", loggedin=True, error='Benutzername kann nicht leer sein')
    if usr['password'] == '':
        return render_template("resetpw.html", loggedin=True, error='Password kann nicht leer sein')
    if usr['password'] == '':
        return render_template("resetpw.html", loggedin=True, error='Neues Password kann nicht leer sein')
    userDB = db.get_user_by_id(userToken)
    passwordHash = hashlib.sha512(usr['password'].encode()).hexdigest()
    if not passwordHash == userDB['passwordHash']:
        return render_template("resetpw.html", loggedin=True, error='Falsches Passwort')
    print("text")
    changePassword(userToken, hashlib.sha512(usr['newpassword'].encode()).hexdigest())
    return redirect('/account/')

@api.route('/changeattributes/', methods=["POST"])
def changeAccountAttributes():
    try:
        userToken = authRequired(request)
    except:
        return redirect('/login/')
    encoded_image = getUserByID(userToken)['image']
    description = request.form.get('description')
    if description == '':
        description = getUserByID(userToken)['description']
    if 'imagefile' in request.files:
        imagefile = request.files['imagefile']
        if imagefile:
            image_data = imagefile.read()
            encoded_image = base64.b64encode(image_data).decode('utf-8')
    changeAccountAttributes(userToken, sanitize(description), encoded_image)
    return redirect('/account/')

@api.route('/<postID>/comment/', methods=['POST'])
def comment(postID):
    try:
        userToken = authRequired(request)
    except:
        return redirect('/login/')
    print(request.form)
    db.add_comment(str(uuid.uuid4()), postID, userToken, request.form['text'], datetime.datetime.now().timestamp())
    return redirect(f'/comment/{postID}/')

def getUserByID(id: str):
    return db.get_user_by_id(id)

def getFeed(offset:int=0, numPosts:int=10):
    return db.get_all_posts(numPosts, offset)[::-1]

def addUsersToPosts(posts:list[dict[str, str]]) -> list[dict[str, str]]:
    for post in posts:
        post.update({'user':db.get_user_by_id(post['userId'])})
    return posts


def addUsersToComments(comments:list[dict[str, str]]) -> list[dict[str, str]]:
    for comment in comments:
        comment.update({'user':db.get_user_by_id(comment['userID'])})
    return comments

def addCommentsToPost(posts:list[dict[str, str]]) -> list[dict[str, str]]:
    comments = [addUsersToComments(getCommentsFromPost(p['id'])) for p in posts]
    for comment, post in zip(comments, posts):
        post.update({'comment':comment})
    return posts

def getUsersFromPosts(posts:list[dict[str, str]]) -> list[dict[str, str]]:
    users = []
    for post in posts:
        users.append(db.get_user_by_id(post['userId']))
    return users

def getPostsOfUser(userId:str):
    return db.get_all_user_posts(userId)
def getCommentsFromPost(id:str):
    return db.get_comments_from_post(id)
  
def deleteUser(id:str):
    db.removeUser(id)

def _changeUser(id, username, passwordHash, description, image):
    db.changeUser(id)

def changePassword(id:str, passwordHash:str) -> dict[str, str]:
    usr = db.get_user_by_id(id)
    print(usr['passwordHash'])
    usr['passwordHash'] = passwordHash

    print(usr['passwordHash'])
    return db.changeUser(**usr)

def changeAccountAttributes(id:str, description:str, image:str):
    usr = db.get_user_by_id(id)
    usr['description'] = sanitize(description)
    usr['image'] = sanitize(image)
    db.changeUser(**usr)
