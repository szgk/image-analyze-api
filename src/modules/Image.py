import base64
import collections
# import os
import tempfile

from cv2 import cv2

from flask import Flask

import numpy as np

import requests


app = Flask(__name__)


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
    if self.img is None or len(self.img) <= 0:
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

  def _imread_web(self, img_url):
    res = requests.get(img_url)
    img = None

    with tempfile.NamedTemporaryFile(dir='./') as fp:
      fp.write(res.content)
      fp.file.seek(0)
      img = cv2.imread(fp.name)
    return img

  def base64_to_ndarray(self, img_base64):
    img = base64.b64decode(img_base64)
    img_np = np.fromstring(img, np.uint8)
    return cv2.imdecode(img_np, cv2.IMREAD_ANYCOLOR)

  def _base64_str_to_ndarray(self, base64_str):
    base64_bytes = base64_str.encode()
    img = self.base64_to_ndarray(base64_bytes)

    return img

  def resize(self, img, num):
    return cv2.resize(img, (int(img.shape[1] * num), int(img.shape[0] * num)))
