from nba_api.stats.endpoints import leaguestandingsv3

nameDict = {
    '76ers': 'PHI',
    'Nets': 'BKN',
    'Bucks': 'MIL',
    'Knicks': 'NY',
    'Hawks': 'ATL',
    'Heat': 'MIA',
    'Celtics': 'BOS',
    'Wizards': 'WSH',
    'Pacers': 'IND',
    'Hornets': 'CHA',
    'Bulls': 'CHI',
    'Raptors': 'TOR',
    'Cavaliers': 'CLE',
    'Magic': 'ORL',
    'Pistons': 'DET',
    'Jazz': 'UTA',
    'Suns': 'PHX',
    'Nuggets': 'DEN',
    'Clippers': 'LAC',
    'Mavericks': 'DAL',
    'Trail Blazers': 'POR',
    'Lakers': 'LAL',
    'Grizzlies': 'MEM',
    'Warriors': 'GSW',
    'Spurs': 'SAS',
    'Pelicans': 'NOP',
    'Kings': 'SAC',
    'Timberwolves': 'MIN',
    'Thunder': 'OKC',
    'Rockets': 'HOU'
}

def getStandings():
    rawStandings = leaguestandingsv3.LeagueStandingsV3(
        league_id='00',
    ).get_dict()
    standings = {}
    getEastWestStandings(standings, rawStandings)
    return standings

def getEastWestStandings(standings, rawStandings):
    headers = rawStandings['resultSets'][0]['headers']
    teamStats = rawStandings['resultSets'][0]['rowSet']
    westStandings = []
    eastStandings = []
    for team in teamStats:
        index = 0
        tempDict = {}
        CONFERENCE_INDEX = 6
        while index < len(headers):
            value = team[index]
            if headers[index] == 'TeamName':
                value = nameDict[value]
            tempDict[headers[index]] = value
            index += 1
        if team[CONFERENCE_INDEX] == 'West':
            westStandings.append(tempDict)
        else:  # east
            eastStandings.append(tempDict)
    leagueStandings = getTotalStandings(eastStandings, westStandings)
    standings.update({'EAST': eastStandings, 'WEST': westStandings, 'LEAGUE': leagueStandings})

def getTotalStandings(eastStandings, westStandings):
    leagueStandings = eastStandings + westStandings
    leagueStandings = sorted(leagueStandings, key=winPercentage, reverse=True)
    return leagueStandings

def winPercentage(elem):
    return elem['WinPCT']

