class OntologyQueryService:
    def __init__(self, repository):
        self.repository = repository

    def parse_query(self, user_text):
        words = user_text.lower().split()
        classes_map = self.repository.get_classes_and_labels()
        properties_map = self.repository.get_object_properties_and_labels()

        classes_map["class"] = "http://www.w3.org/2002/07/owl#Class"
        properties_map["subclassof"] = "http://www.w3.org/2000/01/rdf-schema#subClassOf"

        rdf_type_iri = next((classes_map[word] for word in words if word in classes_map), None)

        synonyms_bridge = {
            "for": "supportslanguage",
            "licensed under": "hassoftwarelicense",
            "depends on": "dependson",
            "supports": "supportslanguage",
            "classess": "class",
            "subclass": "subclassof",
            "subclasses": "subclassof",
        }

        for synonym, prop_label in synonyms_bridge.items():
            if synonym in words and prop_label in properties_map:
                idx = words.index(synonym)
                words[idx] = prop_label

        filters = []
        all_class_iris = list(classes_map.values())
        for idx, word in enumerate(words):
            if word in properties_map:
                property_iri = properties_map[word]
                if idx + 1 < len(words):
                    target_word = words[idx + 1]
                    found_iri = None
                    for ciri in all_class_iris:
                        individuals = self.repository.get_individuals_for_class(ciri)
                        if target_word in individuals:
                            found_iri = individuals[target_word]
                            break
                    if found_iri:
                        not_keyword_found = words[idx - 1] in ["not", "doesn't", "doesnt", "don't", "dont"]
                        filters.append((not_keyword_found, property_iri, found_iri))
                    else:
                        return None, None

        return rdf_type_iri, filters

    def build_sparql_query(self, rdf_type_iri, filters):
        prefixes = """
        PREFIX : <http://127.0.0.1:5000/software-ontology#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        """
        select_clause = "SELECT DISTINCT ?indiv ?label"
        where_clauses = []

        if rdf_type_iri:
            where_clauses.append(f"?indiv a <{rdf_type_iri}> .")

        for _not, prop_iri, val_iri in filters:
            where_clauses.append(f"?indiv <{prop_iri}> <{val_iri}> ." if not _not else f"FILTER NOT EXISTS {{ ?indiv <{prop_iri}> <{val_iri}> }} .")

        where_clauses.append("OPTIONAL { ?indiv rdfs:label ?label . }")

        query = (
                prefixes
                + "\n"
                + select_clause
                + "\nWHERE {\n"
                + "\n".join(where_clauses)
                + "\n}"
        )
        return query
