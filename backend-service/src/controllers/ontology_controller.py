from src.services.ontology_service import OntologyService
from flask import request
from SPARQLWrapper import TURTLE
from SPARQLWrapper.SPARQLExceptions import QueryBadFormed


class OntologyController:
    def __init__(self, app, ontology_service: OntologyService):
        self.ontology_service = ontology_service
        self.app = app
        self.register_routes()

    def register_routes(self):

        @self.app.route("/software-ontology", methods=["GET"])
        def describe():
            if request.args.get('fragment') is None:
                return self.ontology_service.describe()
            else:
                result = self.ontology_service.describe_input(request.base_url + "#" + request.args.get('fragment'))
                if not result:
                    return "", 204
                return result

        @self.app.route("/software-ontology/query", methods=["POST"])
        def query():
            data = request.json
            query = data.get("query")

            if not query:
                return "", 400
            try:
                results = self.ontology_service.execute_query(query, format=TURTLE)
            except QueryBadFormed as e:
                return "", 400

            if not results:
                return "", 204

            return results


