# requires firebase_admin
import firebase_admin
from firebase_admin import db

cred_obj = firebase_admin.credentials.Certificate('API/bionysis-224da-firebase-adminsdk-xsieg-24ec522e83.json')
default_app = firebase_admin.initialize_app(cred_obj, {
    'databaseURL': "https://bionysis-224da-default-rtdb.europe-west1.firebasedatabase.app/"
})

ref = db.reference("/")
test_data = {"name":"Alex", "purpose": {"test_data":"here", "more_data": "here as well"}}
ref.set(test_data)

#TODO:
# 1) setup R package for checking and downloading tiles required for coordinates.
# 2) upload labelled data returned from R package to real-time db.
# 3) setup framework for transforming data returned from db in python to useful format.