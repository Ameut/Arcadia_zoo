from pymongo import MongoClient

mongo_client = MongoClient('mongodb+srv://ameur:K7V4s1ro5rPgamCv@cluster0.pebkoik.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = mongo_client['clic-animal']
clicks_collection = db['clicks']

