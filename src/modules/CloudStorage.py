import os
from google.cloud import storage
from flask import Flask

app = Flask(__name__)

if app.config['ENV'] == 'production':
  app.config.from_pyfile('../configs/prod.cfg')
elif app.config['ENV'] == 'development':
  app.config.from_pyfile('../configs/dev.cfg')
else:
  print('Invalid ENV')

class CloudStorage:

  def __init__(self, backet_name):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.dirname(__file__) + '/../../' + app.config['FIREBASE_CRED_FILE']

    client = storage.Client()
    self.bucket = client.get_bucket(backet_name)

  def upload(self, file_name, path):
    blob = self.bucket.blob(file_name)
    blob.upload_from_filename(filename=path)

  def upload_base64(self, file_name, base64):
    self.upload(file_name, 'data:image/png;base64,'+base64)

  def list_file(self):
    return self.bucket.list_blobs()
