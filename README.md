# Pedidos

## Para instalar
1. Clonar o repositório: git clone git@github.com:backtrunck/pedidos.git
2. Entra na pasta: cd pedidos
3. Criar ambiente virtual: python3 -m venv .venv_pedidos
4. Ativar ambiente virtual: source .venv_pedidos/bin/activate(linux), <br>
 .venv_pedidos/Scripts/activate (windows)
5. Instalar bibliotecas python: pip install -r requirements.txt

## Banco de Dados 
1. Usar os scripts na pasta sql para criar o banco de dados (mysql)
2. Executar na ordem create_database_pedidos.sql e inserts_modelo_pedidos.sql
3. Deve ser criado um usuario para a aplicação com permissões de select, update, insert e delete no banco
4. No script main.py alterar as variáveis user (usuario criado no item 3), pwd (idem item 3), host e banco com os valores apropriados 
para acessar o banco.

