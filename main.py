import pickle

from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField
from wtforms.validators import DataRequired

# criar um modelo para categoria, criar um form para categoria e um template para pesquisar categoria.
# utilizar o modelo, o form, o template e a rota de produto como exemplo.

db = SQLAlchemy()
app = Flask(__name__)
user = 'pedidos_app'
pwd = '#12345'
host = 'localhost'
banco = 'pedidos'
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql://{user}:{pwd}@{host}/{banco}"
app.config['SECRET_KEY'] = 'palavra dificil de advinhar'
db.init_app(app)


class CustomFlaskForm(FlaskForm):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def is_any_filled(self):
        """
        Gera um dicionario com os campos e respectivos valores preenchidos em um formulário
        :return:
        """
        return {key: value for key, value in self.data.items() if value and key not in ('submit', 'csrf_token')}

    def fill_form(self, dados):
        """
        Pega um dicionario de dados passado por parâmetros e preenche o formularios em seus respectivos campos.
        :param dados:
        :return:
        """
        for key, value in dados.items():
            class_attribute = getattr(self, key, None)
            if class_attribute:
                class_attribute.data = value


class ProdutoForm(CustomFlaskForm):
    id = StringField('id')
    cod_barras = StringField('Cód. Barras', validators=[DataRequired()])
    ds_produto = StringField('Descrição')
    categoria_id = StringField('Categoria')
    submit = SubmitField('Pesquisar')


class Cliente(db.Model):
    __tablename__ = 'cliente'
    id = db.Column(db.Integer, primary_key=True)
    cpf = db.Column(db.String(11))
    nm_cliente = db.Column(db.String(200))

    @classmethod
    def buscar_cliente(cls, parametros):
        query = cls.query.order_by(cls.nm_cliente)
        for field_key, field_value in parametros.items():
            if field_key == 'id':
                query = query.filter(cls.id == field_value)
            elif field_key == 'cpf':
                query = query.filter(cls.cpf.like(f'%{field_value}%'))
            elif field_key == 'nm_cliente':
                query = query.filter(cls.nm_cliente.like(f'%{field_value}%'))

        return query


class Produto(db.Model):
    __tablename__ = 'produto'
    id = db.Column(db.Integer, primary_key=True)
    cod_barras = db.Column(db.String(15))
    ds_produto = db.Column(db.String(200))
    categoria_id = db.Column(db.Integer)


    @classmethod
    def buscar_produto(cls, parametros):
        query = cls.query.order_by(cls.ds_produto)
        for field_key, field_value in parametros.items():
            if field_key == 'id':
                query = query.filter(cls.id == field_value)
            elif field_key == 'cod_barras':
                query = query.filter(cls.cod_barras.like(f'%{field_value}%'))
            elif field_key == 'ds_produto':
                query = query.filter(cls.ds_produto.like(f'%{field_value}%'))
            elif field_key == 'categoria_id':
                query = query.filter(cls.categoria_id == field_value)

        return query


@app.route('/')
def index():
    return render_template('base.html')


@app.route('/produtos', methods=['GET', 'POST'])
def obter_produtos():
    param_pesquisa = 'param_pesquisa'
    form_produto = ProdutoForm()

    if form_produto.validate_on_submit():
        if form_produto.submit.raw_data[0].upper() == 'FECHAR':
            # apagando os dados de pesquisa q estão na sessão.
            session.pop(param_pesquisa, None)
            # indo para a página principal
            return redirect(url_for('index'))

        # é porque foi enviado um post
        # pega os dados do formulario (is_any_filled) e guarda na sessão no "formato string pickles".
        session[param_pesquisa] = pickle.dumps(form_produto.is_any_filled())
        return redirect(url_for('obter_produtos'))
    else:
        # pega da sessão a informação preenchida no formulário no "formato string pickles"
        campos_preenchidos = session.get(param_pesquisa, None)
        # se veio dados da sessão
        if campos_preenchidos:
            # pega a inforamação no "formato string pickles" e transforma num dicionário
            campos_preenchidos = pickle.loads(campos_preenchidos)

        if campos_preenchidos:
            # o dict não é vazio
            query = Produto.buscar_produto(campos_preenchidos)
            produtos = query.all()
            form_produto.fill_form(campos_preenchidos)
        else:
            # ainda não tem código de barras inserido na sessão
            produtos = Produto.query.all()

    return render_template('pesquisar_produtos.html',
                           header='Pesquisar Produtos',
                           dados=produtos,
                           form=form_produto)


@app.route('/cliente/<id_cliente>')
def obter_cliente(id_cliente):
    # faz um consulta no banco ao cliente com id = id_cliente
    user_agent = request.headers.get('User-Agent')
    query = Cliente.buscar_cliente({'id': id_cliente})
    # pega o primeiro objeto cliente retornado pelo banco (cada linha do banco vira um objeto do tipo cliente)
    cliente = query.first()
    # a variável cliente é um objeto do classe Cliente
    if cliente:
        html = f'id: {cliente.id} </br> nome: {cliente.nm_cliente} </br> cpf: {cliente.cpf}'
        return html
    else:
        return f'Cliente id:{id_cliente} não encontrado!!!!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
