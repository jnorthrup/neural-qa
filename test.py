import generator_utils

sparql = open("data/dataset/data_300.sparql").readlines()
en = open("data/dataset/data_300.en").readlines()
for lines in range(len(sparql)):
    sparql[lines] = generator_utils.encode(sparql[lines].lower())
    en[lines] = en[lines].lower()

new_sparql = open("data/dataset/data_300.sparql",'w')
new_en= open("data/dataset/data_300.en",'w') 
for lines in range(len(sparql)):
    new_sparql.write(sparql[lines].strip().replace("  "," ")+"\n")
    new_en.write(en[lines].strip().replace("  "," ")+"\n")