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

  def get_colors_by_base64(self, base64):
    """
    save all image's colors in DB.
    """
    image = ImageModule(img_base64=base64)

    img_colors = image.get_img_colors()

    return img_colors

  def get_layout_info_from_base64(self, base64):
    """
    save all image's colors in DB.
    """
    image = ImageModule(img_base64=base64)

    info = image.get_layout_info()

    return {'resize_img': info['resize_img'], 'base64str': info['base64str']}
    # implement code to save colors to DB
