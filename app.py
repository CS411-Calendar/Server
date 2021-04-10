from flask import Flask
from datetime import datetime
from db import db, init

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    init()
    app.run()
