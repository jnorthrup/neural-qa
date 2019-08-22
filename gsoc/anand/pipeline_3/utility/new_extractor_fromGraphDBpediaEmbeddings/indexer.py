import sys
import os
from tqdm import tqdm 

a = [f for f in os.listdir(".") if f.startswith("xa")]
for files in tqdm(a):
    #print(files)
    lines = open(files).readlines()
    writer = open("index.csv",'a')
    for line in range(len(lines)):
        lines[line] = lines[line].split("\t")
        word = lines[line][0]
        if "http://dbpedia.org/resource/" in (word):
            word = word.replace("http://dbpedia.org/resource/","dbr_")
        if "http://dbpedia.org/ontology/" in (word):
            word = word.replace("http://dbpedia.org/ontology/","dbo_")
        writer.write('\t'.join([word,files,str(line)])+'\n')
    writer.close()