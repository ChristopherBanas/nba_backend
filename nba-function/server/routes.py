from flask_restful import Resource
from cosmos.download import *

class Index(Resource):
    def get(self):
        return "Welcome!"

class GetGames(Resource):
    def get(self, month, day, year):
        return downloadGames(month, day, year)

class GetStandings(Resource):
    def get(self):
        return downloadStandings()
