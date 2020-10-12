import json
import argparse
import re

def read_json(file):
    with open(file,'r') as load_f:
         load_dict = json.load(load_f)
         extract_queries(load_dict)
         dataset_id = load_dict['dataset']['id']
         questions = {}
         questions_info = []

         info_names = ['id','answertype','aggregation','onlydbo','hybrid']
         for question_dict in load_dict['questions']:
             id = ""
             question_infos = {}
             for key in question_dict:
                 value = question_dict[key]


                 if key == "id":
                     id = value
                 if key in info_names:
                     question_infos[key] = value

                 elif key == "question":
                     for question in value:
                        if question['language'] == "en":
                            questions[id] = question["string"]
             questions_info.append(question_infos)

    return questions_info, questions
def extract_queries(json_dict):
    queries = []
    pattern1 = re.compile(r'SELECT.*',re.DOTALL)
    pattern2 = re.compile(r'ASK.*',re.DOTALL)
    with open("to_query.txt","w") as w:

        for question_dict in json_dict['questions']:
            query = question_dict["query"]["sparql"]
            try:
                query = re.search(pattern1, query).group()
            except:
                query = re.search(pattern2, query).group()
            print(query)
            w.write(query+"\n")



def write_to_ask(questions):
    with open('to_ask1.txt', 'w') as write_f:
        for key in questions:
            question = questions[key]
            write_f.write(question.lower().replace("?"," ?")+"\n")

if __name__ == "__main__":
    """
    Section to parse the command line arguments.
    """
    parser = argparse.ArgumentParser()
    requiredNamed = parser.add_argument_group('Required Arguments')

    requiredNamed.add_argument('--path', dest='path', metavar='[path]',
                               help='the test set\'s file path', required=True)
    args = parser.parse_args()
    path = args.path
    questions_info, questions = read_json(path)
    print(questions_info, questions)
    # write_to_ask(questions)
    pass