import base64

from cv2 import cv2

import numpy as np


class Image:
  """
  super class of all images class.
  """

  def _format_cv2_colors_list(self, unit8_arr):
    """
    format color list that get by cv2 from image file.
    BGR -> RGB, change numpy.unit8 -> string
    """
    # swap BGR => RGB
    unit8_arr[0], unit8_arr[2] = unit8_arr[2], unit8_arr[0]
    # to use counter, change numpy.unit8 to string.
    unicode_arr = unit8_arr.astype('unicode')
    return str(','.join(unicode_arr))

  def get_img_colors(self, img):
    """
    method to get all pixels colors.
    """
    height, width = img.shape[:2]
    all_pixels = height * width
    # line up all values one row.
    vector = img.reshape(-1)
    # recreate pixels
    all_colors = vector.reshape(all_pixels, 3)

    return map(self._format_cv2_colors_list, all_colors)

  def base64_to_ndarray(self, img_base64):
    img = base64.b64decode(img_base64)
    img_np = np.fromstring(img, np.uint8)
    return cv2.imdecode(img_np, cv2.IMREAD_ANYCOLOR)

  def resize(self, img, num):
    return cv2.resize(img, (int(img.shape[1] * num), int(img.shape[0] * num)))
