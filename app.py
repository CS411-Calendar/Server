from flask import request, Flask, jsonify
from datetime import datetime
# from db import db, init
from weather import get_weather
from flask_cors import CORS, cross_origin
app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/weather', methods=['GET', 'POST'])
def weather():

    if request.method == 'GET':
        lat, lon = request.args.get('lat'), request.args.get('long')
        try:
            forecast = get_weather(float(lat), float(lon))
        except Exception as e:
            return 'Internal Server Error', 500
        return jsonify(forecast), 200

if __name__ == '__main__':
    # init()
    app.run()
