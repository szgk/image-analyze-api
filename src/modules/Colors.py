import collections
import math

from flask import Flask

app = Flask(__name__)

if app.config['ENV'] == 'production':
  from src.Constants import COLOR_NAMES
elif app.config['ENV'] == 'development':
  from ..Constants import COLOR_NAMES
else:
  print('Invalid ENV')


class Colors():
  """
  class for image color.
  """

  def __init__(self):
    self._all_colors = []

  def sort_colors_list(self, colors_list):
    """
    sort colors list
    """
    # cast to string, to count
    pixel_str_list = list(colors_list)

    color_counts_dict = collections.Counter(pixel_str_list)
    # get ordered colors from dict
    order_list = collections.OrderedDict(color_counts_dict)

    # sort by value
    sorted_list = sorted(order_list.items(), reverse=True, key=lambda x: x[1])

    return sorted_list

  def get_RGB_from_hue(self, hue):
    """
    get RGB params(ex. [255,255,255]) from hue degree.
    """
    mx = 255
    r, g, b = 0, 0, 0

    if hue is None or hue < 0:
      raise TypeError('invalid value')

    if 0 <= hue <= 60:
      r = mx
      g = math.floor(hue / 60 * mx)
    elif 60 < hue <= 120:
      r = math.floor((120 - hue) / 60 * mx)
      g = mx
    elif 120 < hue <= 180:
      g = mx
      b = math.floor((hue - 120) / 60 * mx)
    elif 180 < hue <= 240:
      g = math.floor((240 - hue) / 60 * mx)
      b = mx
    elif 240 < hue <= 300:
      r = math.floor((hue - 240) / 60 * mx)
      b = mx
    elif 300 < hue <= 360:
      r = mx
      b = math.floor((360 - hue) / 60 * mx)

    [r, g, b] = map(lambda n: n if 0 <= n <= 255 else 0, [r, g, b])

    return [r, g, b]

  def get_hue_from_RGB(self, rgb):
    """
    get hue degree from RGB params(ex. [255,255,255]).
    """
    hue = 0
    mx = max(rgb)
    mn = min(rgb)
    [r, g, b] = rgb

    if r == mx:
      hue = 60 * (g - b / (mx - mn))
    elif g == mx:
      hue = 60 * (b - r / (mx - mn)) + 120
    elif b == mx:
      hue = 60 * (r - g / (mx - mn)) + 240

    if hue > 360:
      hue %= 360

    return math.floor(hue)

  def get_name_from_hue(self, hue):
    if 0 <= hue <= 30:
      return COLOR_NAMES.R
    elif 30 < hue <= 60:
      return COLOR_NAMES.O
    elif 60 < hue <= 90:
      return COLOR_NAMES.Y
    elif 90 < hue <= 120:
      return COLOR_NAMES.YG
    elif 120 < hue <= 150:
      return COLOR_NAMES.G
    elif 150 < hue <= 180:
      return COLOR_NAMES.BG
    elif 180 <= hue <= 210:
      return COLOR_NAMES.B
    elif 210 < hue <= 240:
      return COLOR_NAMES.DB
    elif 240 < hue <= 270:
      return COLOR_NAMES.DeB
    elif 270 < hue <= 300:
      return COLOR_NAMES.BV
    elif 300 < hue <= 330:
      return COLOR_NAMES.V
    elif 330 < hue <= 360:
      return COLOR_NAMES.RV
