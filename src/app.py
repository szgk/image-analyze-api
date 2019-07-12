from flask import Flask, render_template, request, redirect, jsonify, make_response
from flask_cors import CORS, cross_origin
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os, datetime, json, urllib, sys
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

if app.config['ENV'] == 'production':
  app.config.from_pyfile('configs/prod.cfg')
  from src.models import Image
  from src.modules import Colors
  from src.modules import WebSite
elif app.config['ENV'] == 'development':
  app.config.from_pyfile('configs/dev.cfg')
  from .models import Image
  from .modules import Colors
  from .modules import WebSite
  # use chrome_driver(ver74)
  import chromedriver_binary
else:
  print('Invalid ENV')

@app.route('/', methods=['GET'])
@cross_origin()
def hello():
    return 'hello'

@app.route('/api/website/screenshot', methods=['GET'])
@cross_origin()
def get_website_screenshot():
  """
  endpoint to get screenshot as base64.
  """
  print(app.config['ENV'], file=sys.stderr)
  if request.method == 'GET':
    url = request.args.get('url')
    url = urllib.parse.unquote(url)

    webSite = WebSite()
    webSite.get_screenshot_base64(url)

    return jsonify({'status': 'start'})

@app.route('/api/image/colors', methods=['POST'])
@cross_origin()
def get_image_colors():
  """
  return all colors
  """
  if request.method == 'POST':
    img = json.loads(request.data)['img']

    image = Image(img, app.root_path)
    image_colors = image.save_all_colors()

    colors = Colors()
    sorted_colors_list = colors.sort_colors_list(image_colors)

    return jsonify(sorted_colors_list)

if __name__ == "__main__":
  app.run(debug=True)