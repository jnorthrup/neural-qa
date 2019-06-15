import xmltodict
import pprint
import json
import urllib
from bs4 import BeautifulSoup

xmldoc = open('../utility/dbpedia.owl').read()
pp = pprint.PrettyPrinter(indent=4)
jsondoc = ((xmltodict.parse(xmldoc)))
for val in ((jsondoc['rdf:RDF']['owl:Class'])):
    print(val['@rdf:about'])
    for lang in (val['rdfs:label']):
        if(lang['@xml:lang']=='en'):
            print(lang['#text'])
    print(val['rdfs:subClassOf']['@rdf:resource'])
    url = val['prov:wasDerivedFrom']['@rdf:resource']
    print(url)
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, "html.parser")
    link = soup.findAll('a',attrs={"rel" : "nofollow"})[0]['href']
    print(link)
    exit()

