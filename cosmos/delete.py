from cosmos.client import standingsContainer, gamesContainer

def deleteStandings():
    items = list(standingsContainer.query_items(enable_cross_partition_query=True,
                                                query="SELECT * FROM Items"))
    for item in items:
        standingsContainer.delete_item(item=item, partition_key="standings")
    print("Standings deletion completed")

def deleteGames():
    items = list(gamesContainer.query_items(enable_cross_partition_query=True,
                                                query="SELECT * FROM Items"))
    for item in items:
        gamesContainer.delete_item(item=item, partition_key="games")
    print("Games deletion completed")