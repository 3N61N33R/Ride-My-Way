# import psycopg2
# from flask import current_app
# from flask_testing import TestCase
# from app import app
# from app.v2.models import User, Ride

# class BaseTest(TestCase):

#     def create_app(self):
#         app.test_client()
#         app.config['testing'] = True
        

#         ctx = app.app_context()
#         ctx.push()

#         return app

#     def tearDown(self):
#         conn=psycopg2.connect(f"dbname='{current_app.config['DBNAME']}' user='{current_app.config['DBUSER']}' password='{current_app.config['DBPASSWORD']}'")
#         cur = conn.cursor()
#         cur.execute('''DROP TABLE users CASCADE''')
#         cur.execute('''DROP TABLE rides CASCADE''')
        
        
            

#     def setUp(self):

        # ride = Ride()
        # ride.create ("7","Fedha","Greenfiels"," 10:00a.m")

        # user = User()
        # user.create("May","May","mary5@gmail.com","yolovibes")

        # pass




    
        
