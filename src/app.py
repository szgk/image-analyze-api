import json
import urllib

from flask import Flask, jsonify, request

from flask_cors import CORS, cross_origin


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

if app.config['ENV'] == 'production':
  app.config.from_pyfile('configs/prod.cfg')
  from src.models import Image
  from src.models import WebSite
  from src.modules import Colors
elif app.config['ENV'] == 'development':
  app.config.from_pyfile('configs/dev.cfg')
  from .models import Image
  from .models import WebSite
  from .modules import Colors
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
  if request.method == 'GET':
    url = request.args.get('url')
    url = urllib.parse.unquote(url)

    webSite = WebSite()
    file_name = webSite.start_to_get_sceenshot(url)

    return jsonify({'file_name': file_name})


@app.route('/api/image/colors', methods=['GET'])
@cross_origin()
def get_image_colors():
  """
  return all colors
  """
  if request.method == 'GET':
    img = json.loads(request.data)['img']

    image = Image(img, app.root_path)
    image_colors = image.save_all_colors()

    colors = Colors()
    sorted_colors_list = colors.sort_colors_list(image_colors)

    return jsonify(sorted_colors_list)


if __name__ == "__main__":
  app.run(debug=True)
