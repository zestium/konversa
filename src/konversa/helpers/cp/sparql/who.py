import sys
from SPARQLWrapper import SPARQLWrapper, JSON

class AnswerWho:

    def __init__(self, person_name):

        self.endpoint_url = "https://query.wikidata.org/sparql"
        self.query = """
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wikibase: <http://wikiba.se/ontology#>
PREFIX bd: <http://www.bigdata.com/rdf#>

SELECT ?item ?itemLabel ?itemDescription 
WHERE {
    ?item wdt:P31 wd:Q5 .
    ?item ?label '""" + person_name + """'@en .
    SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }. 
}

LIMIT 1"""

    def get_item_description(self):
        user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
        # TODO adjust user agent; see https://w.wiki/CX6
        sparql = SPARQLWrapper(self.endpoint_url, agent=user_agent)
        sparql.setQuery(self.query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        for result in results["results"]["bindings"]:
            the_result = result['itemDescription']['value']
        
        return the_result
