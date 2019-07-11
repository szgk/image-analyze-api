from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# use chromedriver(ver74)
import os, chromedriver_binary

from src.modules import String

class WebSite:
  """
  class for website model.
  """
  def __init__(self, url, path):
    self._url = url
    self._currentpath = path

  def get_screenshot_base64(self, update=False):
    driver = self._get_screenshot()
    image = driver.get_screenshot_as_base64()
    print(image)
    return image

  def get_screenshot_name(self, update=False):
    filename = String.get_page_name(self._url) + '.png'

    # check file exist
    SAVEPATH = os.path.join(self._currentpath, ("../../public/img/" + filename))

    if(os.path.isfile(SAVEPATH) != True or update):
      self._save_screenshot(SAVEPATH)

    return filename

  def _save_screenshot(self, path):
    driver = self._get_screenshot()
    driver.save_screenshot(path)
    driver.quit()

  def _get_screenshot(self):
    options = Options()

    # local
    # options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'

    # heroku
    options.binary_location = '/app/.apt/usr/bin/google-chrome'

    options.add_argument('--headless')

    # local
    # driver_path = os.path.join(self._currentpath, ("../drivers/chromedriver"))
    # driver = webdriver.Chrome(chrome_options=options, executable_path=driver_path)

    # heroku
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(self._url)

    # get full page size
    page_width = driver.execute_script('return document.body.scrollWidth')
    page_height = driver.execute_script('return document.body.scrollHeight')
    driver.set_window_size(page_width, page_height)
    return driver
