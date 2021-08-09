from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from .routes import *

app = Flask(__name__)
CORS(app)
api = Api(app)

api.add_resource(Index, '/')
api.add_resource(GetGames, '/games/month/<int:month>/day/<int:day>/year/<int:year>')
api.add_resource(GetStandings, '/standings')

