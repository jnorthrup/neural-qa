import xmltodict
import pprint
import json
import sys
import urllib
from bs4 import BeautifulSoup

def get_url(url):
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, "html.parser")
        link = soup.findAll('a',attrs={"rel" : "nofollow"})[0]['href']
        return link

def generate_url(given_label):
        xmldoc = open('../utility/dbpedia.owl').read()
        jsondoc = ((xmltodict.parse(xmldoc)))
        count = 0
        for onto in jsondoc['rdf:RDF'].keys():
                if(not ( onto == 'owl:Class')):
                        continue
                
                for val in ((jsondoc['rdf:RDF'][onto])):
                        count+=1
                        #print("URI: "+val['@rdf:about'])
                        label = ""
                        for lang in (val['rdfs:label']):
                                if(lang['@xml:lang']=='en'):
                                        #print("Label: "+lang['#text'])
                                        label = lang['#text']
                        if(type(val['rdfs:subClassOf'])==list):
                                for subcl in  val['rdfs:subClassOf']:
                                        #print("Sub-class of: "+subcl['@rdf:resource']) 
                                        pass           
                        elif(type(val['rdfs:subClassOf']) != "list"):
                                #print("Sub-class of: "+val['rdfs:subClassOf']['@rdf:resource'])
                                pass
                        url = val['prov:wasDerivedFrom']['@rdf:resource']
                        #print("URL:" + url) 
                        if(label == given_label):
                                return get_url(url)

if __name__ == "__main__":
        print(generate_url(sys.argv[1]))
        pass










"""
 if(( onto == ("owl:ObjectProperty") ) ):
                print(onto)
                for val in ((jsondoc['rdf:RDF'][onto])):
                        count+=1
                        try:
                                print("URI: "+val['@rdf:about'])
                                print("Type: "+ val['rdf:type']["@rdf:resource"] )
                                if(type(val['rdfs:label'])=="<class 'list'>"):
                                        for lang in (val['rdfs:label']):
                                                if(lang['@xml:lang']=='en'):
                                                        print("Label: "+lang['#text'])
                                                        pass
                                elif(type(val['rdfs:label'])=="<class 'collections.OrderedDict'>"):
                                lang = dict(val['rdfs:label'])
                                if(lang['@xml:lang']=='en'):
                                                        print("Label: "+lang['#text'])
                                                        pass   
                                print("Domain: "+ val['rdfs:domain']["@rdf:resource"] )
                                print("Range: "+ val['rdfs:range']["@rdf:resource"] )
                                print("Sub-property of : "+val['rdfs:subPropertyOf']['@rdf:resource'])
                                url = val['prov:wasDerivedFrom']['@rdf:resource']
                                print(url)
                                #page = urllib.request.urlopen(url)
                                #soup = BeautifulSoup(page, "html.parser")
                                #link = soup.findAll('a',attrs={"rel" : "nofollow"})[0]['href']
                                #print("Address of resource: "+link)
                        except:
                                
"""