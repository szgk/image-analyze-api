import json
import urllib

from flask import Flask, jsonify, request

from flask_cors import CORS, cross_origin


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

if app.config['ENV'] == 'production':
  app.config.from_pyfile('configs/prod.cfg')
  from src.modules import Image
elif app.config['ENV'] == 'development':
  app.config.from_pyfile('configs/dev.cfg')
  from .modules import Image
else:
  print('Invalid ENV')


@app.route('/', methods=['GET'])
@cross_origin()
def hello():
  return 'hello'


@app.route('/api/image/colors', methods=['POST'])
@cross_origin()
def post_image():
  """
  return all colors
  """
  if request.method == 'POST':
    referrer = request.headers.get("Referer")
    print('referrer', referrer)
    param_str = request.data.decode()
    param = json.loads(param_str)
    base64 = param['base64']
    img = urllib.parse.unquote(base64)
    image = Image(img_base64=img)
    colors = image.get_img_colors()
    return jsonify({"colors": colors})


if __name__ == "__main__":
  app.run(debug=True)
