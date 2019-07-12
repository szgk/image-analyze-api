from flask import Flask
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os, asyncio

app = Flask(__name__)

import os
if app.config['ENV'] == 'production':
  from src.modules import String
elif app.config['ENV'] == 'development':
  from . import String
  # use chromedriver(ver74)
  import chromedriver_binary
else:
  print('Invalid ENV')

class WebSite:
  def __init__(self):
    self._url = ''

  def get_screenshot_base64(self, url):
    self._url = url
    driver = self._get_driver()
    image = driver.get_screenshot_as_base64()
    driver.quit()
    return image

  def _get_driver(self):
    options = Options()

    is_dev = app.config['ENV'] == 'development'
    is_prod = app.config['ENV'] == 'production'

    if is_dev:
      options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
    elif is_prod:
      options.binary_location = '/app/.apt/usr/bin/google-chrome'
    else:
      options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'

    options.add_argument('--headless')

    if is_dev:
      driver_path = os.path.join(os.path.dirname(__file__), ("../../drivers/chromedriver"))
      driver = webdriver.Chrome(chrome_options=options, executable_path=driver_path)
    elif is_prod:
      options.add_argument('--disable-gpu')
      driver = webdriver.Chrome(chrome_options=options)
    else:
      driver_path = os.path.join(self._currentpath, ("../drivers/chromedriver"))
      driver = webdriver.Chrome(chrome_options=options, executable_path=driver_path)

    driver.get(self._url )

    # get full page size
    page_width = driver.execute_script('return document.body.scrollWidth')
    page_height = driver.execute_script('return document.body.scrollHeight')
    driver.set_window_size(page_width, page_height)
    return driver
