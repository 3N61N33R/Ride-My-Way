users = []
rides = []
requests = []

class User:
    def __init__(self, name, username,email,password):
        self.name = name
        self.username = username
        self.email = email
        self.password = password

    def add(self):
        users.append(self)

        for user in users:
            print(self.serialize(user))
    
    def serialize(self, user):
        return {
            "name": self.name,
            "username": self.username,
            "email": self.email,
            "password": self.password
        }

class Ride:
    ride_id = 1
    def __init__(self, name=None, pickup=None, dropoff=None,time=None):
        self.name = name
        self.pickup = pickup
        self.dropoff = dropoff
        self.time = time
        self.id = Ride.ride_id

        Ride.ride_id +=1

    def add(self):
        rides.append(self)

        for ride in rides:
            print(ride.serialize())

    def get_all(self):
        _rides = []
        for ride in rides:
            _rides.append(ride.serialize())
        return _rides

    def get_one(self, id):
        for ride in rides:
            if ride.id == id: 
                return ride
        return None

    def serialize(self):
        return {
            "name": self.name,
            "pickup": self.pickup,
            "dropoff": self.dropoff,
            "time": self.time,
            "id":self.id

        }

    def delete(self, ride_id):
        ride = self.get_one(ride_id)
        if ride:
            rides.remove(ride)
            return True 
        return False

class Request:
    request_id = 1
    def __init__(self, name=None, ride =None):
        self.name = name
        self.ride = ride
        self.id = Request.request_id

        Request.request_id

    def add(self):
        requests.append(self)

    
    def get_all_requests(self, id ):
        _requests = []
        for request in requests:
            if request.ride.id == id:
                 _requests.append(request.serialize())
        return _requests

    
    def serialize(self):
        return {
            "name": self.name,
            'ride': self.ride.serialize(),
            "id" :self.id

        }

    def get_one_request(self, ride_id, request_id):
        for request in requests:
            if request.id == request_id and request.ride.id == ride_id: 
                return request
        return None

    

        

        
    

    


                
                
    

        

 


