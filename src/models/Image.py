from flask import Flask
app = Flask(__name__)

import os
if app.config['ENV'] == 'production':
  from src.modules.Image import Image as ImageModule
  from src.modules.Colors import Colors
elif app.config['ENV'] == 'development':
  from ..modules import Image as ImageModule
  from ..modules import Colors
else:
  print('Invalid ENV')

class Image:
  """
  class for image model.
  """
  def __init__(self, img, path):
    self._img = img
    self._currentpath = path
    self._img_path = os.path.join(path, '../../public/img/' + img)
    self._img_filename = img

  def save_all_colors(self):
    """
    save all image's colors in DB.
    """
    image = ImageModule(self._img_path)

    resizePath = os.path.join(self._currentpath, '../../public/img/' + '0.15' + self._img_filename)

    if (not os.path.isfile(resizePath)):
      image.resize(0.15)
      image.save('0.15')
    else:
      image = ImageModule(resizePath)

    img_colors = image.get_img_colors()

    return img_colors
    # implement code to save colors to DB
