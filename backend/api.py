import uuid, datetime

from fastapi import FastAPI
import uvicorn

from database import DB, post, user

db = DB()

app = FastAPI(title='FastApi')

@app.get("/")
def main():
    return "This is the flac API"

@app.get('/get_post/{postID}/')
def get_post(postID:str):
    print('requesting post with id: {postID}')
    return {'post': db.get_post_by_id(uuid.UUID(postID)).__dict__()}

@app.post("/post/")
def make_post(userId:str, title:str, image:str, description:str):
    newPost = db.add_post(post(str(uuid.uuid4()), userId, title, image, description, str(datetime.datetime.now().timestamp())))
    print(f'creating post with id: {newPost.id}')
    if newPost is None:
        raise Exception('Post creation has failed')
    return {'post': newPost.__dict__()}

@app.get("/search")
def search(q:str):
    return {'results':{'posts':[x.__dict__() for x in db.searchPosts(q)]}}

@app.get("/feed/")
def feed(offset:int=0, numPosts:int=10):
    return {'results':[x.__dict__() for x in db.get_all_posts(numPosts, offset)]}

uvicorn.run(app, port=8080)