from nba_api.stats.endpoints import boxscoretraditionalv2, leaguegamefinder
from datetime import datetime, timedelta
import time

def main():
    yesterday = str((datetime.now() - timedelta(1)).strftime('%m/%d/%Y'))
    header = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
        "x-nba-stats-origin": "stats"
    }
    date = "7/20/2021"
    rawGames = leaguegamefinder.LeagueGameFinder(
        date_from_nullable=date,
        date_to_nullable=date,
        season_type_nullable="Playoffs",
        league_id_nullable='00'
    ).get_dict()

    GAME_ID_INDEX = 4
    HOME_AWAY_INDEX = 6
    gameIds = set()
    games = {}
    for game in rawGames['resultSets'][0]['rowSet']:
        gameId = game[GAME_ID_INDEX]
        if gameId not in gameIds:
            gameIds.add(gameId)
            if 'vs' in game[HOME_AWAY_INDEX]:  # home team
                games[gameId] = {"HOME": game}
            else:
                games[gameId] = {"AWAY": game}
        else:  # already in
            if 'vs' in game[HOME_AWAY_INDEX]:  # home team
                games[gameId].update({"HOME": game})
            else:
                games[gameId].update({"AWAY": game})
    boxScores = {}
    for gameId in games:
        getTeamBoxScore(boxScores, gameId, games[gameId])
    for gameId in gameIds:
        getPlayerBoxScore(boxScores, gameId)
    topPerformers = getTopPerformances(boxScores['0042000406']['PLAYER_BOX_SCORE']['HOME'])
    for player in topPerformers['TOP_POINTS']:
        print(f"PTS: Player {player['PLAYER_NAME']} : {player['PTS']}")
    print("")
    for player in topPerformers['TOP_ASSISTS']:
        print(f"AST: Player {player['PLAYER_NAME']} : {player['AST']}")
    print("")
    for player in topPerformers['TOP_REBOUNDS']:
        print(f"REB: Player {player['PLAYER_NAME']} : {player['REB']}")

def getTeamBoxScore(boxScores, gameId, gameDict):
    headers = ['SEASON_ID', 'TEAM_ID', 'TEAM_ABBREVIATION', 'TEAM_NAME', 'GAME_ID', 'GAME_DATE', 'MATCHUP', 'WL', 'MIN', 'PTS', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PLUS_MINUS']
    homeBox = homeAwayTeamBoxScore(gameDict['HOME'], headers)
    awayBox = homeAwayTeamBoxScore(gameDict['AWAY'], headers)
    boxScores[gameId] = {"TEAM_BOX_SCORE": {"AWAY": awayBox, "HOME": homeBox}}

def homeAwayTeamBoxScore(teamBox, headers):
    returnBox = []
    tempDict = {}
    index = 0
    for header in headers:
        tempDict[header] = teamBox[index]
        index += 1
    returnBox.append(tempDict)
    return returnBox

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
    boxScores[gameId].update({"PLAYER_BOX_SCORE": {"AWAY": awayBox, "HOME": homeBox}})

def getTopPerformances(boxScore):
    tempBox = boxScore
    topPoints = sorted(tempBox, key=getPoints, reverse=True)[0:3]
    topAssists = sorted(tempBox, key=getAssists, reverse=True)[0:3]
    topRebounds = sorted(tempBox, key=getRebounds, reverse=True)[0:3]
    return {"TOP_POINTS": topPoints, "TOP_ASSISTS": topAssists, "TOP_REBOUNDS": topRebounds}

def getPoints(elem):
    val = elem['PTS']
    if val is None:
        return 0
    return val

def getAssists(elem):
    val = elem['AST']
    if val is None:
        return 0
    return val

def getRebounds(elem):
    val = elem['REB']
    if val is None:
        return 0
    return val

if __name__ == "__main__":
    main()
