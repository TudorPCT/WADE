from SPARQLWrapper import SPARQLWrapper, JSON

SPARQL_ENDPOINT = "http://localhost:3030/wade/sparql"


def get_classes_and_labels():
    sparql = SPARQLWrapper(SPARQL_ENDPOINT)
    query = """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX owl:  <http://www.w3.org/2002/07/owl#>

    SELECT DISTINCT ?class ?label
    WHERE {
      ?class a owl:Class .
      OPTIONAL { ?class rdfs:label ?label . }
    }
    """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    classes_map = {}
    for result in results["results"]["bindings"]:
        class_iri = result["class"]["value"]
        label_raw = result.get("label", {}).get("value", "")
        if label_raw:
            label = label_raw.lower()
        else:
            # Fallback to the IRI fragment
            label = class_iri.split("#")[-1].lower()

        # Add both singular and plural keys to handle "tools" or "frameworks"
        classes_map[label] = class_iri
        classes_map[label + "s"] = class_iri

    return classes_map


def get_individuals_for_class(class_iri):

    sparql = SPARQLWrapper(SPARQL_ENDPOINT)
    query = f"""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT DISTINCT ?indiv ?label
    WHERE {{
      ?indiv a <{class_iri}> .
      OPTIONAL {{ ?indiv rdfs:label ?label . }}
    }}
    """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    indiv_map = {}
    for result in results["results"]["bindings"]:
        indiv_iri = result["indiv"]["value"]
        label_raw = result.get("label", {}).get("value", "")
        if label_raw:
            label = label_raw.lower()
        else:
            label = indiv_iri.split("#")[-1].lower()
        indiv_map[label] = indiv_iri

    return indiv_map



def get_object_properties_and_labels():

    sparql = SPARQLWrapper(SPARQL_ENDPOINT)
    query = """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX owl:  <http://www.w3.org/2002/07/owl#>

    SELECT DISTINCT ?prop ?label
    WHERE {
      ?prop a owl:ObjectProperty .
      OPTIONAL { ?prop rdfs:label ?label . }
    }
    """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    properties_map = {}
    for result in results["results"]["bindings"]:
        prop_iri = result["prop"]["value"]
        label_raw = result.get("label", {}).get("value", "")
        if label_raw:
            label = label_raw.lower()
        else:
            label = prop_iri.split("#")[-1].lower()
        # You might store synonyms as well. For now, just store the direct label.
        properties_map[label] = prop_iri

    return properties_map


def parse_query(user_text):

    words = user_text.lower().split()

    classes_map = get_classes_and_labels()
    rdf_type_iri = None
    for word in words:
        if word in classes_map:
            rdf_type_iri = classes_map[word]
            break

    properties_map = get_object_properties_and_labels()

    synonyms_bridge = {
        "for": "supportslanguage",  # Map "for" to the rdfs:label "supports language"
        "licensed under": "hassoftwarelicense",
        "depends on": "dependson",
        "supports": "supportslanguage"
    }

    for synonym, prop_label in synonyms_bridge.items():
        if synonym in words and prop_label in properties_map:
            # Replace the user-friendly term (e.g., "for") with the real property label
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
                    individuals = get_individuals_for_class(ciri)
                    if target_word in individuals:
                        found_iri = individuals[target_word]
                        break
                if found_iri:
                    filters.append((property_iri, found_iri))

    print(rdf_type_iri, filters)
    return rdf_type_iri, filters


def build_sparql_query(rdf_type_iri, filters):

    prefixes = """
    PREFIX : <http://example.org/extended-software-dev-ontology#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    """
    select_clause = "SELECT DISTINCT ?indiv ?label"
    where_clauses = []

    if rdf_type_iri:
        where_clauses.append(f"?indiv a <{rdf_type_iri}> .")

    for (prop_iri, val_iri) in filters:
        where_clauses.append(f"?indiv <{prop_iri}> <{val_iri}> .")

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


def execute_sparql_query(query):

    sparql = SPARQLWrapper(SPARQL_ENDPOINT)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results["results"]["bindings"]


def main():

    print("Welcome to the ontology query tool!")
    user_input = input("Enter your query (e.g., 'show all frameworks for java'): ")

    rdf_type, filters = parse_query(user_input)

    if not rdf_type:
        words = user_input.lower().split()
        if "all" in words or "list" in words:
            classes_map = get_classes_and_labels()
            for w in words:
                if w in classes_map:
                    rdf_type = classes_map[w]
                    break

    if not rdf_type:
        print("Sorry, I couldn't identify what you're looking for.")
        return

    query = build_sparql_query(rdf_type, filters)
    print("\nGenerated SPARQL Query:\n")
    print(query)

    print("\nQuerying the SPARQL endpoint...\n")
    results = execute_sparql_query(query)

    if not results:
        print("No results found.")
    else:
        print("Results:")
        print(results)
        # for result in results:
        #     label = result.get("label", {}).get("value", "")
        #     indiv_iri = result["indiv"]["value"]
        #     if label:
        #         print(f"- {label} ({indiv_iri})")
        #     else:
        #         fragment = indiv_iri.split("#")[-1]
        #         print(f"- {fragment} ({indiv_iri})")


if __name__ == "__main__":
    while True:
        main()
