from flask_cors import CORS, cross_origin
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'