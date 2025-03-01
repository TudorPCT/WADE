from src.cache.cache import TTL_LRU_Cache
from src.config.sparql_wrapper_config import SPARQLWrapperConfig, JSON, TURTLE
from src.services.query_parser import QueryResultParser


class OntologyRepository:
    def __init__(self, sparql_config: SPARQLWrapperConfig):
        self.sparql = sparql_config.get_sparql_instance()
        self.cache = TTL_LRU_Cache()

    def execute_query(self, query, format=JSON):
        cached_results = self.cache.get(query)

        if not cached_results:
            self.sparql.setQuery(query)
            self.sparql.setReturnFormat(format)
            results = self.sparql.query().convert()
            self.cache.set(query, results)
        else:
            results = cached_results

        return results

    def get_classes_and_labels(self, format=JSON):
        query = """
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX owl:  <http://www.w3.org/2002/07/owl#>
        SELECT DISTINCT ?class ?label
        WHERE {
          ?class a owl:Class .
          OPTIONAL { ?class rdfs:label ?label . }
        }
        """
        results = self.execute_query(query, format)
        return QueryResultParser.parse_results(results, "class", "label", plural=True)

    def get_individuals_for_class(self, class_iri, format=JSON):
        query = f"""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT DISTINCT ?indiv ?label
        WHERE {{
          ?indiv a <{class_iri}> .
          OPTIONAL {{ ?indiv rdfs:label ?label . }}
        }}
        """
        results = self.execute_query(query, format)
        return QueryResultParser.parse_results(results, "indiv", "label")

    def get_object_properties_and_labels(self, format=JSON):
        query = """
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX owl:  <http://www.w3.org/2002/07/owl#>
        SELECT DISTINCT ?prop ?label
        WHERE {
          ?prop a owl:ObjectProperty .
          OPTIONAL { ?prop rdfs:label ?label . }
        }
        """
        results = self.execute_query(query, format)
        return QueryResultParser.parse_results(results, "prop", "label")

    def describe_input(self, input):
        query = f"""
        DESCRIBE <{input}>
        """
        return self.execute_query(query)

    def describe(self):
        query = """
        DESCRIBE ?s
        WHERE {
          ?s ?p ?o .
        }
        """
        return self.execute_query(query, format=TURTLE)
