from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField

db = SQLAlchemy()
app = Flask(__name__)
user = 'pedidos_app'
pwd = '#12345'
host = 'localhost'
banco = 'pedidos'
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql://{user}:{pwd}@{host}/{banco}"
app.config['SECRET_KEY'] = 'palavra dificil de advinhar'
db.init_app(app)


class ProdutoForm(FlaskForm):
    id = StringField('id')
    cod_barras = StringField('Cód. Barras')
    ds_produto = StringField('Descrição')
    categoria_id = StringField('Categoria')
    submit = SubmitField('Pesquisar')

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
    form_produto = ProdutoForm()
    if form_produto.validate_on_submit():
        parametros = {}

        if form_produto.id.data:
            parametros['id'] = form_produto.id.data
        if form_produto.ds_produto.data:
            parametros['ds_produto'] = form_produto.ds_produto.data
        if form_produto.cod_barras.data:
            parametros['cod_barras'] = form_produto.cod_barras.data
        if form_produto.categoria_id.data:
            parametros['categoria_id'] = form_produto.categoria_id.data
        query = Produto.buscar_produto(parametros)

        produtos = query.all()
    else:
        produtos = Produto.query.all()


    return render_template('pesquisar_produtos.html',
                           header='Pesquisar Produtos',
                           dados=produtos,
                           form=form_produto)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
