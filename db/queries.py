
import os
import firebase_admin
from firebase_admin import credentials, db

CURRENT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
CREDENTIALS_PATH = CURRENT_DIRECTORY + '/credentials.json'

cred = credentials.Certificate(CREDENTIALS_PATH)
firebase_admin.initialize_app(cred, {'databaseURL': 'https://ezpark-349308-default-rtdb.europe-west1.firebasedatabase.app/'})

db_garages = db.reference('/Garages')
db_root = db.reference('')


class Garages():
    def get(garage=None):
        if garage == None:
            return list(db_garages.get().items())
        else:
            return list(db_garages.child(garage).get().items())

    def set_current_occupancy(garage, current_occupancy):
        db_garages.child(garage).child('current_occupancy').set(current_occupancy)

    def set_max_occupancy(garage, max_occupancy):
        db_garages.child(garage).child('max_occupancy').set(max_occupancy)


class DemoLocation():
    def get():
        return db_root.child('demo_location').get()

    def set(demo_location):
        db_root.child('demo_location').set(demo_location)

