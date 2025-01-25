from src.services.ontology_query_service import OntologyQueryService


class ParsingService:
    def __init__(self, repo):
        self.repository = repo
        self.query_service = OntologyQueryService(self.repository)

    def process_user_input(self, user_input):
        rdf_type, filters = self.query_service.parse_query(user_input)

        if not rdf_type:
            return

        query = self.query_service.build_sparql_query(rdf_type, filters)

        results = self.repository.execute_query(query)

        return results
