import uuid, datetime

from flask import Flask, redirect, url_for, render_template, session, Response
from flask import Blueprint, request, Request
import hashlib, jwt
from database import DB
import base64

secret = 'abcdefg'

db = DB()

api = Blueprint('api', __name__, url_prefix='/api')

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
    token = jwt.encode({'id': id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, secret)
    resp = redirect('/')
    resp.set_cookie('Session-Cookie', token)
    resp.headers['Authorization'] = 'Bearer ' + token
    return resp

@api.route('/login', methods=["POST"])
def login():
    usr = request.form
    userDB = db.get_user_by_name(usr['username'])
    passwordHash = hashlib.sha512(usr['password'].encode()).hexdigest()
    if not passwordHash == userDB['passwordHash']:
        return {418: "I'm a teadpod"}
    return generateAuthTokenResponse(userDB['id'])

@api.route('/register', methods=["POST"])
def register():
    usr = request.form
    imagefile = request.files['image']
    if not imagefile:
        raise Exception('')
    image_data = imagefile.read()
    encoded_image = base64.b64encode(image_data).decode('utf-8')
    passwordHash = hashlib.sha512(usr['password'].encode()).hexdigest()
    dbUser = db.add_user(str(uuid.uuid4()), usr['username'], passwordHash, usr['description'], encoded_image)
    return generateAuthTokenResponse(dbUser['id'])

@api.route('/')
def main():
    authRequired(request)
    return 'This is the flac API'

@api.route('/get_post/<postID>/', methods=["GET"])
def get_post(postID:str):
    print(f'requesting post with id: {postID}')
    return {'post': db.get_post_by_id(postID)}

@api.route("/post", methods=["POST"])
def make_post():
    usrID = authRequired(request)
    imagefile = request.files['imagefile']
    if not imagefile:
        raise Exception('')
    image_data = imagefile.read()
    encoded_image = base64.b64encode(image_data).decode('utf-8')
    newPost = db.add_post(str(uuid.uuid4()), usrID, request.form['title'], f'data:image/png;base64,{encoded_image}', request.form['description'], str(datetime.datetime.now().timestamp()))    
    print(f'creating post with id: {newPost["id"]}')
    if newPost is None:
        raise Exception('Post creation has failed')
    return {'post': newPost}

@api.route("/search", methods=['POST'])
def search():
    return {'results':{'posts':db.searchPosts(request.get_json()['q'])}}

@api.route("/feed/", methods=['GET'])
def feed(offset:int=0, numPosts:int=10):
    return {'results' : db.get_all_posts(numPosts, offset)[::-1]}

def getUserByID(id: str):
    return db.get_user_by_id(id)

def getFeed(offset:int=0, numPosts:int=10):
    return db.get_all_posts(numPosts, offset)[::-1]

def getPostsOfUser(userId:str):
    return db.get_all_user_posts(userId)

def getCommentsFromPost(id:str):
    return db.get_comments_from_post(id)