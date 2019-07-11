from cv2 import cv2
import collections, math, os, numpy as np

class Image:
  """
  super class of all images class.
  """
  def __init__(self, img_path):
    self.img_path = img_path
    self.img = cv2.imread(img_path)

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

  def save(self, prefix=''):
    """
    save image. if pass name, create new file and path.
    """
    new_img_path = self.img_path
    if(len(prefix) > 0):
      new_img_path = os.path.dirname(self.img_path) + '/' + prefix + os.path.basename(self.img_path)
      self.img_path = new_img_path
    cv2.imwrite(new_img_path, self.img)

  def get_img_colors(self):
    """
    method to get all pixels colors.
    """
    height, width = self.img.shape[:2]
    all_pixels = height * width
    # line up all values one row.
    vector = self.img.reshape(-1)
    # recreate pixels
    all_colors = vector.reshape(all_pixels, 3)

    return map(self._format_cv2_colors_list, all_colors)

  def resize(self, num):
    self.img = cv2.resize(self.img , (int(self.img.shape[1]*num), int(self.img.shape[0]*num)))
