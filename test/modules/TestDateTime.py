import datetime
import os
import sys
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))

from src.modules import DateTime


class TestColors(unittest.TestCase):

  @classmethod
  def setUpClass(self):
    None

  def test_is_over_days(self):
    actuals1 = True
    actuals2 = False
    actuals3 = True

    test_target_datetime1 = datetime.datetime(
        2016, 2, 22, 2, 22, 22, datetime.datetime.timezone.utc)
    test_limitdatetime1 = datetime.datetime(
        2016, 2, 23, 2, 22, 22, datetime.timezone.utc)

    test_target_datetime2 = datetime.datetime(
        2016, 2, 21, 1, 22, 22, datetime.timezone.utc)
    test_limitdatetime2 = datetime.datetime(
        2016, 2, 21, 3, 22, 22, datetime.timezone.utc)

    test_target_datetime3 = datetime.datetime(
        1999, 2, 21, 3, 22, 22, datetime.timezone.utc)

    result1 = DateTime.is_over_days(
        test_target_datetime1, 1, test_limitdatetime1)
    result2 = DateTime.is_over_days(
        test_target_datetime2, 1, test_limitdatetime2)
    result3 = DateTime.is_over_days(test_target_datetime3, 1)

    self.assertEqual(result1, actuals1)
    self.assertEqual(result2, actuals2)
    self.assertEqual(result3, actuals3)


if __name__ == "__main__":
  unittest.main()
