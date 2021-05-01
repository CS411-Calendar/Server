from flask_cors import CORS, cross_origin
from flask import Flask
from dotenv import dotenv_values

config = dotenv_values(".env")
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config['DATABASE_URI']
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'