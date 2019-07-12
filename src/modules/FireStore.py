from flask import Flask
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

app = Flask(__name__)

if app.config['ENV'] == 'production':
  app.config.from_pyfile('../configs/prod.cfg')
elif app.config['ENV'] == 'development':
  app.config.from_pyfile('../configs/dev.cfg')
else:
  print('Invalid ENV')

class FireStore:
  def __init__(self):
    return None
  
  def connect(self):
    cred_path = os.path.dirname(__file__) + '/../../' + app.config['FIREBASE_CRED_FILE']

    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

    db = firestore.client()
    return db
