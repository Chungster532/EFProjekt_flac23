import sqlite3

class DB:
    def __init__(self) -> None:
        self.db = sqlite3.connect("some.db", check_same_thread=False)
        self.cur = self.db.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS users (
                    token TEXT PRIMARY KEY UNIQUE,
                    username TEXT NOT NULL UNIQUE,
                    passwordHash TEXT NOT NULL
                );''')
        
        self.cur.execute('''CREATE TABLE IF NOT EXISTS posts (
                    postId TEXT PRIMARY KEY UNIQUE,
                    userId TEXT NOT NULL UNIQUE,
                    title TEXT NOT NULL,
                    img TEXT NOT NULL,
                    content TEXT NOT NULL,
                    creationDate TEXT NOT NULL,
                );''')
        
        
db = DB()