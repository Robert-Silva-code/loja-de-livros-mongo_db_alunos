from decimal import Decimal
from bson import Decimal128
from flask import Flask, render_template, request, redirect, url_for, flash, session
from forms import LoginForm, CadastroForm, ContatoForm, BuscaForm, RecoveryPasswordForm
from models import Livro, Usuario, Pedido
from bson.objectid import ObjectId
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or "uma_chave_secreta_muito_segura"


# Rota principal
@app.route("/")
def index():
    busca_form = BuscaForm()
    todos_livros = Livro.buscar_todos() or []
    livros_destaque = todos_livros[:4]  # Exemplo: 4 livros em destaque
    return render_template("index.html", livros=livros_destaque, form=busca_form)


# Rota de busca
@app.route("/buscar")
def buscar():
    pagina = int(request.args.get("pagina", 1))
    nome = request.args.get("nome", "")
    preco_min = request.args.get("preco_min", None)
    preco_max = request.args.get("preco_max", None)
    categorias = request.args.getlist("categorias")
    tags_include = request.args.getlist("tags_include")
    tags_exclude = request.args.getlist("tags_exclude")

    form = BuscaForm()
    por_pagina = 12

    # Monta os filtros para a busca
    filtros = {}
    if nome:
        filtros["titulo"] = {"$regex": nome, "$options": "i"}
    if preco_min:
        filtros["preco"] = {"$gte": Decimal128(Decimal(preco_min))}
    if preco_max:
        filtros.setdefault("preco", {})["$lte"] = Decimal128(Decimal(preco_max))
    if categorias:
        filtros["categoria"] = {"$in": categorias}
    if tags_include:
        filtros["tags"] = {"$all": tags_include}
    # Número de autores (exemplo: se for um filtro de igualdade)
    # if form.num_autores.data:
    #     filtros['numero_autores'] = int(form.num_autores.data)

    # Busca paginada via modelo (com fallback caso o método retorne None)
    res = Livro.buscar_livros(filtros, pagina, por_pagina)
    if isinstance(res, tuple) and len(res) == 2:
        livros, total = res
        livros = livros or []
        total = int(total or 0)
    else:
        livros = res or []
        total = len(livros)
    total_paginas = (total // por_pagina) + (1 if total % por_pagina > 0 else 0)

    # Preenche o form com os valores dos filtros (para manter estado)
    if request.method == "POST":
        form.process(request.form)

    categorias = Livro.categorias_disponiveis() or []
    tags = Livro.tags_disponiveis() or []

    return render_template(
        "catalogo.html",
        livros=livros,
        form=form,
        pagina=pagina,
        total_paginas=total_paginas,
        categorias=categorias,
        tags=tags,
    )


# Página do livro
@app.route("/livro/<id_livro>")
def livro(id_livro):
    livro = Livro.buscar_por_id(id_livro)
    if not livro:
        flash("Livro não encontrado!", "error")
        return redirect(url_for("index"))
    return render_template("livro.html", livro=livro)


# Páginas institucionais
@app.route("/sobre")
def sobre():
    return render_template("about.html")


@app.route("/contato", methods=["GET", "POST"])
def contato():
    form = ContatoForm()
    if request.method == "POST" and form.validate_on_submit():
        # TODO: Enviar e-mail ou salvar mensagem
        flash("Mensagem enviada com sucesso!", "success")
        return redirect(url_for("contato"))
    return render_template("contato.html", form=form)


@app.route("/faq")
def faq():
    return render_template("faq.html")


# Autenticação
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        usuario = Usuario.buscar_por_email(form.email.data)
        # TODO: Validar senha (usando bcrypt)
        if usuario:  # Exemplo: sem validação de senha
            session["user_id"] = str(usuario["_id"])
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for("index"))
        flash("E-mail ou senha inválidos!", "error")
    return render_template("login.html", form=form)


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    form = CadastroForm()
    if request.method == "POST" and form.validate_on_submit():
        if form.senha.data != form.confirmar_senha.data:
            flash("As senhas não coincidem!", "error")
        else:
            # TODO: Criptografar senha antes de salvar
            usuario = Usuario(
                nome=form.nome.data, email=form.email.data, senha=form.senha.data
            )
            usuario.salvar()
            flash("Cadastro realizado com sucesso!", "success")
            return redirect(url_for("login"))
    return render_template("register.html", form=form)


@app.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("Você saiu da sua conta.", "info")
    return redirect(url_for("index"))


# Área do cliente
@app.route("/minha-conta")
def minha_conta():
    if "user_id" not in session:
        flash("Faça login para acessar sua conta.", "warning")
        return redirect(url_for("login"))
    pedidos = Pedido.buscar_por_usuario(session["user_id"]) or []
    return render_template("conta.html", pedidos=pedidos)


@app.route("/recuperar-senha", methods=["GET", "POST"])
def recuperar_senha():
    form = RecoveryPasswordForm()
    if form.validate_on_submit():
        # Aqui você processa o e-mail, gera o link, envia e-mail, etc.
        flash(
            "Se o e-mail estiver cadastrado, você receberá um link para redefinir sua senha.",
            "success",
        )
        return redirect(url_for("login"))
    return render_template("recovery_password.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
