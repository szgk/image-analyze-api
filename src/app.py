import json
import urllib

from flask import Flask, abort, jsonify, request

from flask_cors import CORS, cross_origin


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

if app.config['ENV'] == 'production':
  app.config.from_pyfile('configs/prod.cfg')
  from src.models import Image
  from src.modules import Validator
elif app.config['ENV'] == 'development':
  app.config.from_pyfile('configs/dev.cfg')
  from .models import Image
  from .modules import Validator
else:
  print('Invalid ENV')


@app.before_request
def common_func():
  referrer = request.headers.get("Referer")

  if(request.args.get("api_token") == "aejoelaoggembcahagimdiliamlcdmfm"):
    return

  CheckReferer = Validator.CheckReferer(referrer)
  result = CheckReferer.is_valid()

  if(not result or result is None):
    abort(404, {'message': 'invalid referer'})
  else:
    return


@app.route('/', methods=['GET'])
@cross_origin()
def hello():
  return 'hello'


@app.route('/api/image/<resource>', methods=['POST'])
@cross_origin()
def post_image(resource=None):
  param_str = request.data.decode()
  param = json.loads(param_str)
  encoded_base64 = param['base64']
  base64 = urllib.parse.unquote(encoded_base64)
  image = Image()

  if(resource == 'colors'):
    """
    return all colors
    """
    colors = image.get_colors_by_base64(base64)
    return jsonify({"colors": colors})

  elif(resource == 'coordinates'):
    """
    return layout image
    """
    layout_info = image.get_layout_info_from_base64(base64)
    return jsonify(layout_info)

  else:
    abort(404, 'Invalid param')


if __name__ == "__main__":
  app.run(debug=True)
