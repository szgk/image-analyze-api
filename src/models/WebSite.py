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
  from src.modules import DateTime
  from src.modules import WebSite as WebSiteModule
elif app.config['ENV'] == 'development':
  app.config.from_pyfile('../configs/dev.cfg')
  from ..modules import FireStore
  from ..modules import Image
  from ..modules import String
  from ..modules import CloudStorage
  from ..modules import DateTime
  from ..modules import WebSite as WebSiteModule
  # use chromedriver(ver74)
  import chromedriver_binary
else:
  print('Invalid ENV')

class WebSite:
  def __init__(self):
    self.storage = None
    self.fireStore = FireStore()

  def start_to_get_sceenshot(self, url):
    backet_name = app.config['CLOUD_STORAGE_BUCKET']
    directory = app.config['SCREENSHOT_DIR']
    file_name = String.get_page_name(url)
    file_path = directory + file_name

    imageModule = Image()
    self.storage = CloudStorage(backet_name)

    target_file = self._is_exist_file({'prefix': file_path})

    if target_file:
      if DateTime.is_over_days(target_file.time_created, 60):
        # if exist file and over expire date
        target_file.delete()
      else:
        # if exist file and not over expire date
        return file_name

    webSite = WebSiteModule()
    img_base64 = webSite.get_screenshot_base64(url)

    img = imageModule.base64_to_ndarray(img_base64)
    img_resize = imageModule.resize(img, 0.15)


    with tempfile.TemporaryDirectory() as temp_path:
      path = temp_path + '/screenshot.png'
      cv2.imwrite(path, img_resize)
      self.storage.upload(file_name=file_path, path=path)

    return file_name

  def _is_exist_file(self, list_strage_files_option):
    files_len = 0
    target_file = None

    files = self.storage.list_files(list_strage_files_option)

    for file in files:
      if not target_file:
        target_file = file
      files_len += 1

    return target_file
