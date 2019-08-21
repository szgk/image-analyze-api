import base64
import collections
# import os
import tempfile

from cv2 import cv2

import numpy as np


class Image:
  """
  super class of all images class.
  """

  def __init__(self, img_url=None, img_path=None, img_base64=None):
    self.img = []
    if img_path:
      self.img = cv2.imread(img_path)
    if img_url:
      self.img = self._imread_web(img_url)
    if img_base64:
      self.img = self._base64_str_to_ndarray(img_base64)

  def get_img_colors(self, img=[]):
    """
    method to get all pixels colors.
    """
    if len(img) <= 0:
      img = self.img
    if self.img is None or len(img) <= 0:
      return []

    height, width = img.shape[:2]
    all_pixels = height * width
    # line up all values one row.
    vector = img.reshape(-1)
    # recreate pixels
    all_colors = vector.reshape(all_pixels, 3)

    all_colors_list = list(map(self._format_cv2_colors_list, all_colors))

    return self._sort_list_to_desc(all_colors_list)

  def _sort_list_to_desc(self, lists, desc=True):
    counter = collections.Counter(lists)
    d = dict(counter)
    desc_list = sorted(d.items(), reverse=desc, key=lambda x: x[1])
    return desc_list

  def _format_cv2_colors_list(self, unit8_list):
    """
    format color list that get by cv2 from image file.
    BGR -> RGB, change numpy.unit8 -> string
    """
    # swap BGR => RGB
    rgb_list = self._format_BGR_to_RGB(unit8_list)

    # to use counter, change numpy.unit8 to string.
    unicode_arr = rgb_list.astype('unicode')

    return str(','.join(unicode_arr))

  def _format_BGR_to_RGB(self, gbr_list):
    # swap BGR => RGB
    gbr_list[0], gbr_list[2] = gbr_list[2], gbr_list[0]
    return gbr_list

  def base64_to_ndarray(self, img_base64):
    img = base64.b64decode(img_base64)
    img_np = np.fromstring(img, np.uint8)
    return cv2.imdecode(img_np, cv2.IMREAD_ANYCOLOR)

  def _base64_str_to_ndarray(self, base64_str):
    base64_bytes = base64_str.encode()
    img = self.base64_to_ndarray(base64_bytes)

    return img

  def get_layout_info(self):

    gray_img = self._change_to_gray_scale(self.img)
    thresh_img = self._get_2color_img(gray_img)
    rgb_img = self._change_to_rgb(thresh_img)
    resize_img = self._get_resize_with_range(rgb_img)
    base64str = self._get_base64_from_cv2_img(resize_img)

    return {'resize_img': resize_img.tolist(), 'base64str': base64str}

  def _get_2color_img(self, img, thresholod=120):
    # cv2の画像を2値化する
    # ref: https://qiita.com/tokkuri/items/ad5e858cbff8159829e9

    # thresholodを超えた画素を255に
    ret, thresh_img = cv2.threshold(img, thresholod, 255, cv2.THRESH_BINARY)

    return thresh_img

  def _get_base64_from_cv2_img(self, img):
    # cv2の画像からbase64を取得する
    base64str = ''
    with tempfile.TemporaryDirectory() as dirname:
      filepath = dirname + 'temp.png'
      cv2.imwrite(filepath, img)
      base64str = base64.encodestring(
          open(filepath, 'rb').read()).decode('utf-8')

    return base64str

  def _get_resize_with_range(self, img, rng=30000):
    y = len(img)
    x = len(img[0])

    # if(rng > orgPixels):
    #   return self.img
    raito = x / y
    square = rng / raito
    resizeY = int(round(np.sqrt(square)))
    resizeX = int(round(x * (resizeY / y)))

    resize_img = cv2.resize(img, (resizeX, resizeY))

    return resize_img

  def _change_to_gray_scale(self, img):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    return gray_img

  def _change_to_rgb(self, img):
    rgb_img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

    return rgb_img
