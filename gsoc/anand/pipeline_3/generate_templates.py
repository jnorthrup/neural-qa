import argparse
from get_properties import get_properties
from generate_url import generate_url
from sentence_and_template_generator import sentence_and_template_generator


def generate_templates(label,project_name):
    val = generate_url(label)
    url = val[0]
    about = (val[1])
    count =0
    list_of_property_information = get_properties(url=url,project_name=project_name,output_file = "get_properties.csv")
    for property_line in list_of_property_information:
        count+=1
        prop = property_line.split(',')
        prop_name = prop[1]
        prop_type = prop[3]
        prop_domain = prop[2]
        prop_name = prop[0]
        print("**************\n"+str(prop))
        sentence_and_template_generator(project_name=project_name ,prop=prop, suffix = " of <X> ?",count = 2)
        
        


if __name__ == "__main__":
    """
    Section to parse the command line arguments.
    """
    parser = argparse.ArgumentParser()
    requiredNamed = parser.add_argument_group('Required Arguments')

    requiredNamed.add_argument('--label', dest='label', metavar='label',
                                                            help='label: person, place etc.', required=True)
    requiredNamed.add_argument(
        '--project_name', dest='project_name', metavar='project_name', help='test', required=True)
    args = parser.parse_args()
    label = args.label
    project_name = args.project_name
    generate_templates(label=label,project_name=project_name)
    pass