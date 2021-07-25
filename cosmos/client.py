from azure.cosmos import CosmosClient
from tokens import endpoint, key

# Create Cosmos client
client = CosmosClient(endpoint, key)

# Create & connect to the database
database_name = 'nba'
database = client.get_database_client(database_name)

# Connect to containers
standingsContainer = database.get_container_client('standings')
gamesContainer = database.get_container_client('games')