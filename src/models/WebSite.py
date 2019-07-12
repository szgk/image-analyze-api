from flask import Flask
from cv2 import cv2
from uuid import uuid4
import datetime, base64, tempfile, numpy as np

app = Flask(__name__)

if app.config['ENV'] == 'production':
  app.config.from_pyfile('../configs/prod.cfg')
  from src.modules import FireStore
  from src.modules import Image
  from src.modules import String
  from src.modules import CloudStorage
  from src.modules import WebSite as WebSiteModule
elif app.config['ENV'] == 'development':
  app.config.from_pyfile('../configs/dev.cfg')
  from ..modules import FireStore
  from ..modules import Image
  from ..modules import CloudStorage
  from ..modules import String
  from ..modules import WebSite as WebSiteModule
  # use chromedriver(ver74)
  import chromedriver_binary
else:
  print('Invalid ENV')

class WebSite:

  def start_to_get_sceenshot(self, url):
    backet_name = app.config['CLOUD_STORAGE_BUCKET']
    directory = app.config['SCREENSHOT_DIR']
    file_name = directory + String.get_page_name(url) + '_' + String.current_time()
    file_path = directory + file_name

    fireStore = FireStore()
    imageModule = Image()
    storage = CloudStorage(backet_name)

    webSite = WebSiteModule()
    img_base64 = webSite.get_screenshot_base64(url)

    img = imageModule.base64_to_ndarray(img_base64)
    img_resize = imageModule.resize(img, 0.15)

    with tempfile.TemporaryDirectory() as temp_path:
      path = temp_path + '/screenshot.png'
      cv2.imwrite(path, img_resize)
      storage.upload(file_name=file_name, path=path)

    return file_name
