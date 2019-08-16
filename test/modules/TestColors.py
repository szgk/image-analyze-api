import os
import sys
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))

from src.Constants import COLOR_NAMES
from src.modules import Colors


class TestColors(unittest.TestCase):

  @classmethod
  def setUpClass(self):
    self.colors = Colors()

  def test_get_hue_from_RGB(self):
    actuals = []
    testRGB = [
        [255, 0, 0],
        [255, 255, 0],
        [0, 255, 0],
        [0, 255, 255],
        [0, 0, 255],
        [255, 0, 0],
    ]

    for i in range(0, 6):
      actuals.append(self.colors.get_hue_from_RGB(testRGB[i]))

    expected1 = 0
    expected2 = 60
    expected3 = 120
    expected4 = 180
    expected5 = 240
    expected6 = 0

    self.assertEqual(expected1, actuals[0])
    self.assertEqual(expected2, actuals[1])
    self.assertEqual(expected3, actuals[2])
    self.assertEqual(expected4, actuals[3])
    self.assertEqual(expected5, actuals[4])
    self.assertEqual(expected6, actuals[5])

  def test_get_RGB_from_hue(self):
    actuals = []
    for i in range(0, 6):
      deg = i * 60
      res = self.colors.get_RGB_from_hue(deg if 0 < deg < 360 else 0)
      actuals.append(res)

    expected1 = [255, 0, 0]
    expected2 = [255, 255, 0]
    expected3 = [0, 255, 0]
    expected4 = [0, 255, 255]
    expected5 = [0, 0, 255]
    expected6 = [255, 0, 255]

    self.assertEqual(expected1, actuals[0])
    self.assertEqual(expected2, actuals[1])
    self.assertEqual(expected3, actuals[2])
    self.assertEqual(expected4, actuals[3])
    self.assertEqual(expected5, actuals[4])
    self.assertEqual(expected6, actuals[5])

  def test_get_name_from_hue(self):
    actuals = []
    for i in range(0, 12):
      actuals.append(self.colors.get_name_from_hue(
          i * 30 + 1 if 0 < i * 30 < 360 else 0))

    expecteds = [
        COLOR_NAMES.R,
        COLOR_NAMES.O,
        COLOR_NAMES.Y,
        COLOR_NAMES.YG,
        COLOR_NAMES.G,
        COLOR_NAMES.BG,
        COLOR_NAMES.B,
        COLOR_NAMES.DB,
        COLOR_NAMES.DeB,
        COLOR_NAMES.BV,
        COLOR_NAMES.V,
        COLOR_NAMES.RV,
    ]

    for i in range(len(expecteds)):
      self.assertEqual(expecteds[i], actuals[i])

  def test_in_range(self):
    expected1 = True
    actual1 = self.colors.in_range(2, 1, 3)
    expected2 = False
    actual2 = self.colors.in_range(3, 1, 1)
    expected3 = False
    actual3 = self.colors.in_range(3, 1, 0)
    expected4 = True
    actual4 = self.colors.in_range(3, 5, 10)
    self.assertEqual(expected1, actual1)
    self.assertEqual(expected2, actual2)
    self.assertEqual(expected3, actual3)
    self.assertEqual(expected4, actual4)

  def test_is_grey_RGB(self):
    expected1 = True
    actual1 = self.colors.is_grey_RGB([200, 201, 210])
    expected2 = False
    actual2 = self.colors.is_grey_RGB([100, 0, 0])

    self.assertEqual(expected1, actual1)
    self.assertEqual(expected2, actual2)

  def test_is_similer_RGB(self):
    expected1 = True
    actual1 = self.colors.is_similer_RGB([200, 200, 210], [210, 190, 200])
    expected2 = False
    actual2 = self.colors.is_similer_RGB([200, 180, 31], [200, 180, 20])

    self.assertEqual(expected1, actual1)
    self.assertEqual(expected2, actual2)


if __name__ == "__main__":
  unittest.main()
