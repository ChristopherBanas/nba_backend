from upload.api.games import getGames
from upload.api.standings import getStandings
from datetime import datetime, timedelta
from cosmos.upload import uploadStandings, uploadGames

def main():
    today = datetime.today()
    yesterday = today - timedelta(1)
    games(today, yesterday)
    standings(today)


def games(today, yesterday):
    gameDict = getGames('12', '22', '2020')
    for game in gameDict:
        gameJson = {"GAME_ID": game}
        gameJson.update(gameDict[game])
        gameJson.update({'DATE' : today.strftime("%m/%d/%Y")})
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