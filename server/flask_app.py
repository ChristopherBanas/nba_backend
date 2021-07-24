from flask import Flask
from flask_restful import Api

from server.routes import GetGames, GetStandings

app = Flask(__name__)
api = Api(app)

api.add_resource(GetGames, '/games/month/<int:month>/day/<int:day>/year/<int:year>')
api.add_resource(GetStandings, '/standings')

if __name__ == '__main__':
    app.run(debug=True)
