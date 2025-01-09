import os

from flask import Flask

from src.config.sparql_wrapper_config import SPARQLWrapperConfig
from src.controllers.ontology_controller import OntologyController
from src.controllers.preferences_controller import PreferencesController
from src.controllers.search_controller import SearchController
from src.controllers.user_controller import UserController
from src.repositories.ontology_repository import OntologyRepository
from src.repositories.users_repository import UserManagementRepository
from src.services.ontology_service import OntologyService
from src.services.parsing_service import ParsingService
from src.services.preferences_service import PreferencesService
from src.services.user_service import UserService
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.mailersend.net'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_MAX_EMAILS'] = 5
app.config['MAIL_ASCII_ATTACHMENTS'] = False

sparql_endpoint = os.getenv('SPARQL_ENDPOINT')
sparql_config = SPARQLWrapperConfig(sparql_endpoint)
ontology_repository = OntologyRepository(sparql_config)

DATABASE_URL = "postgresql+psycopg2" + os.getenv('DATABASE_URL')[8:]
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
user_repository = UserManagementRepository(Session)
user_service = UserService(app, user_repository, os.getenv('SECRET'))

parsing_controller = SearchController(app, ParsingService(ontology_repository), user_service)
ontology_controller = OntologyController(app, OntologyService(ontology_repository))
users_controller = UserController(app, user_service)
preferences_controller = PreferencesController(app, PreferencesService(user_repository), user_service)

if __name__ == '__main__':
    app.run()
