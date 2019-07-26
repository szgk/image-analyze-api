from flask import Flask

app = Flask(__name__)

if app.config['ENV'] == 'production':
  from src.modules.Image import Image as ImageModule
elif app.config['ENV'] == 'development':
  from ..modules import Image as ImageModule
else:
  print('Invalid ENV')


class Image:
  """
  class for image model.
  """

  def __init__(self, img_path):
    self._img_path = img_path

  def get_desc_color_list(self):
    """
    save all image's colors in DB.
    """
    image = ImageModule(self._img_path)

    img_colors = image.get_img_colors()

    return img_colors
    # implement code to save colors to DB
