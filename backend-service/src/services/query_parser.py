class QueryResultParser:
    @staticmethod
    def parse_results(results, key, fallback_key=None, plural=False):
        parsed_data = {}
        for result in results["results"]["bindings"]:
            iri = result[key]["value"]
            label_raw = result.get(fallback_key, {}).get("value", "")
            label = label_raw.lower() if label_raw else iri.split("#")[-1].lower()
            parsed_data[label] = iri
            if plural:
                parsed_data[label + "s"] = iri
        return parsed_data
