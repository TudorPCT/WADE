from flask import Flask

from src.config.sparql_wrapper_config import SPARQLWrapperConfig
from src.controllers.ontology_controller import OntologyController
from src.controllers.parsing_controller import ParsingController
from src.repositories.ontology_repository import OntologyRepository
from src.services.ontology_service import OntologyService
from src.services.parsing_service import ParsingService

app = Flask(__name__)

sparql_endpoint = "http://localhost:3030/software-ontology/query"
sparql_config = SPARQLWrapperConfig(sparql_endpoint)
repository = OntologyRepository(sparql_config)

parsing_controller = ParsingController(app, ParsingService(repository))
ontology_controller = OntologyController(app, OntologyService(repository))

if __name__ == '__main__':
    app.run()
