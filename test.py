from nba_api.stats.endpoints import boxscoretraditionalv2, leaguegamefinder
from datetime import datetime, timedelta

def main():
    yesterday = str((datetime.now() - timedelta(1)).strftime('%m/%d/%Y'))
    date = "12/25/2020"
    games = leaguegamefinder.LeagueGameFinder(
        date_from_nullable=date,
        date_to_nullable=date,
        season_type_nullable="Regular Season"
    ).get_dict()

    GAME_ID_INDEX = 4
    gameIds = set()
    for game in games['resultSets'][0]['rowSet']:
        gameId = game[GAME_ID_INDEX]
        if gameId not in gameIds:
            gameIds.add(gameId)
    boxScores = []
    for gameId in gameIds:
        getPlayerBoxScore(boxScores, gameId)
    print(boxScores)

def getPlayerBoxScore(boxScores, gameId):
    fullBox = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=gameId).get_dict()
    playerHeaders = fullBox['resultSets'][0]['headers']
    playerStats = fullBox['resultSets'][0]['rowSet']
    playerBox = []
    for header in range(0, len(playerHeaders)):
        for player in range(0, len(playerStats)):
            headerValue = playerHeaders[header]
            playerValue = playerStats[player][header]
            if header == 0:  # first time
                playerBox.append({headerValue: playerValue})
            else:
                tempDict = playerBox[player]
                tempDict[headerValue] = playerValue
                playerBox[player] = tempDict  # update dictionary
        if header == len(playerHeaders) - 1:  # end reached
            awayBox = []
            homeBox = []
            awayId = playerBox[0]['TEAM_ID']
            for box in playerBox:
                if box['TEAM_ID'] == awayId:
                    awayBox.append(box)
                else:  # home team
                    homeBox.append(box)
            boxScores.append({gameId : {"PLAYER_BOX_SCORE": {"AWAY": awayBox, "HOME": homeBox}}})

if __name__ == "__main__":
    main()
