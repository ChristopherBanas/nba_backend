from upload.api.games import getGames
from upload.api.standings import getStandings
from datetime import datetime, timedelta
from cosmos.upload import uploadStandings, uploadGames
from cosmos.delete import deleteGames

def main():
    today = datetime.today()
    yesterday = today - timedelta(1)
    games(yesterday)
    standings(today)

def games(yesterday):
    #gameDict = getGames('5', '16', '2021')
    gameDict = getGames(yesterday.month, yesterday.day, yesterday.year)
    deleteGames()
    for game in gameDict:
        gameJson = {"GAME_ID": game}
        gameJson.update(gameDict[game])
        gameJson.update({'DATE' : yesterday.strftime("%m/%d/%Y")})
        gameJson.update({"games" : "games"})
        uploadGames(gameJson)

def standings(today):
    standingsDict = getStandings()
    standingJson = {"DATE": today.strftime("%m/%d/%Y")}
    standingJson.update(standingsDict)
    standingJson.update({"standings" : "standings"})
    uploadStandings(standingJson)

if __name__ == '__main__':
    main()