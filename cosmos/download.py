from cosmos.cosmosClient import standingsContainer, gamesContainer
from cosmos.delete import deleteStandings

def downloadStandings():
    items = list(standingsContainer.query_items(enable_cross_partition_query=True,
                                                query="SELECT * FROM Items"))
    return items

def downloadGames(month, day, year):
    items = list(gamesContainer.query_items(enable_cross_partition_query=True,
                                                query="SELECT * FROM Items"))
    return items