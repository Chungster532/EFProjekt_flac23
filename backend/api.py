import uuid, datetime

from flask import Flask, redirect, url_for, render_template, session, Response
from flask import Blueprint, request, Request
import hashlib, jwt
from database import DB, post, user

secret = 'abcdefg'

db = DB()

app = Blueprint('api', __name__, url_prefix='/api')

def authRequired(request:Request):
    print(request.headers)
    if not 'Authentication' in request.headers and not 'Session-Cookie' in request.cookies:
        raise Exception('No Auth Token')
    token1 = request.headers['Authentication'].split(' ')[1]
    token2 = request.cookies['Session-Cookie']
    if not token1 == token2:
        raise Exception('Auth tokens dont match')
    payload = jwt.decode(token1, secret, algorithms=["HS256"])
    if not payload:
        raise Exception('invalide token')
    if db.get_user_by_id(payload['id']) is None:
        raise Exception('invalide id')
    return True

def generateAuthTokenResponse(id:str) -> Response:
    token = jwt.encode({'id': id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, secret)
    resp = redirect('/api/')
    resp.set_cookie('Session-Cookie', token)
    resp.headers['Authorization'] = 'Bearer ' + token
    return resp

@app.route('/login', methods=["POST"])
def login():
    usr = request.get_json()
    userDB = db.get_user_by_name(usr['username'])
    passwordHash = hashlib.sha512(usr['password'].encode()).hexdigest()
    if not passwordHash == userDB['passwordHash']:
        return {418: "I'm a teadpod"}
    return generateAuthTokenResponse(userDB['id'])

@app.route('/register', methods=["POST"])
def register():
    usr = request.get_json()
    passwordHash = hashlib.sha512(usr['password'].encode()).hexdigest()
    dbUser = db.add_user(str(uuid.uuid4()), usr['username'], passwordHash, usr['description'], usr['image'])
    return generateAuthTokenResponse(dbUser['id'])

@app.route('/')
def main():
    authRequired(request)
    return {'abc':'def'}

@app.route('/get_post/<postID>/', methods=["GET"])
def get_post(postID:str):
    print(f'requesting post with id: {postID}')
    return {'post': db.get_post_by_id(postID)}

@app.route("/post", methods=["POST"])
def make_post(userId:str, title:str, image:str, description:str):
    newPost = db.add_post(str(uuid.uuid4()), userId, title, image, description, str(datetime.datetime.now().timestamp()))
    print(f'creating post with id: {newPost.id}')
    if newPost is None:
        raise Exception('Post creation has failed')
    return {'post': newPost}

@app.route("/search", methods=['POST'])
def search():
    return {'results':{'posts':db.searchPosts(request.get_json()['q'])}}

@app.route("/feed/", methods=['GET'])
def feed(offset:int=0, numPosts:int=10):
    return {'results' : db.get_all_posts(numPosts, offset)}

def getUserByID(id: str):
    return db.get_user_by_id(id)

def getFeed(offset:int=0, numPosts:int=10):
    return db.get_all_posts(numPosts, offset)

def getPostsOfUser(userId:str):
    return db.get_all_user_posts(userId)

if __name__ == "__main__":
    ap = Flask(__name__)
    ap.register_blueprint(app)
    ap.run(debug=True, port='8080')