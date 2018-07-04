import psycopg2
from flask import current_app
from werkzeug.security import generate_password_hash, \
     check_password_hash

users = []
rides = []
requests = []

class DB:
    def __init__(self, app=None):
        self.conn=psycopg2.connect(f"dbname='{current_app.config['DBNAME']}' user='{current_app.config['DBUSER']}' password='{current_app.config['DBPASSWORD']}'")
        self.cur = self.conn.cursor()

    def commit(self):
        self.conn.commit()

    def get(self):
        return self.cur.fetchone()

    def all(self):
        return self.cur.fetchall()

    def close(self):
        self.cur.close()
        self.conn.close()

class User(DB):
    def __init__(self, name=None, username=None,email=None,password=None):
        super().__init__()
        self.name = name
        self.username = username
        self.email = email
        self.password = generate_password_hash(password) if password else None

    def check_password(self, password):
        # TODO password hashing
        return check_password_hash(self.password, password)

    def create(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS users(
            id SERIAL PRIMARY KEY NOT NULL,
            name VARCHAR(50) NOT NULL,
            username VARCHAR(50) NOT NULL UNIQUE,
            email VARCHAR(50) NOT NULL UNIQUE,
            password VARCHAR(100) NOT NULL
        );
        """)
        self.commit()

    def add(self):
        self.cur.execute("INSERT INTO users (name, username, email, password) VALUES (%s, %s, %s, %s)", (self.name, self.username, self.email, self.password))
        self.commit()

    def get_by_id(self, id):
        self.cur.execute("select * from users where id=%s", (id,))
        self.commit()
        user = self.get()
        return self.make_user(user)

    def get_by_username(self, username):
        self.cur.execute("select * from users where username=%s", (username,))
        self.commit()
        user = self.get()
        if not user:
            return None
        return self.make_user(user)

    def make_user(self, user):
        self.id = user[0]
        self.name = user[1]
        self.username = user[2]
        self.email = user[3]
        self.password = user[4]

        return self

    def serialize(self):
        return {
            "name": self.name,
            "username": self.username,
            "email": self.email
        }
