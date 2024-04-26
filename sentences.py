file1 = open('./input/ground_truth.txt', 'r')
Lines = file1.readlines()
 
count = 0
for line in Lines:
    count+=1
    file = open('./output/sentences/truths/truths_{}.txt'.format(count), 'w')
    file.write(line)

file1 = open('./input/ground_truth_myths.txt', 'r')
Lines = file1.readlines()
 
count = 0
for line in Lines:
    count+=1
    file = open('./output/sentences/myths/myths_{}.txt'.format(count), 'w')
    file.write(line)

input_file = open('./input/tweets.txt', 'r')
Lines = input_file.readlines()

count=0
for sentence in Lines:
    count+=1
    if(count<10):
        file = open('./output/sentences/tweets/tweet_00{}.txt'.format(count), 'w')
    elif(count<100):
        file = open('./output/sentences/tweets/tweet_0{}.txt'.format(count), 'w')
    else:
        file = open('./output/sentences/tweets/tweet_{}.txt'.format(count), 'w')
    file.write(sentence)