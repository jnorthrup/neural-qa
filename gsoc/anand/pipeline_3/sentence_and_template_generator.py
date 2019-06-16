import argparse
from generate_url import generate_url_spec , get_url, generate_url
from get_properties import get_properties

def sentence_and_template_generator(prop,project_name,count=0, suffix = " of <X> ?", query_suffix = ""):
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

    if(count == 0):
        variable = "?x"
    else:
        variable = "?x"+ str(count) 

    val = (generate_url_spec(prop[1]))
    prop_link = val[0]
    if(prop_link=="None" or prop_link== None):
        return
    derived = val[1]
    prop_link = "dbo:"+prop_link.strip().split('http://dbpedia.org/ontology/')[-1]
    sparql_query = ("select ?x where { <X>  "+prop_link + query_suffix +" ?x } ")
    count = count - 1
    query_suffix = query_suffix + " ?x"+str(count)+" . ?x"+str(count)+" "+ prop_link  
    print(natural_language_question+"|"+sparql_query)
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
            sentence_and_template_generator(prop=prop_inside, suffix = suffix,count = count, project_name=project_name, query_suffix = query_suffix )
            
                



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