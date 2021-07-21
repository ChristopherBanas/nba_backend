from nba_api.stats.endpoints import boxscoretraditionalv2, leaguegamefinder
from datetime import datetime, timedelta
import time

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

def getPlayerBoxScore(boxScores, gameId):
    fullBox = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=gameId).get_dict()
    playerHeaders = ['GAME_ID', 'TEAM_ID', 'TEAM_ABBREVIATION', 'TEAM_CITY', 'PLAYER_ID', 'PLAYER_NAME', 'NICKNAME', 'START_POSITION', 'COMMENT', 'MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TO', 'PF', 'PTS', 'PLUS_MINUS']
    playerStats = fullBox['resultSets'][0]['rowSet']
    playerBox = []
    for player in playerStats:
        index = 0
        tempDict = {}
        while index < len(playerHeaders):
            tempDict[playerHeaders[index]] = player[index]
            index += 1
        playerBox.append(tempDict)
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
