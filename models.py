from pymongo import MongoClient
from dotenv import load_dotenv
from bson.objectid import ObjectId
from bson.decimal128 import Decimal128
from decimal import Decimal
from datetime import datetime
import os

load_dotenv()

# Configuração da conexão com o MongoDB Atlas
MONGO_URI = os.getenv("MONGO_URI")
print(MONGO_URI)
client = None
db = None
try:
    if not MONGO_URI:
       raise ValueError("MONGO_URI não definida")
    client = MongoClient(MONGO_URI)
    db = client.livraria  # nome do banco de dados
except Exception as e:
    print(f"Erro ao conectar ao MongoDB: {e}")

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except Exception:
        return None

# Coleções
livros = db.livros
usuarios = db.usuarios
pedidos = db.pedidos


class Livro:
    def __init__(
        self,
        titulo,
        preco,
        categoria,
        tags,
        autores,
        mais_recente_edicao,
        numero_autores,
        data_publicacao,
        editora,
        descricao,
        isbn,
        estoque,
        imagem_capa,
    ):
        self.titulo = titulo
        self.preco = preco
        self.categoria = categoria
        self.tags = tags
        self.autores = autores
        self.mais_recente_edicao = mais_recente_edicao
        self.numero_autores = numero_autores
        self.data_publicacao = data_publicacao
        self.editora = editora
        self.descricao = descricao
        self.isbn = isbn
        self.estoque = estoque
        self.imagem_capa = imagem_capa

    def salvar(self):
        """
        Salvar o livro no banco de dados.

        Entrada:
        - usa os atributos do objeto (`self`) para construir o documento do livro

        Saída:
        - retorna o `_id` do documento inserido (ObjectId) em caso de sucesso
        - ou lança/propaga exceção em caso de erro
        """
        dados_livro = {
            'titulo': self.titulo,
            'preco': Decimal128(Decimal(str(self.preco))),
            'categoria': self.categoria,
            'tags': self.tags,
            'autores': self.autores,
            'mais_recente_edicao': self.mais_recente_edicao,
            'numero_autores': self.numero_autores,
            'data_publicacao': parse_date(self.data_publicacao),
            'editora': self.editora,
            'descricao': self.descricao,
            'isbn': self.isbn,
            'estoque': self.estoque,
            'imagem_capa': self.imagem_capa,
        }

        resultado = livros.insert_one(dados_livro)

        return resultado.inserted_id

    @staticmethod
    def buscar_por_id(id_livro):
        """
        Buscar um livro pelo seu ID.

        Entrada:
        - `id_livro`: string (hex) ou `ObjectId` representando o `_id` do documento

        Saída:
        - dicionário com os dados do livro, ou `None` se não encontrado

        Orientações:
        - Coonverter `id_livro` para `ObjectId` quando necessário.
        - Utilizar `db.livrs.find_one({"_id": ObjectId(id_livro)})`.
        - Tratar possíveis exceções de conversão/consulta.
        """
        pass

    @staticmethod
    def buscar_todos():
        """
        Retornar todos os livros.

        Entrada: nenhuma

        Saída:
        - lista de documentos (cada item é um dicionário representando um livro)

        Orientações:
        - Usar `livros.find()` e converter o cursor em lista.
        """
        pass

    @staticmethod
    def buscar_livros(filtros=None, pagina=1, por_pagina=12):
        """
        Buscar livros aplicando filtros e paginação.

        Entrada:
        - `filtros`: dicionário de filtros MongoDB (opcional)
        - `pagina`: número da página (inteiro, 1-based)
        - `por_pagina`: número de itens por página (inteiro)

        Saída:
        - tupla `(resultado, total)` onde `resultado` é a lista de documentos da página e `total` é o número total de documentos que satisfazem os filtros

        Orientações:
        - Calcular `skip = (pagina - 1) * por_pagina`.
        - Aplicar `.find(filtros).sort(...).skip(skip).limit(por_pagina)` para paginação.
        - Usar `count_documents(filtros)` para obter o total.
        - Validar os parâmetros de entrada (p.ex. pagina >= 1).
        """
        pass

    @staticmethod
    def categorias_disponiveis():
        """
        Retornar a lista de categorias distintas existentes nos documentos.

        Entrada: nenhuma

        Saída:
        - lista de strings com categorias

        Orientações:
        - Utilizar `db.livros.distinct("categoria")`.
        """
        pass

    @staticmethod
    def tags_disponiveis():
        """
        Retornar tags distintas (assumindo que `tags` é uma lista em cada documento).

        Entrada: nenhuma

        Saída:
        - lista de strings com tags únicas

        Orientações:
        - Utilizar um pipeline de agregação com `$unwind` em `tags` seguido de `$group` para obter valores distintos.
        """
        pass


class Usuario:
    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = senha  # Importante: criptografar antes de salvar!

    def salvar(self):
        """
        Salvar o usuário no banco de dados.

        Entrada:
        - usa os atributos do objeto (`self`) para construir o documento do usuário

        Saída:
        - retorna o `_id` do documento inserido (ObjectId) em caso de sucesso
        - ou lança/propaga exceção em caso de erro
        """
        pass

    @staticmethod
    def buscar_por_email(email):
        """
        Buscar usuário por email.

        Entrada:
        - `email`: string

        Saída:
        - dicionário com os dados do usuário ou `None` se não encontrado
        """
        pass

    @staticmethod
    def buscar_por_id(id_usuario):
        """
        Buscar usuário por ID.

        Entrada:
        - `id_usuario`: string (hex) ou `ObjectId`

        Saída:
        - dicionário com os dados do usuário ou `None` se não encontrado
        """
        pass


class Pedido:
    def __init__(self, id_usuario, livros, data, total, status="pendente"):
        self.id_usuario = id_usuario
        self.livros = livros  # lista de dicionários com id_livro, quantidade, preco
        self.data = data  # data do pedido (ex: datetime.now())
        self.total = total
        self.status = status

    def salvar(self):
        """
        Salvar o pedido no banco de dados.

        Entrada:
        - usa os atributos do objeto (`self`) para construir o documento do pedido

        Saída:
        - retorna o `_id` do documento inserido (ObjectId) em caso de sucesso
        - ou lança/propaga exceção em caso de erro
        """
        pass

    @staticmethod
    def buscar_por_usuario(id_usuario):
        """
        Buscar pedidos de um usuário.

        Entrada:
        - `id_usuario`: string (hex) ou `ObjectId`

        Saída:
        - lista de documentos (pedidos) pertencentes ao usuário
        """
        pass

    @staticmethod
    def buscar_por_id(id_pedido):
        """
        Buscar pedido por ID.

        Entrada:
        - `id_pedido`: string (hex) ou `ObjectId`

        Saída:
        - dicionário com os dados do pedido ou `None` se não encontrado
        """
        pass
