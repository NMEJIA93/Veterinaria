import pymongo


mongo_host = 'localhost'  # Dirección IP o nombre del host de MongoDB
mongo_port = 27017  # Puerto de MongoDB por defecto
mongo_db_name = 'Veterinaria'  # Nombre de la base de datos
collection_name = 'historia_clinica'  # Nombre de la colección que deseas crear
collection_name1 = 'carnet_vacunas'  # Nombre de la colección que deseas crear

# Intentar establecer una conexión a MongoDB

client = pymongo.MongoClient(host=mongo_host, port=mongo_port)
db = client[mongo_db_name]
collection=db[collection_name]
collection1=db[collection_name1]