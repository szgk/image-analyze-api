import os
import sys
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))

from src.modules.Validator import CheckReferer


class TestColors(unittest.TestCase):

  @classmethod
  def setUpClass(self):
    None

  def test_is_check_referer(self):
    actuals1 = True
    actuals2 = False

    checkReferer = CheckReferer('localhost:9000')
    result1 = checkReferer.is_valid()

    checkReferer = CheckReferer('localhost:90002')
    result2 = checkReferer.is_valid()

    checkReferer = CheckReferer('szgk.github.io')
    result3 = checkReferer.is_valid()

    checkReferer = CheckReferer('szgk.github.ioo')
    result4 = checkReferer.is_valid()

    self.assertEqual(result1, actuals1)
    self.assertEqual(result2, actuals2)
    self.assertEqual(result3, actuals1)
    self.assertEqual(result4, actuals2)


if __name__ == "__main__":
  unittest.main()
