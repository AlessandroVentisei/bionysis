# requires firebase_admin
import firebase_admin
from firebase_admin import db
import subprocess
import os


cred_obj = firebase_admin.credentials.Certificate('API/bionysis-224da-firebase-adminsdk-xsieg-24ec522e83.json')
default_app = firebase_admin.initialize_app(cred_obj, {
    'databaseURL': "https://bionysis-224da-default-rtdb.europe-west1.firebasedatabase.app/"
})

# Hand in coordinates to the Rscript run here
res = subprocess.run(["Rscript", "API/EALiDAR.r", "420000", "592000"])

print(res)