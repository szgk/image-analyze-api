from flask import Flask, render_template, request, redirect, jsonify, make_response
from flask_cors import CORS, cross_origin
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# use chrome_driver(ver74)
# import chromedriver_binary
import os, datetime, json, urllib

from src.models import WebSite, Image
from src.modules.Colors import Colors

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/', methods=['GET'])
@cross_origin()
def hello():
    return 'hello'

@app.route('/api/website/screenshot', methods=['GET'])
@cross_origin()
def get_website_screenshot():
  """
  endpoint to create screenshot of website.
  """
  if request.method == 'GET':
    url = request.args.get('url')
    print(url)
    url = urllib.parse.unquote(url)
    print(url)
    webSite = WebSite(url, app.root_path)
    image = webSite.get_screenshot_base64()

    return jsonify({'image': image})

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