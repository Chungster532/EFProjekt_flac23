import uuid

from fastapi import FastAPI
import uvicorn

app = FastAPI(title='FastApi')

@app.get("/")
def main():
    return "This is the flag API"

@app.get('get_post/{postID}/')
def get_post(postID:str):
    print('requesting post with id: {postID}')

@app.post("/post/")
def post(userToken:str, title:str, image:str, description:str):
    postID = str(uuid.uuid4())
    print(f'creating post with id: {postID}')

    return {'postID': postID}

@app.get("/search")
def search(q:str):

    return {'results':['postID']}

@app.get("/feed/")
def feed():
    return {'results':['postID']}

uvicorn.run(app, port=8080)