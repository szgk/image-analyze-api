source ./venv/bin/activate
export PYTHONDONTWRITEBYTECODE=1
export FLASK_APP="./src/app.py"
export FLASK_DEBUG=${DEV}
export FLASK_ENV=development
flask run