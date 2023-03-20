import pickle
from flask import current_app, flash, make_response, redirect, render_template, session, url_for


from app.main import main
from app.main.forms import CategoriaForm, ProdutoForm, ClienteForm
from app.models import Categoria, Cliente, Produto

PAGES = 3


@main.route('/')
def index():
    pagina_atual = 'index'
    # a requisição está vindo de uma página diferente?????
    if session.get('pagina_atual', None) != pagina_atual:
        session['pagina_atual'] = pagina_atual

    return render_template('base.html')


@main.route('/produtos', defaults={'page': 1}, methods=('post', 'get'))
@main.route('/produtos/<int:page>')
def obter_produto(page):
    resposta = pesquisar('param_pesquisa',
                         'obter_produtos',
                         'main.obter_produto',
                         ProdutoForm(),
                         Produto,
                         'pesquisar_produto.html',
                         'Pesquisar Produto',
                         page,
                         3,
                         'produtos',
                         16000)
    return resposta


@main.route('/categoria', defaults={'page': 1}, methods=('post', 'get'))
@main.route('/categoria/<int:page>')
# @app.route('/categoria', methods=['GET', 'POST'])
def obter_categoria(page):
    resposta = pesquisar('param_pesquisa',
                         'obter_categoria',
                         'main.obter_categoria',
                         CategoriaForm(),
                         Categoria,
                         'pesquisar_categoria.html',
                         'Pesquisar Categoria',
                         page,
                         3,
                         'categorias',
                         16000)
    return resposta


@main.route('/cliente', defaults={'page': 1}, methods=('post', 'get'))
@main.route('/cliente/<int:page>')
def obter_cliente(page):

    resposta = pesquisar('param_pesquisa',
                         'obter_cliente',
                         'main.obter_cliente',
                         ClienteForm(),
                         Cliente,
                         'pesquisar_cliente.html',
                         'Pesquisar Cliente',
                         page,
                         3,
                         'clientes',
                         16000)
    return resposta

def pesquisar(param_pesquisa,
              pagina_atual,
              rota,
              form,
              modelo,
              nome_template,
              titulo,
              page,
              itens_per_pages,
              file_name,
              qt_itens_max):

    # param_pesquisa = 'param_pesquisa'
    # pagina_atual = 'obter_categoria'
    # form = CategoriaForm()

    if session.get('pagina_atual', None) != pagina_atual:
        session.pop(param_pesquisa, None)
        session['pagina_atual'] = pagina_atual

    if form.validate_on_submit():
        if form.submit.raw_data[0].upper() == 'FECHAR':
            # apagando os dados de pesquisa q estão na sessão.
            session.pop(param_pesquisa, None)
            # indo para a página principal
            return redirect(url_for('main.index'))  # é porque foi enviado um post
        if form.submit.raw_data[0].upper() == 'EXCEL':
            session['button_excel'] = 'S'
            # é porque foi enviado um post
            # pega os dados do formulario (is_any_filled) e guarda na sessão no "formato string pickles".
        session[param_pesquisa] = pickle.dumps(form.is_any_filled())
        return redirect(url_for(rota))

    else:
        excel = False
        # se clicou no botão excel
        if session.get('button_excel', None) == 'S':
            excel = True
            # limpando a sesão
            session.pop('button_excel', None)

        # pega da sessão a informação preenchida no formulário no "formato string pickles"
        campos_preenchidos = session.get(param_pesquisa, None)
        # se veio dados da sessão
        if campos_preenchidos:
            # pega a inforamação no "formato string pickles" e transforma num dicionário
            campos_preenchidos = pickle.loads(campos_preenchidos)

        if campos_preenchidos:
            # o dict não é vazio
            query = modelo.buscar(campos_preenchidos)
            form.fill_form(campos_preenchidos)
        else:
            query = modelo.query

        paginacao = query.paginate(page=page, per_page=itens_per_pages)
        # a pesquisa retornou dados?
        if paginacao.pages == 0:
            flash('Não foram encontrados contratos para esta pesquisa.')
            dados = []
            return render_template(nome_template,
                                   header=titulo,
                                   dados=dados,
                                   form=form,
                                   paginacao=paginacao)
        else:
            qt_itens = itens_per_pages
            if paginacao.pages > 1:
                qt_itens = itens_per_pages * (paginacao.pages - 1)
            dados = paginacao.items

        if excel:
            if qt_itens > qt_itens_max:
                flash('Arquivo muito grande, restrinja a pesquisa.')
            else:
                content = modelo.gerar_xlsx(campos_preenchidos, query)
                response = make_response(content)
                response.headers['Content-Disposition'] = f'attachment; filename={file_name}.xlsx'
                response.headers['Content-type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                return response

    return render_template(nome_template,
                           header=titulo,
                           dados=dados,
                           form=form,
                           paginacao=paginacao)