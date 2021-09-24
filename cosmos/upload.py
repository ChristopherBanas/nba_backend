from cosmos.client import standingsContainer, gamesContainer
from cosmos.delete import deleteStandings

def uploadStandings(json):
    deleteStandings()
    standingsContainer.upsert_item(json)
    print("Standings upload completed")

def uploadGames(json):
    gamesContainer.upsert_item(json)
    print("Games upload completed")