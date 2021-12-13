from nba_api.stats.endpoints import boxscoretraditionalv2, leaguegamefinder
import time

def getGames(month, day, year):
    date = f"{month}/{day}/{year}"
    seasonType = "Regular Season"
    playoffMonths = {9, 6, 7}
    if int(month) in playoffMonths:
        seasonType = "Playoffs"
    rawGames = leaguegamefinder.LeagueGameFinder(
        date_from_nullable=date,
        date_to_nullable=date,
        season_type_nullable=seasonType,
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
    print("Game summary completed")
    for gameId in boxScores:  # get box score for each team
        getPlayerBoxScore(boxScores, gameId)
        getQuarterData(boxScores, gameId)
    print("Box scores completed")
    for gameId in boxScores:  # get top performers for each team
        getTopPerformances(boxScores[gameId])
    print("Top performers completed")
    return boxScores


def getTeamBoxScore(boxScore, gameId, gameDict):
    homeBox = homeAwayTeamBoxScore(gameDict['HOME'])
    awayBox = homeAwayTeamBoxScore(gameDict['AWAY'])
    boxScore[gameId] = {"TEAM_BOX_SCORE": {"AWAY": {"TOTAL": awayBox}, "HOME": {"TOTAL": homeBox}}}

def homeAwayTeamBoxScore(teamBox):
    # hard coded, no need to pass in entirety of rawGames dictionary to get them
    headers = ['SEASON_ID', 'TEAM_ID', 'TEAM_ABBREVIATION', 'TEAM_NAME', 'GAME_ID', 'GAME_DATE', 'MATCHUP', 'WL', 'MIN', 'PTS', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TO', 'PF', 'PLUS_MINUS']
    tempDict = {}
    index = 0
    for header in headers:
        tempDict[header] = checkDecimal(header, teamBox[index])
        index += 1
    return tempDict

def checkDecimal(header, value):
    if 'PCT' in header:  # make sure it is a good double
        if value is None:
            value = 0
        value = round(float(value) * 100, 2)
    return value

def getQuarterData(boxScores, gameId):
    # first half, second half, 1q, 2q, 3q, 4q
    ranges = [(0,14400),(14400,28800),(0,7200),(7200,14400),(14400,21600),(21600,28800)]
    nameList = ['FIRST_HALF', "SECOND_HALF", 'Q1', 'Q2', 'Q3', 'Q4']
    awayId = boxScores[gameId]['TEAM_BOX_SCORE']['AWAY']['TOTAL']['TEAM_ID']
    for i in range(0, len(ranges)):
        print(f"Getting {nameList[i]} stats for {gameId}")
        time.sleep(5)
        start = ranges[i][0]
        end = ranges[i][1]
        fullBox = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=gameId,
                                                              end_period=10,
                                                              end_range=end,
                                                              range_type=2,
                                                              start_period=1,
                                                              start_range=start).get_dict()['resultSets']
        homeBox = []
        awayBox = []
        PLAYER_INDEX = 0
        sharedPlayer(homeBox, awayBox, awayId, fullBox[PLAYER_INDEX]['headers'], fullBox[PLAYER_INDEX]['rowSet'])
        awayDict = {f"{nameList[i]}" : awayBox}
        homeDict = {f"{nameList[i]}" : homeBox}
        boxScores[gameId]['PLAYER_BOX_SCORE']['AWAY'].update(awayDict)
        boxScores[gameId]['PLAYER_BOX_SCORE']['HOME'].update(homeDict)

        homeBox = []
        awayBox = []
        TEAM_INDEX = 1
        sharedPlayer(homeBox, awayBox, awayId, fullBox[TEAM_INDEX]['headers'], fullBox[TEAM_INDEX]['rowSet'])
        awayDict = {f"{nameList[i]}" : awayBox[0]}
        homeDict = {f"{nameList[i]}" : homeBox[0]}
        boxScores[gameId]['TEAM_BOX_SCORE']['AWAY'].update(awayDict)
        boxScores[gameId]['TEAM_BOX_SCORE']['HOME'].update(homeDict)

def sharedPlayer(homeBox, awayBox, awayId, playerHeaders, playerStats):
    TEAM_ID_INDEX = 1
    for player in playerStats:
        index = 0
        tempDict = {}
        while index < len(playerHeaders):  # loop through all of the stats from a player
            tempDict[playerHeaders[index]] = checkDecimal(playerHeaders[index], player[index])
            index += 1
        if player[TEAM_ID_INDEX] == awayId:
            awayBox.append(tempDict)
        else:  # home
            homeBox.append(tempDict)

def getPlayerBoxScore(boxScores, gameId):
    fullBox = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=gameId).get_dict()
    playerHeaders = fullBox['resultSets'][0]['headers']
    playerStats = fullBox['resultSets'][0]['rowSet']
    awayBox = []
    homeBox = []
    awayId = boxScores[gameId]['TEAM_BOX_SCORE']['AWAY']['TOTAL']['TEAM_ID']
    sharedPlayer(homeBox, awayBox, awayId, playerHeaders, playerStats)
    boxScores[gameId].update({"PLAYER_BOX_SCORE": {"AWAY": {"TOTAL": awayBox}, "HOME": {'TOTAL': homeBox}}})

def getTopPerformances(boxScore):
    boxScore.update({'TOP_PERFORMERS':
                         {'AWAY' : homeAwayTopPerformers(boxScore['PLAYER_BOX_SCORE']['AWAY']['TOTAL']),
                          'HOME': homeAwayTopPerformers(boxScore['PLAYER_BOX_SCORE']['HOME']['TOTAL'])}})

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

