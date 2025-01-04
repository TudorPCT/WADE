from SPARQLWrapper import SPARQLWrapper, JSON


class SPARQLWrapperConfig:
    def __init__(self, endpoint):
        self.endpoint = endpoint

    def get_sparql_instance(self):
        sparql = SPARQLWrapper(self.endpoint)
        return sparql
