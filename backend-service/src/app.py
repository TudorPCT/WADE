import os

from flask import Flask
from flask_cors import CORS

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from src.config.sparql_wrapper_config import SPARQLWrapperConfig
from src.controllers.ontology_controller import OntologyController
from src.controllers.preferences_controller import PreferencesController
from src.controllers.search_controller import SearchController
from src.controllers.user_controller import UserController
from src.repositories.ontology_repository import OntologyRepository
from src.repositories.preferences_repository import PreferencesRepository
from src.repositories.users_repository import UserManagementRepository
from src.services.ontology_service import OntologyService
from src.services.parsing_service import ParsingService
from src.services.preferences_service import PreferencesService
from src.services.user_service import UserService
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
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
preferences_controller = PreferencesController(app, PreferencesService(PreferencesRepository(Session)), user_service)

scheduler = BackgroundScheduler()
scheduler.add_job(user_service.delete_unactivated_users, CronTrigger(hour=0, minute=1))
scheduler.start()

if __name__ == '__main__':
    try:
        app.run()
    finally:
        scheduler.shutdown()
