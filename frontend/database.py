import sqlite3, datetime

def userToDict(id, username, passwordHash, description, image, **args):
    return {'id':id, 'username':username, 'passwordHash': passwordHash, 'description':description, 'image':image}

def postToDict(id, userId, title, image, description, timestamp):
    return {'id': id, 'userId': userId, 'title': title, 'image':image, 'description':description, 'timestamp':str(datetime.datetime.fromtimestamp(float(timestamp)))}

class DB:
    def __init__(self) -> None:
        self.db = sqlite3.connect("some.db", check_same_thread=False)
        self.cur = self.db.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS users ( id TEXT PRIMARY KEY NOT NULL UNIQUE, username TEXT NOT NULL UNIQUE, passwordhash TEXT NOT NULL, description TEXT NOT NULL, image TEXT NOT NULL );''')
        
        self.cur.execute('''CREATE TABLE IF NOT EXISTS posts ( id TEXT PRIMARY KEY NOT NULL UNIQUE, userId TEXT NOT NULL, title TEXT NOT NULL, image TEXT NOT NULL, description TEXT NOT NULL, creationDate TEXT NOT NULL );''')
    def add_post(self, *args) -> dict[str, str]:
        """Function to add post to the db"""
        #try:
        self.cur.execute("INSERT INTO posts VALUES(?,?,?,?,?,?)", args)
        print('\n'.join(list(self.db.iterdump())))
        self.db.commit()
        return self.get_post_by_id(args[0])
    def add_user(self, *args) -> dict[str, str]:
        """Function to add user to the db"""
        self.cur.execute("INSERT INTO users VALUES(?,?,?,?,?)", args)
        print('\n'.join(list(self.db.iterdump())))
        self.db.commit()
        return self.get_user_by_name(args[1])
    def get_post_by_id(self, id:str) -> dict[str, str]:
        """return a list containing all attributes of a post specified b an uuid"""
        print(f'fetching id {id}')
        pst =  self.cur.execute("""SELECT * FROM posts WHERE id=?""", (id,)).fetchone()
        return postToDict(*pst) if pst else None
    
    def get_user_by_name(self, name:str) -> dict[str, str]:
        """return a list containing all attributes of a post specified b an uuid"""
        print(f'fetching id {name}')
        pst =  self.cur.execute("""SELECT * FROM users WHERE username=?""", (name,)).fetchone()
        return userToDict(*pst) if pst else None
    def get_user_by_id(self, id:str) -> dict[str, str]:
        """return a list containing all attributes of a post specified b an uuid"""
        print(f'fetching id {id}')
        pst =  self.cur.execute("""SELECT * FROM users WHERE id=?""", (id,)).fetchone()
        return userToDict(*pst) if pst else None

    def get_all_posts(self, count:int, offset:int) -> list[dict[str, str]]:
        """function which return all posts"""
        return [postToDict(*pst) if pst else None for pst in self.cur.execute("""SELECT * FROM posts LIMIT ? OFFSET ?""", (str(count), str(offset),)).fetchall()]
    
    def get_all_user_posts(self, id:str) -> list[dict[str, str]]:
        """function which return all posts"""
        return [postToDict(*pst) if pst else None for pst in self.cur.execute("""SELECT * FROM posts WHERE userID=?""", (str(id),)).fetchall()]
    
    def searchUser(self, name:str) -> list[dict[str, str]]:
        """Function to search for a user by name"""
        [userToDict(usr) if usr else None for usr in self.cur.execute("""SELECT * FROM posts WHERE username LIKE ?""", ('%'+name+'%',)).fetchall()]
        return 
    
    def searchPosts(self, name:str) -> list[dict[str, str]]:
        """Function to search posts by prompt"""
        return [postToDict(*pst) if pst else None for pst in self.cur.execute("""SELECT * FROM posts WHERE title LIKE ? OR description LIKE ?""", ('%'+name+'%', '%'+name+'%')).fetchall()]