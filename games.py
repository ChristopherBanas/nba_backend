from nba_api.stats.endpoints import boxscoretraditionalv2, leaguegamefinder
from datetime import datetime, timedelta

def main():
    yesterday = str((datetime.now() - timedelta(1)).strftime('%m/%d/%Y'))
    date = "7/17/2021"
    rawGames = leaguegamefinder.LeagueGameFinder(
        date_from_nullable=date,
        date_to_nullable=date,
        season_type_nullable="Playoffs",
        league_id_nullable='00'  # nba league id is 00
    ).get_dict()

    GAME_ID_INDEX = 4
    HOME_AWAY_INDEX = 6
    gameIds = set()
    games = {}
    for game in rawGames['resultSets'][0]['rowSet']:
        gameId = game[GAME_ID_INDEX]
        if gameId not in gameIds:  # done to avoid repeat games
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
    for gameId in games:  # get game summary for each team
        getTeamBoxScore(boxScores, gameId, games[gameId])
    for gameId in boxScores:  # get box score for each team
        getPlayerBoxScore(boxScores, gameId)
    for gameId in boxScores:  # get top performers for each team
        getTopPerformances(boxScores[gameId])
    for gameId in boxScores:
        print("------------------------------------------------------------------------")
        print(f"GAME: {boxScores[gameId]['TEAM_BOX_SCORE']['AWAY']['TEAM_NAME']} (AWAY) VS {boxScores[gameId]['TEAM_BOX_SCORE']['HOME']['TEAM_NAME']} (HOME)")
        print(f"     DATE: {boxScores[gameId]['TEAM_BOX_SCORE']['AWAY']['GAME_DATE']}")
        print(f"     OUTCOME: {boxScores[gameId]['TEAM_BOX_SCORE']['AWAY']['TEAM_NAME']} - {boxScores[gameId]['TEAM_BOX_SCORE']['AWAY']['WL']} ({boxScores[gameId]['TEAM_BOX_SCORE']['AWAY']['PTS']}) || {boxScores[gameId]['TEAM_BOX_SCORE']['HOME']['TEAM_NAME']} - {boxScores[gameId]['TEAM_BOX_SCORE']['HOME']['WL']} ({boxScores[gameId]['TEAM_BOX_SCORE']['HOME']['PTS']})")
        print("     TOP PERFORMERS:")
        print("         PTS:")
        for player in boxScores[gameId]['TOP_PERFORMERS']['HOME']['TOP_POINTS']:
            print(f"            HOME || {player['PLAYER_NAME']} - {player['PTS']}")
        print("             ---------------------------")
        for player in boxScores[gameId]['TOP_PERFORMERS']['AWAY']['TOP_POINTS']:
            print(f"            AWAY || {player['PLAYER_NAME']} - {player['PTS']}")
        print("         REBOUNDS:")
        for player in boxScores[gameId]['TOP_PERFORMERS']['HOME']['TOP_REBOUNDS']:
            print(f"            HOME || {player['PLAYER_NAME']} - {player['REB']}")
        print("             ---------------------------")
        for player in boxScores[gameId]['TOP_PERFORMERS']['AWAY']['TOP_REBOUNDS']:
            print(f"            AWAY || {player['PLAYER_NAME']} - {player['REB']}")
        print("         ASSISTS:")
        for player in boxScores[gameId]['TOP_PERFORMERS']['HOME']['TOP_ASSISTS']:
            print(f"            HOME || {player['PLAYER_NAME']} - {player['AST']}")
        print("             ---------------------------")
        for player in boxScores[gameId]['TOP_PERFORMERS']['AWAY']['TOP_ASSISTS']:
            print(f"            AWAY || {player['PLAYER_NAME']} - {player['AST']}")


def getTeamBoxScore(boxScore, gameId, gameDict):
    homeBox = homeAwayTeamBoxScore(gameDict['HOME'])
    awayBox = homeAwayTeamBoxScore(gameDict['AWAY'])
    boxScore[gameId] = {"TEAM_BOX_SCORE": {"AWAY": awayBox, "HOME": homeBox}}

def homeAwayTeamBoxScore(teamBox):
    # hard coded, no need to pass in entirety of rawGames dictionary to get them
    headers = ['SEASON_ID', 'TEAM_ID', 'TEAM_ABBREVIATION', 'TEAM_NAME', 'GAME_ID', 'GAME_DATE', 'MATCHUP', 'WL', 'MIN', 'PTS', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PLUS_MINUS']
    tempDict = {}
    index = 0
    for header in headers:
        tempDict[header] = teamBox[index]
        index += 1
    return tempDict

def getPlayerBoxScore(boxScores, gameId):
    fullBox = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=gameId).get_dict()
    playerHeaders = fullBox['resultSets'][0]['headers']
    playerStats = fullBox['resultSets'][0]['rowSet']
    awayBox = []
    homeBox = []
    awayId = boxScores[gameId]['TEAM_BOX_SCORE']['AWAY']['TEAM_ID']
    TEAM_ID_INDEX = 1
    for player in playerStats:
        index = 0
        tempDict = {}
        while index < len(playerHeaders):  # loop through all of the stats from a player
            tempDict[playerHeaders[index]] = player[index]
            index += 1
        if player[TEAM_ID_INDEX] == awayId:
            awayBox.append(tempDict)
        else:  # home
            homeBox.append(tempDict)
    boxScores[gameId].update({"PLAYER_BOX_SCORE": {"AWAY": awayBox, "HOME": homeBox}})

def getTopPerformances(boxScore):
    boxScore.update({'TOP_PERFORMERS':
                         {'AWAY' : homeAwayTopPerformers(boxScore['PLAYER_BOX_SCORE']['AWAY']),
                          'HOME': homeAwayTopPerformers(boxScore['PLAYER_BOX_SCORE']['HOME'])}})

def homeAwayTopPerformers(teamBox):
    tempBox = teamBox  # so the order of teamBox is not messed up
    topPoints = sorted(tempBox, key=getPoints, reverse=True)[0:3]
    topAssists = sorted(tempBox, key=getAssists, reverse=True)[0:3]
    topRebounds = sorted(tempBox, key=getRebounds, reverse=True)[0:3]
    return {"TOP_POINTS": topPoints, "TOP_ASSISTS": topAssists, "TOP_REBOUNDS": topRebounds}

def getPoints(elem):
    return checkVal(elem['PTS'])

def getAssists(elem):
    return checkVal(elem['AST'])

def getRebounds(elem):
    return checkVal(elem['REB'])

def checkVal(val):
    if val is None:
        return 0
    return val

if __name__ == "__main__":
    main()
