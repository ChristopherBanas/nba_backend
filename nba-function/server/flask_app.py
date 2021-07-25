from flask import Flask
from flask_restful import Api

from .routes import *

app = Flask(__name__)
api = Api(app)

api.add_resource(Index, '/')
api.add_resource(GetGames, '/games/month/<int:month>/day/<int:day>/year/<int:year>')
api.add_resource(GetStandings, '/standings')

