import urllib
import urllib.request
import json
import sys
import csv
import io
import argparse
import os
from bs4 import BeautifulSoup
from tqdm import tqdm

def get_properties(url,  project_name="test_project", output_file = "get_properties.csv", multi=False):
    """
    - This function extracts the information regarding : [Name, Range, Cardinality, All usages] from a page like this :
    https://yago-knowledge.org/resource/schema:Airline and saves it in a file in CSV format.
    - This code on execution creates a csv which contains all the properties, ontology,
    class related information and data types as field values in each row.
    - This function also returns a 2D list of the information mentioned above to the calling
    function
    """
    page = urllib.request.urlopen(url)
    print("Page received.")
    soup = BeautifulSoup(page, "html.parser")
    if(not os.path.isdir(project_name)):
        os.makedirs(project_name)
    if multi:
        output_file = open(project_name + "/" + output_file, 'a', encoding="utf-8")
    else:
        output_file = open(project_name+"/" + output_file, 'w', encoding="utf-8")
    fl = 0
    accum = []
    property_names = soup.find_all("th")
    for i,rows in tqdm(enumerate(soup.find_all("tr"))):
        property_names = soup.find_all("th")
        x = rows.find_all("td")

        if len(x) <= 2:
            continue
        print(i, "x", len(x), x)

        name = property_names[i+3].find_all("a")[0].get_text() # Need +3 because of the structure of the page

        range = rows.find_all("td")[0].get_text()
        cardinality = rows.find_all("td")[1].get_text()
        usages = rows.find_all("td")[2].get_text()
        if rows.find_all("td")[0].find('a'):
            URL_name = ((rows.find_all("td")[0].find('a').attrs['href']))

        final = name + "\t" + range + "\t" + cardinality + "\t" + usages
        #+ ","+ URL_name.split(':')[-1]
        accum.append(final)
        output_file.write(final+"\n")
    output_file.close()
    return accum


"""
Name, Label, Domain, Range, URL_name
"""

if __name__ == "__main__":
    """
    Section to parse the command line arguments.
    """
    parser = argparse.ArgumentParser()
    requiredNamed = parser.add_argument_group('Required Arguments')

    requiredNamed.add_argument('--url', dest='url', metavar='url',
                                                            help='Webpage URL: eg-http://mappings.dbpedia.org/server/ontology/classes/Place', required=True)
    requiredNamed.add_argument(
        '--output_file', dest='out_put', metavar='out_put', help='temp.csv', required=True)
    requiredNamed.add_argument(
        '--project_name', dest='project_name', metavar='project_name', help='test', required=True)
    args = parser.parse_args()
    url = args.url
    output_file = args.out_put
    project_name = args.project_name
    get_properties(url = url, project_name= project_name,  output_file = output_file)
    pass
