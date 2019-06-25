from tqdm import tqdm

lines = open('eukaryotes/results.csv','r').readlines()

print(len(lines))
accum = []
nspm_ready = open("nspm_ready.csv",'w')
for line in tqdm(lines):
    values = line.split(";")
    if(values[-1]=="TRUE\n"):
        accum.append(";".join(values[:-2])+"\n")
        nspm_ready.write(accum[-1])
nspm_ready.close()


        