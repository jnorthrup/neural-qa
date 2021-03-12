import argparse
import http.client
import json
import os
import sys
import urllib.parse
import urllib.request

from bs4 import BeautifulSoup

ENDPOINT = "http://dbpedia.org/sparql"
GRAPH = "http://dbpedia.org"

def read_sparqls():
    os.system("pwd")
    sparqls = []
    file_path = "../gsoc/zheyuan/utility/benchmark/output_decoded1.txt"
    with open(file_path, 'r') as lines:
        for line in lines:
            sparqls.append(line)
    return sparqls

def retrieve(query):
    print(query)
    # python3
    query = urllib.parse.quote_plus(query)
    # except:  # python2
    #     query = urllib.quote_plus(query)
    url = "https://dbpedia.org/sparql?default-graph-uri=http%3A%2F%2Fdbpedia.org&query=" + query + "&format=text%2Fhtml&CXML_redir_for_subjs=121&CXML_redir_for_hrefs=&timeout=30000&debug=on"
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, "html.parser")
    total = len(soup.find_all("tr"))
    answers = []

    for rows in (soup.find_all("tr")):
        answer_dict = {
            "head": {
                "vars": ["uri"]
            }, "results": {
                "bindings": []
            }
        }
        for td in rows.find_all("a"):
            for a in td:
                uri = {
                    "uri": {
                        "type": "uri",
                        "value": a
                    }
                }


                answer_dict["results"]["bindings"].append(uri)

        for td in rows.find_all("pre"):
            for pre in td:
                # Eliminate the answer if it is longer than 50(not a URI nor a simple literal)
                if len(pre) <= 50:
                    uri = {
                        "uri": {
                            "type": "uri",
                            "value": pre
                        }
                    }

                    answer_dict["results"]["bindings"].append(uri)
        if answer_dict["results"]["bindings"]:
            answers.append(answer_dict)

    if not answers:
        return [{
                  "head" : {
                    "vars" : [ "date" ]
                  },
                  "results" : { }
                }]
    return answers

def retrieve_param(query):

    param = dict()
    param["default-graph-uri"] = GRAPH
    param["query"] = query
    param["format"] = "JSON"
    param["CXML_redir_for_subjs"] = "121"
    param["CXML_redir_for_hrefs"] = ""
    param["timeout"] = "600"
    param["debug"] = "on"
    try:
        resp = urllib.request.urlopen(ENDPOINT + "?" + urllib.parse.urlencode(param))
        print(resp)
        j = resp.read()
        resp.close()
    except (urllib.error.HTTPError, http.client.BadStatusLine):

        j = '{ "results": { "bindings": [] } }'
    sys.stdout.flush()
    return json.loads(j)

def retrieve_post(query):
    data = {
        "query": query
    }
    data = urllib.parse.urlencode(data)
    data = bytes(data, encoding='utf-8')

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        "origin": GRAPH,
        "referer": ENDPOINT,
        "x-requested-with": "XMLHttpRequest",
        "accept": "application/sparql-results+json,*/*;q=0.9",
    }
    req = urllib.request.Request(ENDPOINT, data=data, headers=headers)

    response = urllib.request.urlopen(req)

    return response

if __name__ == "__main__":
    """
    Section to parse the command line arguments.
    """
    parser = argparse.ArgumentParser()
    requiredNamed = parser.add_argument_group('Required Arguments')

    requiredNamed.add_argument('--query', dest='query', metavar='query',
                               help='query of SPARQL', required=True)
    args = parser.parse_args()
    query = args.query
    query = "select ?x where{<http://dbpedia.org/resource/Indigo> dbo:wavelength ?x }"
    answer = retrieve(query)
    print(answer)

    # answer_groups = []
    # i = 1
    # with open("../output_decoded.txt", 'r') as lines:
    #      for line in lines:
    #          i+=1
    #          try:
    #              answer_group = retrieve(line)
    #          except:
    #              answer_group=[]
    #          answer_groups.append(answer_group)
    #
    # print(len(answer_groups), answer_groups)


    pass