from cosmos.client import standingsContainer

def deleteStandings():
    items = list(standingsContainer.query_items(enable_cross_partition_query=True,
                                                query="SELECT * FROM Items"))
    for item in items:
        standingsContainer.delete_item(item=item, partition_key="standings")