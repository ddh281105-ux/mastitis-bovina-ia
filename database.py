from pymongo import MongoClient

# Conexión local MongoDB
client = MongoClient(
    "mongodb://localhost:27017/"
)

# Base de datos
db = client["mastitis_ai_system"]

# Colecciones
ganaderos = db["ganaderos"]
vacas = db["vacas"]
predicciones = db["predicciones"]

