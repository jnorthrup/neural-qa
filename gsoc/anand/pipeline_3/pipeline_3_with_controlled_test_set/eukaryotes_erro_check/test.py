lines = open('nspm_ready.csv','r').readlines()
test = open('test.csv','r').readlines()

final_test = open('final_test.csv','w')
count = 0
for cnt in test:
    ori = cnt
    cnt = cnt.split(";")[3]
    for v in lines:
        if(cnt in v):
             print("Hi")
             count+=1
             final_test.write(';'.join(ori.split(";")[:-1])+'\n')
 
print(count)
final_test.close()

test = open('sentence_and_template_generator','r').readlines()
final_test = open('final_train','w')
count = 0
for cnt in test:
    ori = cnt
    cnt = cnt.split(";")[3]
    for v in lines:
        if(cnt in v):
             print("Hi")
             count+=1
             final_test.write(';'.join(ori.split(";")[:-1])+'\n')
 
print(count)
final_test.close()