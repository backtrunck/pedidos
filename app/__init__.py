from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import config

db = SQLAlchemy()


def create_app(ambiente):
    # criando a aplicação flask
    app = Flask(__name__)
    # configurando a aplicação
    app.config.from_object(config[ambiente])
    config[ambiente].init_app(app)
    # iniciando o BD
    db.init_app(app)

    # Registrando o blueprint principal
    from app.main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    # retornando a aplicação flask
    return app



