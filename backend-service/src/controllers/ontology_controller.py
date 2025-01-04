from src.services.ontology_service import OntologyQueryService


class OntologyController:
    def __init__(self, ontology_service: OntologyQueryService):
        self.ontology_service = ontology_service



