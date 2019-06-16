import argparse
from generate_url import generate_url_spec , get_url, generate_url
from get_properties import get_properties
import urllib
import urllib.parse
from bs4 import BeautifulSoup

def check_query(query):
    query_original = query
    query = urllib.parse.quote(query)
    url = "https://dbpedia.org/sparql?default-graph-uri=http%3A%2F%2Fdbpedia.org&query="+query+"&format=text%2Fhtml&CXML_redir_for_subjs=121&CXML_redir_for_hrefs=&timeout=30000&debug=on&run=+Run+Query+"
    #print(url)
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, "html.parser")
    print((soup.text))
    if(soup.text=="false"):
        return False
    else:
        print(query_original)
        return True

def sentence_and_template_generator(prop,project_name,count=0, suffix = " of <X> ?", query_suffix = "", list_prop = [] ):
    if(type(prop)==str):
        prop = prop.split(',')
    question_starts_with =" "
    if(prop[3]=="owl:Thing" or prop[3]=="xsd:string"):
        question_starts_with = "What is the "
    if(prop[3]=="Place"):
       question_starts_with = "Where is the "
    if(prop[3]=="Person"):
       question_starts_with = "Who is the "
    if(prop[3]=="xsd:date" or "date" in prop[3] or "year" in prop[3] or "date" in prop[3] ):
       question_starts_with = "When is the "      
    else:
       question_starts_with = "What is the " 
    natural_language_question = (question_starts_with+prop[1]+ suffix)
    

    val = (generate_url_spec(prop[1]))
    prop_link = val[0]
    if(prop_link=="None" or prop_link== None):
        return
    derived = val[1]
    prop_link = "dbo:"+prop_link.strip().split('http://dbpedia.org/ontology/')[-1]
    list_prop.append(prop_link)
    sparql_query = ("select ?x where { <X>  "+ query_suffix + prop_link  +" ?x } ")
    if(query_suffix==""):
        query_answer = ("select distinct(?y) where { ?y "+prop_link+" []  } ")
    else :
        query_answer = ("select distinct(?y) where { ?y "+query_suffix.split(" ")[0]+" [] . ?y  "+query_suffix +" "+ prop_link +" ?x } ")

    if(query_suffix==""):
        flag = (check_query(query_answer.replace("select distinct(?y)","ask")))
    else :
        flag = (check_query(query_answer.replace("select distinct(?y)","ask")))
    if(not flag):
        return

    count = count - 1
    if(count == 0):
        variable = "?x"
    else:
        variable = "?x"+ str(count) 
    query_suffix = prop_link + " "+variable+" . "+variable+" " 
    print(natural_language_question+"\n"+sparql_query+"\n"+query_answer+"\n*************")
    
    suffix = " of "+ prop[1] +" of <X> ?"
    
    if(count>0):
        print(prop[3].split(":")[-1])
        val = generate_url(prop[3].split(":")[-1].lower())
        url = val[0]
        if(not url.startswith("http://mappings.dbpedia.org")):
            return
        list_of_property_information = get_properties(url=url,project_name=project_name,output_file =prop[1]+".csv" )
        for property_line in list_of_property_information:
            prop_inside = property_line.split(',')
            sentence_and_template_generator(prop=prop_inside, suffix = suffix,count = count, project_name=project_name, query_suffix = query_suffix , list_prop=list_prop)
            
                



if __name__ == "__main__":
    """
    Section to parse the command line arguments.
    """
    parser = argparse.ArgumentParser()
    requiredNamed = parser.add_argument_group('Required Arguments')

    requiredNamed.add_argument('--prop', dest='prop', metavar='prop',
                                                            help='prop: person, place etc.', required=True)
    args = parser.parse_args()
    prop = args.prop
    sentence_and_template_generator(prop=prop)
    pass