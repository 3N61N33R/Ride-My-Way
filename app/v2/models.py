import psycopg2
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
import sys


class DB:
    def __init__(self, app=None):
        self.conn = psycopg2.connect(
            database=current_app.config["DBNAME"],
            user=current_app.config["DBUSER"],
            password=current_app.config["DBPASSWORD"],
        )
        self.cur = self.conn.cursor()

    def commit(self):
        self.conn.commit()

    def get(self):
        return self.cur.fetchone()

    def all(self):
        return self.cur.fetchall()

    def drop(self, tablename):
        self.cur.execute("DROP TABLE IF EXISTS {} CASCADE".format(tablename))
        self.commit()

    def close(self):
        self.cur.close()
        self.conn.close()


class User(DB):
    def __init__(self, name=None, username=None, email=None, password=None):
        super().__init__()
        self.name = name
        self.username = username
        self.email = email
        self.password = generate_password_hash(password) if password else None
        self.create()

    def check_password(self, password):
        # TODO password hashing
        return check_password_hash(self.password, password)

    def create(self):
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS users(
            id SERIAL PRIMARY KEY NOT NULL,
            name VARCHAR(50) NOT NULL,
            username VARCHAR(50) NOT NULL UNIQUE,
            email VARCHAR(50) NOT NULL UNIQUE,
            password VARCHAR(100) NOT NULL
        );
        """
        )
        self.commit()

    def add(self):
        self.cur.execute(
            "INSERT INTO users (name, username, email, password) VALUES (%s, %s, %s, %s)",
            (self.name, self.username, self.email, self.password),
        )
        self.commit()

    def get_by_id(self, _id):
        try:
            self.cur.execute("SELECT * FROM users WHERE id=%s", (_id,))
            user = self.get()
            return self.make_user(user)
        except Exception as e:
            raise e

    def get_by_username(self, username):
        self.cur.execute("SELECT * FROM users WHERE username=%s", (username,))
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
        return {"name": self.name, "username": self.username, "email": self.email}


class Ride(DB):
    def __init__(self, driver=None, pickup=None, dropoff=None, time=None):
        super().__init__()
        self.driver = driver
        self.pickup = pickup
        self.dropoff = dropoff
        self.time = time
        self.id = None

    def create(self):
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS rides (
            id SERIAL PRIMARY KEY NOT NULL,
            driver_id INTEGER NOT NULL,
            pickup VARCHAR(50) NOT NULL,
            dropoff VARCHAR(50) NOT NULL,
            time TIMESTAMP NOT NULL,
            FOREIGN KEY (driver_id) REFERENCES users (id) ON DELETE CASCADE
        );
        """
        )
        self.commit()

    def add(self, _id):

        self.cur.execute(
            "INSERT INTO rides (driver_id, pickup, dropoff, time) VALUES (%s, %s, %s, %s)",
            (_id, self.pickup, self.dropoff, self.time),
        )
        self.commit()

    def get_all(self):
        self.cur.execute("SELECT * from rides")
        rides = self.all()

        if not rides:
            return None
        return [self.make_ride(ride) for ride in rides]

    def get_one(self, _id):
        self.cur.execute("SELECT * from rides where id=%s", (_id,))
        ride = self.get()

        return self.make_ride(ride) if ride else None

    def get_by_user(self, user):
        self.cur.execute("SELECT * from rides where driver_id =%s", (user,))
        rides = self.all()

        if not rides:
            return None
        return [self.make_ride(ride) for ride in rides]

    def update(self):
        self.cur.execute(
            "UPDATE rides SET pickup=%s, dropoff=%s, time=%s where id=%s",
            (self.pickup, self.dropoff, self.time, self.id),
        )
        self.commit()

    def make_ride(self, ride):
        self.id = ride[0]
        self.driver = User().get_by_id(ride[1])
        self.pickup = ride[2]
        self.dropoff = ride[3]
        self.time = ride[4]

        return self

    def serialize(self):
        return {
            "driver": self.driver.serialize(),
            "pickup": self.pickup,
            "dropoff": self.dropoff,
            "time": self.time,
            "id": self.id,
        }

    def delete(self, ride_id):
        self.cur.execute("DELETE FROM rides WHERE id=%s;", (ride_id,))
        self.commit()


class Request(DB):
    def __init__(self, user=None, ride=None):
        super().__init__()
        self.user = user
        self.ride = ride
        self.request_status = "pending"

    def create(self):
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS ride_requests(
            id SERIAL PRIMARY KEY NOT NULL, 
            ride_id INT NOT NULL, 
            requestor_id INT NOT NULL, 
            request_status VARCHAR(140) NOT NULL,
            FOREIGN KEY (ride_id) REFERENCES rides (id) ON DELETE CASCADE,
            FOREIGN KEY (requestor_id) REFERENCES users (id) ON DELETE CASCADE
        );
        """
        )

        self.commit()

    def add(self):
        self.cur.execute(
            "INSERT INTO ride_requests (ride_id, requestor_id, request_status) VALUES (%s, %s, %s)",
            (self.ride.id, self.user.id, self.request_status),
        )
        self.commit()

    def get_all_requests(self, _id):
        self.cur.execute(
            "SELECT id, ride_id, requestor_id, request_status FROM ride_requests WHERE ride_id=%s",
            (_id,),
        )
        request_ride = self.all()
        return [self.make_request(request).serialize() for request in request_ride]

    def make_request(self, request_ride):
        self.id = request_ride[0]
        self.ride = Ride().get_one(request_ride[1])
        self.user = User().get_by_id(request_ride[2])
        self.request_status = request_ride[3]

        return self

    def serialize(self):
        return {
            "user": self.user.serialize(),
            "ride": self.ride.serialize(),
            "request_status": self.request_status,
            "id": self.id,
        }

    def get_one_request(self, ride_id, request_id):
        self.cur.execute(
            "SELECT * FROM ride_requests WHERE ride_id=%s and id=%s",
            (str(ride_id), str(request_id)),
        )
        request_ride = self.get()

        return self.make_request(request_ride)
