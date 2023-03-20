import configparser
import os

default = 'DEFAULT'
desenv = 'desenvolvimento'
prod = 'producao'

basedir = os.path.relpath(os.path.dirname(__file__))

file_config = configparser.ConfigParser()
file_config.read(os.path.join(basedir, '.local_settings.cfg'))


class Config:
    PAGES = file_config[desenv]['PAGES']
    SECRET_KEY = file_config[default]['SECRET_KEY']
    USER = file_config[default]['USER']
    PWD = file_config[default]['PWD']
    HOST = file_config[default]['HOST']
    BANCO = file_config[default]['BANCO']
    SQLALCHEMY_DATABASE_URI = f"mysql://{USER}:{PWD}@{HOST}/{BANCO}"

    @staticmethod
    def init_app(app):
        pass


class DesenvolvimentoConfig(Config):
    PAGES = file_config[desenv]['PAGES']
    USER = file_config[desenv]['USER']
    PWD = file_config[desenv]['PWD']
    HOST = file_config[desenv]['HOST']
    BANCO = file_config[desenv]['BANCO']
    SQLALCHEMY_DATABASE_URI = f"mysql://{USER}:{PWD}@{HOST}/{BANCO}"
    SECRET_KEY = file_config[desenv]['SECRET_KEY']


class ProducaoConfig(Config):
    PAGES = file_config[desenv]['PAGES']
    USER = file_config[prod]['USER']
    PWD = file_config[prod]['PWD']
    HOST = file_config[prod]['HOST']
    BANCO = file_config[prod]['BANCO']
    SQLALCHEMY_DATABASE_URI = f"mysql://{USER}:{PWD}@{HOST}/{BANCO}"
    SECRET_KEY = file_config[prod]['SECRET_KEY']


config = {
    default: Config,
    desenv: DesenvolvimentoConfig,
    prod: ProducaoConfig
}





