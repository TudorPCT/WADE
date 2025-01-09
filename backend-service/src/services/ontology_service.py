import json

from src.repositories.ontology_repository import OntologyRepository, JSON


class OntologyService:
    def __init__(self, repository: OntologyRepository):
        self.repository = repository

    def describe_input(self, input):
        graph = self.repository.describe_input(input)

        if not graph:
            return None

        result = []
        for s, p, o in graph:
            result.append({
                "subject": str(s),
                "predicate": str(p),
                "object": str(o)
            })

        return result

    def describe(self):
        return self.repository.describe()

    def execute_query(self, query, format=JSON):
        return self.repository.execute_query(query, format)
