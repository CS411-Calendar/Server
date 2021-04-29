from flask import request, jsonify
from datetime import datetime
# from db import db, init
from weather import get_weather


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
