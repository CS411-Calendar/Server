from flask import request, Flask, jsonify
from datetime import datetime
# from db import db, init
from weather import get_weather

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'

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
            forecast = [[e]]
        #return f"Found lat: {lat} long: {lon}"
        return jsonify(forecast)

if __name__ == '__main__':
    # init()
    app.run()
