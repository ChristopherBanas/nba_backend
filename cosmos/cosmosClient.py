from azure.cosmos import CosmosClient

# Initialize the Cosmos client
endpoint = "https://nba-database.documents.azure.com:443/"
key = 'OjCIsSMTexQ9N2pIUvMgZn1bPB0LVJ3QKN0YWBTvPrDwfucHTQardxA2TYRqRQHbIhYZG1OWeYPs07vIDDa9BQ=='

# Create Cosmos client
client = CosmosClient(endpoint, key)

# Create & connect to the database
database_name = 'nba'
database = client.get_database_client(database_name)

# Connect to containers
standingsContainer = database.get_container_client('standings')
gamesContainer = database.get_container_client('games')