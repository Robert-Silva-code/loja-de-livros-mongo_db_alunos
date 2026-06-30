from flask_wtf import FlaskForm
from wtforms import (
    StringField, IntegerField, SelectMultipleField, RadioField,
    BooleanField, SubmitField, PasswordField, TextAreaField, DateField
)
from wtforms.widgets import ListWidget, CheckboxInput
from wtforms.validators import DataRequired, Email, Length, Optional

class LoginForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(min=6)])
    lembrar = BooleanField('Lembrar de mim')
    submit = SubmitField('Entrar')

class CadastroForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(min=6)])
    confirmar_senha = PasswordField('Confirmar Senha', validators=[DataRequired()])
    submit = SubmitField('Cadastrar')

class RecoveryPasswordForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    submit = SubmitField('Enviar link de recuperação')
    
class ContatoForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    mensagem = TextAreaField('Mensagem', validators=[DataRequired(), Length(min=10, max=500)])
    submit = SubmitField('Enviar')

class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()

class BuscaForm(FlaskForm):
    # EQUAL - Nome do livro
    nome = StringField('Nome do Livro', validators=[Optional()])
    
    # GREATER/LESS - Preço
    preco_min = IntegerField('Preço Mínimo', validators=[Optional()])
    preco_max = IntegerField('Preço Máximo', validators=[Optional()])
    
    # IN/NIN - Categorias
    categorias = SelectMultipleField('Categorias',
        choices=[
            ('Literatura Clássica', 'Literatura Clássica'),
            ('Ficção Científica', 'Ficção Científica'),
            ('Romance', 'Romance'),
            ('Terror', 'Terror'),
            ('Biografia', 'Biografia')
        ],
        default=[],
        validators=[Optional()])
    categoria_tipo = RadioField('Tipo de filtro de categoria',
        choices=[
            ('incluir', 'Incluir categorias'),
            ('excluir', 'Excluir categorias')
        ],
        default='incluir')
    
    # EXISTS - Mais recente edição
    mais_recente = BooleanField('Apenas edições mais recentes', validators=[Optional()])
    
    # ALL - Tags (usando MultiCheckboxField)
    tags = MultiCheckboxField('Tags',
        choices=[
            ('romance', 'Romance'),
            ('literatura brasileira', 'Literatura Brasileira'),
            ('século XIX', 'Século XIX'),
            ('ficção', 'Ficção'),
            ('clássico', 'Clássico')
        ],
        validators=[Optional()])
    
    # SIZE - Número de autores
    num_autores = RadioField('Número de autores',
        choices=[
            ('1', '1 autor'),
            ('2', '2 autores'),
            ('3', '3+ autores')
        ],
        validators=[Optional()])
    
    submit = SubmitField('Buscar')

# Exemplo de formulário para adicionar/editar livro (opcional)
class LivroForm(FlaskForm):
    titulo = StringField('Título', validators=[DataRequired(), Length(min=2, max=200)])
    preco = StringField('Preço', validators=[DataRequired()])
    categoria = StringField('Categoria', validators=[DataRequired()])
    tags = StringField('Tags (separadas por vírgula)', validators=[Optional()])
    autores = StringField('Autores (separados por vírgula)', validators=[Optional()])
    mais_recente_edicao = BooleanField('Edição mais recente', validators=[Optional()])
    numero_autores = IntegerField('Número de autores', validators=[Optional()])
    data_publicacao = DateField('Data de publicação', format='%Y-%m-%d', validators=[Optional()])
    editora = StringField('Editora', validators=[Optional()])
    descricao = TextAreaField('Descrição', validators=[DataRequired()])
    isbn = StringField('ISBN', validators=[Optional()])
    estoque = IntegerField('Estoque', validators=[Optional()])
    imagem_capa = StringField('Imagem da capa (URL)', validators=[Optional()])
    submit = SubmitField('Salvar')
