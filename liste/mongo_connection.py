from pymongo import MongoClient

client = MongoClient('localhost', 27017)  # Modifier avec vos propres paramètres de connexion
db = client['clic-animal']
