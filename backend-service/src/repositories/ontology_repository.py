from src.config.sparql_wrapper_config import SPARQLWrapperConfig, JSON
from src.services.query_parser import QueryResultParser


class OntologyRepository:
    def __init__(self, sparql_config: SPARQLWrapperConfig):
        self.sparql = sparql_config.get_sparql_instance()

    def execute_query(self, query):
        self.sparql.setQuery(query)
        self.sparql.setReturnFormat(JSON)
        return self.sparql.query().convert()

    def get_classes_and_labels(self):
        query = """
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX owl:  <http://www.w3.org/2002/07/owl#>
        SELECT DISTINCT ?class ?label
        WHERE {
          ?class a owl:Class .
          OPTIONAL { ?class rdfs:label ?label . }
        }
        """
        results = self.execute_query(query)
        return QueryResultParser.parse_results(results, "class", "label", plural=True)

    def get_individuals_for_class(self, class_iri):
        query = f"""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT DISTINCT ?indiv ?label
        WHERE {{
          ?indiv a <{class_iri}> .
          OPTIONAL {{ ?indiv rdfs:label ?label . }}
        }}
        """
        results = self.execute_query(query)
        return QueryResultParser.parse_results(results, "indiv", "label")

    def get_object_properties_and_labels(self):
        query = """
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX owl:  <http://www.w3.org/2002/07/owl#>
        SELECT DISTINCT ?prop ?label
        WHERE {
          ?prop a owl:ObjectProperty .
          OPTIONAL { ?prop rdfs:label ?label . }
        }
        """
        results = self.execute_query(query)
        return QueryResultParser.parse_results(results, "prop", "label")
