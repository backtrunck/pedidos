from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Length


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


class CategoriaForm(CustomFlaskForm):
    id = StringField('id')
    ds_categoria = StringField('Descrição')
    submit = SubmitField('Pesquisar')


class ProdutoForm(CustomFlaskForm):
    id = StringField('id')
    # validators=[DataRequired()]
    cod_barras = StringField('Cód. Barras', validators=[Length(max=15)])
    ds_produto = StringField('Descrição')
    categoria_id = StringField('Categoria')
    submit = SubmitField('Pesquisar')


class ClienteForm(CustomFlaskForm):
    id = StringField('id')
    # validators=[DataRequired()]
    cpf = StringField('cpf')
    nm_cliente = StringField('nm_cliente')
    submit = SubmitField('Pesquisar')
