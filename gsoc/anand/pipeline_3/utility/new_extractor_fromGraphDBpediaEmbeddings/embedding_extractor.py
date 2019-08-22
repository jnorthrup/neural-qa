import json
from tqdm import tqdm 
index = open("index.csv").readlines()
diction = {}
for line in tqdm(range(len(index))):
    index[line] = index[line].split('\t')
    diction[index[line][0]] = {}
    diction[index[line][0]]['file'] = index[line][1]
    diction[index[line][0]]['line'] = index[line][2].strip()
with open("data_file.json", "w") as write_file:
    json.dump(diction, write_file)

vocab = open("vocab.sparql",'r').raedlines()
filename = []
for word in vocab:
    if(word in diction.keys()):
        



