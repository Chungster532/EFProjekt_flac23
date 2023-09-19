import sqlite3, datetime, uuid

class post:
    def __init__(self, id:str, userId:str, title:str, image:str, description:str, creationDate:str) -> None:
        self.id:uuid = uuid.UUID(id)
        self.userId:uuid = uuid.UUID(userId)
        self.title:str = title
        self.image:str = image
        self.description:str = description
        self.creationDate:datetime.datetime = datetime.datetime.fromtimestamp(float(creationDate))
    def __iter__(self) -> iter:
        print(str(self.id), str(self.userId), self.title, self.image, self.description)
        print(str(self.creationDate.timestamp()))
        return iter((str(self.id), str(self.userId), self.title, self.image, self.description, str(self.creationDate.timestamp())))
    def __dict__(self) -> dict:
        print({'id': str(self.id), 'userId': str(self.userId), 'title': self.title, 'image':self.image, 'description':self.description, 'timestamp':str(self.creationDate.timestamp())})
        return {'id': str(self.id), 'userId': str(self.userId), 'title': self.title, 'image':self.image, 'description':self.description, 'timestamp':str(self.creationDate.timestamp())}

class user:
    id:str
    username:str
    description:str
    image:str
    def __init__(self, id:str, username:str, description:str, image:str) -> None:
        self.id = id
        self.username = username
        self.description = description
        self.image = image
    def __iter__(self):
        return iter((self.id, self.username, self.description, self.image))
    def __dict__(self) -> dict:
        return {'id':self.id, 'username':self.username, 'description':self.description, 'image':self.image}

class DB:
    def __init__(self) -> None:
        self.db = sqlite3.connect("some.db", check_same_thread=False)
        self.cur = self.db.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS users ( id TEXT PRIMARY KEY NOT NULL UNIQUE, username TEXT NOT NULL UNIQUE, passwordhash TEXT NOT NULL, description TEXT NOT NULL, image TEXT NOT NULL );''')
        
        self.cur.execute('''CREATE TABLE IF NOT EXISTS posts ( id TEXT PRIMARY KEY NOT NULL UNIQUE, userId TEXT NOT NULL, title TEXT NOT NULL, image TEXT NOT NULL, description TEXT NOT NULL, creationDate TEXT NOT NULL );''')
    def add_post(self, post:post) -> post:
        """Function to add post to the db"""
        #try:
        self.cur.execute("INSERT INTO posts VALUES(?,?,?,?,?,?)", tuple(post))
        print('\n'.join(list(self.db.iterdump())))
        self.db.commit()
        return self.get_post_by_id(post.id)
        #except Exception as e:
        #    print(e)
        #    return None
    def get_post_by_id(self, id:str) -> post:
        """return a list containing all attributes of a post specified b an uuid"""
        print(f'fetching id {id}')
        pst =  self.cur.execute("""SELECT * FROM posts WHERE id=?""", (str(id),)).fetchone()
        print(pst, post(*pst) if pst else None)
        return post(*pst) if pst else None

    def get_all_posts(self, count:int, offset:int) -> list[post]:
        """function which return all posts"""
        return [post(*pst) if pst else None for pst in self.cur.execute("""SELECT * FROM posts LIMIT ? OFFSET ?""", (str(count), str(offset),)).fetchall()]
    
    def searchUser(self, name:str) -> list[user]:
        """Function to search for a user by name"""
        [user(*usr) if usr else None for usr in self.cur.execute("""SELECT * FROM posts WHERE username LIKE ?""", ('%'+name+'%',)).fetchall()]
        return 
    
    def searchPosts(self, name:str) -> list[post]:
        """Function to search posts by prompt"""
        return [post(*pst) if pst else None for pst in self.cur.execute("""SELECT * FROM posts WHERE title LIKE ? OR description LIKE ?""", ('%'+name+'%', '%'+name+'%')).fetchall()]