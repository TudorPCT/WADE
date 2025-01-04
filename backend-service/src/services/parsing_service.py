from src.config.sparql_wrapper_config import SPARQLWrapperConfig
from src.repositories.ontology_repository import OntologyRepository
from src.services.ontology_service import OntologyQueryService


class ParsingService:
    def __init__(self, sparql_endpoint):
        self.sparql_config = SPARQLWrapperConfig(sparql_endpoint)
        self.repository = OntologyRepository(self.sparql_config)
        self.query_service = OntologyQueryService(self.repository)

    def process_user_input(self, user_input):
        rdf_type, filters = self.query_service.parse_query(user_input)

        if not rdf_type:
            return

        query = self.query_service.build_sparql_query(rdf_type, filters)
        results = self.repository.execute_query(query)

        return results

    def start(self):
        print("Welcome to the ontology query tool!")
        while True:
            user_input = input("Enter your query (e.g., 'show all frameworks for java'): ")
            self.process_user_input(user_input)
