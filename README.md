Loja de Livros — Orientações para Alunos
=====================================

Visão geral
-----------

Este repositório é uma atividade prática para o curso Superior de Sistemas para Internet.
Os alunos devem:
- Criar um cluster no MongoDB Atlas.
- Configurar a variável de ambiente `MONGO_URI` em `.env`.
- Testar a conexão com `banco/teste_conexao.py`.
- Popular o banco com `banco/popula_banco.py`.
- Rodar a aplicação Flask (`app.py`).
- Implementar os métodos marcados com `pass` em `models.py` para que as páginas funcionem corretamente.

Pré-requisitos
--------------

- Python 3.8+ instalado
- Conta no MongoDB Atlas (gratuita serve para a atividade)
- Recomenda-se criar um ambiente virtual

Instalação local
----------------

1. Criar e ativar um ambiente virtual (Windows):

```powershell
python -m venv venv
venv\Scripts\activate
```

Em Unix/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Instalar dependências:

```bash
pip install -r requirements.txt
```

Configurar o MongoDB Atlas
--------------------------

1. Acesse https://www.mongodb.com/atlas e crie uma conta.
2. Crie um cluster grátis (Shared Cluster).
3. Em "Database Access" crie um usuário (username + password).
4. Em "Network Access" permita o acesso do seu IP (ou use 0.0.0.0/0 para liberação total em laboratório).
5. Em "Clusters" clique em "Connect" → "Connect your application" → selecione driver Python e copie a connection string.

Exemplo de connection string (template):

```
mongodb+srv://<usuario>:<senha>@<cluster>.mongodb.net/<nome_do_banco>?retryWrites=true&w=majority
```

Editar o arquivo `.env`
-----------------------

No arquivo `.env` (na raiz do projeto) substitua pelos seus valores:

- `MONGO_URI`: a connection string do Atlas (substitua `<usuario>`, `<senha>`, `<cluster>` e `<nome_do_banco>`).
- `SECRET_KEY`: uma string aleatória para o Flask.

O repositório já contém um `.env` de exemplo com placeholders.

Testar conexão com o Atlas
-------------------------

Execute:

```bash
python banco/teste_conexao.py
```

Se der certo, verá uma mensagem de sucesso e a lista de bancos de dados disponíveis.

Popular o banco com dados de exemplo
-----------------------------------

Para carregar os livros de exemplo no Atlas execute:

```bash
python banco/popula_banco.py
```

Isso irá inserir documentos na coleção `livros` do banco `livraria`.

Rodar a aplicação
-----------------

```bash
python app.py
```

Acesse http://127.0.0.1:5000 no navegador.

Implementação em `models.py`
---------------------------

O arquivo `models.py` contém classes com métodos marcados com `pass` que vocês devem implementar.
Os métodos principais são (arquivo: [models.py](models.py)):

- `Livro.salvar()`
- `Livro.buscar_por_id(id_livro)`
- `Livro.buscar_todos()`
- `Livro.buscar_livros(filtros=None, pagina=1, por_pagina=12)`
- `Livro.categorias_disponiveis()`
- `Livro.tags_disponiveis()`
- `Usuario.salvar()`
- `Usuario.buscar_por_email(email)`
- `Usuario.buscar_por_id(id_usuario)`
- `Pedido.salvar()`
- `Pedido.buscar_por_usuario(id_usuario)`
- `Pedido.buscar_por_id(id_pedido)`

Dicas e exemplos de implementação
---------------------------------

1) Conversão de IDs

Quando métodos recebem IDs vindos de templates, APIs ou sessions, converta para `ObjectId` de forma robusta. Exemplo genérico para um sistema com `Produto`:

```python
from bson.objectid import ObjectId

def _to_objectid(id_entrada):
    try:
        return ObjectId(id_entrada) if not isinstance(id_entrada, ObjectId) else id_entrada
    except Exception:
        return None

# Uso em Produto.buscar_por_id
oid = _to_objectid(id_entrada)
if oid is None:
    return None
```

2) Campos numéricos e `Decimal128`

Em aplicações que armazenam preços ou valores monetários, use `Decimal128` para evitar erros de ponto flutuante. Exemplo genérico para um campo `preco` em `Produto`:

```python
from bson.decimal128 import Decimal128
from decimal import Decimal

def _to_decimal128(valor):
    return Decimal128(Decimal(str(valor)))

doc = {'nome': produto.nome, 'preco': _to_decimal128(produto.preco)}
```

3) Exemplo de busca paginada (genérico)

Uma função de listagem paginada para qualquer coleção (`produtos`, `items`, etc.):

```python
def buscar_paginado(col, filtros=None, pagina=1, por_pagina=20):
    filtros = filtros or {}
    pagina = max(int(pagina), 1)
    por_pagina = int(por_pagina)
    skip = (pagina - 1) * por_pagina

    total = col.count_documents(filtros)
    cursor = col.find(filtros).skip(skip).limit(por_pagina)
    return (list(cursor), total)
```

4) Exemplo de salvar usuário com hash de senha (genérico)

Armazene senhas apenas em forma de hash. Exemplo para um modelo `Cliente`:

```python
import bcrypt

def salvar_cliente(cliente, colecao_clientes):
    hashed = bcrypt.hashpw(cliente.senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    doc = {'nome': cliente.nome, 'email': cliente.email, 'senha': hashed}
    res = colecao_clientes.insert_one(doc)
    return res.inserted_id
```

5) Exemplo de busca de recursos relacionados (genérico)

Buscar documentos relacionados por referência (ex.: `Pedido` por `cliente_id`):

```python
def buscar_pedidos_por_cliente(colecao_pedidos, id_cliente):
    try:
        oid = ObjectId(id_cliente) if not isinstance(id_cliente, ObjectId) else id_cliente
    except Exception:
        return []
    return list(colecao_pedidos.find({'cliente_id': oid}))
```

6) Boas práticas

- Trate exceções ao converter `ObjectId` e valide inputs.
- Converta tipos antes de enviar para o banco (ex.: `Decimal128` para valores monetários).
- Mantenha a lógica de acesso ao banco separada das rotas/controllers.
- Documente expectativas de tipos e formatos nos métodos do modelo.

Boa prática: nunca comitem credenciais reais no repositório. O `.env` do repositório contém apenas exemplos.
