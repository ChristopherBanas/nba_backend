from flask_restful import Resource
from cosmos.download import *

class Index(Resource):
    def get(self):
        return "Welcome!"

class GetGames(Resource):
    def get(self):
        return downloadGames()

class GetStandings(Resource):
    def get(self):
        return downloadStandings()
