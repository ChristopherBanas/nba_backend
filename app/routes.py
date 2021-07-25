from flask_restful import Resource
from nba.games import getGames
from nba.standings import getStandings

class Index(Resource):
    def get(self):
        return "Welcome!"

class GetGames(Resource):
    def get(self, month, day, year):
        return getGames(month, day, year)

class GetStandings(Resource):
    def get(self):
        return getStandings()
