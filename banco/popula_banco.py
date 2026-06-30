import json
from pymongo import MongoClient
from bson.decimal128 import Decimal128
from decimal import Decimal
import os
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

json_path = Path(__file__).resolve().parent / "livros.json"
with open(json_path, "r", encoding="utf-8") as file:
    livros = json.load(file)

MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise ValueError("Variável de ambiente MONGO_URI não encontrada!")

client = MongoClient(MONGO_URI)
db = client.livraria
livros_collection = db.livros

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except Exception:
        return None

# Evita duplicação ao repopular: limpa a coleção e recarrega a base.
livros_collection.delete_many({})

for livro in livros:
    livro_doc = {
        "id": livro["id"],
        "titulo": livro["titulo"],
        "preco": Decimal128(Decimal(str(livro["preco"]))),  # Conversão para Decimal128
        "categoria": livro["categoria"],
        "tags": livro["tags"],
        "autores": livro["autores"],
        "mais_recente_edicao": livro.get("mais_recente_edicao", False),
        "data_publicacao": parse_date(livro["data_publicacao"]),
        "editora": livro["editora"],
        "descricao": livro["descricao"],
        "isbn": livro["isbn"],
        "estoque": livro["estoque"]
    }
    livros_collection.insert_one(livro_doc)

client.close()
print("Banco de dados populado com sucesso!")
