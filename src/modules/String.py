from urllib.parse import urlparse

"""
module about string.
"""

import re
import datetime

def current_time():
  return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def get_page_name(url):
  """
  method to get name from url formated filename safety
  """
  parsed_url = urlparse(url)
  path_name = parsed_url.path.replace('/', '-')
  page_name = parsed_url.netloc
  if(path_name != '-'):
    page_name = parsed_url.netloc + '-' + path_name

  return page_name.rstrip('-')
