from nba_api.stats.endpoints import leaguestandingsv3

def main():
    rawStandings = leaguestandingsv3.LeagueStandingsV3(
        league_id='00',
    ).get_dict()
    standings = {}
    getStandings(standings, rawStandings)

def getStandings(standings, rawStandings):
    headers = rawStandings['resultSets'][0]['headers']
    teamStats = rawStandings['resultSets'][0]['rowSet']
    westStandings = []
    eastStandings = []
    for team in teamStats:
        index = 0
        tempDict = {}
        CONFERENCE_INDEX = 6
        while index < len(headers):
            tempDict[headers[index]] = team[index]
            index += 1
        if team[CONFERENCE_INDEX] == 'West':
            westStandings.append(tempDict)
        else:  # east
            eastStandings.append(tempDict)
    leagueStandings = getLeagueStandings(eastStandings, westStandings)
    standings.update({'EAST': eastStandings, 'WEST': westStandings, 'LEAGUE': leagueStandings})

def getLeagueStandings(eastStandings, westStandings):
    leagueStandings = eastStandings + westStandings
    leagueStandings = sorted(leagueStandings, key=winPercentage, reverse=True)
    return leagueStandings

def winPercentage(elem):
    return elem['WinPCT']

if __name__ == '__main__':
    main()