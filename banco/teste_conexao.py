import os
from dotenv import load_dotenv
import pymongo

# Carrega as variáveis de ambiente do .env
load_dotenv()

# Obtém a URI do MongoDB Atlas do .env
MONGO_URI = os.getenv('MONGO_URI')

# Tenta conectar ao MongoDB Atlas
try:
    client = pymongo.MongoClient(MONGO_URI)
    # Testa a conexão listando os nomes dos bancos de dados disponíveis
    print("Conectado ao MongoDB Atlas com sucesso!")
    print("Bancos de dados disponíveis:", client.list_database_names())
    # Fecha a conexão
    client.close()
except Exception as e:
    print(f"Erro ao conectar ao MongoDB Atlas: {e}")
