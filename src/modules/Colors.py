import collections
import math
from decimal import Decimal, ROUND_HALF_UP

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
    hue = 0
    mx = max(rgb)
    mn = min(rgb)
    [r, g, b] = rgb

    if (r == mx):
      hue = 60 * ((g - b) / (mx - mn))

    elif (g == mx):
      hue = 60 * ((b - r) / (mx - mn)) + 120
    elif(b == mx):
      hue = 60 * ((r - g) / (mx - mn)) + 240

    if (hue > 360):
      hue %= 360

    if (hue < 0):
      hue += 360

    return int(Decimal(str(hue)).quantize(Decimal('0'), rounding=ROUND_HALF_UP))

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

  def is_similer_RGB(self, rgb1, rgb2, rng=10):
    [r1, g1, b1] = rgb1
    [r2, g2, b2] = rgb2

    return self.in_range(r1, r2, rng) and self.in_range(g1, g2, rng) and self.in_range(b1, b2, rng)

  def is_grey_RGB(self, rgb, rng=10):
    [r, g, b] = rgb
    avarage = sum(rgb) / len(rgb)

    return self.in_range(avarage, r, rng) and self.in_range(avarage, g, rng) and self.in_range(avarage, b, rng)

  def in_range(self, num1, num2, rng):
    num1Exist = not num1 and not (num1 == 0)
    num2Exist = not num2 and not (num2 == 0)

    if (not num1Exist and num2Exist):
      return False
    if (num1Exist and not num2Exist):
      return False
    if (num1 == num2):
      return True

    diff = num1 - num2

    abst = abs(diff)
    return abst <= rng
